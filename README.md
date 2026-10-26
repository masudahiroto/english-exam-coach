# English Exam Coach

A Muse skill that runs IELTS style English exam practice as a real test, not a worksheet. Reading, listening, speaking and writing sections are generated on the fly for each session, presented in timed stages, scored against IELTS criteria, and folded back into a learner profile that steers the next test toward the learner weak points.

No question bank ships with the skill. Every passage, listening script, cue card and essay task is written at run time from a blueprint, validated, used once and discarded. Only scores, error patterns and vocabulary are kept.

The MVP runs entirely on Muse built in capabilities. Listening audio is synthesized with Muse text to speech, speaking answers are given as voice notes and scored from their transcripts, and no external speech service, API key or account is required. An external provider such as ElevenLabs can replace the speech layer later without changing the test engine.

## How a session runs

1. Setup, first run only: target exam and format, target score, exam date if any, session length, plus a speech synthesis check.
2. Blueprint: topic, question types, difficulty and time limits are chosen from the learner profile, weighted toward weak areas.
3. Generation and validation: material, questions and the answer key are created together, then checked by solving the questions blind against the key, counting words and confirming timing.
4. Timed stages: material first, questions only when the stage timer ends or the learner says they are done. A one time scheduled message enforces the deadline in chat where possible.
5. Scoring and review: objective sections are graded from the hidden key, speaking and writing are scored on the four IELTS criteria, and every score is reported as a practice estimate.
6. Adaptation: errors and vocabulary are logged, difficulty and question type weighting adjust for the next session, and due vocabulary opens the next session as a review round.

## Layout

- `SKILL.md` holds the method the agent follows.
- `skill.yaml` is the Muse skill descriptor.
- `references/` holds the format pack contract and the IELTS pack, the generation and validation rules, the profile and personalization design, and notes on speech with Muse built in tools. Exam specific content lives in format packs, so TOEFL and other exams can be added as two new reference files without touching the engine or the scripts.
- Sessions scale from a full mock down to a quick drill of a single question, which runs through the same staged flow and is scored as a raw result without a band conversion.
- `scripts/profile.py` manages the learner profile, the error log, the vocabulary list and session history.
- `scripts/session.py` is the session and stage engine. It stores the hidden answer key, stage timestamps and deadlines, grades objective answers and closes sessions into history.
- `templates/` holds example profile and blueprint files.
- `data/` is created at run time and holds all learner data. It is gitignored and must never be committed.

## Scripts quick start

```bash
cd scripts

# first run setup
python3 profile.py init --target-exam IELTS --target-format Academic --target-score 7.0 --session-minutes 25

# start a session from a blueprint file (the blueprint carries the answer key)
python3 session.py create --preset single-section --blueprint-file ../templates/blueprint.example.json

# move a stage and set its deadline in minutes
python3 session.py stage --id <session-id> --name listening_audio --minutes 3

# store answers and grade them against the hidden key
python3 session.py set-answers --id <session-id> --answers-json '{"q1": "example answer"}'
python3 session.py grade --id <session-id>

# log learning data and close out
python3 profile.py log-error --category collocation --pattern "do a decision" --example "I did a decision."
python3 profile.py add-vocab --term "make a decision" --meaning "to decide"
python3 session.py close --id <session-id>
```

Both scripts use only the Python 3 standard library. Data location defaults to the skill `data` folder and can be overridden with `--data-dir` or the `ENGLISH_EXAM_COACH_DATA` environment variable.

## Status

MVP. The IELTS format pack is complete for all four skills. TOEFL and other exams are designed as additional format packs and are not implemented yet. Speaking pronunciation is scored approximately from transcripts, because a transcript carries no intonation. Scores are practice estimates, not predictions of real exam results.

## License

MIT
