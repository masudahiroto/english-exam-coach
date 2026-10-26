# Profile and personalization

The skill is generic. Everything personal lives in one profile file per learner under the `data` folder, managed only through `scripts/profile.py`. Publishing or sharing the skill folder never shares the learner, because `data` is ignored by version control.

## Profile fields

- `target_exam` and `target_format`: for example IELTS and Academic.
- `target_score`: the band or score the learner is aiming for, in their own words from setup.
- `exam_date`: optional, used only to pace full mock frequency.
- `session_minutes`: the default session length the learner asked for.
- `estimated_level`: the current working difficulty, as a band aim and CEFR level, updated by results rather than by self report alone.
- `weak_question_types`: question types with the lowest recent accuracy, recomputed from session history.
- `voice_cast`: the listening voices the learner settled on, as voice ids with accent and role.
- `created_at` and `updated_at`: timestamps.

Alongside the profile, the same folder holds `errors.jsonl` with one tagged error pattern per line, `vocab.jsonl` with words and phrases to review, and `history.jsonl` with one summary line per closed session. The scripts own these files, so read and write them through the scripts.

## How adaptation works

- The blueprint for each new session reads the profile, the last twenty errors and the session history before choosing topics, question types and difficulty.
- A question type joins the weak list when accuracy on it drops under 60 percent across the last three attempts, and leaves after two attempts at 80 percent or better.
- Difficulty moves by the rule in the generation reference, one lever at a time.
- Topics rotate through the common IELTS set: education, environment, technology, health, work, transport, cities, media, science, food, travel and society. A topic returns only after at least three other topics have run, unless the learner asks for it.
- Vocabulary review uses expanding intervals of 1, 3, 7, 14 and 30 days. Items the learner produces correctly in a later speaking or writing answer graduate off the list.
- At the start of a session, due vocabulary and the two most recent error patterns become a five minute review round before new material.

## Setup conversation

Setup stays short. Ask for target exam and format, target score, exam date if any, and preferred session length. Set the starting difficulty from any past score the learner mentions, otherwise start at band 6.0 and CEFR B2 and let the first two sessions calibrate it. Run one short listening sample during setup only when the learner wants to pick voices, and store the chosen cast in the profile.
