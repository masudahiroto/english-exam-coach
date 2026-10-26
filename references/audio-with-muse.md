# Audio with Muse

The MVP uses only Muse built in speech tools. No external speech account, API key or connector is required. This file records what those tools do, verified against the local tools, and where an external provider would later plug in.

## Speech synthesis for listening

- Synthesize monologues with `/opt/hatch/bin/tts speak` and `--voice`, which writes an MP3 file and needs no account connection.
- Synthesize every dialogue with `/opt/hatch/bin/tts synthesize-script`, a saved script file and one `--speaker Name=voice_id` mapping per speaker. Speaker labels in the script are routing information for the synthesizer and are never spoken.
- Never put speaker labels in text sent to `speak`, and never use the `speak` two voice prefix options for exam dialogues. An early sample made that way read the labels aloud and rendered the whole dialogue in a single voice.
- Set `--language en` for English material and use `--speed` between 1 and 200 to slow practice audio or match a harder target pace. The default is 100.
- Spell out numbers, dates and abbreviations in the script the way they should be heard, because the synthesizer reads what it is given.

## Casting voices

- Read the voice catalog at `/opt/muse/assets/voice-selector/voice_source.json`, where each voice lists an id, a gender and an accent.
- Cast IELTS listening with contrasting British, Australian and American voices, and keep the same cast across sessions once the learner has settled on one. The catalog holds over a hundred British voices and dozens of Australian and American ones, so accent coverage is not the limiting factor.
- Prefer clear, neutral tones for exam material over character voices, and store the chosen ids in the learner profile.

## Speech to text for speaking

- The learner answers with a voice note in chat, and the message arrives with a transcript. Work from that transcript for content, grammar and fluency evidence.
- Longer recordings on the automatic voice note path cap at about 8 MB, which covers a speaking part comfortably but not a full mock in one file, so collect answers part by part.
- Speaker separation is not guaranteed, which is fine for solo speaking answers and a reason to keep listening dialogues synthetic rather than recorded.
- A transcript cannot carry intonation or stress. Score pronunciation approximately, say what was and was not judged, and never present a pronunciation band as precise.

## Known limits of the built in route

- No word level timestamps, so pause length and words per minute come from recording length and transcript word count rather than exact timings.
- Voice choice is limited to the catalog and saved designed voices. Arbitrary new voices cannot be designed on request.
- Synthesis runs per chunk with a default chunk size of 1,200 characters for scripts, so long listening sections are assembled from chunks and should be checked for joins before the session starts.

## Swapping in an external provider later

The skill talks about speech through two operations only, turning a script into an audio file and turning a spoken answer into a transcript. An external provider such as ElevenLabs, through its official MCP server, replaces those two operations without touching the session engine, the blueprints or the rubrics. It would add word level timestamps, speaker diarization and a wider designed voice library, at the cost of each learner connecting their own account and credits. Keep that swap behind the setup flow, so the skill still runs with built in speech when no provider is connected.
