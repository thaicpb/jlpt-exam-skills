'use strict';
/* Sổ tay từ vựng JLPT — offline flashcard PWA.
   Data comes from data/*.json produced by tools/build_webapp.py. */

const STORE = 'jlpt-fc-v1';
const app = document.getElementById('app');
const toastEl = document.getElementById('toast');

const ICON = {
  back: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
  star: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3.2l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.6l-5.2 2.8 1-5.9L3.5 9.4l5.9-.8z"/></svg>',
  starLine: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3.2l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.6l-5.2 2.8 1-5.9L3.5 9.4l5.9-.8z"/></svg>',
  speak: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4 4 0 010 6M18 6.5a7.5 7.5 0 010 11"/></svg>',
  shuffle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h4v4M4 20L20 4M20 16v4h-4M14.5 14.5L20 20M4 4l5 5"/></svg>',
  gear: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.8-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1.1-1.5 1.7 1.7 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.8 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1.1 1.7 1.7 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.8.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.8V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/></svg>',
};

/* ---------- persistent state ---------- */
const DEFAULTS = { marks: {}, seen: {}, level: null, front: 'jp', shuffle: false, last: null };
let state = loadState();
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORE) || '{}');
    return Object.assign({}, DEFAULTS, saved, { marks: saved.marks || {}, seen: saved.seen || {} });
  } catch (_) { return Object.assign({}, DEFAULTS, { marks: {}, seen: {} }); }
}
function save() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (_) { /* storage unavailable */ } }
const cardKey = (level, lesson, c) => `${level}/${lesson}/${c.w}/${c.r}`;
function askPersist() { if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {}); }

/* ---------- helpers ---------- */
function h(tag, attrs, ...kids) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') node.className = v;
    else if (k === 'html') node.innerHTML = v; // only used with static ICON strings
    else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat()) if (kid != null && kid !== false) node.append(kid.nodeType ? kid : String(kid));
  return node;
}
let toastTimer;
function toast(message, action) {
  toastEl.replaceChildren(h('span', null, message));
  if (action) toastEl.append(h('button', { type: 'button', onclick: action.run }, action.label));
  toastEl.hidden = false;
  clearTimeout(toastTimer);
  if (!action) toastTimer = setTimeout(() => { toastEl.hidden = true; }, 2600);
}
function shuffled(list) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
const plainReading = (r) => r.replace(/[（(][^)）]*[)）]/g, '').replace(/\s+/g, '');

/* ---------- speech ---------- */
let jaVoice = null;
function pickVoice() {
  if (!('speechSynthesis' in window)) return;
  const voices = speechSynthesis.getVoices();
  jaVoice = voices.find((v) => v.lang === 'ja-JP' && /Kyoko|O-ren|Otoya|Hattori/i.test(v.name)) || voices.find((v) => /^ja/i.test(v.lang)) || null;
}
if ('speechSynthesis' in window) { pickVoice(); speechSynthesis.addEventListener('voiceschanged', pickVoice); }
function speak(text) {
  if (!('speechSynthesis' in window)) { toast('Thiết bị không hỗ trợ đọc phát âm.'); return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'ja-JP'; u.rate = 0.9;
  if (jaVoice) u.voice = jaVoice;
  speechSynthesis.speak(u);
}

/* ---------- data ---------- */
let catalog = null;
const lessonCache = new Map();
async function getJSON(url) {
  const inline = window.__JLPT_DATA__; // set only by the single-file preview build
  if (inline && inline[url]) return inline[url];
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url}: ${res.status}`);
  return res.json();
}
async function loadCatalog() {
  catalog = await getJSON('data/catalog.json');
  const ids = catalog.levels.map((l) => l.id);
  if (!ids.includes(state.level)) state.level = ids[0];
}
const levelOf = (id) => catalog.levels.find((l) => l.id === id);
const lessonOf = (level, id) => (levelOf(level) || { lessons: [] }).lessons.find((l) => l.id === id);
async function loadLesson(level, id) {
  const meta = lessonOf(level, id);
  if (!meta) throw new Error('Không tìm thấy bài học.');
  const cacheId = `${level}/${id}`;
  if (!lessonCache.has(cacheId)) lessonCache.set(cacheId, await getJSON(meta.file));
  return lessonCache.get(cacheId).map((c, i) => ({ ...c, level, lesson: id, idx: i, key: cardKey(level, id, c) }));
}
function countWhere(obj, prefix) { let n = 0; for (const k in obj) if (k.startsWith(prefix)) n++; return n; }

/* ---------- router ---------- */
function route() {
  const parts = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean);
  if (parts.length === 2 && levelOf(parts[0])) {
    state.level = parts[0]; save();
    renderStudy(parts[0], parts[1]).catch(showError);
  } else renderHome();
}
function go(hash) { if (location.hash === hash) route(); else location.hash = hash; }
function showError(err) {
  app.replaceChildren(h('div', { class: 'screen' },
    h('div', { class: 'empty' }, h('b', null, 'Không mở được dữ liệu'), h('p', null, String(err.message || err)),
      h('button', { class: 'btn primary', type: 'button', onclick: () => go('#/') }, 'Về trang chính'))));
}

/* ---------- home ---------- */
function renderHome() {
  document.documentElement.dataset.level = state.level;
  const level = levelOf(state.level);
  const marked = countWhere(state.marks, `${level.id}/`);
  const quick = h('div', { class: 'quick' });
  const last = state.last && state.last.level === level.id && lessonOf(level.id, state.last.lesson) ? state.last : null;
  if (last) {
    const meta = lessonOf(level.id, last.lesson);
    quick.append(h('button', { type: 'button', class: 'primary-card', onclick: () => go(`#/${level.id}/${last.lesson}`) },
      h('span', null, h('strong', null, 'Học tiếp'), h('small', null, `${meta.title} · thẻ ${Math.min(last.pos + 1, meta.count)}/${meta.count}`)), '›'));
  }
  if (marked) {
    quick.append(h('button', { type: 'button', onclick: () => go(`#/${level.id}/review`) },
      h('span', null, h('strong', null, 'Ôn từ cần xem lại'), h('small', null, `${marked} từ đã đánh dấu trong ${level.id}`)), '›'));
  }

  const grid = h('div', { class: 'lessons' });
  for (const lesson of level.lessons) {
    const prefix = `${level.id}/${lesson.id}/`;
    const seen = Math.min(countWhere(state.seen, prefix), lesson.count);
    const flags = countWhere(state.marks, prefix);
    const pct = lesson.count ? Math.round((seen / lesson.count) * 100) : 0;
    grid.append(h('button', { type: 'button', class: 'lesson', onclick: () => go(`#/${level.id}/${lesson.id}`), 'aria-label': `${lesson.title}, ${lesson.count} từ, đã xem ${seen}` },
      h('b', null, lesson.title),
      h('span', null, `${lesson.count} từ · đã xem ${seen}`),
      flags ? h('span', { class: 'flag' }, `★ ${flags} cần xem lại`) : null,
      h('div', { class: 'bar' }, h('i', { style: `width:${pct}%` }))));
  }

  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  app.replaceChildren(h('div', { class: 'screen' },
    h('header', { class: 'masthead' },
      h('div', null, h('div', { class: 'brand' }, '日本語 · Mỗi ngày một chút'), h('h1', null, 'Sổ tay từ vựng')),
      h('button', { type: 'button', class: 'icon-btn', 'aria-label': 'Cài đặt và sao lưu', html: ICON.gear, onclick: openSettings })),
    h('div', { class: 'segmented', role: 'group', 'aria-label': 'Cấp độ' },
      catalog.levels.map((l) => h('button', { type: 'button', 'aria-pressed': String(l.id === level.id),
        onclick: () => { state.level = l.id; save(); renderHome(); } }, `JLPT ${l.id}`))),
    quick,
    h('p', { class: 'section-title' }, `${level.lessons.length} bài · ${level.lessons.reduce((s, l) => s + l.count, 0)} từ`),
    grid,
    h('footer', { class: 'foot' },
      standalone ? null : h('p', null, 'Trên iPhone: mở bằng Safari → Chia sẻ → “Thêm vào MH chính” để dùng như app, kể cả khi offline.'),
      h('p', null, `Dữ liệu phiên bản ${catalog.version}`))));
  window.scrollTo(0, 0);
}

/* ---------- study ---------- */
let session = null;
async function renderStudy(levelId, lessonId) {
  document.documentElement.dataset.level = levelId;
  app.replaceChildren(h('p', { class: 'loading' }, 'Đang tải bài…'));
  const review = lessonId === 'review';
  let cards;
  let title;
  if (review) {
    title = `Cần xem lại · ${levelId}`;
    const lessons = levelOf(levelId).lessons.filter((l) => countWhere(state.marks, `${levelId}/${l.id}/`));
    cards = (await Promise.all(lessons.map((l) => loadLesson(levelId, l.id)))).flat().filter((c) => state.marks[c.key]);
  } else {
    const meta = lessonOf(levelId, lessonId);
    if (!meta) throw new Error('Bài học không tồn tại.');
    title = `${levelId} · ${meta.title}`;
    cards = await loadLesson(levelId, lessonId);
  }
  session = { levelId, lessonId, review, title, all: cards, filter: 'all', deck: [], pos: 0, flipped: false };
  const resume = !review && !state.shuffle && state.last && state.last.level === levelId && state.last.lesson === lessonId;
  buildDeck(resume ? state.last.pos : 0);
  drawStudy();
}
function buildDeck(pos = 0) {
  const pool = session.filter === 'marked' ? session.all.filter((c) => state.marks[c.key]) : session.all;
  session.deck = state.shuffle ? shuffled(pool) : pool.slice();
  session.pos = Math.max(0, Math.min(pos, session.deck.length - 1));
  session.flipped = false;
}
function remember() {
  if (session.review || session.filter !== 'all' || state.shuffle) return;
  state.last = { level: session.levelId, lesson: session.lessonId, pos: session.pos };
  save();
}
function drawStudy() {
  const s = session;
  const markedCount = s.all.filter((c) => state.marks[c.key]).length;
  const screen = h('div', { class: 'screen study' },
    h('div', { class: 'topbar' },
      h('button', { type: 'button', class: 'icon-btn', 'aria-label': 'Quay lại danh sách bài', html: ICON.back, onclick: () => go('#/') }),
      h('div', { class: 'title' }, h('b', null, s.title), h('span', { id: 'counter' }))),
    s.review ? null : h('div', { class: 'tools' },
      h('div', { class: 'segmented', role: 'group', 'aria-label': 'Lọc thẻ' },
        h('button', { type: 'button', 'aria-pressed': String(s.filter === 'all'), onclick: () => setFilter('all') }, `Tất cả (${s.all.length})`),
        h('button', { type: 'button', 'aria-pressed': String(s.filter === 'marked'), onclick: () => setFilter('marked') }, `★ Xem lại (${markedCount})`)),
      h('button', { type: 'button', class: 'chip', 'aria-pressed': String(state.shuffle), 'aria-label': 'Trộn thứ tự thẻ', html: ICON.shuffle + '<span>Trộn</span>', onclick: toggleShuffle })),
    h('div', { class: 'progress' }, h('i', { id: 'progress' })),
    h('div', { class: 'stage', id: 'stage' }),
    h('div', { class: 'controls' },
      h('button', { type: 'button', id: 'prev', onclick: () => move(-1) }, '‹ Trước'),
      h('button', { type: 'button', id: 'flip', class: 'flip', onclick: flip }, 'Lật thẻ'),
      h('button', { type: 'button', id: 'next', onclick: () => move(1) }, 'Tiếp ›')));
  app.replaceChildren(screen);
  drawCard();
  window.scrollTo(0, 0);
}
function setFilter(filter) {
  const current = session.deck[session.pos];
  session.filter = filter;
  buildDeck(0);
  if (current) { const i = session.deck.findIndex((c) => c.key === current.key); if (i >= 0) session.pos = i; }
  drawStudy();
}
function toggleShuffle() {
  state.shuffle = !state.shuffle; save();
  buildDeck(0);
  drawStudy();
  toast(state.shuffle ? 'Đã trộn thứ tự thẻ' : 'Học theo thứ tự trong bài');
}

function exampleNode(c) {
  const p = h('p', { class: 'jp', lang: 'ja' });
  const plain = (text) => {
    text.split(c.w).forEach((part, i) => { if (i) p.append(h('mark', null, c.w)); if (part) p.append(part); });
  };
  if (c.s) {
    for (const [text, extra] of c.s) {
      if (extra === 1) p.append(h('mark', null, text));
      else if (extra) p.append(h('ruby', null, text, h('rt', null, extra)));
      else plain(text);
    }
  } else plain(c.e);
  return p;
}
function actions(c) {
  const marked = !!state.marks[c.key];
  return h('div', { class: 'acts' },
    h('button', { type: 'button', class: 'speak', 'aria-label': 'Nghe phát âm', html: ICON.speak,
      onclick: (e) => { e.stopPropagation(); speak(plainReading(c.r) || c.w); } }),
    h('button', { type: 'button', class: 'mark', 'aria-pressed': String(marked), 'aria-label': marked ? 'Bỏ đánh dấu cần xem lại' : 'Đánh dấu cần xem lại',
      html: marked ? ICON.star : ICON.starLine, onclick: (e) => { e.stopPropagation(); toggleMark(c); } }));
}
function drawCard() {
  const s = session;
  const stage = document.getElementById('stage');
  const total = s.deck.length;
  document.getElementById('counter').textContent = total ? `Thẻ ${s.pos + 1} / ${total}` : 'Không có thẻ';
  document.getElementById('progress').style.width = total ? `${((s.pos + 1) / total) * 100}%` : '0';
  document.getElementById('prev').disabled = !total || s.pos === 0;
  document.getElementById('next').disabled = !total || s.pos >= total - 1;
  document.getElementById('flip').disabled = !total;
  document.getElementById('flip').textContent = s.flipped ? 'Mặt trước' : 'Lật thẻ';
  if (!total) {
    stage.replaceChildren(h('div', { class: 'empty' }, h('b', null, 'Chưa có từ cần xem lại'),
      h('p', null, 'Bấm ★ trên thẻ để đánh dấu những từ bạn muốn ôn riêng.')));
    return;
  }
  const c = s.deck[s.pos];
  const where = s.review ? lessonOf(c.level, c.lesson).title : `Thẻ ${c.idx + 1}`;
  const frontBody = state.front === 'vi'
    ? h('div', { class: 'front-body' }, h('p', { class: 'front-meaning' }, c.m), h('p', { class: 'hint' }, 'Nhớ lại từ tiếng Nhật, rồi chạm để lật'))
    : h('div', { class: 'front-body' }, h('p', { class: 'word', lang: 'ja' }, c.w), h('p', { class: 'hint' }, 'Nhớ cách đọc và nghĩa, rồi chạm để lật'));
  const card = h('div', { class: 'card' + (s.flipped ? ' flipped' : ''), id: 'card', role: 'group', 'aria-label': 'Thẻ từ vựng, chạm để lật' },
    h('section', { class: 'face front', 'aria-hidden': String(s.flipped) },
      h('div', { class: 'face-head' }, h('span', { class: 'num' }, where), actions(c)), frontBody),
    h('section', { class: 'face back', 'aria-hidden': String(!s.flipped) },
      h('div', { class: 'face-head' }, h('span', { class: 'num' }, where), actions(c)),
      h('div', { class: 'back-scroll' },
        h('div', { class: 'back-word' }, h('p', { class: 'w', lang: 'ja' }, c.w), h('p', { class: 'r', lang: 'ja' }, c.r)),
        h('p', { class: 'label' }, 'Ý nghĩa'), h('p', { class: 'meaning' }, c.m),
        h('div', { class: 'example' }, h('p', { class: 'label' }, 'Câu mẫu'), exampleNode(c),
          h('p', { class: 'tr' }, c.t || 'Chưa có bản dịch câu mẫu.')))));
  attachGestures(card);
  stage.replaceChildren(card);
}
function flip() {
  if (!session.deck.length) return;
  session.flipped = !session.flipped;
  const card = document.getElementById('card');
  card.classList.toggle('flipped', session.flipped);
  card.querySelector('.front').setAttribute('aria-hidden', String(session.flipped));
  card.querySelector('.back').setAttribute('aria-hidden', String(!session.flipped));
  document.getElementById('flip').textContent = session.flipped ? 'Mặt trước' : 'Lật thẻ';
  if (session.flipped) {
    const c = session.deck[session.pos];
    if (!state.seen[c.key]) { state.seen[c.key] = 1; save(); }
  }
}
function move(step) {
  const next = session.pos + step;
  if (next < 0 || next >= session.deck.length) return;
  session.pos = next;
  session.flipped = false;
  remember();
  drawCard();
}
function toggleMark(c) {
  if (state.marks[c.key]) delete state.marks[c.key];
  else { state.marks[c.key] = 1; askPersist(); }
  save();
  if (!session.review) {
    const count = session.all.filter((x) => state.marks[x.key]).length;
    const btn = document.querySelectorAll('.tools .segmented button')[1];
    if (btn) btn.textContent = `★ Xem lại (${count})`;
  }
  const flipped = session.flipped;
  drawCard();
  if (flipped) document.getElementById('card').classList.add('flipped');
  toast(state.marks[c.key] ? 'Đã thêm vào “Cần xem lại”' : 'Đã bỏ khỏi “Cần xem lại”');
}
function attachGestures(card) {
  let x0 = 0, y0 = 0, moved = false, active = false;
  card.addEventListener('pointerdown', (e) => { active = true; moved = false; x0 = e.clientX; y0 = e.clientY; });
  card.addEventListener('pointermove', (e) => { if (active && Math.abs(e.clientX - x0) > 10) moved = true; });
  card.addEventListener('pointerup', (e) => {
    if (!active) return; active = false;
    const dx = e.clientX - x0, dy = e.clientY - y0;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) { moved = true; move(dx < 0 ? 1 : -1); }
  });
  card.addEventListener('pointercancel', () => { active = false; });
  card.addEventListener('click', (e) => {
    if (moved) { moved = false; return; }
    if (e.target.closest('button') || (window.getSelection && String(window.getSelection()))) return;
    flip();
  });
}
document.addEventListener('keydown', (e) => {
  if (!session || !document.getElementById('card') || e.target.closest('input,textarea,dialog')) return;
  if (e.key === 'ArrowRight') move(1);
  else if (e.key === 'ArrowLeft') move(-1);
  else if (e.key === ' ' || e.key === 'Enter') { if (!e.target.closest('button')) { e.preventDefault(); flip(); } }
  else if (e.key.toLowerCase() === 's') toggleMark(session.deck[session.pos]);
});

/* ---------- settings & backup ---------- */
function openSettings() {
  const backup = JSON.stringify({ app: 'jlpt-fc', v: 1, marks: Object.keys(state.marks), seen: Object.keys(state.seen) });
  const out = h('textarea', { readonly: true, 'aria-label': 'Mã sao lưu' });
  out.value = backup;
  const input = h('textarea', { placeholder: 'Dán mã sao lưu vào đây', 'aria-label': 'Dán mã sao lưu' });
  let resetArmed = false;
  const dialog = h('dialog', { 'aria-label': 'Cài đặt' },
    h('div', { class: 'sheet' },
      h('h2', null, 'Mặt trước thẻ'),
      h('p', null, 'Chọn thứ bạn muốn nhìn trước khi lật.'),
      h('div', { class: 'segmented' },
        ['jp', 'vi'].map((v) => h('button', { type: 'button', 'aria-pressed': String(state.front === v),
          onclick: (e) => { state.front = v; save(); e.currentTarget.parentNode.querySelectorAll('button').forEach((b, i) => b.setAttribute('aria-pressed', String(['jp', 'vi'][i] === v))); } },
          v === 'jp' ? 'Từ tiếng Nhật' : 'Nghĩa tiếng Việt'))),
      h('hr'),
      h('h2', null, 'Sao lưu'),
      h('p', null, `${Object.keys(state.marks).length} từ cần xem lại · ${Object.keys(state.seen).length} từ đã xem. Lưu mã này (Ghi chú, tin nhắn…) để khôi phục khi đổi máy hoặc Safari xoá dữ liệu.`),
      out,
      h('div', { class: 'row' },
        h('button', { type: 'button', class: 'btn primary', onclick: async () => {
          try { await navigator.clipboard.writeText(backup); toast('Đã sao chép mã sao lưu'); }
          catch (_) { out.select(); toast('Hãy chọn và sao chép mã thủ công'); } } }, 'Sao chép'),
        navigator.share ? h('button', { type: 'button', class: 'btn', onclick: () => navigator.share({ title: 'Sao lưu JLPT', text: backup }).catch(() => {}) }, 'Chia sẻ…') : null),
      h('h2', null, 'Khôi phục'),
      input,
      h('div', { class: 'row' },
        h('button', { type: 'button', class: 'btn primary', onclick: () => {
          try {
            const data = JSON.parse(input.value.trim());
            if (data.app !== 'jlpt-fc' || !Array.isArray(data.marks)) throw new Error();
            data.marks.forEach((k) => { state.marks[k] = 1; });
            (data.seen || []).forEach((k) => { state.seen[k] = 1; });
            save(); dialog.close(); toast(`Đã khôi phục ${data.marks.length} từ cần xem lại`); route();
          } catch (_) { toast('Mã sao lưu không hợp lệ'); }
        } }, 'Khôi phục (gộp)')),
      h('hr'),
      h('div', { class: 'row' },
        h('button', { type: 'button', class: 'btn', onclick: (e) => {
          if (!resetArmed) { resetArmed = true; e.currentTarget.textContent = 'Bấm lần nữa để xoá hết tiến độ'; return; }
          state.marks = {}; state.seen = {}; state.last = null; save(); dialog.close(); toast('Đã xoá tiến độ'); route();
        } }, 'Xoá tiến độ học'),
        h('button', { type: 'button', class: 'btn', onclick: () => dialog.close() }, 'Đóng')),
      h('p', null, `Dữ liệu phiên bản ${catalog.version}. Tiến độ chỉ lưu trên thiết bị này.`)));
  dialog.addEventListener('close', () => { dialog.remove(); if (session && document.getElementById('card')) drawCard(); });
  dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
  document.body.append(dialog);
  dialog.showModal();
}

/* ---------- service worker (offline + updates) ---------- */
function setupServiceWorker() {
  if (!('serviceWorker' in navigator) || location.protocol === 'file:') return;
  let reloading = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => { if (!reloading) { reloading = true; location.reload(); } });
  const hadController = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.register('sw.js').then((reg) => {
    const offer = (worker) => toast('Có bài học mới', { label: 'Cập nhật', run: () => worker.postMessage({ type: 'SKIP_WAITING' }) });
    if (reg.waiting && hadController) offer(reg.waiting);
    reg.addEventListener('updatefound', () => {
      const worker = reg.installing;
      worker.addEventListener('statechange', () => {
        if (worker.state === 'installed' && navigator.serviceWorker.controller) offer(worker);
        if (worker.state === 'activated' && !hadController) toast('Đã lưu toàn bộ bài để dùng offline');
      });
    });
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') reg.update().catch(() => {}); });
  }).catch(() => {});
}

/* ---------- start ---------- */
loadCatalog().then(() => { window.addEventListener('hashchange', route); route(); }).catch(showError);
setupServiceWorker();
