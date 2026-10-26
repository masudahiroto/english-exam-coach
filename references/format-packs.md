# Format packs

The engine of this skill is exam agnostic. The session stages, the generation and validation rules, the learner profile and both scripts know nothing about IELTS. Everything exam specific lives in a format pack, and the loaded pack is chosen from the learner target exam at session start.

## What a pack contains

A pack is two reference files plus a row in the index below.

- A formats file named `exam-formats-<exam>.md` that defines the sections and their order, the timing of each section, word counts for reading passages and listening scripts, the question types in rotation, the practice slice sizes and the session presets.
- A scoring file named `scoring-<exam>.md` that defines the score scale, any raw score conversion tables, the subjective marking criteria with band or score anchors, the feedback order and the error taxonomy additions the pack needs.

## Pack index

- IELTS: formats in [Exam formats](exam-formats.md), scoring in [Scoring rubrics](scoring-rubrics.md). These two files are the IELTS pack and keep their original names because the MVP shipped with them.
- TOEFL, EIKEN and others: not yet written. Add them under the naming rule above and register the row here.

## How the engine uses a pack

- Setup stores only the exam name and variant in the profile, for example IELTS Academic or TOEFL iBT. No exam values are baked into the scripts.
- A session records the exam and format from the pack, and the blueprint draws section specs, question types and difficulty calibration from the pack formats file.
- Objective grading never changes between packs, because it compares learner answers with the session answer key. Only the conversion of raw scores into the pack scale comes from the pack scoring file.
- Subjective scoring loads the pack scoring file, so speaking and writing criteria follow the target exam rather than IELTS by default.
- Difficulty is expressed inside a pack in its own scale, with a CEFR level kept alongside as the common reference when a learner switches exams.

## Adding a new pack

1. Write the formats file and the scoring file for the exam, following the headings of the IELTS pack files.
2. Register the pack in the index above.
3. Nothing else changes. The scripts take exam and format as free text fields, the stage engine is timing based, and the profile already stores any target exam and score in the learner own words.
