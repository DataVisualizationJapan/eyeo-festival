#!/usr/bin/env python3
"""Collect the official, public Vimeo listing. No API keys or video downloads."""
import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://vimeo.com/eyeofestival/videos'


class Listing(HTMLParser):
    def __init__(self):
        super().__init__()
        self.videos = {}
        self.pages = set()
        self.current = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'li':
            self.current = re.fullmatch(r'clip_(\d+)', a.get('id', ''))
        if tag == 'a':
            if a.get('data-page', '').isdigit():
                self.pages.add(int(a['data-page']))
            if self.current and a.get('title') and re.fullmatch(r'/\d+', a.get('href', '')):
                vid = self.current[1]
                self.videos[vid] = {'id': vid, 'original_title': a['title'], 'url': f'https://vimeo.com/{vid}'}

    def handle_endtag(self, tag):
        if tag == 'li':
            self.current = None

    def handle_data(self, data):
        self.text.append(data)


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (EyeoArchiveResearch)'}), timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def classify(v):
    v = {k: v[k] for k in ('id', 'original_title', 'url')}
    title = v['original_title']
    year = re.search(r'(?<!\d)(201[1-9]|202[0-2])(?!\d)', title)
    v['year'] = int(year[1]) if year else None
    lower = title.lower()
    if re.search(r'trailer|teaser|highlights|\btitles\b|title sequence|recap|sponsor|thank you|workshop|zygotes', lower) or title == 'eyeo festival 2018' or v['id'] == '110408261':
        kind = 'documentation'
    elif 'ignite' in lower:
        kind = 'ignite'
    elif 'panel' in lower or 'conversation' in lower:
        kind = 'panel'
    elif year and ('eyeo' in lower):
        kind = 'talk'
    else:
        kind = 'unconfirmed'
    v.update(kind=kind, speakers=[], metadata_status='title_only', event='eyeo' if 'eyeo' in lower else 'instint' if re.search(r'inst-?int', lower) else 'unconfirmed')
    # This is a label, not an assertion about the participants in a panel.
    label = re.sub(r'(?i)eyeo(?:\s+festival)?|201\d|202[0-2]', '', title)
    label = re.sub(r'(?i)ignite!?[_\s]*(?:#?\d+)?|\.(?:mov|mp4)$', '', label)
    v['listing_label'] = label.strip(' -–—|:')
    if kind == 'ignite':
        v['listing_label'] = re.sub(r'^\d+\s+', '', v['listing_label'])
    if not v['listing_label']:
        v['listing_label'] = title
    if v['event'] == 'eyeo' and kind in ('talk', 'ignite'):
        v['speakers'] = [s.strip() for s in re.split(r'\s+&\s+|\s+and\s+|,\s*', v['listing_label']) if s.strip()]
    return v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'data/videos.json')
    args = parser.parse_args()
    first = fetch(BASE + '/page:1/sort:date')
    parsed = Listing()
    parsed.feed(first.decode())
    total_pages = max(parsed.pages)
    text = ' '.join(parsed.text)
    count = re.search(r'([\d,]+)\s+Videos', text)
    expected = int(count[1].replace(',', '')) if count else None
    videos, pages = {}, []
    for n in range(1, total_pages + 1):
        url = f'{BASE}/page:{n}/sort:date'
        raw = first if n == 1 else fetch(url)
        p = Listing()
        p.feed(raw.decode())
        if not p.videos:
            raise SystemExit(f'Empty listing: {url}; existing data was not replaced')
        for vid in p.videos:
            if vid in videos:
                raise SystemExit(f'Duplicate {vid}; listing may have changed during collection')
        videos.update(p.videos)
        pages.append({'page': n, 'url': url, 'count': len(p.videos), 'sha256': hashlib.sha256(raw).hexdigest()})
        print(f'{n}/{total_pages}: {len(videos)} videos', flush=True)
        if n < total_pages:
            time.sleep(0.3)
    if expected is not None and len(videos) != expected:
        raise SystemExit(f'Expected {expected}, got {len(videos)}; existing data was not replaced')
    result = {'source': BASE, 'collected_at': datetime.now(timezone.utc).isoformat(),
              'expected_count': expected, 'count': len(videos), 'pages': pages,
              'videos': [classify(v) for v in videos.values()]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
