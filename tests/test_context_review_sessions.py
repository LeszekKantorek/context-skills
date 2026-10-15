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
SCRIPT = ROOT / "skills" / "context-review-sessions" / "scripts" / "context_read_sessions.py"
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
        self.assertIn("bytes=", output)
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


    def test_blank_path_record_is_rejected(self):
        path, _ = self.record(transcript=None)
        before = path.read_bytes()
        result, _, errors = self.cli("--mark-reviewed", "session-a")
        self.assertEqual(result, 2)
        self.assertIn("invalid session record", errors)
        self.assertEqual(path.read_bytes(), before)


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


    def add_transcript(self, session_id, size):
        path = self.root / (session_id + ".jsonl")
        path.write_bytes(b"x" * size)
        return self.record(session_id, str(path))[1]


    def test_listing_reports_all_pending_files_and_sizes_without_changes(self):
        for name, size in (("d", 800000), ("c", 4), ("b", 9), ("a", 0)):
            self.add_transcript(name, size)
        before = self.snapshot()
        code, output, errors = self.cli()
        self.assertEqual(code, 0, errors)
        lines = output.splitlines()[1:]
        self.assertEqual([line.split()[0] for line in lines], ["a", "b", "c", "d"])
        for line, size in zip(lines, (0, 9, 4, 800000)):
            self.assertIn("bytes=%d  " % size, line)
        self.assertEqual(self.snapshot(), before)


    def test_listing_excludes_reviewed_sessions_and_keeps_missing_files_visible(self):
        done = self.add_transcript("done", 4)
        self.add_transcript("available", 4)
        self.record("missing", str(self.root / "absent.jsonl"))
        READER["inventory"](self.queue, ["done"])
        code, output, errors = self.cli()
        self.assertEqual(code, 0, errors)
        self.assertIn("reviewed: 1, pending: 2", output)
        self.assertNotIn("done", output)
        self.assertIn("transcript=missing-file  bytes=-", output)


    def test_metadata_error_does_not_block_other_sessions(self):
        self.add_transcript("denied", 4)
        self.add_transcript("available", 4)
        original = Path.stat

        def deny_one(path, *args, **kwargs):
            if path.name == "denied.jsonl":
                raise PermissionError("denied")
            return original(path, *args, **kwargs)

        with patch.object(Path, "stat", deny_one):
            code, output, errors = self.cli()
        self.assertEqual(code, 0, errors)
        self.assertIn("transcript=unavailable  bytes=-", output)
        self.assertIn('error="denied"', output)
        self.assertIn("transcript=available  bytes=4", output)


    def test_grouping_options_are_not_supported(self):
        for arguments in (("--max-files", "3"), ("--max-bytes", "512"), ("--prepare",)):
            with self.subTest(arguments=arguments), self.assertRaises(SystemExit) as error:
                self.cli(*arguments)
            self.assertEqual(error.exception.code, 2)


    def test_changed_transcript_can_be_marked_by_id(self):
        self.add_transcript("session", 4)
        self.cli()
        (self.root / "session.jsonl").write_text("additional conversation", encoding="utf-8")
        code, output, errors = self.cli("--mark-reviewed", "session")
        self.assertEqual(code, 0, errors)
        self.assertIn("reviewed: 1, pending: 0", output)
        row = READER["read_sessions"](self.queue)["session"]
        self.assertEqual(row["reviewed_date"], datetime.date.today().isoformat())


    def test_marking_is_locked_and_idempotent(self):
        self.add_transcript("session", 4)
        with READER["queue_lock"](self.queue):
            code, _, errors = self.cli("--mark-reviewed", "session")
        self.assertEqual(code, 2)
        self.assertIn("queue is busy", errors)
        self.assertEqual(READER["read_sessions"](self.queue)["session"]["reviewed_date"], "")
        self.assertEqual(self.cli("--mark-reviewed", "session")[0], 0)
        before = self.log.read_bytes()
        self.assertEqual(self.cli("--mark-reviewed", "session")[0], 0)
        self.assertEqual(self.log.read_bytes(), before)


    def test_unknown_or_unavailable_session_is_not_marked(self):
        self.assertEqual(self.cli("--mark-reviewed", "unknown")[0], 2)
        self.assertFalse(self.queue.exists())
        for session_id, path in (("missing", self.root / "absent.jsonl"), ("directory", self.root)):
            self.record(session_id, str(path))
            before = self.log.read_bytes()
            self.assertEqual(self.cli("--mark-reviewed", session_id)[0], 2)
            self.assertEqual(self.log.read_bytes(), before)


    def test_concurrent_review_and_registration_preserve_other_rows(self):
        row = self.add_transcript("review", 4)
        self.add_transcript("keep", 4)
        with ThreadPoolExecutor(max_workers=2) as executor:
            marking = executor.submit(READER["inventory"], self.queue, ["review"])
            adding = executor.submit(HOOK["register"], self.queue, "new", row["path"])
            marking.result(timeout=5)
            adding.result(timeout=5)
        rows = READER["read_sessions"](self.queue)
        self.assertEqual(set(rows), {"review", "keep", "new"})
        self.assertTrue(rows["review"]["reviewed_date"])
        self.assertEqual(rows["keep"]["reviewed_date"], "")


    def test_multiple_sessions_use_one_write_and_keep_existing_dates(self):
        for session_id in ("first", "second", "done", "keep"):
            self.add_transcript(session_id, 4)
        rows = READER["read_sessions"](self.queue)
        rows["done"]["reviewed_date"] = "2025-01-03"
        READER["write_sessions"](self.log, rows)
        with patch("os.replace", wraps=READER["os"].replace) as replace:
            code, _, errors = self.cli("--mark-reviewed", "first", "second", "first", "done")
        self.assertEqual(code, 0, errors)
        self.assertEqual(replace.call_count, 1)
        rows = READER["read_sessions"](self.queue)
        for session_id in ("first", "second"):
            self.assertEqual(rows[session_id]["reviewed_date"], datetime.date.today().isoformat())
        self.assertEqual(rows["done"]["reviewed_date"], "2025-01-03")
        self.assertEqual(rows["keep"]["reviewed_date"], "")
        with patch("os.replace") as replace:
            self.assertEqual(self.cli("--mark-reviewed", "first", "second", "done")[0], 0)
        replace.assert_not_called()


    def test_invalid_member_prevents_partial_batch_update(self):
        self.add_transcript("valid", 4)
        self.record("missing", str(self.root / "absent.jsonl"))
        for invalid in ("unknown", "missing"):
            before = self.log.read_bytes()
            with patch("os.replace") as replace:
                code, _, errors = self.cli("--mark-reviewed", "valid", invalid)
            self.assertEqual(code, 2)
            self.assertIn(invalid, errors)
            replace.assert_not_called()
            self.assertEqual(self.log.read_bytes(), before)


    def test_mark_reviewed_requires_at_least_one_id(self):
        with self.assertRaises(SystemExit) as error:
            self.cli("--mark-reviewed")
        self.assertEqual(error.exception.code, 2)
