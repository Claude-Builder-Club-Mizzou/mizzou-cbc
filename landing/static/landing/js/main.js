// ===== Navbar scroll effect =====
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== Mobile menu toggle =====
const hamburger = document.querySelector('.hamburger');
const mobileMenu = document.querySelector('.mobile-menu');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open');
});

// Close mobile menu on link click
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
  });
});

// ===== Benefits merch dropdown =====
document.querySelectorAll('.merch-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.benefit-card');
    const open = card.classList.toggle('merch-open');
    btn.setAttribute('aria-expanded', open);
  });
});

// ===== FAQ Accordion =====
document.querySelectorAll('.faq-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const wasOpen = item.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-item.open').forEach(openItem => {
      openItem.classList.remove('open');
    });

    // Toggle clicked
    if (!wasOpen) {
      item.classList.add('open');
    }
  });
});

// ===== Scroll Animations =====
const observerOptions = { threshold: 0.15 };

const fadeObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      fadeObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));

// Staggered items
const staggerObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const items = entry.target.querySelectorAll('.stagger-item');
      items.forEach((item, i) => {
        setTimeout(() => item.classList.add('visible'), i * 100);
      });
      staggerObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.stagger-container').forEach(el => staggerObserver.observe(el));

// ===== Animated Number Counter =====
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const target = parseInt(el.dataset.target, 10);
      const finalText = el.dataset.final;

      if (!target || target === 0) {
        el.textContent = finalText;
        counterObserver.unobserve(el);
        return;
      }

      const duration = 1500;
      const steps = 40;
      const stepTime = duration / steps;
      let step = 0;

      const timer = setInterval(() => {
        step++;
        const progress = step / steps;
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(target * eased);
        el.textContent = current.toLocaleString() + (finalText.includes('+') ? '+' : '');
        if (step >= steps) {
          clearInterval(timer);
          el.textContent = finalText;
        }
      }, stepTime);

      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(el => counterObserver.observe(el));

// ===== Page load fade-in =====
window.addEventListener('load', () => {
  document.body.classList.add('loaded');

  // Hero entrance animation
  document.querySelectorAll('.hero-anim').forEach((el, i) => {
    setTimeout(() => el.classList.add('visible'), i * 150);
  });
});

// ===== Back to Top Button =====
const backToTop = document.getElementById('backToTop');
if (backToTop) {
  window.addEventListener('scroll', () => {
    backToTop.classList.toggle('visible', window.scrollY > 600);
  });
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ===== Scroll Progress Bar =====
const scrollProgress = document.getElementById('scrollProgress');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / docHeight) * 100;
  scrollProgress.style.width = progress + '%';
});

// ===== Gallery Lightbox =====
(function() {
  var collage = document.getElementById('galCollage');
  var box = document.getElementById('lightbox');
  if (!collage || !box) return;

  var ROWS = 3;
  var SPEED_DESKTOP = 22; // px per second
  var SPEED_MOBILE = 12;

  var sources = Array.prototype.slice.call(collage.children);
  var tiles = sources.filter(function(t) { return t.tagName === 'BUTTON'; });
  var img = document.getElementById('lbImg');
  var label = document.getElementById('lbLabel');
  var idx = 0;
  var opener = null;
  var rows = [];
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Clones keep data-index, so every copy of a photo opens the same lightbox slide
  tiles.forEach(function(t, i) { t.dataset.index = i; });

  // Deal tiles across the rows round-robin
  collage.textContent = '';
  collage.classList.add('gallery-marquee');
  for (var r = 0; r < ROWS; r++) {
    var group = sources.filter(function(s, i) { return i % ROWS === r; });
    if (!group.length) continue;
    var row = document.createElement('div');
    row.className = 'gallery-row' + (r % 2 ? ' reverse' : '');
    var track = document.createElement('div');
    track.className = 'gallery-track';
    group.forEach(function(t) { track.appendChild(t); });
    row.appendChild(track);
    collage.appendChild(row);
    rows.push({ track: track, group: group });
  }

  // Repeat each row's photos until one half of the track is wider than the
  // viewport, then double it: the animation scrolls exactly one half.
  function fill() {
    if (reduceMotion) return;
    var speed = window.innerWidth <= 640 ? SPEED_MOBILE : SPEED_DESKTOP;
    rows.forEach(function(o) {
      o.track.querySelectorAll('[data-clone]').forEach(function(c) { c.remove(); });
      var setW = o.track.offsetWidth;
      if (!setW) return;
      var copies = Math.max(1, Math.ceil(collage.clientWidth / setW));
      for (var c = 0; c < copies * 2 - 1; c++) {
        o.group.forEach(function(t) {
          var cl = t.cloneNode(true);
          cl.dataset.clone = '1';
          cl.setAttribute('aria-hidden', 'true');
          cl.tabIndex = -1;
          o.track.appendChild(cl);
        });
      }
      o.track.style.setProperty('--dur', (setW * copies / speed) + 's');
    });
  }

  var fillTimer;
  function refill() {
    clearTimeout(fillTimer);
    fillTimer = setTimeout(fill, 100);
  }

  collage.querySelectorAll('img').forEach(function(im) {
    if (!im.complete) im.addEventListener('load', refill);
  });
  window.addEventListener('resize', refill);
  fill();

  function show(i) {
    idx = (i + tiles.length) % tiles.length;
    img.src = tiles[idx].dataset.full;
    img.alt = tiles[idx].dataset.caption;
    // "Project Picture" -> "project-picture"
    var slug = tiles[idx].dataset.caption.trim().toLowerCase().replace(/\s+/g, '-');
    label.textContent = slug;
    label.hidden = !slug;
  }

  function open(i) {
    opener = tiles[i];
    show(i);
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    document.getElementById('lbClose').focus();
  }

  function close() {
    box.classList.remove('open');
    document.body.style.overflow = '';
    if (opener) opener.focus();
  }

  collage.addEventListener('click', function(e) {
    var t = e.target.closest('button.gallery-tile');
    if (t) open(parseInt(t.dataset.index, 10));
  });

  document.getElementById('lbClose').addEventListener('click', close);
  document.getElementById('lbPrev').addEventListener('click', function() { show(idx - 1); });
  document.getElementById('lbNext').addEventListener('click', function() { show(idx + 1); });

  // click on the backdrop (not the image or buttons) closes
  box.addEventListener('click', function(e) { if (e.target === box) close(); });

  document.addEventListener('keydown', function(e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(idx - 1);
    else if (e.key === 'ArrowRight') show(idx + 1);
  });
})();

// ===== Events Calendar =====
(function() {
  var dataEl = document.getElementById('events-data');
  if (!dataEl) return;

  var events = JSON.parse(dataEl.textContent);
  var root = document.getElementById('eventsRoot');
  var grid = document.getElementById('calGrid');
  var label = document.getElementById('calMonthLabel');
  var prevBtn = document.getElementById('calPrev');
  var nextBtn = document.getElementById('calNext');
  var todayBtn = document.getElementById('calToday');
  var mainEl = document.getElementById('eventMain');
  var nextEl = document.getElementById('eventNext');

  if (!root || !grid || !label || !mainEl || !nextEl) return;

  var MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  function dateKey(e) { return e.year + '-' + e.month_num + '-' + e.day_num; }
  function eventDate(e) { return new Date(e.year, e.month_num - 1, e.day_num); }

  var now = new Date();
  var todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var currentYear = now.getFullYear();
  var currentMonth = now.getMonth();

  // Chronological order; the server already sorts by date + start time, and sort() is stable.
  var sorted = events.slice().sort(function(a, b) { return eventDate(a) - eventDate(b); });
  var upcoming = sorted.filter(function(e) { return eventDate(e) >= todayStart; });

  var eventsByDay = {};
  sorted.forEach(function(e) {
    var k = dateKey(e);
    (eventsByDay[k] = eventsByDay[k] || []).push(e);
  });

  var selected = null;

  // ----- Safe DOM builder (event text is admin-entered; never inject it as HTML) -----
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  // ----- Calendar -----
  function renderCalendar(year, month) {
    grid.innerHTML = '';
    label.textContent = MONTH_NAMES[month] + ' ' + year;

    var firstDay = new Date(year, month, 1).getDay();
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var daysInPrevMonth = new Date(year, month, 0).getDate();
    var isCurrentMonth = (now.getFullYear() === year && now.getMonth() === month);
    var selectedKey = selected ? dateKey(selected) : null;

    function makeCell(dayNum, extraClass) {
      var cell = el('div', 'calendar-day' + (extraClass ? ' ' + extraClass : ''));
      cell.appendChild(el('span', 'calendar-day-num', dayNum));
      return cell;
    }

    for (var i = firstDay - 1; i >= 0; i--) {
      grid.appendChild(makeCell(daysInPrevMonth - i, 'other-month'));
    }

    for (var d = 1; d <= daysInMonth; d++) {
      var cell = makeCell(d);
      var key = year + '-' + (month + 1) + '-' + d;

      if (isCurrentMonth && d === now.getDate()) cell.classList.add('today');
      if (key === selectedKey) cell.classList.add('active');

      if (eventsByDay[key]) {
        cell.classList.add('has-event');
        cell.setAttribute('role', 'button');
        cell.setAttribute('tabindex', '0');
        cell.setAttribute('aria-label', 'View event on ' + MONTH_NAMES[month] + ' ' + d);
        cell.dataset.dateKey = key;

        eventsByDay[key].forEach(function(ev) {
          cell.appendChild(el('span', 'calendar-event-title', ev.title));
        });

        cell.addEventListener('click', onDayActivate);
        cell.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onDayActivate.call(this);
          }
        });
      }
      grid.appendChild(cell);
    }

    var totalCells = firstDay + daysInMonth;
    var remaining = (totalCells <= 35) ? 35 - totalCells : 42 - totalCells;
    for (var j = 1; j <= remaining; j++) {
      grid.appendChild(makeCell(j, 'other-month'));
    }
  }

  function onDayActivate() {
    var list = eventsByDay[this.dataset.dateKey];
    if (!list) return;
    selectEvent(list[0]);
    if (window.innerWidth <= 960) {
      mainEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  // ----- Event cards -----
  function titleBar(titleText, tagText, muted) {
    var bar = el('div', 'term-bar');
    var dots = el('span', 'term-dots');
    dots.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 3; i++) dots.appendChild(document.createElement('i'));
    bar.appendChild(dots);
    bar.appendChild(el('span', 'term-bar-title', titleText));
    if (tagText) bar.appendChild(el('span', 'term-tag' + (muted ? ' muted' : ''), tagText));
    return bar;
  }

  function mainTag(ev) {
    var d = eventDate(ev);
    if (d < todayStart) return { text: 'past', muted: true };
    if (upcoming.length && upcoming[0] === ev) return { text: d.getTime() === todayStart.getTime() ? 'today' : 'next up', muted: false };
    if (d.getTime() === todayStart.getTime()) return { text: 'today', muted: false };
    return { text: 'upcoming', muted: false };
  }

  function metaRow(dl, k, v) {
    dl.appendChild(el('dt', null, k));
    dl.appendChild(el('dd', null, v));
  }

  function renderMain(ev) {
    var tag = mainTag(ev);
    mainEl.innerHTML = '';
    mainEl.appendChild(titleBar('event --rsvp', tag.text, tag.muted));

    var body = el('div', 'event-body');
    var prompt = el('div', 'ec-prompt');
    prompt.appendChild(el('b', null, '$ '));
    prompt.appendChild(document.createTextNode('cat events/' + ev.year + '-' + pad(ev.month_num) + '-' + pad(ev.day_num) + '.md'));
    body.appendChild(prompt);

    body.appendChild(el('h3', 'ec-title', ev.title));

    var dl = el('dl', 'ec-meta');
    metaRow(dl, 'date', ev.weekday + ', ' + MONTH_NAMES[ev.month_num - 1] + ' ' + ev.day_num + ', ' + ev.year);
    metaRow(dl, 'time', ev.time);
    metaRow(dl, 'where', ev.location);
    body.appendChild(dl);

    if (ev.description) body.appendChild(el('p', 'ec-desc', ev.description));

    body.appendChild(renderRsvp(ev));
    mainEl.appendChild(body);
  }

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function renderRsvp(ev) {
    if (eventDate(ev) < todayStart) {
      return el('div', 'rsvp-closed', '# rsvp closed: this event has already happened');
    }
    if (!ev.rsvp_url) {
      return el('div', 'rsvp-closed', '# rsvp link coming soon \u2014 check the GroupMe');
    }
    var wrap = el('div', 'rsvp');
    var link = el('a', 'btn-gold rsvp-submit', 'RSVP \u2192');
    link.href = ev.rsvp_url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    wrap.appendChild(link);
    wrap.appendChild(el('span', 'rsvp-note', 'opens the campus RSVP page'));
    return wrap;
  }

  function renderNext(current) {
    nextEl.innerHTML = '';
    // The event after the selected one, never one that already happened.
    var idx = sorted.indexOf(current);
    var following = null;
    for (var i = idx + 1; i < sorted.length; i++) {
      if (eventDate(sorted[i]) >= todayStart) { following = sorted[i]; break; }
    }

    nextEl.appendChild(titleBar('git log --next', following ? 'then' : null));
    var body = el('div', 'event-body');

    if (!following) {
      body.appendChild(el('p', 'next-empty', '# nothing scheduled after this — check the GroupMe'));
    } else {
      var link = el('button', 'next-link');
      link.type = 'button';
      link.appendChild(el('div', 'next-when', following.weekday + ', ' + following.month + ' ' + following.day + ' · ' + following.time));
      link.appendChild(el('div', 'next-title', following.title));
      link.appendChild(el('div', 'next-loc', '@ ' + following.location));
      link.addEventListener('click', function() { selectEvent(following); });
      body.appendChild(link);
    }
    nextEl.appendChild(body);
  }

  // ----- Past events log (newest first) -----
  var PAST_PREVIEW = 5;
  var pastEl = document.getElementById('eventPast');
  var past = sorted.filter(function(e) { return eventDate(e) < todayStart; }).reverse();
  var pastExpanded = false;

  function renderPast() {
    if (!pastEl) return;
    if (!past.length) { pastEl.hidden = true; return; }
    pastEl.hidden = false;
    pastEl.innerHTML = '';
    pastEl.appendChild(titleBar('git log --past', past.length + (past.length === 1 ? ' event' : ' events'), true));

    var body = el('div', 'event-body');
    var list = el('ul', 'past-list');
    var shown = pastExpanded ? past : past.slice(0, PAST_PREVIEW);

    shown.forEach(function(ev) {
      var li = el('li');
      var btn = el('button', 'past-item' + (ev === selected ? ' active' : ''));
      btn.type = 'button';
      btn.appendChild(el('span', 'past-date', pad(ev.month_num) + '/' + pad(ev.day_num) + '/' + ev.year));
      btn.appendChild(el('span', 'past-title', ev.title));
      btn.appendChild(el('span', 'past-loc', ev.location));
      btn.addEventListener('click', function() {
        selectEvent(ev);
        mainEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
      li.appendChild(btn);
      list.appendChild(li);
    });
    body.appendChild(list);

    if (past.length > PAST_PREVIEW) {
      var toggle = el('button', 'past-toggle', pastExpanded ? '# show less' : '# show all ' + past.length + ' past events');
      toggle.type = 'button';
      toggle.addEventListener('click', function() {
        pastExpanded = !pastExpanded;
        renderPast();
      });
      body.appendChild(toggle);
    }
    pastEl.appendChild(body);
  }

  function selectEvent(ev, keepMonth) {
    selected = ev;
    if (!keepMonth) {
      currentYear = ev.year;
      currentMonth = ev.month_num - 1;
    }
    renderCalendar(currentYear, currentMonth);
    renderMain(ev);
    renderNext(ev);
    renderPast();
  }

  // ----- Navigation -----
  prevBtn.addEventListener('click', function() {
    currentMonth--;
    if (currentMonth < 0) { currentMonth = 11; currentYear--; }
    renderCalendar(currentYear, currentMonth);
  });

  nextBtn.addEventListener('click', function() {
    currentMonth++;
    if (currentMonth > 11) { currentMonth = 0; currentYear++; }
    renderCalendar(currentYear, currentMonth);
  });

  todayBtn.addEventListener('click', function() {
    currentYear = now.getFullYear();
    currentMonth = now.getMonth();
    renderCalendar(currentYear, currentMonth);
  });

  // ----- Initial state: feature the next upcoming event, else the most recent past one -----
  var featured = upcoming.length > 0 ? upcoming[0] : sorted[sorted.length - 1];
  if (featured) {
    selectEvent(featured);
  } else {
    renderCalendar(currentYear, currentMonth);
    mainEl.appendChild(titleBar('event --rsvp'));
    var empty = el('div', 'event-body');
    empty.appendChild(el('p', 'next-empty', '# no events scheduled yet — check back soon'));
    mainEl.appendChild(empty);
    nextEl.appendChild(titleBar('git log --next'));
  }
})();
