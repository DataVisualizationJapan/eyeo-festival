#!/usr/bin/env python3
"""Build browse pages and editorial status from the catalog and article front matter."""
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def article_data(path):
    return json.JSONDecoder().raw_decode(path.read_text())[0]


def speaker_slug(name):
    base = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    base = re.sub(r'[^a-z0-9]+', '-', base).strip('-') or 'speaker'
    return base + '-' + hashlib.sha256(name.encode()).hexdigest()[:6]


def write_page(relative, metadata, body=''):
    p = ROOT / 'content' / relative
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n\n' + body + '\n')


def main():
    path = ROOT / 'data/videos.json'
    catalog = json.loads(path.read_text())
    articles = {article_data(p)['video_id']: article_data(p) for p in (ROOT / 'content/talks').glob('*.md') if p.name != '_index.md'}
    videos = catalog['videos']
    for v in videos:
        article = articles.get(v['id'])
        v['article_status'] = article.get('editorial_status', 'draft') if article else 'not_started'
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    # Generated sections contain browse metadata only, never transcript text.
    for section in ('years', 'speakers'):
        folder = ROOT / 'content' / section
        folder.mkdir(parents=True, exist_ok=True)
        for f in folder.glob('*.md'):
            if f.name != '_index.md':
                f.unlink()
    eyeo = [v for v in videos if v['event'] == 'eyeo']
    for year in sorted({v['year'] for v in eyeo if v['year']}):
        write_page(f'years/{year}.md', {'title': str(year), 'layout': 'catalog', 'filter_year': year}, f'Eyeo {year}の講演と関連映像。日本語記事のある動画は、記事からも読むことができます。')
    speakers = sorted({s for v in eyeo for s in v['speakers']}, key=str.casefold)
    for speaker in speakers:
        write_page(f'speakers/{speaker_slug(speaker)}.md', {'title': speaker, 'layout': 'catalog', 'filter_speaker': speaker}, '動画タイトルなどに記載された登壇者名から、講演をまとめています。')
    print(f'{len(articles)} articles; {len(speakers)} speaker pages; {len(eyeo)} Eyeo videos')


if __name__ == '__main__':
    main()
