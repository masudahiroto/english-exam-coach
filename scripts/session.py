#!/usr/bin/env python3
"""Session and stage engine for the English Exam Coach skill.

A session file holds the blueprint, the hidden answer key, the learner
answers, stage timestamps with deadlines, and scores. The answer key is
only ever read by the grade command, never printed on its own.
Stdlib only.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def now():
    return datetime.now(timezone.utc)


def now_iso():
    return now().isoformat(timespec="seconds")


def data_dir(args):
    d = Path(args.data_dir or os.environ.get("ENGLISH_EXAM_COACH_DATA") or DEFAULT_DATA_DIR)
    (d / "sessions").mkdir(parents=True, exist_ok=True)
    return d


def session_path(d, session_id):
    return d / "sessions" / f"{session_id}.json"


def load_session(d, session_id):
    p = session_path(d, session_id)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save_session(d, session):
    session["updated_at"] = now_iso()
    session_path(d, session["id"]).write_text(
        json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def public_view(session):
    """Session data with the answer key removed, safe to show or summarize."""
    view = {k: v for k, v in session.items() if k != "answer_key"}
    return view


def cmd_create(args):
    d = data_dir(args)
    blueprint = {}
    if args.blueprint_file:
        blueprint = json.loads(Path(args.blueprint_file).read_text(encoding="utf-8"))
    elif args.blueprint_json:
        blueprint = json.loads(args.blueprint_json)
    answer_key = blueprint.pop("answer_key", {})
    if args.answer_key_file:
        answer_key = json.loads(Path(args.answer_key_file).read_text(encoding="utf-8"))
    stamp = now().strftime("%Y%m%d-%H%M%S")
    session_id = f"{stamp}-{args.preset.replace(' ', '-')}"
    session = {
        "id": session_id,
        "status": "open",
        "preset": args.preset,
        "exam": blueprint.get("exam", args.exam),
        "format": blueprint.get("format", args.format),
        "blueprint": blueprint,
        "answer_key": answer_key,
        "answers": {},
        "scores": {},
        "current_stage": "created",
        "stage_started_at": now_iso(),
        "deadline": None,
        "stage_history": [{"stage": "created", "at": now_iso()}],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    save_session(d, session)
    print(json.dumps({"id": session_id, "status": "open", "stage": "created"}, ensure_ascii=False))
    return 0


def cmd_stage(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    started = now()
    deadline = None
    if args.minutes:
        deadline = (started + timedelta(minutes=args.minutes)).isoformat(timespec="seconds")
    session["current_stage"] = args.name
    session["stage_started_at"] = started.isoformat(timespec="seconds")
    session["deadline"] = deadline
    session["stage_history"].append({"stage": args.name, "at": session["stage_started_at"], "deadline": deadline})
    save_session(d, session)
    print(json.dumps({
        "id": args.id,
        "stage": args.name,
        "started_at": session["stage_started_at"],
        "deadline": deadline,
    }, ensure_ascii=False))
    return 0


def cmd_time_left(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    result = {"id": args.id, "stage": session["current_stage"], "deadline": session["deadline"]}
    if session["deadline"]:
        delta = datetime.fromisoformat(session["deadline"]) - now()
        result["seconds_left"] = int(delta.total_seconds())
        result["overdue"] = delta.total_seconds() < 0
    started = datetime.fromisoformat(session["stage_started_at"])
    result["elapsed_seconds"] = int((now() - started).total_seconds())
    print(json.dumps(result, ensure_ascii=False))
    return 0


def cmd_set_answers(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    answers = {}
    if args.answers_file:
        answers = json.loads(Path(args.answers_file).read_text(encoding="utf-8"))
    elif args.answers_json:
        answers = json.loads(args.answers_json)
    session["answers"].update({str(k): v for k, v in answers.items()})
    save_session(d, session)
    print(json.dumps({"id": args.id, "answers_stored": len(session["answers"])}, ensure_ascii=False))
    return 0


def normalize(value):
    text = str(value).lower().strip()
    text = re.sub(r"[.,;:!?'\"]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def is_correct(given, expected):
    if given is None:
        return False
    options = expected if isinstance(expected, list) else [expected]
    return normalize(given) in {normalize(o) for o in options}


def cmd_grade(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    key = session.get("answer_key", {})
    answers = session.get("answers", {})
    items = []
    correct = 0
    for qid in sorted(key, key=lambda x: (len(x), x)):
        ok = is_correct(answers.get(qid), key[qid])
        correct += 1 if ok else 0
        items.append({"id": qid, "correct": ok, "given": answers.get(qid), "expected": key[qid]})
    total = len(key)
    result = {
        "id": args.id,
        "correct": correct,
        "total": total,
        "percent": round(100 * correct / total) if total else 0,
        "items": items,
    }
    session["scores"]["objective"] = {"correct": correct, "total": total, "percent": result["percent"]}
    save_session(d, session)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_set_score(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    session["scores"][args.section] = args.score
    save_session(d, session)
    print(json.dumps({"id": args.id, "scores": session["scores"]}, ensure_ascii=False))
    return 0


def cmd_show(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    view = public_view(session) if not args.include_key else session
    print(json.dumps(view, ensure_ascii=False, indent=2))
    return 0


def cmd_close(args):
    d = data_dir(args)
    session = load_session(d, args.id)
    if session is None:
        print(json.dumps({"error": "session not found"}))
        return 1
    session["status"] = "closed"
    session["current_stage"] = "closed"
    save_session(d, session)
    summary = {
        "ts": now_iso(),
        "session_id": args.id,
        "exam": session.get("exam"),
        "format": session.get("format"),
        "preset": session.get("preset"),
        "blueprint": session.get("blueprint", {}),
        "scores": session.get("scores", {}),
    }
    with (d / "history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args):
    d = data_dir(args)
    rows = []
    for p in sorted((d / "sessions").glob("*.json")):
        s = json.loads(p.read_text(encoding="utf-8"))
        rows.append({"id": s["id"], "status": s["status"], "preset": s["preset"], "stage": s["current_stage"]})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="English Exam Coach session engine")
    parser.add_argument("--data-dir", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create")
    p.add_argument("--preset", default="single-section")
    p.add_argument("--exam", default="IELTS")
    p.add_argument("--format", default="Academic")
    p.add_argument("--blueprint-file", default=None)
    p.add_argument("--blueprint-json", default=None)
    p.add_argument("--answer-key-file", default=None)
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("stage")
    p.add_argument("--id", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--minutes", type=float, default=None)
    p.set_defaults(func=cmd_stage)

    p = sub.add_parser("time-left")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_time_left)

    p = sub.add_parser("set-answers")
    p.add_argument("--id", required=True)
    p.add_argument("--answers-file", default=None)
    p.add_argument("--answers-json", default=None)
    p.set_defaults(func=cmd_set_answers)

    p = sub.add_parser("grade")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_grade)

    p = sub.add_parser("set-score")
    p.add_argument("--id", required=True)
    p.add_argument("--section", required=True)
    p.add_argument("--score", required=True)
    p.set_defaults(func=cmd_set_score)

    p = sub.add_parser("show")
    p.add_argument("--id", required=True)
    p.add_argument("--include-key", action="store_true", help="include the answer key (grading and debugging only)")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("close")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_close)

    p = sub.add_parser("list")
    p.set_defaults(func=cmd_list)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
