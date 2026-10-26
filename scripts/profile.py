#!/usr/bin/env python3
"""Learner profile store for the English Exam Coach skill.

All personal data lives in a data directory (default: ../data relative to
this script, override with --data-dir or ENGLISH_EXAM_COACH_DATA).
Stdlib only, so the skill runs anywhere Python 3 does.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REVIEW_INTERVALS_DAYS = [1, 3, 7, 14, 30]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def data_dir(args):
    d = Path(args.data_dir or os.environ.get("ENGLISH_EXAM_COACH_DATA") or DEFAULT_DATA_DIR)
    d.mkdir(parents=True, exist_ok=True)
    return d


def profile_path(d):
    return d / "profile.json"


def load_profile(d):
    p = profile_path(d)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save_profile(d, profile):
    profile["updated_at"] = now_iso()
    profile_path(d).write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path, record):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def cmd_init(args):
    d = data_dir(args)
    if profile_path(d).exists() and not args.force:
        print(json.dumps({"error": "profile already exists, use --force to overwrite"}))
        return 1
    profile = {
        "target_exam": args.target_exam,
        "target_format": args.target_format,
        "target_score": args.target_score,
        "exam_date": args.exam_date,
        "session_minutes": args.session_minutes,
        "estimated_level": {"band": args.level_band, "cefr": args.level_cefr},
        "weak_question_types": [],
        "voice_cast": {},
        "speech_check_passed": False,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    save_profile(d, profile)
    for name in ("errors.jsonl", "vocab.jsonl", "history.jsonl"):
        (d / name).touch(exist_ok=True)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def cmd_show(args):
    d = data_dir(args)
    profile = load_profile(d)
    if profile is None:
        print(json.dumps({"exists": False}))
        return 0
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def cmd_update(args):
    d = data_dir(args)
    profile = load_profile(d)
    if profile is None:
        print(json.dumps({"error": "no profile, run init first"}))
        return 1
    for field in ("target_exam", "target_format", "target_score", "exam_date", "session_minutes"):
        value = getattr(args, field)
        if value is not None:
            profile[field] = value
    if args.level_band is not None or args.level_cefr is not None:
        level = profile.get("estimated_level", {})
        if args.level_band is not None:
            level["band"] = args.level_band
        if args.level_cefr is not None:
            level["cefr"] = args.level_cefr
        profile["estimated_level"] = level
    if args.speech_check_passed:
        profile["speech_check_passed"] = True
    save_profile(d, profile)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def cmd_set_voices(args):
    d = data_dir(args)
    profile = load_profile(d)
    if profile is None:
        print(json.dumps({"error": "no profile, run init first"}))
        return 1
    try:
        cast = json.loads(args.cast_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"invalid cast json: {e}"}))
        return 1
    profile["voice_cast"] = cast
    save_profile(d, profile)
    print(json.dumps({"voice_cast": cast}, ensure_ascii=False))
    return 0


def cmd_log_error(args):
    d = data_dir(args)
    record = {
        "ts": now_iso(),
        "category": args.category,
        "pattern": args.pattern,
        "example": args.example,
        "session_id": args.session_id,
    }
    append_jsonl(d / "errors.jsonl", record)
    print(json.dumps(record, ensure_ascii=False))
    return 0


def cmd_errors(args):
    d = data_dir(args)
    rows = read_jsonl(d / "errors.jsonl")
    print(json.dumps(rows[-args.recent:], ensure_ascii=False, indent=2))
    return 0


def cmd_add_vocab(args):
    d = data_dir(args)
    due = (datetime.now(timezone.utc) + timedelta(days=REVIEW_INTERVALS_DAYS[0])).date().isoformat()
    record = {
        "ts": now_iso(),
        "term": args.term,
        "meaning": args.meaning,
        "example": args.example,
        "stage": 0,
        "due": due,
        "graduated": False,
    }
    append_jsonl(d / "vocab.jsonl", record)
    print(json.dumps(record, ensure_ascii=False))
    return 0


def cmd_vocab_due(args):
    d = data_dir(args)
    today = datetime.now(timezone.utc).date().isoformat()
    rows = [r for r in read_jsonl(d / "vocab.jsonl") if not r.get("graduated") and r.get("due", "") <= today]
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def cmd_history(args):
    d = data_dir(args)
    rows = read_jsonl(d / "history.jsonl")
    print(json.dumps(rows[-args.recent:], ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="English Exam Coach learner profile store")
    parser.add_argument("--data-dir", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--target-exam", required=True)
    p.add_argument("--target-format", required=True)
    p.add_argument("--target-score", required=True)
    p.add_argument("--exam-date", default=None)
    p.add_argument("--session-minutes", type=int, default=25)
    p.add_argument("--level-band", default="6.0")
    p.add_argument("--level-cefr", default="B2")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("show")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("update")
    p.add_argument("--target-exam", default=None)
    p.add_argument("--target-format", default=None)
    p.add_argument("--target-score", default=None)
    p.add_argument("--exam-date", default=None)
    p.add_argument("--session-minutes", type=int, default=None)
    p.add_argument("--level-band", default=None)
    p.add_argument("--level-cefr", default=None)
    p.add_argument("--speech-check-passed", action="store_true")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("set-voices")
    p.add_argument("--cast-json", required=True, help='JSON object like {"examiner": {"voice_id": "...", "accent": "British"}}')
    p.set_defaults(func=cmd_set_voices)

    p = sub.add_parser("log-error")
    p.add_argument("--category", required=True)
    p.add_argument("--pattern", required=True)
    p.add_argument("--example", default="")
    p.add_argument("--session-id", default=None)
    p.set_defaults(func=cmd_log_error)

    p = sub.add_parser("errors")
    p.add_argument("--recent", type=int, default=20)
    p.set_defaults(func=cmd_errors)

    p = sub.add_parser("add-vocab")
    p.add_argument("--term", required=True)
    p.add_argument("--meaning", default="")
    p.add_argument("--example", default="")
    p.set_defaults(func=cmd_add_vocab)

    p = sub.add_parser("vocab-due")
    p.set_defaults(func=cmd_vocab_due)

    p = sub.add_parser("history")
    p.add_argument("--recent", type=int, default=10)
    p.set_defaults(func=cmd_history)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
