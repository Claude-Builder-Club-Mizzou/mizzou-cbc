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

// ===== Dark mode toggle =====
const allDarkToggles = document.querySelectorAll('.dark-toggle');
const savedTheme = localStorage.getItem('theme');

function applyDark(isDark) {
  document.body.classList.toggle('dark', isDark);
  document.documentElement.classList.toggle('dark', isDark);
  allDarkToggles.forEach(btn => btn.textContent = isDark ? '☀️' : '🌙');
}

const shouldBeDark = savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches);
applyDark(shouldBeDark);

allDarkToggles.forEach(btn => {
  btn.addEventListener('click', () => {
    const isDark = !document.body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    applyDark(isDark);
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

// ===== Floating Particles =====
const canvas = document.getElementById('heroParticles');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animId;

  function resizeCanvas() {
    const hero = canvas.parentElement;
    canvas.width = hero.offsetWidth;
    canvas.height = hero.offsetHeight;
  }

  function createParticles() {
    particles = [];
    const count = Math.floor((canvas.width * canvas.height) / 15000);
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2 + 0.5,
        dx: (Math.random() - 0.5) * 0.4,
        dy: (Math.random() - 0.5) * 0.4,
        opacity: Math.random() * 0.5 + 0.1,
      });
    }
  }

  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((p, i) => {
      p.x += p.dx;
      p.y += p.dy;

      if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(241, 184, 45, ${p.opacity})`;
      ctx.fill();

      // Draw lines between nearby particles
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(241, 184, 45, ${0.06 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    });

    animId = requestAnimationFrame(drawParticles);
  }

  resizeCanvas();
  createParticles();
  drawParticles();

  window.addEventListener('resize', () => {
    resizeCanvas();
    createParticles();
  });

  // Pause particles when hero is not visible
  const heroObserver = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) {
      cancelAnimationFrame(animId);
    } else {
      drawParticles();
    }
  });
  heroObserver.observe(canvas.parentElement);
}

// ===== Parallax Orbs =====
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  document.querySelectorAll('.parallax-orb').forEach((orb, i) => {
    const speed = i === 0 ? 0.3 : 0.2;
    orb.style.transform = `translateY(${scrollY * speed}px)`;
  });
});

// Enlarge cursor on interactive elements
document.querySelectorAll('a, button, .tilt-card, .faq-btn').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('cursor-hover'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('cursor-hover'));
});

// ===== 3D Tilt Effect on Cards =====
document.querySelectorAll('.tilt-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -8;
    const rotateY = ((x - centerX) / centerX) * 8;

    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale(1)';
  });
});

// ===== Magnetic Buttons =====
document.querySelectorAll('.magnetic').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });

  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'translate(0, 0)';
  });
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

    // Register calendar event days with custom cursor
    grid.querySelectorAll('.has-event').forEach(function(el) {
      el.addEventListener('mouseenter', function() { cursor.classList.add('cursor-hover'); });
      el.addEventListener('mouseleave', function() { cursor.classList.remove('cursor-hover'); });
    });
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