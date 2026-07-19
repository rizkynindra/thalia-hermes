---
name: thalia-hermes
description: Generate selfie images of your agent using xAI Grok Imagine Edit via fal.ai — edits reference image directly, preserving face identity perfectly.
tags: [image-gen, character, selfie, ai-art, grok, xai, fal-ai]
---

# 🎭 Thalia Hermes

Generate selfie images using [xAI Grok Imagine](https://fal.ai/models/xai/grok-imagine-image/edit) via fal.ai.

**Key difference from standard T2I:** Grok Imagine is an **image-to-image edit model**. It takes the reference photo and **edits** it (changing outfit, background, pose) while preserving the original face/identity perfectly. No more wonky faces!

## Prerequisites

### 1. fal.ai API Key
- Sign up at https://fal.ai
- Get API key from https://fal.ai/dashboard/keys
- Save to config: `~/.config/fal/api_key` or set as env `FAL_KEY`

### 2. Reference Images
Reference images for thalia's identity are stored at:
```
~/.hermes/skills/thalia-hermes/references/
```
Currently available:
- `thalia_ref_1.png` — thalia's reference photo (white dress, turquoise water background)

### 3. Dependencies
```bash
pip install requests
```

### 4. API Key
```bash
export FAL_KEY="your-key-here"
# Or save to ~/.config/fal/api_key as: FAL_KEY=your-key-here
```

## Usage

### CLI Tool
```bash
# Inside skill venv:
cd ~/.hermes/skills/thalia-hermes && source .venv/bin/activate

# Mirror selfie (default) — best for outfit/fashion
python scripts/generate.py \
  --prompt "wearing a white dress on the beach" \
  --output ~/thalia_selfie.jpeg

# Direct selfie — best for close-up/location shots
python scripts/generate.py \
  --prompt "at a cozy cafe with warm lighting" \
  --mode direct \
  --output ~/thalia_cafe.jpeg

# Pre-defined scene
python scripts/generate.py \
  --scene sunset --mode direct --output ~/thalia_sunset.jpeg
```

### Selfie Modes

| Mode | Best For | Example Prompt |
|------|----------|---------------|
| `mirror` (default) | Outfit, fashion, full-body | "wearing a red kebaya" |
| `direct` | Close-up, location, expression | "at a snowy cafe" |

### Pre-defined Scenes
| Scene | Description |
|-------|-------------|
| `sunset` | Kedungu beach golden hour |
| `beach` | Bali beach with waves |
| `cafe` | Cozy cafe warm lighting |
| `snow` | Snowy landscape |
| `forest` | Tropical forest sun rays |
| `bedroom` | Cozy morning light |
| `portrait` | Studio professional lighting |
| `traditional` | Balinese kebaya at temple |

### Prompt Examples
```
"wearing a cozy sweater, drinking coffee at a snowy cafe"
"wearing elegant Balinese kebaya at a traditional temple"
"at sunset on Kedungu beach, golden light, gentle breeze"
"wearing a tank top, in a cozy bedroom with morning light"
"wearing a strapless dress, confident look, soft lighting"
"wearing a casual white t-shirt, sitting in a garden"
"swimming in a beautiful turquoise Bali sea, sunny day"
"at the beach wearing summer vacation clothes, sunny day"
```

## ⚠️ Safety Filter (Important!)

xAI Grok Imagine has a **server-side safety filter** that cannot be disabled.

## Architecture

```
User Request → Hermes Agent (thalia) → thalia_generate()
  → xAI Grok Imagine Edit (via fal.ai)
  → Edits thalia's reference photo directly (identity preserved!)
  → Image saved locally → MEDIA: path → Telegram
```

## Tips for Good Results
- Keep prompts simple and focused on **what to change** (outfit, location)
- Avoid describing facial features in the prompt — the reference handles that
- Use `--mode direct` for close-up/expressive shots
- Use `--mode mirror` (default) for full-body/outfit shots

## Files
- `scripts/generate.py` — Main generation script
- `references/` — thalia's reference images
