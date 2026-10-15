"""Check session metadata and reuse the registry behavior checks for the review helper."""

import importlib.util
import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "review_session_registry_checks", ROOT / "tests" / "test_context_read_sessions.py"
)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
checks.SCRIPT = ROOT / "skills" / "context-review-sessions" / "scripts" / "context_read_sessions.py"
checks.READER = runpy.run_path(str(checks.SCRIPT))


class SessionInventoryTests(unittest.TestCase):
    setUp = checks.SessionInventoryTests.setUp
    record = checks.SessionInventoryTests.record
    snapshot = checks.SessionInventoryTests.snapshot
    cli = checks.SessionInventoryTests.cli
    test_listing_missing_queue_creates_nothing = checks.SessionInventoryTests.test_listing_missing_queue_creates_nothing
    test_invalid_csv_fails_without_creating_lock_or_changing_log = checks.SessionInventoryTests.test_invalid_csv_fails_without_creating_lock_or_changing_log
    test_failed_replacement_retries_once_and_keeps_log = checks.SessionInventoryTests.test_failed_replacement_retries_once_and_keeps_log
    test_replacement_error_retries_complete_write_then_succeeds = checks.SessionInventoryTests.test_replacement_error_retries_complete_write_then_succeeds
    test_temporary_file_creation_error_is_retried = checks.SessionInventoryTests.test_temporary_file_creation_error_is_retried
    test_partial_csv_write_is_retried_without_duplicate_rows = checks.SessionInventoryTests.test_partial_csv_write_is_retried_without_duplicate_rows
    test_listing_during_write_returns_a_complete_snapshot = checks.SessionInventoryTests.test_listing_during_write_returns_a_complete_snapshot

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
        checks.READER["inventory"](self.queue, ["done"])
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
        row = checks.READER["read_sessions"](self.queue)["session"]
        self.assertEqual(row["reviewed_date"], datetime.date.today().isoformat())

    def test_marking_is_locked_and_idempotent(self):
        self.add_transcript("session", 4)
        with checks.READER["queue_lock"](self.queue):
            code, _, errors = self.cli("--mark-reviewed", "session")
        self.assertEqual(code, 2)
        self.assertIn("queue is busy", errors)
        self.assertEqual(checks.READER["read_sessions"](self.queue)["session"]["reviewed_date"], "")
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
            marking = executor.submit(checks.READER["inventory"], self.queue, ["review"])
            adding = executor.submit(checks.HOOK["register"], self.queue, "new", row["path"])
            marking.result(timeout=5)
            adding.result(timeout=5)
        rows = checks.READER["read_sessions"](self.queue)
        self.assertEqual(set(rows), {"review", "keep", "new"})
        self.assertTrue(rows["review"]["reviewed_date"])
        self.assertEqual(rows["keep"]["reviewed_date"], "")

    def test_multiple_sessions_use_one_write_and_keep_existing_dates(self):
        for session_id in ("first", "second", "done", "keep"):
            self.add_transcript(session_id, 4)
        rows = checks.READER["read_sessions"](self.queue)
        rows["done"]["reviewed_date"] = "2025-01-03"
        checks.READER["write_sessions"](self.log, rows)
        with patch("os.replace", wraps=checks.READER["os"].replace) as replace:
            code, _, errors = self.cli("--mark-reviewed", "first", "second", "first", "done")
        self.assertEqual(code, 0, errors)
        self.assertEqual(replace.call_count, 1)
        rows = checks.READER["read_sessions"](self.queue)
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
