"""Session queue checks use temporary directories and never import transcripts."""

import contextlib
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch


SCRIPT = (Path(__file__).resolve().parents[1] / "skills"
          / "context-import-sessions" / "scripts" / "context_read_sessions.py")
READER = runpy.run_path(str(SCRIPT))
HOOK = runpy.run_path(str(Path(__file__).resolve().parents[1]
                         / "integrations" / "codex" / ".codex" / "hooks" / "context_register_session.py"))


class SessionInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.queue = self.root / ".context" / "sessions"

    def record(self, session_id="session-a", transcript=None):
        self.queue.mkdir(parents=True, exist_ok=True)
        path = self.queue / (session_id + ".json")
        row = {"session_id": session_id, "updated_at": "2026-10-11T10:00:00+00:00",
               "transcript_path": transcript, "reviewed_at": None}
        path.write_text(json.dumps(row), encoding="utf-8")
        return path, row

    def snapshot(self):
        return {str(path.relative_to(self.root)): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in self.root.rglob("*") if path.is_file()}

    def cli(self, *arguments):
        output, errors = io.StringIO(), io.StringIO()
        git_result = subprocess.CompletedProcess([], 0, stdout=str(self.root) + "\n")
        with patch("sys.argv", [str(SCRIPT), str(self.root), *arguments]), \
                patch("subprocess.run", return_value=git_result), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            result = READER["main"]()
        return result, output.getvalue(), errors.getvalue()

    def test_listing_missing_queue_creates_no_directories(self):
        self.assertEqual(self.cli(), (0, "queued: 0, reviewed: 0, pending: 0\n", ""))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_listing_reports_path_and_file_gaps_without_writes_or_transcript_reads(self):
        transcript = self.root / "unreadable-as-text.jsonl"
        transcript.write_bytes(b"\xff\xfe\x00")
        self.record("available", str(transcript))
        self.record("missing-file", str(self.root / "absent.jsonl"))
        self.record("missing-path")
        before = self.snapshot()

        result, output, errors = self.cli()

        self.assertEqual(result, 0, errors)
        self.assertIn("queued: 3, reviewed: 0, pending: 3", output)
        self.assertIn("transcript=available", output)
        self.assertIn("transcript=missing-path", output)
        self.assertIn("transcript=missing-file", output)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_record_fails_without_creating_lock(self):
        path, _ = self.record()
        path.write_text("{}", encoding="utf-8")
        before = self.snapshot()
        result, _, errors = self.cli()
        self.assertEqual(result, 2)
        self.assertIn("invalid session record", errors)
        self.assertEqual(self.snapshot(), before)

    @unittest.skipUnless(os.name == "nt", "Windows replacement sharing semantics")
    def test_concurrent_listing_does_not_discard_hook_or_review_updates(self):
        load_json, replace = json.load, os.replace
        for writer in ("hook", "review"):
            with self.subTest(writer=writer):
                path, original = self.record()
                blocked = threading.Event()
                futures = []

                def observe_replace(source, destination):
                    try:
                        return replace(source, destination)
                    except PermissionError:
                        blocked.set()
                        raise

                def update_during_read(handle):
                    if threading.current_thread() is threading.main_thread():
                        if writer == "hook":
                            futures.append(executor.submit(HOOK["register"], self.queue,
                                                           original["session_id"], "new.jsonl"))
                        else:
                            futures.append(executor.submit(READER["inventory"], self.queue,
                                                           original["session_id"], original["updated_at"]))
                        self.assertTrue(blocked.wait(timeout=2), "writer did not reach replacement")
                    return load_json(handle)

                with ThreadPoolExecutor(max_workers=1) as executor, \
                        patch("os.replace", side_effect=observe_replace), \
                        patch("json.load", side_effect=update_during_read):
                    snapshot = READER["inventory"](self.queue)
                    # The reader is closed; the writer must retry and save its update.
                    self.assertEqual(len(futures), 1)
                    futures[0].result(timeout=5)
                self.assertEqual(snapshot[original["session_id"]][1], original)
                updated = json.loads(path.read_text(encoding="utf-8"))
                if writer == "hook":
                    self.assertEqual(updated["transcript_path"], "new.jsonl")
                    self.assertNotEqual(updated["updated_at"], original["updated_at"])
                    self.assertIsNone(updated["reviewed_at"])
                    with self.assertRaisesRegex(ValueError, "checkpoint changed"):
                        READER["inventory"](self.queue, original["session_id"], original["updated_at"])
                else:
                    self.assertTrue(updated["reviewed_at"])
                    self.assertEqual({**updated, "reviewed_at": None}, original)

    @unittest.skipUnless(os.name == "nt", "Windows replacement retry policy")
    def test_failed_replacement_keeps_previous_record_and_cleans_temporary_file(self):
        for module in (READER, HOOK):
            for winerror, expected_attempts in ((5, 2), (32, 2), (33, 2), (87, 1)):
                with self.subTest(writer=module["__file__"], winerror=winerror):
                    path, original = self.record()
                    before = self.snapshot()
                    error = OSError("replacement denied")
                    error.winerror = winerror
                    with patch("os.replace", side_effect=error) as replacement, \
                            patch("time.monotonic", side_effect=[0, 0.1, 1.1]), \
                            patch("time.sleep") as sleeping:
                        with self.assertRaises(OSError):
                            module["write_record"](path, {**original, "reviewed_at": "later"})
                    self.assertEqual(replacement.call_count, expected_attempts)
                    self.assertEqual(sleeping.call_count, expected_attempts - 1)
                    self.assertEqual(self.snapshot(), before)

    @unittest.skipUnless(os.name == "nt", "Windows replacement retry policy")
    def test_transient_replacement_errors_retry_then_succeed(self):
        replace = os.replace
        for module in (READER, HOOK):
            for winerror in (5, 32, 33):
                with self.subTest(writer=module["__file__"], winerror=winerror):
                    path, original = self.record()
                    error = OSError("temporary reader conflict")
                    error.winerror = winerror
                    attempts = 0

                    def conflict_once(source, destination):
                        nonlocal attempts
                        attempts += 1
                        if attempts == 1:
                            raise error
                        return replace(source, destination)

                    updated = {**original, "reviewed_at": "later"}
                    with patch("os.replace", side_effect=conflict_once), patch("time.sleep"):
                        module["write_record"](path, updated)
                    self.assertEqual(attempts, 2)
                    self.assertEqual(json.loads(path.read_text(encoding="utf-8")), updated)
                    self.assertEqual(list(self.queue.glob("*.tmp")), [])

    def test_marking_stale_checkpoint_preserves_record(self):
        path, _ = self.record()
        before = path.read_bytes()
        result, _, errors = self.cli("--mark-reviewed", "session-a", "--updated-at", "older")
        self.assertEqual(result, 2)
        self.assertIn("checkpoint changed", errors)
        self.assertEqual(path.read_bytes(), before)

    def test_marking_exact_checkpoint_is_locked_and_idempotent(self):
        path, row = self.record()
        with READER["queue_lock"](self.queue):
            result, _, errors = self.cli("--mark-reviewed", row["session_id"],
                                         "--updated-at", row["updated_at"])
        self.assertEqual(result, 2)
        self.assertIn("queue is busy", errors)
        self.assertIsNone(json.loads(path.read_text(encoding="utf-8"))["reviewed_at"])

        result, output, errors = self.cli("--mark-reviewed", row["session_id"],
                                         "--updated-at", row["updated_at"])
        self.assertEqual(result, 0, errors)
        self.assertIn("reviewed: 1, pending: 0", output)
        marked = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(marked["reviewed_at"])
        self.assertEqual({**marked, "reviewed_at": None}, row)
        before = path.read_bytes()
        self.assertEqual(self.cli("--mark-reviewed", row["session_id"],
                                  "--updated-at", row["updated_at"])[0], 0)
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
