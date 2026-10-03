"""Behavior checks for the optional Codex hook and queue helpers."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "integrations" / "codex" / ".codex"
END = CODEX / "hooks" / "context_queue_session.py"
SCAN = ROOT / "skills" / "context-harvest" / "scripts" / "scan_queue.py"


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "project"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def invoke(self, script, event):
        return subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            cwd=self.repo,
            check=True,
        )

    @unittest.skipUnless(sys.platform == "win32", "Windows command override")
    def test_windows_commands_from_subdirectory_with_spaces(self):
        hook_dir = self.repo / ".codex" / "hooks"
        hook_dir.mkdir(parents=True)
        (hook_dir / END.name).write_bytes(END.read_bytes())
        context = self.repo / ".context"
        context.mkdir()
        (context / "INDEX.md").write_text("# Index\n", encoding="utf-8")
        cwd = self.repo / "directory with spaces"
        cwd.mkdir()
        config = json.loads((CODEX / "hooks.json").read_text())
        for name, groups in config["hooks"].items():
            command = groups[0]["hooks"][0]["commandWindows"]
            result = subprocess.run(
                command, shell=True, cwd=cwd,
                input=json.dumps({"hook_event_name": name, "cwd": str(cwd),
                                 "session_id": "windows-session"}),
                text=True, capture_output=True, check=True,
            )
            if name == "SessionStart":
                self.assertIn(".context/INDEX.md", result.stdout)
        queue = self.repo / ".context" / "sessions" / "windows-session.json"
        item = json.loads(queue.read_text())
        self.assertEqual(item["hook_event_name"], "SessionEnd")
        self.assertEqual(len(list(queue.parent.glob("*.json"))), 1)

    def test_end_queues_metadata_and_scan_marks_reviewed(self):
        transcript = self.repo / "session.jsonl"
        transcript.write_text("secret-canary\n", encoding="utf-8")
        event = {
            "hook_event_name": "SessionEnd",
            "session_id": "session-123",
            "cwd": str(self.repo),
            "transcript_path": str(transcript),
        }
        self.assertEqual(self.invoke(END, event).stdout, "")
        queue = self.repo / ".context" / "sessions" / "session-123.json"
        item = json.loads(queue.read_text(encoding="utf-8").strip())
        self.assertEqual(item["session_id"], "session-123")
        self.assertEqual(item["repo_root"], str(self.repo.resolve()))
        self.assertNotIn("secret-canary", queue.read_text(encoding="utf-8"))

        listing = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo)],
            text=True, capture_output=True, check=True,
        ).stdout
        self.assertIn("pending: 1", listing)
        self.assertIn("transcript=available", listing)
        reviewed = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed", "session-123"],
            text=True, capture_output=True, check=True,
        ).stdout
        self.assertIn("pending: 0", reviewed)
        reviewed_item = json.loads(queue.read_text(encoding="utf-8"))
        self.assertTrue(reviewed_item["reviewed_at"])
        self.assertEqual(reviewed_item["transcript_path"], str(transcript))
        self.assertEqual(len(list(queue.parent.iterdir())), 1)
        self.invoke(END, event)
        self.assertIsNone(json.loads(queue.read_text())["reviewed_at"])
        resumed = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo)],
            text=True, capture_output=True, check=True,
        ).stdout
        self.assertIn("pending: 1", resumed)

    def test_frequent_events_queue_once_per_session_in_inventory(self):
        for name in ("Stop", "Interrupt", "PreCompact", "SessionEnd"):
            event = {
                "hook_event_name": name,
                "session_id": "same-session",
                "turn_id": "turn-1",
                "cwd": str(self.repo),
                "last_assistant_message": "secret-canary" + "x" * 70000,
            }
            output = self.invoke(END, event).stdout
            if name in {"Stop", "PreCompact"}:
                self.assertEqual(json.loads(output), {})
            else:
                self.assertEqual(output, "")
        queue = self.repo / ".context" / "sessions" / "same-session.json"
        item = json.loads(queue.read_text())
        self.assertEqual(item["hook_event_name"], "SessionEnd")
        self.assertEqual(len(list(queue.parent.iterdir())), 1)
        self.assertNotIn("secret-canary", queue.read_text())
        listing = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo)],
            text=True, capture_output=True, check=True,
        ).stdout
        self.assertIn("queued: 1, reviewed: 0, pending: 1", listing)

    def test_scan_rejects_unqueued_review_id(self):
        result = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed", "unknown"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.repo / ".context" / "sessions").exists())

    def test_sessions_have_separate_files_and_review_state(self):
        for session_id in ("first-session", "second-session"):
            self.invoke(END, {"hook_event_name": "Stop", "session_id": session_id,
                              "cwd": str(self.repo)})
        subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed", "first-session"],
            text=True, capture_output=True, check=True,
        )
        state = self.repo / ".context" / "sessions"
        self.assertEqual(sorted(path.name for path in state.iterdir()),
                         ["first-session.json", "second-session.json"])
        self.assertTrue(json.loads((state / "first-session.json").read_text())["reviewed_at"])
        self.assertIsNone(json.loads((state / "second-session.json").read_text())["reviewed_at"])

    def test_scan_rejects_review_of_changed_checkpoint(self):
        event = {"hook_event_name": "Stop", "session_id": "resumed-session",
                 "cwd": str(self.repo)}
        self.invoke(END, event)
        path = self.repo / ".context" / "sessions" / "resumed-session.json"
        old_timestamp = json.loads(path.read_text())["queued_at"]
        self.invoke(END, event)
        result = subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed", "resumed-session",
             "--queued-at", old_timestamp], text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkpoint changed", result.stderr)
        self.assertIsNone(json.loads(path.read_text())["reviewed_at"])

    def test_hook_rejects_unsafe_session_filenames(self):
        for session_id in ("../escaped", "folder/session", "CON", "session:stream"):
            self.invoke(END, {"hook_event_name": "Stop", "session_id": session_id,
                              "cwd": str(self.repo)})
        self.assertFalse((self.repo / ".context" / "sessions").exists())


if __name__ == "__main__":
    unittest.main()
