"""Check session metadata and reuse the registry behavior checks for the review helper."""

import importlib.util
from pathlib import Path
import runpy
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "review_session_registry_checks", ROOT / "tests" / "test_context_read_sessions.py"
)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
checks.SCRIPT = ROOT / "skills" / "context-review-sessions" / "scripts" / "context_read_sessions.py"
checks.READER = runpy.run_path(str(checks.SCRIPT))


class SessionInventoryTests(checks.SessionInventoryTests):
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
        checks.READER["inventory"](self.queue, "done", checks.READER["checkpoint"](done))
        code, output, errors = self.cli()
        self.assertEqual(code, 0, errors)
        self.assertIn("reviewed: 1, pending: 2", output)
        self.assertNotIn("done", output)
        self.assertIn("transcript=missing-file  bytes=-  checkpoint=-", output)

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
        self.assertIn("transcript=unavailable  bytes=-  checkpoint=-", output)
        self.assertIn('error="denied"', output)
        self.assertIn("transcript=available  bytes=4", output)

    def test_grouping_options_are_not_supported(self):
        for arguments in (("--max-files", "3"), ("--max-bytes", "512"), ("--prepare",)):
            with self.subTest(arguments=arguments), self.assertRaises(SystemExit) as error:
                self.cli(*arguments)
            self.assertEqual(error.exception.code, 2)
