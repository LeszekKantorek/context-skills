"""Behavior checks for the optional Codex hook and queue helpers."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "integrations" / "codex" / "context_session_start.py"
END = ROOT / "integrations" / "codex" / "context_queue_session.py"
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

    def test_start_only_points_to_existing_index(self):
        event = {"hook_event_name": "SessionStart", "cwd": str(self.repo)}
        self.assertEqual(self.invoke(START, event).stdout, "")
        context = self.repo / ".context"
        context.mkdir()
        (context / "INDEX.md").write_text("secret-canary\n", encoding="utf-8")
        output = self.invoke(START, event).stdout
        self.assertIn(".context/INDEX.md", output)
        self.assertNotIn("secret-canary", output)
        self.assertEqual(json.loads(output)["hookSpecificOutput"]["hookEventName"], "SessionStart")

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
        queue = self.repo / ".git" / "context-skills" / "queue.jsonl"
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
        self.invoke(END, event)
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
        queue = self.repo / ".git" / "context-skills" / "queue.jsonl"
        rows = [json.loads(line) for line in queue.read_text().splitlines()]
        self.assertEqual([row["hook_event_name"] for row in rows],
                         ["Stop", "Interrupt", "PreCompact", "SessionEnd"])
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
        self.assertFalse((self.repo / ".git" / "context-skills" / "reviewed.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
