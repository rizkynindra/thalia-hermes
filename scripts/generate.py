#!/usr/bin/env python3
"""
Thalia Hermes Selfie Generator — OpenAI GPT Image 2 Edit via fal.ai

Edits Kyeri's reference image using GPT Image 2 (image-to-image edit),
preserving face/identity while changing outfit, background, pose, etc.

Note: "Thalia" is the skill name. The character in the photos is Kyeri.

Usage:
    # Mirror selfie (default) — best for outfit, full-body
    python generate.py --prompt "wearing a white dress on the beach"
    
    # Direct selfie — best for close-up, location
    python generate.py --prompt "at a cozy cafe" --mode direct
    
    # Pre-defined scene
    python generate.py --scene sunset --mode direct
    
    # With custom output path
    python generate.py --prompt "wearing kebaya" --output ~/thalia_baru.png
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


# ─── Konfigurasi ───
SKILL_DIR = Path(__file__).parent.parent
REF_DIR = SKILL_DIR / "references"
REF_IMAGE_PATH = REF_DIR / "thalia_ref_1.jpg"

# Default ref image URL (uploaded to CDN or local path)
# For now we use local file via data URL; GPT Image 2 supports image_urls

FAL_BASE = "https://fal.run"
EDIT_ENDPOINT = f"{FAL_BASE}/openai/gpt-image-2/edit"


def get_api_key() -> str:
    """Get fal.ai API key from env or config file."""
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    
    config_path = Path.home() / ".config" / "fal" / "api_key"
    if config_path.exists():
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("FAL_KEY="):
                    return line.split("=", 1)[1]
    
    raise ValueError(
        "FAL_KEY not found. Set env FAL_KEY or save to ~/.config/fal/api_key"
    )


def encode_image_to_data_url(image_path: str | Path) -> str:
    """Encode image to base64 data URL for API."""
    import base64
    path = Path(image_path)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/jpeg")
    
    return f"data:{mime};base64,{data}"


def build_edit_prompt(user_context: str, mode: str) -> str:
    """Build prompt for GPT Image 2 Edit based on mode."""
    if mode == "direct":
        return (
            f"Edit this image: a close-up selfie taken by herself {user_context}, "
            "direct eye contact with the camera, looking straight into the lens, "
            "eyes centered and clearly visible, not a mirror selfie, "
            "phone held at arm's length, face fully visible. "
            "Keep the person's face and identity intact."
        )
    else:
        # Mirror selfie (default)
        return (
            f"Edit this image: make this person {user_context}. "
            "The person is taking a mirror selfie. "
            "Keep the person's face and identity intact."
        )


def generate_selfie(
    prompt: str,
    ref_path: str | Path | None = None,
    mode: str = "mirror",
    output_path: str | None = None,
    api_key: str | None = None,
    num_images: int = 1,
    quality: str = "medium",
) -> dict:
    """Generate a Thalia selfie using GPT Image 2 Edit.
    
    Args:
        prompt: What Thalia should be doing/wearing/where
        ref_path: Path to reference image
        mode: "mirror" or "direct"
        output_path: Save image to this path
        api_key: fal.ai API key
        num_images: Number of images to generate
        quality: "low", "medium", or "high"
    
    Returns:
        dict with keys: url(s), output_path
    """
    if not api_key:
        api_key = get_api_key()
    
    # Resolve reference image
    if not ref_path:
        ref_path = REF_IMAGE_PATH
    ref_path = Path(ref_path)
    
    if not ref_path.exists():
        raise FileNotFoundError(f"Reference image not found: {ref_path}")
    
    # Build edit prompt
    edit_prompt = build_edit_prompt(prompt, mode)
    image_data_url = encode_image_to_data_url(ref_path)
    
    # Prepare request
    payload = {
        "image_urls": [image_data_url],
        "prompt": edit_prompt,
        "quality": quality,
        "output_format": "jpeg",
    }
    
    print(f"[Thalia] 🎨 Mode: {mode}")
    print(f"[Thalia] 📝 Prompt: {edit_prompt[:100]}...")
    print(f"[Thalia] 🔗 Endpoint: {EDIT_ENDPOINT}")
    
    # Call API
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }
    
    resp = requests.post(EDIT_ENDPOINT, json=payload, headers=headers)
    
    if resp.status_code != 200:
        error_detail = resp.text[:500]
        raise RuntimeError(f"API Error {resp.status_code}: {error_detail}")
    
    result = resp.json()
    images = result.get("images", [])
    
    print(f"[Thalia] ✅ Generated: {len(images)} image(s)")
    
    output = {
        "images": images,
        "urls": [img.get("url", "") for img in images],
    }
    
    # Download and save
    if output_path and images:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        urls = []
        for i, img in enumerate(images):
            url = img.get("url", "")
            if not url:
                continue
            
            if len(images) > 1:
                save_path = path.with_stem(f"{path.stem}_{i}")
            else:
                save_path = path
            
            img_resp = requests.get(url)
            if img_resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(img_resp.content)
                output["output_path"] = str(save_path.resolve())
                print(f"[Thalia] 💾 Saved: {save_path}")
                urls.append(str(save_path.resolve()))
            else:
                print(f"[Thalia] ⚠️ Download failed for image {i}")
        
        output["saved_paths"] = urls
    
    print(f"[Thalia] ✨ Done!")
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Thalia Selfie Generator — OpenAI GPT Image 2 Edit (fal.ai)"
    )
    
    # Input
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--prompt", "-p", help="What Thalia should do/wear/where")
    input_group.add_argument("--scene", "-s",
        choices=["sunset", "beach", "cafe", "snow", "forest", "bedroom", "portrait", "traditional"],
        help="Pre-defined scene")
    
    # Mode
    parser.add_argument("--mode", "-m", choices=["mirror", "direct"], default="mirror",
        help="Selfie mode: mirror (outfit/full-body) or direct (close-up/location)")
    
    # Reference
    parser.add_argument("--ref", default=str(REF_IMAGE_PATH),
        help="Path to reference image")
    
    # Output
    parser.add_argument("--output", "-o", default="thalia_selfie.jpeg",
        help="Output path")
    
    # API
    parser.add_argument("--api-key", help="fal.ai API key (or set FAL_KEY env)")
    
    args = parser.parse_args()
    
    # Build prompt from scene if needed
    prompt = args.prompt
    if args.scene and not prompt:
        scenes = {
            "sunset": "at sunset on Kedungu beach, golden light",
            "beach": "on a beautiful Bali beach with gentle waves",
            "cafe": "in a cozy Bali cafe with warm lighting",
            "snow": "in a snowy landscape with snowflakes falling",
            "forest": "in a lush tropical forest with sun rays",
            "bedroom": "in a cozy bedroom with morning light",
            "portrait": "in a studio with soft professional lighting",
            "traditional": "wearing elegant Balinese kebaya at a temple",
        }
        prompt = scenes[args.scene]
    
    # Generate
    try:
        result = generate_selfie(
            prompt=prompt,
            ref_path=args.ref,
            mode=args.mode,
            output_path=args.output,
            api_key=args.api_key,
        )
        
        if result.get("output_path"):
            from urllib.parse import quote
            print(f"\n✅ Selesai! {result['output_path']}")
            print(f"📤 Kirim via: MEDIA:{result['output_path']}")
        elif result.get("urls"):
            print(f"\n🔗 URL: {result['urls'][0]}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
