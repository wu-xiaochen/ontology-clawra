#!/usr/bin/env python3
"""
MiniMax Image Generation - image-01 model
Usage: python3 gen.py --prompt "description" [--aspect_ratio 1:1] [--count 1] [--output ./output]
"""
import argparse
import base64
import os
import sys
import requests
import json
from pathlib import Path

DEFAULT_BASE_URL = "https://api.minimaxi.com/v1"
DEFAULT_MODEL = "image-01"
ASPECT_RATIOS = ["1:1", "16:9", "9:16", "3:4", "4:3", "21:9"]

def generate_image(prompt, aspect_ratio="1:1", n=1, api_key=None, base_url=None, output_dir="."):
    api_key = api_key or os.getenv("MINIMAX_CN_API_KEY")
    base_url = base_url or os.getenv("MINIMAX_CN_BASE_URL", DEFAULT_BASE_URL).replace("/anthropic", "").replace("/v1", "")
    base_url = f"{base_url}/v1".rstrip("/")

    if not api_key:
        raise ValueError("MINIMAX_CN_API_KEY not set. Set it in ~/.hermes/.env or pass --api_key")

    url = f"{base_url}/image_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "base64",
        "n": min(n, 4)
    }

    print(f"Generating {n} image(s) with image-01...", file=sys.stderr)
    print(f"Prompt: {prompt}", file=sys.stderr)
    print(f"Aspect ratio: {aspect_ratio}", file=sys.stderr)

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text}")

    data = resp.json()
    images = data["data"]["image_base64"]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for i, img_b64 in enumerate(images):
        ext = "jpg"
        filename = output_dir / f"minimax_{i+1}_{Path(__file__).stem}.{ext}"
        # Decode and save
        img_data = base64.b64decode(img_b64)
        with open(filename, "wb") as f:
            f.write(img_data)
        paths.append(str(filename))
        print(f"Saved: {filename}", file=sys.stderr)

    return paths

def main():
    parser = argparse.ArgumentParser(description="MiniMax image-01 generation")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--aspect_ratio", "-a", default="1:1",
                        choices=ASPECT_RATIOS, help="Aspect ratio (default: 1:1)")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of images (max 4)")
    parser.add_argument("--output", "-o", default="./output", help="Output directory")
    parser.add_argument("--api_key", help="Override MINIMAX_CN_API_KEY")
    parser.add_argument("--base_url", help="Override base URL")
    args = parser.parse_args()

    paths = generate_image(
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        n=min(args.count, 4),
        api_key=args.api_key,
        base_url=args.base_url,
        output_dir=args.output
    )

    # Output JSON for agent parsing
    result = {"success": True, "images": paths}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
