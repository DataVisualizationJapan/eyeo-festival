#!/usr/bin/env python3
"""Reconcile local sources without changing them. Fuzzy suggestions never auto-match."""
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from collect_videos import classify

ROOT = Path(__file__).resolve().parents[1]


def normalize(s):
    s = unicodedata.normalize('NFKD', s).lower()
    s = re.sub(r'u2013|eyeo(?:\s+festival)?|20\d\d|\.mp4|\.md', '', s)
    return ''.join(c for c in s if c.isalnum() and not unicodedata.combining(c))


def main():
    path = ROOT / 'data/videos.json'
    catalog = json.loads(path.read_text())
    videos = [classify(v) for v in catalog['videos']]
    overrides = json.loads((ROOT / 'data/overrides.json').read_text())
    for v in videos:
        v.update(overrides.get('videos', {}).get(v['id'], {}))
        v.update(transcript_status='missing', article_status='not_started', transcript_sources=[])
    rows = []
    for f in sorted((ROOT / '_documents').rglob('*.md')):
        text = f.read_text()
        year = int(f.parent.name)
        fmt = 'csv' if 'In,Out,Duration,Text,Speaker,Status' in text else 'timestamp' if re.search(r'\[\d\d:\d\d:', text) else 'plain'
        key = normalize(f.name)
        candidates = [v for v in videos if v['event'] == 'eyeo' and v['year'] == year]
        matches = [v for v in candidates if normalize(v['original_title']) == key]
        relative = str(f.relative_to(ROOT))
        explicit = overrides.get('transcripts', {}).get(relative)
        if explicit:
            matches = [v for v in candidates if v['id'] == explicit['video_id']]
            if len(matches) != 1:
                raise ValueError(f'Invalid override: {relative}')
        row = {'path': relative, 'year': year, 'format': fmt, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
               'characters': len(text), 'video_id': matches[0]['id'] if len(matches) == 1 else None,
               'match_status': 'reviewed' if explicit else 'exact' if len(matches) == 1 else 'unresolved'}
        if explicit:
            row['match_note'] = explicit['reason']
        if row['video_id']:
            matches[0]['transcript_sources'].append(relative)
        else:
            ranked = sorted(candidates, key=lambda v: SequenceMatcher(None, key, normalize(v['original_title'])).ratio(), reverse=True)[:3]
            row['candidates'] = [{'id': v['id'], 'title': v['original_title'], 'score': round(SequenceMatcher(None, key, normalize(v['original_title'])).ratio(), 3)} for v in ranked]
        rows.append(row)
    by_path = {r['path']: r for r in rows}
    for v in videos:
        sources = v['transcript_sources']
        if sources:
            v['transcript_status'] = 'available'
            v['preferred_transcript'] = sorted(sources, key=lambda p: ({'csv': 0, 'timestamp': 1, 'plain': 2}[by_path[p]['format']], p))[0]
    catalog['videos'] = videos
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    inventory = {'file_count': len(rows), 'matched_files': sum(r['video_id'] is not None for r in rows),
                 'matched_videos': sum(bool(v['transcript_sources']) for v in videos),
                 'by_year': dict(sorted(Counter(r['year'] for r in rows).items())), 'files': rows}
    (ROOT / 'data/transcripts.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    print(f"{inventory['file_count']} files; {inventory['matched_files']} matched files; {inventory['matched_videos']} videos")
    for r in rows:
        if r['video_id'] is None:
            print('UNRESOLVED', r['path'], r.get('candidates', [])[:1])


if __name__ == '__main__':
    main()
