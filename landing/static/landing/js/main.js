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

// ===== Scroll Spy — active nav link =====
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    const top = section.offsetTop - 100;
    if (window.scrollY >= top) {
      current = section.getAttribute('id');
    }
  });
  navAnchors.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
});

// ===== Scroll Progress Bar =====
const scrollProgress = document.getElementById('scrollProgress');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / docHeight) * 100;
  scrollProgress.style.width = progress + '%';
});

// ===== Gallery Carousel =====
(function() {
  var track = document.getElementById('galTrack');
  var dots = document.getElementById('galDots');
  if (!track) return;

  var slides = track.querySelectorAll('.gallery-slide');
  var total = slides.length;
  var idx = 0;

  function buildDots() {
    dots.innerHTML = '';
    for (var i = 0; i < total; i++) {
      var d = document.createElement('button');
      d.classList.add('gallery-dot');
      if (i === 0) d.classList.add('active');
      d.dataset.i = i;
      d.addEventListener('click', function() { goTo(parseInt(this.dataset.i)); });
      dots.appendChild(d);
    }
  }

  function goTo(i) {
    idx = i;
    if (idx < 0) idx = total - 1;
    if (idx >= total) idx = 0;
    track.style.transform = 'translateX(-' + (idx * 100) + '%)';
    dots.querySelectorAll('.gallery-dot').forEach(function(d, j) {
      d.classList.toggle('active', j === idx);
    });
  }

  document.getElementById('galPrev').addEventListener('click', function() { goTo(idx - 1); });
  document.getElementById('galNext').addEventListener('click', function() { goTo(idx + 1); });

  // Auto-advance every 5s
  var timer = setInterval(function() { goTo(idx + 1); }, 5000);
  track.closest('.gallery').addEventListener('mouseenter', function() { clearInterval(timer); });
  track.closest('.gallery').addEventListener('mouseleave', function() {
    timer = setInterval(function() { goTo(idx + 1); }, 5000);
  });

  buildDots();
})();

// ===== Events Calendar =====
(function() {
  var dataEl = document.getElementById('events-data');
  if (!dataEl) return;

  var events = JSON.parse(dataEl.textContent);
  var grid = document.getElementById('calGrid');
  var label = document.getElementById('calMonthLabel');
  var prevBtn = document.getElementById('calPrev');
  var nextBtn = document.getElementById('calNext');
  var todayBtn = document.getElementById('calToday');

  if (!grid || !label) return;

  // Map date keys to event titles for display in calendar cells
  var eventDateMap = {};
  events.forEach(function(e) {
    var key = e.year + '-' + e.month_num + '-' + e.day_num;
    if (!eventDateMap[key]) eventDateMap[key] = [];
    eventDateMap[key].push(e.title);
  });

  var selectedKey = null;
  var now = new Date();
  var currentYear = now.getFullYear();
  var currentMonth = now.getMonth();

  var MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  function renderCalendar(year, month) {
    grid.innerHTML = '';
    label.textContent = MONTH_NAMES[month] + ' ' + year;

    var firstDay = new Date(year, month, 1).getDay();
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var daysInPrevMonth = new Date(year, month, 0).getDate();

    var today = new Date();
    var isCurrentMonth = (today.getFullYear() === year && today.getMonth() === month);

    function makeCell(dayNum, extraClass) {
      var cell = document.createElement('div');
      cell.classList.add('calendar-day');
      if (extraClass) cell.classList.add(extraClass);
      var numSpan = document.createElement('span');
      numSpan.classList.add('calendar-day-num');
      numSpan.textContent = dayNum;
      cell.appendChild(numSpan);
      return cell;
    }

    // Previous month trailing days
    for (var i = firstDay - 1; i >= 0; i--) {
      grid.appendChild(makeCell(daysInPrevMonth - i, 'other-month'));
    }

    // Current month days
    for (var d = 1; d <= daysInMonth; d++) {
      var cell = makeCell(d);
      var dateKey = year + '-' + (month + 1) + '-' + d;

      if (isCurrentMonth && d === today.getDate()) {
        cell.classList.add('today');
      }
      if (dateKey === selectedKey) {
        cell.classList.add('active');
      }

      if (eventDateMap[dateKey]) {
        cell.classList.add('has-event');
        cell.setAttribute('role', 'button');
        cell.setAttribute('tabindex', '0');
        cell.setAttribute('aria-label', 'View event on ' + MONTH_NAMES[month] + ' ' + d);
        cell.dataset.dateKey = dateKey;

        // Add event title labels inside the cell
        eventDateMap[dateKey].forEach(function(title) {
          var titleEl = document.createElement('span');
          titleEl.classList.add('calendar-event-title');
          titleEl.textContent = title;
          cell.appendChild(titleEl);
        });

        cell.addEventListener('click', function() {
          handleDateClick(this.dataset.dateKey, this);
        });
        cell.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handleDateClick(this.dataset.dateKey, this);
          }
        });
      }

      grid.appendChild(cell);
    }

    // Next month leading days
    var totalCells = firstDay + daysInMonth;
    var remaining = (totalCells <= 35) ? 35 - totalCells : 42 - totalCells;
    for (var i = 1; i <= remaining; i++) {
      grid.appendChild(makeCell(i, 'other-month'));
    }
  }

  var detailContent = document.getElementById('detailContent');
  var detailDate = document.getElementById('detailDate');
  var detailCards = document.getElementById('detailCards');

  function showEventDetail(dateKey) {
    var matched = events.filter(function(e) {
      return (e.year + '-' + e.month_num + '-' + e.day_num) === dateKey;
    });

    if (matched.length > 0 && detailContent && detailCards && detailDate) {
      var parts = dateKey.split('-');
      detailDate.textContent = MONTH_NAMES[parseInt(parts[1]) - 1] + ' ' + parts[2] + ', ' + parts[0];

      detailCards.innerHTML = '';
      matched.forEach(function(ev) {
        var card = document.createElement('div');
        card.classList.add('detail-card');
        card.innerHTML =
          '<div class="detail-card-title text-heading">' + ev.title + '</div>' +
          '<div class="detail-card-desc text-muted">' + ev.description + '</div>' +
          '<div class="detail-card-meta text-muted">' +
            '<span>\u{1F4CD} ' + ev.location + '</span>' +
            '<span>\u{1F550} ' + ev.time + '</span>' +
          '</div>';
        detailCards.appendChild(card);
      });

      document.querySelectorAll('.detail-event-item').forEach(function(item) {
        item.classList.remove('active');
        if (item.dataset.date === dateKey) {
          item.classList.add('active');
        }
      });
    }
  }

  function handleDateClick(dateKey, cell) {
    selectedKey = dateKey;
    grid.querySelectorAll('.calendar-day.active').forEach(function(c) {
      c.classList.remove('active');
    });
    cell.classList.add('active');

    showEventDetail(dateKey);

    if (window.innerWidth <= 960) {
      document.getElementById('eventDetailPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  // Click on all-events list items to trigger calendar selection
  document.querySelectorAll('.detail-event-item').forEach(function(item) {
    item.addEventListener('click', function() {
      var dateKey = this.dataset.date;
      if (!dateKey) return;
      var parts = dateKey.split('-');
      var targetMonth = parseInt(parts[1]) - 1;
      var targetYear = parseInt(parts[0]);

      // Navigate calendar to the right month if needed
      if (targetYear !== currentYear || targetMonth !== currentMonth) {
        currentYear = targetYear;
        currentMonth = targetMonth;
        renderCalendar(currentYear, currentMonth);
      }

      // Find and click the matching calendar day
      var dayCell = grid.querySelector('.calendar-day.has-event[data-date-key="' + dateKey + '"]');
      if (dayCell) {
        handleDateClick(dateKey, dayCell);
      }
    });
  });

  prevBtn.addEventListener('click', function() {
    currentMonth--;
    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    }
    renderCalendar(currentYear, currentMonth);
  });

  nextBtn.addEventListener('click', function() {
    currentMonth++;
    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }
    renderCalendar(currentYear, currentMonth);
  });

  todayBtn.addEventListener('click', function() {
    var t = new Date();
    currentYear = t.getFullYear();
    currentMonth = t.getMonth();
    renderCalendar(currentYear, currentMonth);
  });

  // ----- Pick the NEXT upcoming event (today or later), not the first one added -----
  function eventDate(e) { return new Date(e.year, e.month_num - 1, e.day_num); }
  function keyToDate(key) {
    var p = key.split('-');
    return new Date(parseInt(p[0]), parseInt(p[1]) - 1, parseInt(p[2]));
  }

  var todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var sorted = events.slice().sort(function(a, b) { return eventDate(a) - eventDate(b); });
  var upcoming = sorted.filter(function(e) { return eventDate(e) >= todayStart; });

  // Hide past events from the "All Upcoming" list (they stay visible on the calendar)
  if (upcoming.length > 0) {
    document.querySelectorAll('.detail-event-item').forEach(function(item) {
      if (item.dataset.date && keyToDate(item.dataset.date) < todayStart) {
        item.style.display = 'none';
      }
    });
  }

  // Feature the next upcoming event; if everything is in the past, fall back to the latest one
  var featured = upcoming.length > 0 ? upcoming[0] : sorted[sorted.length - 1];

  if (featured) {
    selectedKey = featured.year + '-' + featured.month_num + '-' + featured.day_num;
    // Open the calendar on the month of that event so the highlight is visible
    currentYear = featured.year;
    currentMonth = featured.month_num - 1;
  }

  renderCalendar(currentYear, currentMonth);
  if (selectedKey) showEventDetail(selectedKey);
})();
