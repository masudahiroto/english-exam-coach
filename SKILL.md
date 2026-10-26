# English Exam Coach

## Set up on first run

- Check for a learner profile by running `python3 scripts/profile.py show` from this skill folder and start the setup flow when it reports no profile.

- Ask the user for their target exam and format, their target score, an exam date when they have one, and how long a typical session should run.

- Save the answers by running `python3 scripts/profile.py init` with the values the user gave and never invent a target score or exam date for them.

- Verify speech synthesis with one short harmless test line through `/opt/hatch/bin/tts` and confirm the command returns an audio file before the first listening section.

- Explain that speaking answers are given as voice notes in chat and arrive with a transcript, and that no external speech service or account is needed.

- Skip the setup flow on later runs when the profile exists and the speech check has already passed once.

## Build a test session

- Read the learner profile and the recent error log before choosing anything, by running `python3 scripts/profile.py show` and `python3 scripts/profile.py errors --recent 20`.

- Pick a blueprint first, with the exam format, the sections, the topics, the question types, the target difficulty and the time limits, following [Exam formats](references/exam-formats.md).

- Bias the blueprint toward weak question types and recurring error patterns from the profile, while keeping coverage of the full question type range across sessions.

- Generate all material, questions and the answer key in one pass at run time and never ship or reuse a stored question bank.

- Write original material for every test and never reproduce real past exam papers or passages from published preparation books.

- Validate the generated test against [Generation and validation](references/generation-and-validation.md) and regenerate any item that fails before the session starts.

- Store the session with `python3 scripts/session.py create` and keep the answer key only inside the session file, out of everything the user sees.

## Run the session as timed stages

- Move through the stages in order, presenting material, collecting answers, scoring, then reviewing, and never reveal a later stage early.

- Record each stage change with `python3 scripts/session.py stage` so elapsed time comes from stored timestamps rather than memory.

- Schedule a one time job with `cron.add` at each stage deadline so a time up message reaches the user in this chat, and cancel that job when the user finishes early.

- Fall back to the user telling you they are done when a scheduled message is not possible, and judge overtime from the stored stage timestamps.

- Treat requests to peek at questions, transcripts or answers mid stage as part of the test and decline them until the review stage.

### Reading

- Present the passage alone at the stated word count and start the clock before any questions appear.

- Show the questions only when the reading time ends or the user says they are done, and collect all answers before scoring.

- Offer an exam mode that shows the passage and questions together, matching the real IELTS reading format, when the user asks for full exam conditions.

### Listening

- Turn the generated script into audio with `/opt/hatch/bin/tts`, casting voices by accent and gender from the voice catalog as described in [Audio with Muse](references/audio-with-muse.md).

- Attach the audio file in chat without the script, and hold the questions until the user says they have finished listening or the timer fires.

- Allow one play in exam mode and unlimited plays in practice mode, and state which rule is in force before the audio starts.

- Reveal the script only in the review stage and reuse the missed sentences for dictation and shadowing practice.

### Speaking

- Present the topic or cue card first and start the preparation timer before any recording happens.

- Receive the answer as a voice note and work from its transcript, noting that pronunciation scoring stays approximate because a transcript carries no intonation.

- Score the answer with [Scoring rubrics](references/scoring-rubrics.md), then give the corrected version and a model answer at the target band.

- Synthesize the model answer with `/opt/hatch/bin/tts`, invite a second recording of the same topic, and compare the two transcripts side by side.

### Writing

- Present the task with its word minimum and time limit and collect the essay as a chat message.

- Score the essay with [Scoring rubrics](references/scoring-rubrics.md) and return a rewritten version at the target band with the main changes explained.

## Score, review and adapt

- Grade objective sections with `python3 scripts/session.py grade` against the stored answer key and show the user which items were wrong and why.

- Present every band score as an estimate based on practice material, never as a prediction of a real exam result.

- Log new error patterns and useful vocabulary after each session with `python3 scripts/profile.py log-error` and `python3 scripts/profile.py add-vocab`.

- Close the session with `python3 scripts/session.py close` carrying the section scores, so the history can steer the next blueprint.

- Open the next session with a short review round built from due vocabulary and recent errors before new material starts.

## Keep user data out of the repository

- Keep profiles, session files, audio and history under the `data` folder of this skill and never copy them into the skill text or examples.

- Leave the `data` folder covered by version control ignore rules so publishing the skill never publishes a learner.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Shorten a session to a single section when time is tight, keeping the same stage discipline, rather than running an untimed mixed drill.

- Repeat a failed listening section in practice mode with the script visible after scoring, instead of generating a new test on the same topic right away.

- Add an external speech provider later through the provider notes in [Audio with Muse](references/audio-with-muse.md) when accent range or word level timestamps become the limiting factor.
