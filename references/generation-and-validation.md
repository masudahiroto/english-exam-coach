# Generation and validation

Every test is generated at run time from a blueprint. Nothing is drawn from a stored question bank, and generated questions are discarded after the session. Only scores, error patterns and vocabulary survive into the learner profile.

## The blueprint

Fix these fields before generating anything:

- Exam and format pack, section and slice size
- Topic, drawn from the rotation in the profile reference and checked against recent sessions so topics do not repeat back to back
- Question types for this slice, weighted toward the learner weak types
- Target difficulty, expressed as an IELTS band aim and a CEFR level
- Word count for reading passages or spoken words for listening scripts
- Time limit for each stage

## Generation rules

- Write the material, the questions and the answer key in one pass so they agree with each other.
- Build listening and reading questions around paraphrase. The correct answer should rarely reuse the exact wording of the material, and distractors should be plausible statements the material contradicts or never makes.
- Keep every question answerable from the material alone. Outside knowledge must never decide an answer.
- Give objective questions exactly one defensible answer. Avoid negative stems and trick wording that the real exam would not use.
- Write listening scripts as speech, with natural fillers kept light, numbers and spellings spoken the way a person would say them, and speaker turns short enough for two voice synthesis.
- Calibrate difficulty through vocabulary range, sentence length, speech speed, density of distractors and how directly answers are stated, in that order of preference.
- Stay at the stated word count within about five percent either way. Count words with a tool rather than estimating.

## Validation before the session starts

Run these checks and regenerate the failing item, never the whole test, when one fails:

1. Solve the questions blind from the material alone, without looking at the key. Any mismatch with the key means the item is ambiguous or wrong, so rewrite it.
2. Check the word count of each passage and script against the blueprint.
3. Check that every question type in the slice appears in the rotation for that section.
4. Check that names, numbers and facts are consistent across the material, the questions and the key.
5. For listening, estimate audio length from word count at roughly 150 words per minute and confirm it fits the stage timing.
6. Confirm the material is original. Similar topics to real exams are fine, copied passages and remembered past paper items are not.

## Difficulty adjustment between sessions

Raise the target difficulty one step after two consecutive slices at 80 percent or better. Lower it one step after a slice under 50 percent. Change only one calibration lever at a time so the learner can feel what changed.
