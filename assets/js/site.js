/* Browser-local filtering. Analytics receives counts, never search text. */
(() => {
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase('ja').replace(/\s+/g, ' ').trim();
  const form = document.querySelector('[data-catalog-filters]');
  if (form) {
    const rows = [...document.querySelectorAll('[data-video-row]')];
    const search = rows.map(row => normalize(row.dataset.search));
    const count = document.querySelector('[data-result-count]');
    const empty = document.querySelector('[data-empty]');
    const fields = ['q', 'year', 'kind', 'article'];
    const params = new URLSearchParams(location.search);
    for (const key of fields) {
      const control = form.elements.namedItem(key);
      if (params.has(key)) control.value = params.get(key);
    }
    let analyticsTimer = 0;
    function filter(writeURL = true) {
      const values = Object.fromEntries(fields.map(k => [k, form.elements.namedItem(k).value]));
      const terms = normalize(values.q).split(' ').filter(Boolean);
      let visible = 0;
      rows.forEach((row, i) => {
        const match = terms.every(t => search[i].includes(t)) && ['year', 'kind', 'article'].every(k => !values[k] || row.dataset[k] === values[k]);
        row.hidden = !match;
        if (match) visible++;
      });
      count.textContent = `${visible}本 / ${rows.length}本の動画`;
      empty.hidden = visible !== 0;
      if (writeURL) {
        const next = new URL(location.href);
        fields.forEach(k => values[k] ? next.searchParams.set(k, values[k]) : next.searchParams.delete(k));
        const changed = next.href !== location.href;
        history.replaceState(null, '', next);
        if (changed) {
          clearTimeout(analyticsTimer);
          analyticsTimer = setTimeout(() => window.dvjAnalytics?.event('filter_apply', {
            result_count: visible, has_search: Boolean(values.q),
          }), 600);
        }
      }
    }
    form.hidden = false;
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => filter());
    form.addEventListener('change', () => filter());
    form.addEventListener('reset', () => setTimeout(() => filter(), 0));
    filter(false);
  }
  document.querySelectorAll('[data-video-id]').forEach(panel => {
    const button = panel.querySelector('button');
    button.addEventListener('click', () => {
      if (!/^\d+$/.test(panel.dataset.videoId)) return;
      const frame = document.createElement('iframe');
      frame.src = `https://player.vimeo.com/video/${panel.dataset.videoId}?autoplay=1&dnt=1`;
      frame.title = 'Eyeo Festival 講演動画（Vimeo）';
      frame.allow = 'autoplay; fullscreen; picture-in-picture';
      frame.allowFullscreen = true;
      window.dvjAnalytics?.event('video_load', {video_id: panel.dataset.videoId});
      panel.replaceChildren(frame);
      frame.focus();
    }, {once: true});
  });
})();
