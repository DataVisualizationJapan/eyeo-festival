#!/usr/bin/env python3
"""Validate catalog, source provenance, and article references without network access."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from collections import Counter
from prepare_content import article_data, speaker_slug

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit('ERROR: ' + message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--without-sources', action='store_true', help='Validate public metadata without private source files; skips source hashes and timestamp boundaries')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'data/videos.json').read_text())
    inventory = json.loads((ROOT / 'data/transcripts.json').read_text())
    records = catalog['videos']
    videos = {v['id']: v for v in records}
    require(len(videos) == catalog['count'] == len(records), 'Duplicate IDs or count mismatch')
    require(catalog['expected_count'] == catalog['count'], 'Incomplete account listing')
    pages = catalog['pages']
    require([p['page'] for p in pages] == list(range(1, len(pages) + 1)), 'Missing listing pages')
    require(sum(p['count'] for p in pages) == len(records), 'Listing page counts do not add up')
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / '_documents').rglob('*.md')}
    indexed = {r['path'] for r in inventory['files']}
    require(len(indexed) == inventory['file_count'], 'Source inventory count mismatch')
    if not args.without_sources:
        require(actual == indexed, 'Source inventory is stale; run build_inventory.py')
    for row in inventory['files']:
        path = ROOT / row['path']
        if not args.without_sources:
            require(hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], f'Source changed: {path}')
        require(row['video_id'] in videos, f'Unresolved transcript: {path}')
        v = videos[row['video_id']]
        require(v['year'] == row['year'] and v['event'] == 'eyeo', f'Wrong year or event: {path}')
        require(row['path'] in v['transcript_sources'], f'Missing reverse source link: {path}')
    article_ids = set()
    for f in (ROOT / 'content/talks').glob('*.md'):
        if f.name == '_index.md':
            continue
        metadata, end = json.JSONDecoder().raw_decode(f.read_text())
        vid = metadata['video_id']
        require(vid in videos and vid not in article_ids, f'Duplicate or missing article video: {f}')
        article_ids.add(vid)
        v = videos[vid]
        require(f.stem == vid, f'Unstable article URL: {f}')
        require(metadata['original_title'] == v['original_title'], f'Original title mismatch: {f}')
        require(metadata['year'] == v['year'], f'Article year mismatch: {f}')
        require(metadata['editorial_status'] == v['article_status'], f'Article status stale: {f}')
        require(metadata['editorial_status'] in ('draft', 'published'), f'Unknown editorial status: {f}')
        require(bool(metadata.get('draft', False)) == (metadata['editorial_status'] == 'draft'), f'Draft flag disagrees with editorial status: {f}')
        require(metadata['speakers'] and metadata['topics'] and metadata['summary'], f'Missing metadata: {f}')
        sources = metadata['transcript_sources']
        require(sources and all(p in v['transcript_sources'] for p in sources), f'Invalid article sources: {f}')
        if not args.without_sources:
            source_text = '\n'.join((ROOT / p).read_text() for p in sources)
            boundaries = {int(h)*3600 + int(m)*60 + int(s) for h,m,s in re.findall(r'(?m)^(\d\d):(\d\d):(\d\d)\.\d+,', source_text)}
            for linked_vid, minutes, seconds in re.findall(r'https://vimeo.com/(\d+)#t=(\d+)m(\d+)s', f.read_text()[end:]):
                require(linked_vid == vid and int(minutes)*60+int(seconds) in boundaries, f'Timestamp not at source boundary: {f}: {minutes}:{seconds}')
        body = f.read_text()[end:]
        require('編集上の考察' in body and '## 出典' in body, f'Missing editorial attribution: {f}')
    for v in records:
        require(re.fullmatch(r'\d+', v['id']) and v['url'] == f"https://vimeo.com/{v['id']}", 'Invalid video identity')
        require(v['kind'] in {'talk','panel','ignite','documentation','unconfirmed'}, f'Unknown kind: {v["id"]}')
        require(bool(v['listing_label'].strip()), f'Empty listing title: {v["id"]}')
        sources = v['transcript_sources']
        require(v['transcript_status'] == ('available' if sources else 'missing'), 'Transcript status mismatch')
        require(all(p in indexed for p in sources), 'Orphaned source link')
        if sources:
            require(v['preferred_transcript'] in sources, 'Preferred source missing')
        if v['article_status'] != 'not_started':
            require(v['id'] in article_ids, 'Orphaned article status')
    eyeo = [v for v in records if v['event'] == 'eyeo']
    expected_speakers = {s for v in eyeo for s in v['speakers']}
    expected_speaker_files = {speaker_slug(s) + '.md' for s in expected_speakers}
    actual_speaker_files = {f.name for f in (ROOT / 'content/speakers').glob('*.md') if f.name != '_index.md'}
    require(actual_speaker_files == expected_speaker_files, 'Speaker pages stale; run prepare_content.py')
    for s in expected_speakers:
        require(article_data(ROOT / 'content/speakers' / (speaker_slug(s) + '.md'))['filter_speaker'] == s, 'Speaker filter mismatch')
    expected_years = {str(v['year']) for v in eyeo if v['year']}
    actual_years = {f.stem for f in (ROOT / 'content/years').glob('*.md') if f.name != '_index.md'}
    require(actual_years == expected_years, 'Year pages stale; run prepare_content.py')
    print(f'OK: {len(records)} videos, {len(pages)} pages, {len(indexed)} source files, {len(article_ids)} articles')
    if args.without_sources:
        print('Public metadata mode: source hashes and timestamp boundaries were not checked')
    print('Events:', dict(Counter(v['event'] for v in records)))


if __name__ == '__main__':
    main()
