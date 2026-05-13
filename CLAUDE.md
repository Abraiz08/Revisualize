# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Revisualize converts short story scripts into sample storyboards using Google's Gemini API. It is in an early, exploratory state — there is no packaging metadata (no `pyproject.toml` / `requirements.txt`), the `tests/` directory is empty, and dependencies are installed ad-hoc into `.venv/`.

## Running

The entry point is `src/main.py`. It expects:
- `GEMINI_API_KEY` set in the environment (read implicitly by `genai.Client()`).
- A scene script at `data/scene.txt` (CWD-relative — run from the project root).
- An existing `output/` directory if image generation is re-enabled (currently commented out in `main()`).

```powershell
.\.venv\Scripts\Activate.ps1
python src\main.py
```

The program prompts for a number of panels on stdin, then prints accumulating panel JSON to stdout.

Dependencies in use: `google-genai`, `Pillow`. Install with `pip install google-genai pillow` into `.venv`.

## Architecture

Pipeline is a sequential loop in `createSceneObjects` (`src/main.py:61`):

1. Read full scene text from `data/scene.txt`.
2. For each of N panels, call `decomposeSceneToJSON(scene, context)` where `context` is the concatenation of all previously-generated panel JSON. The growing context is how the model is told "find the *next* visual beat after these."
3. Each call uses `gemini-3-flash-preview` with a fixed `PROMPT` that constrains output to a `visual_description` JSON object (`subject`, `action`, `setting`, `key_elements`).
4. `generateImage` (currently unused from `main`) calls `gemini-3.1-flash-image-preview` to render a panel and is meant to save to `output/generated_image.png` via `part.as_image()`.

Key things to know when editing:
- The richer panel schema in the commented block at the top of `main.py` (cinematography, lighting, technical metadata, continuity) is the *intended* target schema — the live `PROMPT` only emits the `visual_description` subset. Expanding the prompt to match is in-scope future work.
- `TODO` markers flag known gaps: input is not type-safe, and the model is not yet primed to split the scene into N beats up front before per-panel generation (current code re-derives "next beat" each iteration from accumulated context).
- Model IDs are hardcoded in `decomposeSceneToJSON` and `generateImage`; change them in both places if updating.
