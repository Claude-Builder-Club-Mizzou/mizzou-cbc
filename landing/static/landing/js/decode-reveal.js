// "Decode" reveal for banner images: a wave of random block characters sweeps top to bottom
// over the letters, and each cell locks into the real SVG as the wave passes.
// Opt in with data-decode-reveal="<delay ms>"; it starts once the enclosing .terminal-frame is .visible.
(function () {
  var ROWS = 6;                 // figlet rows in every banner
  var CELL_COLS = 2;            // grid columns per cell, so cells are roughly square
  var SPAN = 600;               // ms for the wave to travel from the top row to the bottom row
  var SKEW = 120;               // ms of extra left-to-right lag, so each row's edge isn't perfectly flat
  var JITTER = 220;             // random extra ms before a cell locks
  var LEAD = 380;               // ms a cell scrambles before it locks
  var FRAME_MS = 45;
  var CHARS = '█▓▒░▌▐▀▄';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function finish(img, canvas) {
    img.classList.add('decode-done');
    if (canvas && canvas.parentNode) canvas.parentNode.removeChild(canvas);
  }

  function run(img) {
    var w = img.offsetWidth, h = img.offsetHeight;
    if (reduceMotion || !w || !h) return finish(img);
    var canvas = null;
    try {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var cw = Math.round(w * dpr), ch = Math.round(h * dpr);

      // Sharp copy of the banner, used to read which cells have ink and to draw locked cells
      var src = document.createElement('canvas');
      src.width = cw; src.height = ch;
      var sctx = src.getContext('2d');
      sctx.drawImage(img, 0, 0, cw, ch);
      var px = sctx.getImageData(0, 0, cw, ch).data;

      var cols = Math.round(12 * w / h);          // banner viewBoxes are 12 units tall
      var gcols = Math.ceil(cols / CELL_COLS);
      var cellW = cw / gcols, cellH = ch / ROWS;
      var cells = [];
      for (var gy = 0; gy < ROWS; gy++) {
        for (var gx = 0; gx < gcols; gx++) {
          var x0 = Math.floor(gx * cellW), y0 = Math.floor(gy * cellH);
          var x1 = Math.min(cw, Math.ceil((gx + 1) * cellW)), y1 = Math.min(ch, Math.ceil((gy + 1) * cellH));
          var rgb = null;
          for (var y = y0; y < y1 && !rgb; y++) {
            for (var x = x0; x < x1; x++) {
              var i = (y * cw + x) * 4;
              if (px[i + 3] > 120) { rgb = px[i] + ',' + px[i + 1] + ',' + px[i + 2]; break; }
            }
          }
          if (rgb) cells.push({ x: x0, y: y0, w: x1 - x0, h: y1 - y0, rgb: rgb,
                                lock: (gy / ROWS) * SPAN + (gx / gcols) * SKEW + Math.random() * JITTER });
        }
      }

      canvas = document.createElement('canvas');
      canvas.width = cw; canvas.height = ch;
      canvas.setAttribute('aria-hidden', 'true');
      // The parent must be the containing block before img.offsetLeft/Top are read
      img.parentNode.style.position = 'relative';
      canvas.style.cssText = 'position:absolute;pointer-events:none;width:' + w + 'px;height:' + h +
        'px;left:' + img.offsetLeft + 'px;top:' + img.offsetTop + 'px;';
      img.parentNode.appendChild(canvas);
      var ctx = canvas.getContext('2d');
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = '700 ' + Math.round(cellH * 0.9) + 'px "Fira Code","JetBrains Mono",monospace';

      var t0 = performance.now(), end = SPAN + SKEW + JITTER + FRAME_MS;
      (function frame() {
        var t = performance.now() - t0;
        ctx.clearRect(0, 0, cw, ch);
        for (var k = 0; k < cells.length; k++) {
          var c = cells[k];
          if (t >= c.lock) {
            ctx.drawImage(src, c.x, c.y, c.w, c.h, c.x, c.y, c.w, c.h);
          } else if (t >= c.lock - LEAD) {
            ctx.fillStyle = 'rgba(' + c.rgb + ',0.8)';
            ctx.fillText(CHARS.charAt((Math.random() * CHARS.length) | 0), c.x + c.w / 2, c.y + c.h / 2);
          }
        }
        if (t >= end) return finish(img, canvas);
        setTimeout(frame, FRAME_MS);
      })();
    } catch (e) {
      finish(img, canvas);
    }
  }

  function start(img) {
    if (img.complete && img.naturalWidth) run(img);
    else {
      img.addEventListener('load', function () { run(img); }, { once: true });
      img.addEventListener('error', function () { finish(img); }, { once: true });
    }
  }

  document.querySelectorAll('[data-decode-reveal]').forEach(function (img) {
    var delay = parseInt(img.getAttribute('data-decode-reveal'), 10) || 0;
    var frame = img.closest('.terminal-frame');
    function go() { setTimeout(function () { start(img); }, delay); }
    if (!frame || frame.classList.contains('visible')) return go();
    var mo = new MutationObserver(function () {
      if (frame.classList.contains('visible')) { mo.disconnect(); go(); }
    });
    mo.observe(frame, { attributes: true, attributeFilter: ['class'] });
  });
})();
