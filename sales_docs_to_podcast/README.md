

# Sales Docs to Podcast — Showcase

Turn long-form sales materials into a short, single‑speaker podcast your sellers can listen to in the car. This showcase ingests a sales document, crafts a spoken‑word briefing using an LLM, and synthesizes natural audio using a TTS service. The output is an MP3 saved locally.

## What this is
- A pragmatic demo for sales enablement: convert slides, briefs, or product notes into a listenable summary.
- Optimized for in‑car comprehension: clear signposts, minimal jargon, and pacing that favors retention.
- Designed for internal use; it begins with an AI disclaimer and avoids reading dense tables verbatim.

## High‑level architecture
```
┌──────────────────────────┐     ┌────────────────────────┐     ┌──────────────────────┐
│ Document Ingestion       │ --->│ Script Generation      │ --->│ Text‑to‑Speech (TTS) │
│ (CLI + file reader)      │     │ (LLM w/ prompt)        │     │ (voice synthesis)    │
└─────────────┬────────────┘     └────────────────────────┘     └────────────┬─────────┘
              │                                                              │
              │                                                              ▼
              │                                                     ┌───────────────────┐
              │                                                     │ MP3 Writer        │
              │                                                     │ (out/ directory)  │
              ▼                                                     └───────────────────┘
     ┌────────────────┐
     │ Prompt Template│
     │ (prompts/)     │  Provides style/structure guidance to the LLM
     └────────────────┘
```

Components:
- Document ingestion: Accepts a path to a text file and loads the content.
- Script generation: Combines the content with a narrative prompt to produce a single‑speaker podcast script suitable for listening.
- Text‑to‑speech: Synthesizes the script into natural speech using a hosted TTS model.
- Orchestration: Wires these stages together and saves the resulting MP3 to the out folder.

## End‑to‑end flow
1. You provide a path to a sales document.
2. The system loads a prompt that enforces a friendly, professional, in‑car‑ready style with an opening disclaimer and clear structure.
3. An LLM generates a concise, single‑voice script covering why it matters, key takeaways, a scoped deep dive, and a short action checklist.
4. A TTS engine converts that script into an MP3 using a configured voice.
5. The audio file is exported.

## Setup
- Requirements
  - Python 3.10+ is recommended.
  - Install dependencies: `pip install -r requirements.txt`
- Credentials
  - Create .env from .env.template
  - Set the following environment variables:
    - OPENAI_API_KEY — for script generation
    - ELEVENLABS_API_KEY — for text‑to‑speech
- Network access must be enabled to call the LLM and TTS services.

## Running the showcase
From the project root:

```powershell
cd .\sales_docs_to_podcast
python .\transform_to_podcast.py ".\data\GlimmerGlas.txt"
```

Notes
- Input: Only Plain‑text documents.
- Output: MP3 File.
- Duration: Target length is roughly 5–10 minutes (actual time depends on content and model pacing).

## Extending the showcase
- Inputs: Add loaders for other formats (e.g., PDF via OCR or markdown parsing) before handing text to the script generation stage.
- Prompting: Adjust the prompt template to match your brand voice, length, or compliance constraints.
- Voices: Swap or configure alternative TTS voices or providers.
- Multi‑segment podcasts: Insert chaptering, transitions, or brief Q&A interludes while keeping a single‑speaker style.

## Privacy and responsible use
- Treat sales documents as confidential. Do not paste sensitive data into systems you do not control.
- The generated audio includes an AI disclaimer; still, verify facts before external use.
- Respect licensing and terms of any external model or voice provider you use.

---
