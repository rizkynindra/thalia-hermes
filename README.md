# 🎭 Thalia Hermes

> Generate selfie images of **Kyeri** using **xAI Grok Imagine** via fal.ai — AI image-to-image editing that preserves face identity perfectly.

![Thalia Hermes Demo](references/thalia_ref_1.jpg)

## ✨ How It Works

Unlike standard AI image generators that create images from scratch (where faces often look different), Thalia Hermes uses **Grok Imagine's image-to-image editing**. It takes Kyeri's reference photo and **edits** it — changing outfit, background, and pose — while keeping the original face and identity intact.

## 🚀 Features

- **Identity Preservation** — Face stays consistent across all selfies
- **Two Selfie Modes** — Mirror selfie (outfit/full-body) & Direct selfie (close-up/location)
- **Pre-defined Scenes** — Sunset, beach, cafe, snow, forest, and more
- **Hermes Agent Integration** — Works as an installable Hermes skill
- **Telegram Ready** — Output sends directly via MEDIA: path

## 📋 Prerequisites

1. **fal.ai Account** — Sign up at [fal.ai](https://fal.ai)
2. **API Key** — Get from [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. **A Reference Photo** — A clear photo of the character (face visible, front-facing)

## 🛠️ Installation

```bash
# 1. Install dependencies
pip install requests

# 2. Set up your API key
echo "FAL_KEY=your_fal_api_key_here" > ~/.config/fal/api_key
chmod 600 ~/.config/fal/api_key

# 3. Add your reference photo
cp your_reference_photo.jpg references/thalia_ref_1.jpg
```

## 📸 Usage

### CLI

```bash
# Mirror selfie (outfit/fashion focus)
python scripts/generate.py \
  --prompt "wearing a white dress on the beach" \
  --output kyeri_selfie.jpeg

# Direct selfie (close-up/location focus)
python scripts/generate.py \
  --prompt "at a cozy cafe with warm lighting" \
  --mode direct \
  --output kyeri_cafe.jpeg

# Pre-defined scene
python scripts/generate.py \
  --scene sunset --mode direct --output kyeri_sunset.jpeg
```

### Selfie Modes

| Mode | Best For | Example |
|------|----------|---------|
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

### Example Prompts

```
"wearing a cozy sweater, drinking coffee at a snowy cafe"
"wearing elegant Balinese kebaya at a traditional temple"
"at sunset on Kedungu beach, golden light, gentle breeze"
"wearing a casual white t-shirt, sitting in a garden"
"at a traditional Bali market, holding flowers"
"swimming in a turquoise Bali sea, sunny day"
```

## ⚙️ Arguments

| Argument | Alias | Description |
|----------|-------|-------------|
| `--prompt` | `-p` | What the character should do/wear/where |
| `--scene` | `-s` | Pre-defined scene name |
| `--mode` | `-m` | Selfie mode: `mirror` or `direct` |
| `--ref` | | Path to reference image |
| `--output` | `-o` | Output file path |
| `--api-key` | | fal.ai API key (or set `FAL_KEY` env) |

## 🏗️ Architecture

```
User Request → generate.py
  → xAI Grok Imagine Edit (via fal.ai API)
  → Edits reference photo directly (identity preserved!)
  → Image saved locally → Send to Telegram / Chat
```

## ⚠️ Safety Filter Note

xAI Grok Imagine has a **server-side safety filter** that cannot be disabled. Content containing nudity, underwear, or explicit swimwear will return a `422 content_policy_violation` error. Use descriptive prompts focused on outfits, locations, and activities that pass the filter.

**Works:** summer clothes, tanktop, strapless dress, swimming, casual wear, elegant dress
**Blocked:** bikini, underwear, bra, swimsuit, revealing lingerie

## 📁 Project Structure

```
thalia-hermes/
├── README.md                    # This file
├── SKILL.md                     # Hermes Agent skill definition
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── scripts/
│   └── generate.py              # Main generation script
└── references/
    ├── thalia_ref_1.jpg         # Kyeri's reference photo
    └── grok-imagine-api.md      # Grok Imagine API reference
```

## 📝 Notes

- Output images are ~880×1168 (portrait orientation)
- Generation time: ~15-30 seconds
- The name "Thalia" is the project/skill name. The character in the photos is **Kyeri**.

## 📄 License

MIT — Use freely, modify, and share!
