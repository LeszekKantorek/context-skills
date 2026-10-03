"""Integration checks for the session registrar and checkpoint review helper."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "integrations" / "codex" / ".codex"
HOOK = CODEX / "hooks" / "context_queue_session.py"
SCAN = ROOT / "skills" / "context-consolidate" / "scripts" / "scan_queue.py"
FIELDS = {"session_id", "updated_at", "transcript_path", "reviewed_at"}


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HOOK_API = load_script("queue_hook", HOOK)
SCAN_API = load_script("queue_scan", SCAN)


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "project with spaces"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.state = self.repo / ".context" / "sessions"

    def event(self, session_id="session-123", name="Stop", **extra):
        return {"hook_event_name": name, "session_id": session_id,
                "cwd": str(self.repo), **extra}

    def invoke(self, event, check=True):
        return subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(event),
            text=True, capture_output=True, cwd=self.repo, check=check,
        )

    def scan(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), *args],
            text=True, capture_output=True, check=check,
        )

    def records(self):
        return {row["session_id"]: (path, row)
                for path in self.state.glob("*.json")
                for row in [json.loads(path.read_text(encoding="utf-8"))]}

    def mark(self, session_id, checkpoint):
        return self.scan("--mark-reviewed", session_id, "--updated-at", checkpoint)

    @unittest.skipUnless(sys.platform == "win32", "Windows command override")
    def test_windows_hook_commands_from_subdirectory_with_spaces(self):
        hook_dir = self.repo / ".codex" / "hooks"
        hook_dir.mkdir(parents=True)
        (hook_dir / HOOK.name).write_bytes(HOOK.read_bytes())
        cwd = self.repo / "nested directory"
        cwd.mkdir()
        config = json.loads((CODEX / "hooks.json").read_text(encoding="utf-8"))
        for name, groups in config["hooks"].items():
            result = subprocess.run(
                groups[0]["hooks"][0]["commandWindows"], shell=True, cwd=cwd,
                input=json.dumps(self.event("windows-session", name, cwd=str(cwd))),
                text=True, capture_output=True, check=True,
            )
            if name == "SessionStart":
                self.assertIn("context-apply", result.stdout)
                self.assertFalse((self.repo / ".context").exists())
        self.assertEqual(len(self.records()), 1)
        self.assertIn("windows-session", self.records())
        self.assertFalse((self.repo / ".context" / "INDEX.md").exists())

    @unittest.skipIf(sys.platform == "win32", "POSIX command")
    def test_posix_hook_commands_from_subdirectory_with_spaces(self):
        hook_dir = self.repo / ".codex" / "hooks"
        hook_dir.mkdir(parents=True)
        (hook_dir / HOOK.name).write_bytes(HOOK.read_bytes())
        cwd = self.repo / "nested directory"
        cwd.mkdir()
        config = json.loads((CODEX / "hooks.json").read_text(encoding="utf-8"))
        for name, groups in config["hooks"].items():
            subprocess.run(
                groups[0]["hooks"][0]["command"], shell=True, cwd=cwd,
                input=json.dumps(self.event("posix-session", name, cwd=str(cwd))),
                text=True, capture_output=True, check=True,
            )
        self.assertEqual(len(self.records()), 1)
        self.assertIn("posix-session", self.records())

    def test_exact_record_and_review_lifecycle_without_reading_transcript(self):
        transcript = self.repo / "session.jsonl"
        transcript.write_text("secret-canary\n", encoding="utf-8")
        event = self.event("session-123", "SessionEnd", transcript_path=str(transcript))
        self.assertEqual(self.invoke(event).stdout, "")
        path, row = self.records()["session-123"]
        self.assertEqual(set(row), FIELDS)
        self.assertNotEqual(path.stem, row["session_id"])
        self.assertEqual(row["transcript_path"], str(transcript))
        self.assertIsNone(row["reviewed_at"])
        self.assertNotIn("secret-canary", path.read_text(encoding="utf-8"))
        self.assertIn("transcript=available", self.scan().stdout)
        self.assertIn("pending: 0", self.mark("session-123", row["updated_at"]).stdout)
        reviewed = self.records()["session-123"][1]
        self.assertTrue(reviewed["reviewed_at"])
        self.mark("session-123", row["updated_at"])
        self.assertEqual(self.records()["session-123"][1], reviewed)
        self.invoke(event)
        updated = self.records()["session-123"][1]
        self.assertGreater(updated["updated_at"], row["updated_at"])
        self.assertIsNone(updated["reviewed_at"])
        self.assertEqual(len(self.records()), 1)

    def test_all_events_update_one_record_and_do_not_store_message_content(self):
        last = None
        for name in ("Stop", "Interrupt", "PreCompact", "SessionEnd"):
            result = self.invoke(self.event(name=name, turn_id="turn-1",
                                           last_assistant_message="secret-canary" * 7000))
            self.assertEqual(result.stdout.strip(), "{}" if name in {"Stop", "PreCompact"} else "")
            path, row = self.records()["session-123"]
            if last:
                self.assertGreater(row["updated_at"], last)
            last = row["updated_at"]
            self.assertEqual(set(row), FIELDS)
            self.assertIsNone(row["transcript_path"])
            self.assertNotIn("secret-canary", path.read_text(encoding="utf-8"))
        self.assertEqual(len(self.records()), 1)
        self.assertIn("queued: 1, reviewed: 0, pending: 1", self.scan().stdout)

    def test_record_identity_survives_rename(self):
        self.invoke(self.event())
        old_path, row = self.records()["session-123"]
        renamed = old_path.with_name("delivery-investigation.json")
        old_path.rename(renamed)
        self.mark("session-123", row["updated_at"])
        self.invoke(self.event())
        path, current = self.records()["session-123"]
        self.assertEqual(path, renamed)
        self.assertIsNone(current["reviewed_at"])
        self.assertEqual(len(self.records()), 1)

    def test_session_id_is_data_and_cannot_control_file_paths(self):
        for identity in ("../escaped", "folder/session", "CON", "session:stream"):
            self.invoke(self.event(identity))
        self.assertEqual(len(self.records()), 4)
        self.assertTrue(all(path.parent == self.state for path, _ in self.records().values()))
        self.assertFalse((self.repo / ".context" / "escaped.json").exists())

    def test_missing_or_relative_transcript(self):
        self.invoke(self.event("missing"))
        self.assertIsNone(self.records()["missing"][1]["transcript_path"])
        self.assertIn("transcript=missing", self.scan().stdout)
        self.invoke(self.event("relative", transcript_path="logs/session.jsonl"))
        self.assertEqual(self.records()["relative"][1]["transcript_path"],
                         str((self.repo / "logs" / "session.jsonl").resolve()))

    def test_review_requires_exact_checkpoint_and_rejects_stale_one(self):
        self.invoke(self.event())
        _, old = self.records()["session-123"]
        self.assertEqual(self.scan("--mark-reviewed", "session-123", check=False).returncode, 2)
        self.invoke(self.event())
        result = self.scan("--mark-reviewed", "session-123",
                           "--updated-at", old["updated_at"], check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkpoint changed", result.stderr)
        self.assertIsNone(self.records()["session-123"][1]["reviewed_at"])

    def test_empty_inventory_does_not_create_queue(self):
        self.assertIn("queued: 0", self.scan().stdout)
        result = self.scan("--mark-reviewed", "unknown", "--updated-at", "unknown", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.state.exists())

    def test_separate_sessions_keep_independent_review_state(self):
        for identity in ("first-session", "second-session"):
            self.invoke(self.event(identity))
        self.mark("first-session", self.records()["first-session"][1]["updated_at"])
        self.assertTrue(self.records()["first-session"][1]["reviewed_at"])
        self.assertIsNone(self.records()["second-session"][1]["reviewed_at"])

    def test_duplicate_identity_is_reported_without_mutation(self):
        self.invoke(self.event())
        path, _ = self.records()["session-123"]
        (path.parent / "duplicate.json").write_bytes(path.read_bytes())
        before = {p.name: p.read_bytes() for p in self.state.glob("*.json")}
        self.assertIn("duplicate session_id", self.scan(check=False).stderr)
        self.assertEqual(self.invoke(self.event(), check=False).returncode, 1)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.state.glob("*.json")})

    def test_malformed_record_is_reported_without_mutation(self):
        self.state.mkdir(parents=True)
        path = self.state / "broken.json"
        path.write_text("{broken", encoding="utf-8")
        self.assertEqual(self.scan(check=False).returncode, 2)
        self.assertEqual(self.invoke(self.event(), check=False).returncode, 1)
        self.assertEqual(path.read_text(encoding="utf-8"), "{broken")
        self.assertEqual(len(list(self.state.glob("*.json"))), 1)

    def test_invalid_events_and_non_git_directory_are_ignored(self):
        for event in ({}, [], self.event(name="SessionStart"), self.event(session_id="")):
            self.assertEqual(self.invoke(event).returncode, 0)
        self.assertFalse(self.state.exists())
        other = Path(self.temp.name) / "not a repository"
        other.mkdir()
        self.invoke(self.event(cwd=str(other)))
        self.assertFalse((other / ".context").exists())

    def test_concurrent_registration_deduplicates_session(self):
        workers = [subprocess.Popen(
            [sys.executable, str(HOOK)], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for _ in range(4)]
        for worker in workers:
            worker.stdin.write(json.dumps(self.event("shared")))
            worker.stdin.close()
            worker.stdin = None
        for worker in workers:
            out, err = worker.communicate(timeout=10)
            self.assertEqual(worker.returncode, 0, err)
            self.assertEqual(out.strip(), "{}")
        self.assertEqual(len(self.records()), 1)

    def test_review_waits_for_registration_lock_then_checks_current_record(self):
        self.invoke(self.event())
        path, row = self.records()["session-123"]
        with HOOK_API.queue_lock(self.state):
            worker = subprocess.Popen(
                [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed",
                 row["session_id"], "--updated-at", row["updated_at"]],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            with self.assertRaises(subprocess.TimeoutExpired):
                worker.wait(timeout=0.2)
            updated = dict(row, updated_at="2099-01-01T00:00:00+00:00")
            HOOK_API.write_record(path, updated)
        _, err = worker.communicate(timeout=10)
        self.assertEqual(worker.returncode, 2, err)
        self.assertIn("checkpoint changed", err)
        self.assertEqual(self.records()["session-123"][1], updated)

    def test_registration_waits_for_review_lock_then_resets_review(self):
        self.invoke(self.event())
        path, row = self.records()["session-123"]
        with SCAN_API.queue_lock(self.state):
            worker = subprocess.Popen(
                [sys.executable, str(HOOK)], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            worker.stdin.write(json.dumps(self.event()))
            worker.stdin.close()
            worker.stdin = None
            with self.assertRaises(subprocess.TimeoutExpired):
                worker.wait(timeout=0.2)
            SCAN_API.write_record(path, dict(row, reviewed_at="2026-10-03T12:00:00+00:00"))
        _, err = worker.communicate(timeout=10)
        self.assertEqual(worker.returncode, 0, err)
        self.assertIsNone(self.records()["session-123"][1]["reviewed_at"])
        self.assertGreater(self.records()["session-123"][1]["updated_at"], row["updated_at"])


if __name__ == "__main__":
    unittest.main()
