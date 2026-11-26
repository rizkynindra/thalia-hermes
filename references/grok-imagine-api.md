# xAI Grok Imagine Edit — API Reference

Endpoint: `POST https://fal.run/xai/grok-imagine-image/edit`

## Request Payload
```json
{
  "image_url": "data:image/jpeg;base64,...",  // or public URL
  "prompt": "make a pic of this person, but wearing a strapless dress. the person is taking a mirror selfie",
  "num_images": 1,
  "output_format": "jpeg"
}
```

## Response
```json
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/...",
      "content_type": "image/jpeg",
      "file_name": "image.jpg",
      "file_size": null,
      "width": 880,
      "height": 1168
    }
  ],
  "revised_prompt": null   // usually null for Grok Imagine
}
```

## Authentication
```
Authorization: Key <FAL_KEY>
Content-Type: application/json
```

## Prompt Modes

### Mirror Selfie (outfit/fashion focus)
```
make a pic of this person, but <CONTEXT>. the person is taking a mirror selfie
```

### Direct Selfie (close-up/location focus)
```
a close-up selfie taken by herself <CONTEXT>, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

## Safety Filter
Returns HTTP 422 with `content_policy_violation` for blocked content.
Cannot be disabled — server-side enforcement by xAI.

## Notes
- `revised_prompt` is typically `null` for Grok Imagine (unlike Flux/other models)
- No `seed` parameter supported (unlike flux-pro)
- `enable_safety_checker` parameter has **no effect** — xAI enforces server-side content policy
- Safety filter is strict: blocks `bikini`, `swimsuit`, `one-piece`, `underwear`, `lingerie`, `nude`
- Works with data URLs (base64) up to ~10MB
- Typical output: ~880×1168 (portrait orientation)
- Generation time: ~15-30 seconds
- HTTP 422 with `content_policy_violation` — prompt was blocked; no way to bypass
