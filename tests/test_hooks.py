"""Integration checks for the CSV session registrar and review helper."""

from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "integrations" / "codex" / ".codex"
HOOK = CODEX / "hooks" / "context_register_session.py"
SCAN = ROOT / "skills" / "context-review-sessions" / "scripts" / "context_read_sessions.py"
FIELDS = ["session_date", "session_id", "path", "reviewed_date"]


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
        self.state = self.repo / ".context"
        self.log = self.state / "sessions.log"
        self.transcript = self.repo / "session.jsonl"
        self.transcript.write_text("secret-canary\n", encoding="utf-8")

    def event(self, session_id="session-123", name="Stop", **extra):
        return {"hook_event_name": name, "session_id": session_id,
                "cwd": str(self.repo), "transcript_path": "session.jsonl", **extra}

    def invoke(self, event, check=True):
        return subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(event),
            text=True, encoding="utf-8", capture_output=True, cwd=self.repo, check=check,
        )

    def scan(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(SCAN), str(self.repo), *args],
            text=True, encoding="utf-8", capture_output=True, check=check,
        )

    def records(self):
        if not self.log.exists():
            return {}
        with self.log.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, FIELDS)
            return {row["session_id"]: row for row in reader}

    def mark(self, identity="session-123"):
        return self.scan("--mark-reviewed", identity)

    def write_rows(self, rows):
        self.state.mkdir(exist_ok=True)
        with self.log.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_hook_commands_from_subdirectory_with_spaces(self):
        hook_dir = self.repo / ".codex" / "hooks"
        hook_dir.mkdir(parents=True)
        (hook_dir / HOOK.name).write_bytes(HOOK.read_bytes())
        cwd = self.repo / "nested directory"
        cwd.mkdir()
        config = json.loads((CODEX / "hooks.json").read_text(encoding="utf-8"))
        command_field = "commandWindows" if sys.platform == "win32" else "command"
        for name, groups in config["hooks"].items():
            result = subprocess.run(
                groups[0]["hooks"][0][command_field], shell=True, cwd=cwd,
                input=json.dumps(self.event("windows-session", name, cwd=str(cwd))),
                text=True, capture_output=True, check=True,
            )
            if name == "SessionStart":
                expected_skills = {
                    path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")
                }
                mentioned_skills = set(re.findall(r"\bcontext-[a-z-]+\b", result.stdout))
                self.assertEqual(mentioned_skills, expected_skills)
                self.assertNotIn("index", result.stdout.lower())
                self.assertIn(".context/sessions.log", result.stdout)
                self.assertIn(".context/.sessions.lock", result.stdout)
                self.assertFalse(self.state.exists())
        self.assertEqual(len(self.records()), 1)
        self.assertFalse((self.state / "INDEX.md").exists())
        self.assertFalse((self.state / "sessions").exists())

    def test_record_and_review_lifecycle(self):
        self.assertEqual(self.invoke(self.event(name="SessionEnd")).stdout, "")
        row = self.records()["session-123"]
        self.assertEqual(row, {
            "session_date": datetime.date.today().isoformat(), "session_id": "session-123",
            "path": str(self.transcript), "reviewed_date": "",
        })
        self.assertNotIn("secret-canary", self.log.read_text(encoding="utf-8"))
        self.assertIn("transcript=available", self.scan().stdout)
        self.assertIn("pending: 0", self.mark().stdout)
        reviewed = self.records()["session-123"]
        self.assertEqual(reviewed["reviewed_date"], datetime.date.today().isoformat())
        before = self.log.read_bytes()
        self.mark()
        self.assertEqual(self.log.read_bytes(), before)
        self.invoke(self.event())
        self.assertEqual(self.records()["session-123"], reviewed)

    def test_all_events_keep_one_row_and_preserve_review(self):
        self.invoke(self.event())
        self.mark()
        reviewed_date = self.records()["session-123"]["reviewed_date"]
        for name in ("Stop", "Interrupt", "PreCompact", "SessionEnd"):
            result = self.invoke(self.event(name=name, last_assistant_message="secret-canary" * 7000))
            self.assertEqual(result.stdout.strip(), "{}" if name in {"Stop", "PreCompact"} else "")
            self.assertEqual(len(self.records()), 1)
            self.assertEqual(self.records()["session-123"]["reviewed_date"], reviewed_date)
        self.assertNotIn("secret-canary", self.log.read_text(encoding="utf-8"))

    def test_registration_preserves_dates_when_path_changes(self):
        self.invoke(self.event())
        row = dict(self.records()["session-123"], **{"session_date": "2025-01-02", "reviewed_date": "2025-01-03"})
        self.write_rows([row])
        self.invoke(self.event(transcript_path="moved.jsonl"))
        self.assertEqual(self.records()["session-123"]["session_date"], "2025-01-02")
        self.assertEqual(self.records()["session-123"]["reviewed_date"], "2025-01-03")
        self.assertEqual(self.records()["session-123"]["path"], str(self.repo / "moved.jsonl"))

    def test_csv_round_trip_for_paths_and_identifiers(self):
        path = self.repo / "żółć, flight logs" / "session.jsonl"
        path.parent.mkdir()
        path.write_text("example", encoding="utf-8")
        identities = ("../escaped", "folder/session", "CON", 'id,"quoted"')
        for identity in identities:
            self.invoke(self.event(identity, transcript_path=str(path)))
        self.assertEqual(set(self.records()), set(identities))
        self.assertTrue(all(row["path"] == str(path) for row in self.records().values()))
        self.assertEqual(len(list(self.state.glob("*.log"))), 1)
        self.assertEqual(list(self.state.glob("*.json")), [])
        self.assertFalse((self.repo / "escaped").exists())

    def test_pathless_events_do_not_create_or_change_records(self):
        for name in ("Stop", "Interrupt", "PreCompact", "SessionEnd"):
            for transcript in (None, "", "   ", 42):
                result = self.invoke(self.event(name=name, transcript_path=transcript))
                self.assertEqual(result.stdout.strip(), "{}" if name in {"Stop", "PreCompact"} else "")
                self.assertFalse(self.state.exists())
        self.invoke(self.event())
        self.mark()
        self.invoke(self.event("unknown", transcript_path=None))
        self.assertTrue(self.records()["session-123"]["reviewed_date"])
        before = self.log.read_bytes()
        for empty_path in (None, "", "   ", 42):
            self.invoke(self.event(transcript_path=empty_path))
            self.assertEqual(self.log.read_bytes(), before)
        self.assertEqual(len(self.records()), 1)

    def test_missing_transcript_is_registered_but_cannot_be_marked(self):
        self.invoke(self.event(transcript_path="logs/not-yet-created.jsonl"))
        self.assertEqual(self.records()["session-123"]["path"],
                         str(self.repo / "logs" / "not-yet-created.jsonl"))
        self.assertIn("transcript=missing-file", self.scan().stdout)
        result = self.scan("--mark-reviewed", "session-123", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.records()["session-123"]["reviewed_date"], "")

    def test_same_day_transcript_change_does_not_block_review(self):
        self.invoke(self.event())
        self.transcript.write_text("new evidence after listing\n", encoding="utf-8")
        self.invoke(self.event())
        self.mark()
        self.assertEqual(self.records()["session-123"]["reviewed_date"], datetime.date.today().isoformat())

    def test_separate_sessions_keep_independent_review_state(self):
        for identity in ("first", "second"):
            self.invoke(self.event(identity))
        second = self.records()["second"]
        self.mark("first")
        self.assertEqual(self.records()["second"], second)
        self.invoke(self.event("second"))
        self.assertTrue(self.records()["first"]["reviewed_date"])
        self.assertEqual(self.records()["second"]["reviewed_date"], "")

    def test_old_json_records_are_not_imported(self):
        old_directory = self.state / "sessions"
        old_directory.mkdir(parents=True)
        old_record = old_directory / "old.json"
        old_record.write_text('{"session_id":"old"}', encoding="utf-8")
        self.assertIn("queued: 0, reviewed: 0, pending: 0", self.scan().stdout)
        self.assertFalse(self.log.exists())
        self.invoke(self.event("new"))
        self.assertEqual(set(self.records()), {"new"})

    def test_old_csv_schema_is_rejected_without_conversion(self):
        self.state.mkdir()
        content = "date-added,guid,path,date-reviewd\n2026-10-14,old,old.jsonl,\n"
        self.log.write_text(content, encoding="utf-8")
        self.assertEqual(self.scan(check=False).returncode, 2)
        self.assertEqual(self.invoke(self.event(), check=False).returncode, 1)
        self.assertEqual(self.log.read_text(encoding="utf-8"), content)

    def test_duplicate_or_malformed_log_is_never_overwritten(self):
        self.invoke(self.event())
        row = self.records()["session-123"]
        self.write_rows([row, row])
        cases = [self.log.read_bytes(), b"broken\n", b"session_date,session_id,path,reviewed_date\n2026-99-01,id,path,\n"]
        for content in cases:
            self.log.write_bytes(content)
            self.assertEqual(self.scan(check=False).returncode, 2)
            self.assertEqual(self.invoke(self.event(), check=False).returncode, 1)
            self.assertEqual(self.log.read_bytes(), content)

    def test_invalid_events_and_non_git_directory_are_ignored(self):
        for event in ({}, [], self.event(name="SessionStart"), self.event(session_id="")):
            self.assertEqual(self.invoke(event).returncode, 0)
        self.assertFalse(self.state.exists())
        other = Path(self.temp.name) / "not a repository"
        other.mkdir()
        self.invoke(self.event(cwd=str(other)))
        self.assertFalse((other / ".context").exists())

    def test_subagent_with_transcript_is_not_filtered(self):
        self.invoke(self.event("subagent", source={"subagent": {"thread_spawn": {}}}))
        self.assertIn("subagent", self.records())

    def test_concurrent_registration_preserves_all_sessions_and_deduplicates(self):
        identities = ["shared", "first", "shared", "second"]
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda identity: self.invoke(self.event(identity)), identities))
        self.assertTrue(all(result.returncode == 0 for result in results))
        self.assertEqual(set(self.records()), {"shared", "first", "second"})

    def test_registration_waits_for_review_lock_then_preserves_review(self):
        self.invoke(self.event())
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
            rows = self.records()
            rows["session-123"]["reviewed_date"] = "2026-10-03"
            SCAN_API.write_sessions(self.log, rows)
        _, errors = worker.communicate(timeout=10)
        self.assertEqual(worker.returncode, 0, errors)
        self.assertEqual(self.records()["session-123"]["reviewed_date"], "2026-10-03")

    def test_review_waits_for_lock_and_accepts_changed_transcript(self):
        self.invoke(self.event())
        with HOOK_API.queue_lock(self.state):
            worker = subprocess.Popen(
                [sys.executable, str(SCAN), str(self.repo), "--mark-reviewed", "session-123"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            with self.assertRaises(subprocess.TimeoutExpired):
                worker.wait(timeout=0.2)
            self.transcript.write_text("changed while reviewer waited", encoding="utf-8")
        _, errors = worker.communicate(timeout=10)
        self.assertEqual(worker.returncode, 0, errors)
        self.assertEqual(self.records()["session-123"]["reviewed_date"], datetime.date.today().isoformat())


if __name__ == "__main__":
    unittest.main()
