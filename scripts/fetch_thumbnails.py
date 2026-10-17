#!/usr/bin/env python3
"""Save official Vimeo oEmbed thumbnails for locally authored articles."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from prepare_content import article_data

ROOT = Path(__file__).resolve().parents[1]


def get(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (EyeoArchiveResearch)'}), timeout=60) as response:
        return response.read(), response.headers.get_content_type()


def main():
    target = ROOT / 'assets/thumbnails'
    target.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / 'data/thumbnails.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for p in sorted((ROOT / 'content/talks').glob('*.md')):
        if p.name == '_index.md':
            continue
        vid = article_data(p)['video_id']
        raw, _ = get('https://vimeo.com/api/oembed.json?' + urlencode({'url': f'https://vimeo.com/{vid}', 'width': 1280}))
        info = json.loads(raw)
        url = info['thumbnail_url']
        if urlsplit(url).scheme != 'https' or urlsplit(url).hostname != 'i.vimeocdn.com':
            raise ValueError(f'Unexpected thumbnail origin for {vid}')
        content, mime = get(url)
        extension = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}[mime]
        name = f'{vid}.{extension}'
        (target / name).write_bytes(content)
        manifest[vid] = {'asset': f'thumbnails/{name}', 'source_url': url,
                         'video_url': f'https://vimeo.com/{vid}', 'title': info['title'],
                         'width': info['thumbnail_width'], 'height': info['thumbnail_height'],
                         'fetched_at': datetime.now(timezone.utc).isoformat(),
                         'sha256': hashlib.sha256(content).hexdigest()}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        print(f'{vid}: {info["thumbnail_width"]}x{info["thumbnail_height"]} ({len(content)} bytes)', flush=True)


if __name__ == '__main__':
    main()
