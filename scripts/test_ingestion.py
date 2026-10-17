#!/usr/bin/env python3
import unittest
from collect_videos import Listing, classify
from build_inventory import normalize


class IngestionTests(unittest.TestCase):
    def video(self, title, vid='123'):
        return classify({'id': vid, 'original_title': title, 'url': f'https://vimeo.com/{vid}'})

    def test_legacy_year_without_spaces(self):
        v = self.video('Eyeo2012 - Nervous System: Jessica Rosenkrantz & Jesse Louis-Rosenberg')
        self.assertEqual(v['year'], 2012)
        self.assertEqual(v['event'], 'eyeo')
        self.assertEqual(v['kind'], 'talk')

    def test_other_event_does_not_enter_eyeo(self):
        self.assertEqual(self.video('INST-INT 2013 - Panel 4')['event'], 'instint')

    def test_documentation_is_not_a_talk(self):
        for title in ('Eyeo 2019 TITLES', 'eyeo festival 2018', 'Kinetic Flora Workshop at Eyeo 2022.mov'):
            self.assertEqual(self.video(title)['kind'], 'documentation')

    def test_listing_label_is_never_empty(self):
        self.assertEqual(self.video('eyeo festival 2018')['listing_label'], 'eyeo festival 2018')

    def test_reclassification_drops_stale_derived_fields(self):
        v = self.video('Eyeo 2016 - Ben Fry')
        v['preferred_transcript'] = 'old-source.md'
        self.assertNotIn('preferred_transcript', classify(v))

    def test_upload_year_is_not_used(self):
        self.assertIsNone(self.video('Eyeo - A talk')['year'])

    def test_ignite_label_excludes_sequence_number(self):
        v = self.video('Ignite_Eyeo2012 - 12 Golan Levin.mov')
        self.assertEqual(v['kind'], 'ignite')
        self.assertEqual(v['speakers'], ['Golan Levin'])

    def test_normalization_of_encoded_separator(self):
        self.assertEqual(normalize('Eyeo 2016 u2013 Ben Fry.mp4.md'), normalize('Eyeo 2016 – Ben Fry'))

    def test_html_entities_and_pagination(self):
        p = Listing()
        p.feed('<li id="clip_123"><a href="/123" title="Eyeo 2022 - A &amp; B">video</a></li><a data-page="37">37</a>')
        self.assertEqual(p.videos['123']['original_title'], 'Eyeo 2022 - A & B')
        self.assertEqual(p.pages, {37})


if __name__ == '__main__':
    unittest.main()
