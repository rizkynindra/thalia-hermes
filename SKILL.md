---
name: thalia-hermes
description: Generate consistent character selfies with OpenAI GPT Image 2 Edit via fal.ai — edits a reference photo while preserving identity.
tags: [image-gen, character, selfie, ai-art, gpt-image, openai, fal-ai]
---

# 🎭 Thalia Hermes

A reusable template for generating **selfies and lifestyle images of a persistent character** — an AI companion, story protagonist, or your own persona — using [OpenAI GPT Image 2 Edit](https://fal.ai/models/openai/gpt-image-2/edit) via fal.ai.

> 📝 *"Thalia" is just the project name. Point it at your own character and reference photo.*

**Key mechanism:** GPT Image 2 Edit is an **image-to-image edit model**. It takes one reference photo of your character and **edits** it (outfit, background, pose, lighting) while preserving the original face and identity. An earlier revision of this workflow used xAI Grok Imagine Edit; GPT Image 2 Edit generally returns more detail and a more natural look, but the Grok script is kept as `generate.py.grok-backup` for rollback.

## Prerequisites

### 1. fal.ai API Key
- Set the `FAL_KEY` environment variable, or store the key at `~/.config/fal/api_key`. Never echo or log the value.

### 2. Reference Image
- Put one clear photo of your character under `references/` and point `REF_IMAGE_PATH` in the script at it.
- Best results come from a single subject, front-facing, evenly lit, no heavy filters, no other people in frame.

### 3. Dependencies
- `requests`, installed into the skill's own virtualenv:
  ```bash
  python3 -m venv .venv && .venv/bin/pip install requests
  ```
- Never copy a `.venv` between machines or directories — copied virtualenvs break on their absolute paths.

## Usage

```bash
cd <skill_dir> && source .venv/bin/activate

# Mirror selfie (default) — best for outfit / fashion / full-body
python scripts/generate.py \
  --prompt "wearing a summer dress by the sea" \
  --output ./out/selfie_01.png

# Direct selfie — best for close-ups, locations, expressions
python scripts/generate.py \
  --prompt "at a cozy cafe with warm lighting" \
  --mode direct \
  --output ./out/cafe_01.png

# Pre-defined scene
python scripts/generate.py --scene sunset --mode direct --output ./out/sunset_01.png
```

Endpoint used by the script: `https://fal.run/openai/gpt-image-2/edit`, payload `image_urls: [data-url]` (plural — GPT Image 2 accepts multiple input images), plus `quality` (low/medium/high) and `output_format`.

### Selfie modes

| Mode | Best for |
|------|----------|
| `mirror` (default) | Outfit, fashion, full-body |
| `direct` | Close-up, location, expression |

### Candid (non-selfie) shots
Use `--mode direct` with portrait phrasing: "portrait photo taken by someone else", "both hands resting", "no phone visible", "natural candid pose". The edit keeps the base face structure but can still produce a selfie-like arm angle — iterate the prompt.

### Pre-defined scenes
`sunset`, `beach`, `cafe`, `snow`, `forest`, `bedroom`, `portrait`, `traditional` (long-sleeve kebaya + batik sarung at a temple). Edit the `SCENES` dict to match your own character's world.

## ⚠️ Safety filters (important)

Image endpoints enforce a **server-side prompt pre-filter** you cannot disable. Keyword heuristics differ per model, but these strategies are broadly portable:

- **❌ Don't name the restricted item — describe the activity.** "swimming in the sea" passes where "bikini/swimsuit" is blocked; the model infers appropriate clothing from the scene. Exception: when a specific garment type is required, name it explicitly — a pool prompt with no garment word can produce an unrelated garment instead of swimwear.
- **❌ Avoid "sexy".** Use "elegant", "confident", "soft mood lighting".
- **✅ On a block, rephrase by removing the flagged word entirely.** Filters are keyword-heuristic, not semantic: "pajamas" passes where "sleepwear/camisole" is blocked; "light summer beach dress" passes where "deep v-neckline beach dress" is blocked.
- **🔥 Skin glow without "sweat/wet"** (both blocked): "just finished exercising on a sunny day, glowing sun-kissed skin, slightly flushed cheeks".
- **❌ Post-activity framing implies nudity and gets blocked** ("towel after shower", "after a warm bath"). Attach the same garment to a neutral context instead — "spa towel wrap", "skincare night routine" pass.
- **✅ Register swaps that passed on GPT Image 2:** "tank top" blocked in a bedtime context → "sleeveless cotton sleep shirt"; "white towel after shower" → "soft fluffy white spa towel wrap"; "bathrobe + night routine" passes outright. Keep the garment, change the vocabulary register. "swimming in a pool" + "modest one-piece swimsuit, sporty swimwear" also passed; only bikini / two-piece phrasing is risky.
- **✅ Religious or cultural settings need modesty.** For temples and ceremonies, default to modest traditional attire (long sleeves, sarung/skirt), never halter or off-shoulder cuts.
- **📉 Anatomically explicit framings are effectively unavailable** — the direct phrasing is blocked and euphemisms just yield an ordinary photo. Say so plainly instead of burning attempts.
- **🚫 Undress, nude, and lingerie requests are declined** — that is a boundary of the workflow, not a filter bug. Decline once, offer a tasteful alternative (swimwear, sleepwear, spa context), and do not switch engines to route around it.
- **🖼️ Keep identity edits on the Edit path.** Pure text-to-image models will happily render blocked prompts, but the face comes out generic and the character is lost. When a prompt is blocked, rework the wording for the Edit model instead of changing engines.

`references/safety-filter-probes.md` holds older probe tables (blocked/allowed keywords) from the Grok era — the strategies carry over, but re-probe individual words before trusting a row.

## Tips for good results

- Prompt **what to change** (outfit, location, mood); don't describe facial features — the reference handles identity.
- `--mode direct` for close-up/expression shots, `--mode mirror` for outfit/full-body.
- Keep one reference photo per character. Mixing references drifts the face.

## Delivery notes (if driven by an agent)

1. **Keep the chat clean** — run the script quietly (e.g. `| tail -5`); don't paste generation logs into the reply.
2. **Send the image on the same turn** — once the file exists, reply with a media/link message pointing at the absolute output path.
3. **Don't retry a refused reference analysis** — if a vision backend refuses to describe the reference, ask the user to describe the outfit or scene in words instead.

## Files

- `scripts/generate.py` — main generation script (GPT Image 2 Edit endpoint); `scripts/generate.py.grok-backup` is the previous Grok version
- `references/` — your character reference image(s) plus model notes
- `references/safety-filter-probes.md` — historical probe results (strategies still apply)
- `references/grok-imagine-api.md` — legacy Grok API notes, kept for rollback
- `requirements.txt` — Python dependency list
