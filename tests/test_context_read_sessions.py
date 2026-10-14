"""CSV inventory, review, validation, and atomic replacement checks."""

import contextlib
from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
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

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "context-import-sessions" / "scripts" / "context_read_sessions.py"
READER = runpy.run_path(str(SCRIPT))
HOOK = runpy.run_path(str(ROOT / "integrations" / "codex" / ".codex" / "hooks" / "context_register_session.py"))
FIELDS = ["session_date", "session_id", "path", "reviewed_date"]


class SessionInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.queue = self.root / ".context"
        self.log = self.queue / "sessions.log"
        self.transcript = self.root / "session.jsonl"

    def record(self, session_id="session-a", transcript="default"):
        self.queue.mkdir(exist_ok=True)
        if transcript == "default":
            self.transcript.write_text("evidence", encoding="utf-8")
            transcript = str(self.transcript)
        rows = READER["read_sessions"](self.queue)
        row = {"session_date": "2026-10-11", "session_id": session_id,
               "path": transcript or "", "reviewed_date": ""}
        rows[session_id] = row
        with self.log.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows.values())
        return self.log, row

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

    def test_listing_missing_queue_creates_nothing(self):
        self.assertEqual(self.cli(), (0, "queued: 0, reviewed: 0, pending: 0\n", ""))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_listing_reports_gaps_without_writes_or_transcript_reads(self):
        self.transcript.write_bytes(b"\xff\xfe\x00")
        self.record("available", str(self.transcript))
        self.record("missing-file", str(self.root / "absent.jsonl"))
        before = self.snapshot()
        original_open = Path.open

        def deny_transcript_open(path, *args, **kwargs):
            if path == self.transcript:
                raise AssertionError("inventory must not read transcript contents")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", deny_transcript_open):
            result, output, errors = self.cli()
        self.assertEqual(result, 0, errors)
        self.assertIn("queued: 2, reviewed: 0, pending: 2", output)
        for availability in ("available", "missing-file"):
            self.assertIn("transcript=" + availability, output)
        self.assertIn("checkpoint=", output)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_csv_fails_without_creating_lock_or_changing_log(self):
        path, _ = self.record()
        bad_rows = [
            "{}", "session_date,session_id,path,reviewed_date\n2026-10-11,id,path\n",
            "session_date,session_id,path,reviewed_date\n20261011,id,path,\n",
            "session_date,session_id,path,reviewed_date\n2026-02-30,id,path,\n",
            "session_date,session_id,path,reviewed_date\n2026-10-11,,path,\n",
            'session_date,session_id,path,reviewed_date\n2026-10-11,id,"unterminated',
        ]
        for content in bad_rows:
            path.write_text(content, encoding="utf-8")
            before = self.snapshot()
            result, _, errors = self.cli()
            self.assertEqual(result, 2, content)
            self.assertIn("could not inspect queue", errors)
            self.assertEqual(self.snapshot(), before)

    def test_marking_stale_checkpoint_preserves_log(self):
        path, _ = self.record()
        before = path.read_bytes()
        result, _, errors = self.cli("--mark-reviewed", "session-a", "--checkpoint", "older")
        self.assertEqual(result, 2)
        self.assertIn("checkpoint changed", errors)
        self.assertEqual(path.read_bytes(), before)

    def test_marking_is_locked_and_idempotent(self):
        path, row = self.record()
        token = READER["checkpoint"](row)
        with READER["queue_lock"](self.queue):
            result, _, errors = self.cli("--mark-reviewed", row["session_id"], "--checkpoint", token)
        self.assertEqual(result, 2)
        self.assertIn("queue is busy", errors)
        self.assertEqual(READER["read_sessions"](self.queue)[row["session_id"]]["reviewed_date"], "")
        result, output, errors = self.cli("--mark-reviewed", row["session_id"], "--checkpoint", token)
        self.assertEqual(result, 0, errors)
        self.assertIn("reviewed: 1, pending: 0", output)
        marked = READER["read_sessions"](self.queue)[row["session_id"]]
        self.assertEqual(marked["reviewed_date"], datetime.date.today().isoformat())
        self.assertEqual({**marked, "reviewed_date": ""}, row)
        before = path.read_bytes()
        self.assertEqual(self.cli("--mark-reviewed", row["session_id"], "--checkpoint", token)[0], 0)
        self.assertEqual(path.read_bytes(), before)

    def test_changed_path_or_file_metadata_invalidates_token(self):
        path, row = self.record()
        token = READER["checkpoint"](row)
        self.transcript.write_text("new evidence with a different size", encoding="utf-8")
        self.assertNotEqual(READER["checkpoint"](row), token)
        moved = self.root / "other.jsonl"
        moved.write_bytes(self.transcript.read_bytes())
        self.assertNotEqual(READER["checkpoint"]({**row, "path": str(moved)}), READER["checkpoint"](row))

    def test_blank_path_record_is_rejected(self):
        path, _ = self.record(transcript=None)
        before = path.read_bytes()
        result, _, errors = self.cli("--mark-reviewed", "session-a", "--checkpoint", "-")
        self.assertEqual(result, 2)
        self.assertIn("invalid session record", errors)
        self.assertEqual(path.read_bytes(), before)

    def test_same_size_edit_on_same_day_invalidates_token(self):
        _, row = self.record()
        token = READER["checkpoint"](row)
        original = self.transcript.stat()
        self.transcript.write_text("revision", encoding="utf-8")
        os.utime(self.transcript, ns=(original.st_atime_ns, original.st_mtime_ns + 1_000_000))
        self.assertEqual(self.transcript.stat().st_size, original.st_size)
        self.assertNotEqual(READER["checkpoint"](row), token)
        result, _, errors = self.cli("--mark-reviewed", row["session_id"], "--checkpoint", token)
        self.assertEqual(result, 2)
        self.assertIn("checkpoint changed", errors)

    def test_unknown_session_does_not_create_queue(self):
        result, _, errors = self.cli("--mark-reviewed", "missing", "--checkpoint", "missing")
        self.assertEqual(result, 2)
        self.assertIn("not in the queue", errors)
        self.assertFalse(self.queue.exists())

    def test_review_requires_both_arguments(self):
        for arguments in (["--mark-reviewed", "session-a"], ["--checkpoint", "token"]):
            with self.subTest(arguments=arguments), self.assertRaises(SystemExit) as result:
                self.cli(*arguments)
            self.assertEqual(result.exception.code, 2)

    def test_concurrent_review_and_registration_preserve_other_rows(self):
        _, row = self.record("review")
        self.record("keep")
        token = READER["checkpoint"](row)
        with ThreadPoolExecutor(max_workers=2) as executor:
            marking = executor.submit(READER["inventory"], self.queue, "review", token)
            adding = executor.submit(HOOK["register"], self.queue, "new", str(self.transcript))
            marking.result(timeout=5)
            adding.result(timeout=5)
        rows = READER["read_sessions"](self.queue)
        self.assertEqual(set(rows), {"review", "keep", "new"})
        self.assertTrue(rows["review"]["reviewed_date"])
        self.assertEqual(rows["keep"]["reviewed_date"], "")

    def test_failed_replacement_retries_once_and_keeps_log(self):
        for module in (READER, HOOK):
            with self.subTest(module=module["__file__"]):
                path, row = self.record()
                before = self.snapshot()
                with patch("os.replace", side_effect=OSError("write denied")) as replacement, \
                        patch("time.sleep") as sleeping:
                    with self.assertRaisesRegex(OSError, "write denied"):
                        module["write_sessions"](path, {row["session_id"]: {**row, "reviewed_date": "2026-10-12"}})
                self.assertEqual(replacement.call_count, 2)
                sleeping.assert_called_once()
                self.assertEqual(self.snapshot(), before)

    def test_replacement_error_retries_complete_write_then_succeeds(self):
        replace = os.replace
        for module in (READER, HOOK):
            with self.subTest(module=module["__file__"]):
                path, row = self.record()
                attempts = 0

                def conflict_once(source, destination):
                    nonlocal attempts
                    attempts += 1
                    if attempts == 1:
                        raise OSError("temporary write failure")
                    return replace(source, destination)

                updated = {**row, "reviewed_date": "2026-10-12"}
                with patch("os.replace", side_effect=conflict_once), patch("time.sleep"):
                    module["write_sessions"](path, {row["session_id"]: updated})
                self.assertEqual(attempts, 2)
                self.assertEqual(READER["read_sessions"](self.queue)[row["session_id"]], updated)
                self.assertEqual(list(self.queue.glob("*.tmp")), [])

    def test_temporary_file_creation_error_is_retried(self):
        create = tempfile.NamedTemporaryFile
        for module in (READER, HOOK):
            with self.subTest(module=module["__file__"]):
                path, row = self.record()
                attempts = 0

                def fail_once(*args, **kwargs):
                    nonlocal attempts
                    attempts += 1
                    if attempts == 1:
                        raise OSError("temporary creation failure")
                    return create(*args, **kwargs)

                updated = {**row, "reviewed_date": "2026-10-12"}
                with patch("tempfile.NamedTemporaryFile", side_effect=fail_once), patch("time.sleep"):
                    module["write_sessions"](path, {row["session_id"]: updated})
                self.assertEqual(attempts, 2)
                self.assertEqual(READER["read_sessions"](self.queue)[row["session_id"]], updated)
                self.assertEqual(list(self.queue.glob("*.tmp")), [])

    def test_partial_csv_write_is_retried_without_duplicate_rows(self):
        make_writer = csv.writer
        for module in (READER, HOOK):
            with self.subTest(module=module["__file__"]):
                path, row = self.record()
                failed = False

                class FailingWriter:
                    def __init__(self, handle, **kwargs):
                        self.writer = make_writer(handle, **kwargs)

                    def writerow(self, values):
                        nonlocal failed
                        self.writer.writerow(values)
                        if values[0] != "session_date" and not failed:
                            failed = True
                            raise OSError("partial write")

                updated = {**row, "reviewed_date": "2026-10-12"}
                with patch("csv.writer", side_effect=FailingWriter), patch("time.sleep"):
                    module["write_sessions"](path, {row["session_id"]: updated})
                self.assertTrue(failed)
                self.assertEqual(READER["read_sessions"](self.queue), {row["session_id"]: updated})
                self.assertEqual(list(self.queue.glob("*.tmp")), [])

    @unittest.skipUnless(os.name == "nt", "Windows replacement sharing semantics")
    def test_listing_during_write_returns_a_complete_snapshot(self):
        path, row = self.record()
        original_reader, original_replace = csv.reader, os.replace
        blocked = threading.Event()
        futures = []

        def observe_replace(source, destination):
            try:
                return original_replace(source, destination)
            except PermissionError:
                blocked.set()
                raise

        def start_writer(handle, *args, **kwargs):
            if threading.current_thread() is threading.main_thread():
                futures.append(executor.submit(HOOK["register"], self.queue, "new", str(self.transcript)))
                self.assertTrue(blocked.wait(timeout=2), "writer did not reach replacement")
            return original_reader(handle, *args, **kwargs)

        with ThreadPoolExecutor(max_workers=1) as executor, \
                patch("csv.reader", side_effect=start_writer), patch("os.replace", side_effect=observe_replace):
            snapshot = READER["inventory"](self.queue)
            futures[0].result(timeout=5)
        self.assertEqual(snapshot, {row["session_id"]: row})
        self.assertEqual(set(READER["read_sessions"](self.queue)), {"session-a", "new"})


if __name__ == "__main__":
    unittest.main()
