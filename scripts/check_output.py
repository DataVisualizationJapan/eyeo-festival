#!/usr/bin/env python3
"""Check all local HTML links, fragment targets, base paths, and source exclusion."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.iframes = [], set(), []
        self.h1s = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == 'iframe':
            self.iframes.append(attrs)
        if tag == 'h1':
            self.h1s += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('--base-path', default='/')
    parser.add_argument('--base-url')
    args = parser.parse_args()
    root = args.directory.resolve()
    base_path = urlsplit(args.base_url).path if args.base_url else args.base_path
    base_path = '/' + base_path.strip('/') + '/' if base_path.strip('/') else '/'
    origin = args.base_url or ('https://example.org' + base_path)
    docs = {}
    for f in root.rglob('*.html'):
        doc = Document()
        text = f.read_text()
        assert '_documents/' not in text and 'transcript_sources' not in text, f'Private source metadata published in {f}'
        doc.feed(text)
        assert not doc.iframes, f'Video loaded before consent: {f}'
        assert doc.h1s == 1, f'Expected one H1 in {f}, got {doc.h1s}'
        docs[f] = doc
    assert docs, 'No built HTML found'
    count = 0
    for f, doc in docs.items():
        relative = f.relative_to(root).as_posix()
        page_url = urljoin(origin, relative)
        for href in doc.links:
            parsed = urlsplit(urljoin(page_url, href))
            if parsed.netloc != urlsplit(origin).netloc or parsed.scheme not in ('http','https'):
                continue
            path = unquote(parsed.path)
            assert path.startswith(base_path), f'Escaped deployment base path: {f}: {href}'
            target = (root / path[len(base_path):]).resolve()
            assert target.is_relative_to(root), f'Escaped output directory: {href}'
            if target.is_dir() or path.endswith('/'):
                target /= 'index.html'
            assert target.is_file(), f'Broken link: {f}: {href} -> {target}'
            if parsed.fragment and target in docs:
                assert unquote(parsed.fragment) in docs[target].ids, f'Broken fragment: {f}: {href}'
            count += 1
    assert not (root / '_documents').exists(), 'Original transcripts were published'
    assert not (root / 'data/transcripts.json').exists(), 'Inventory was published'
    print(f'OK: {len(docs)} HTML documents, {count} internal links/assets, base path {base_path}')


if __name__ == '__main__':
    main()
