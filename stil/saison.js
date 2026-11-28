/* Saison auf happymatty.de (CLAUDE.md, Abschnitt „Saison“).
   Weihnachtszeit: vom 24. November bis einschließlich 6. Januar bekommt <html> die Klasse „weihnachten“,
   und die Seite wird geschmückt; das Aussehen steht in saison.css, die Bilder liegen in /stil/weihnachten/.
   Es wird nichts gespeichert und nichts von fremden Servern geladen.
   Zum Prüfen lässt sich das Datum in der Adresse vorgeben: ?datum=2026-12-06 */
(function () {
  var d = document, html = d.documentElement;
  var heute = new Date(), probe = /[?&]datum=(\d{4})-(\d\d)-(\d\d)/.exec(location.search);
  if (probe) heute = new Date(+probe[1], +probe[2] - 1, +probe[3], 12);
  var monat = heute.getMonth() + 1, tag = heute.getDate();
  var weihnachten = (monat === 11 && tag >= 24) || monat === 12 || (monat === 1 && tag <= 6);
  if (weihnachten) html.className += (html.className ? ' ' : '') + 'weihnachten';
  if (!weihnachten && !probe) return;

  function bereit(f) { if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', f); else f(); }

  /* Ein Probedatum wandert über die Links der Seite mit */
  if (probe) bereit(function () {
    var a = d.querySelectorAll('a[href^="/"]');
    for (var i = 0; i < a.length; i++) {
      var h = a[i].getAttribute('href');
      if (!/\.pdf$|\?/.test(h)) a[i].setAttribute('href', h + '?datum=' + probe[1] + '-' + probe[2] + '-' + probe[3]);
    }
  });
  if (!weihnachten) return;

  var BILD = '/stil/weihnachten/';
  var farbe = d.createElement('meta'); farbe.name = 'theme-color'; farbe.content = '#07122A'; d.head.appendChild(farbe);

  function neu(tag, klasse, innen) {
    var e = d.createElement(tag); e.className = klasse; e.setAttribute('aria-hidden', 'true');
    if (innen) e.innerHTML = innen;
    return e;
  }
  function zufall(n) { var x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); }  /* fest, bei jedem Laden gleich */

  /* Wie viele Adventssonntage waren schon? Der vierte Advent ist der letzte Sonntag bis zum 24. Dezember. */
  function advent(h) {
    var jahr = h.getMonth() === 0 ? h.getFullYear() - 1 : h.getFullYear();
    var vierter = 24 - new Date(jahr, 11, 24).getDay(), n = 0;
    for (var i = 0; i < 4; i++) if (h >= new Date(jahr, 11, vierter - 7 * (3 - i))) n++;
    return n;
  }

  function kranz() {
    var n = advent(heute), t = '', dauer = [1.9, 1.5, 2.3, 1.7], start = [0.3, 1.1, 0.7, 1.6];
    for (var i = 0; i < 4; i++) {
      var an = i < n, hoch = an ? 22 - 2 * (n - i - 1) : 22;
      t += '<span class="w-kerze" style="left:' + (26 + 24 * i) + 'px;height:' + hoch + 'px">'
        + (an ? '<u></u><b style="animation-duration:' + dauer[i] + 's;animation-delay:-' + start[i] + 's"><i></i></b>' : '') + '</span>';
    }
    return '<div class="w-kranz">' + t + '<div class="w-kranz-gruen"></div></div>';
  }

  /* Feine Lichterkette: kleine LEDs in der Girlande, jede funkelt in ihrem eigenen Takt */
  function leds(box) {
    var W = box.clientWidth, t = '', schritt = 12.5, k0 = Math.ceil(W / 2 / schritt);
    for (var k = -k0; k < k0; k++) {
      var x = W / 2 + (k + 0.5) * schritt;
      if (Math.abs(x - W / 2) < 60 || x < 4 || x > W - 4) continue;       /* in der Mitte stehen die Kerzen */
      var u = ((((x - W / 2) % 175) + 175) % 175) / 175;                  /* Lage im Bogen der Girlande */
      var y = 2 + 10 * (1 - (2 * u - 1) * (2 * u - 1)) + 2 + 10 * zufall(k + 50);
      t += '<i' + (zufall(k + 7) < 0.3 ? ' class="w-blitz"' : '') + ' style="left:' + x.toFixed(1) + 'px;top:' + y.toFixed(1)
        + 'px;animation-duration:' + (2.2 + 3.2 * zufall(k + 99)).toFixed(2) + 's;animation-delay:-' + (5 * zufall(k + 123)).toFixed(2) + 's"></i>';
    }
    box.innerHTML = t;
  }

  /* Drei Kugeln hängen an der ersten Kachel. Jede, die Schrift verdecken würde, bleibt weg. */
  var KUGELN = [[16, 13, 9.5, 'rot'], [44, 19, 11.5, 'gold'], [71, 11, 8.5, 'blau']], kugelbild = null;
  function kugeln() {
    var f = { rot: ['#F0655A', '#C62828', '#7F1616'], gold: ['#F8DC8A', '#DDA93A', '#9C6F12'], blau: ['#6FB7E6', '#0072B2', '#024A75'] }, t = '<defs>';
    for (var n in f) t += '<radialGradient id="w-k-' + n + '" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="' + f[n][0]
      + '"/><stop offset=".55" stop-color="' + f[n][1] + '"/><stop offset="1" stop-color="' + f[n][2] + '"/></radialGradient>';
    t += '</defs>';
    for (var i = 0; i < KUGELN.length; i++) {
      var x = KUGELN[i][0], l = KUGELN[i][1], r = KUGELN[i][2], cy = l + 3.4 + r, hx = x - r * 0.36, hy = cy - r * 0.42;
      t += '<g><line x1="' + x + '" y1="0" x2="' + x + '" y2="' + l + '" stroke="#A88924" stroke-width="1.1"/>'
        + '<rect x="' + (x - 2.8) + '" y="' + l + '" width="5.6" height="4" rx="1" fill="#C9A227"/>'
        + '<circle cx="' + x + '" cy="' + cy + '" r="' + r + '" fill="url(#w-k-' + KUGELN[i][3] + ')"/>'
        + '<ellipse cx="' + hx + '" cy="' + hy + '" rx="' + r * 0.24 + '" ry="' + r * 0.14 + '" fill="#fff" opacity=".7" transform="rotate(-32 ' + hx + ' ' + hy + ')"/></g>';
    }
    var s = neu('span', 'w-kugeln', '<svg width="88" height="48" viewBox="0 0 88 48">' + t + '</svg>');
    return s;
  }
  function kugelnPlatz() {
    if (!kugelbild) return;
    var karte = kugelbild.parentNode, teile = karte.querySelectorAll('.titel,.text,.unterzeile'), schrift = [], i, j;
    for (i = 0; i < teile.length; i++) {
      var r = d.createRange(); r.selectNodeContents(teile[i]);
      var z = r.getClientRects(); for (j = 0; j < z.length; j++) schrift.push(z[j]);
    }
    var ort = kugelbild.getBoundingClientRect(), g = kugelbild.querySelectorAll('g');
    for (i = 0; i < g.length; i++) {
      var x = KUGELN[i][0], rr = KUGELN[i][2] + 2, cy = KUGELN[i][1] + 3.4 + KUGELN[i][2], frei = true;
      for (j = 0; j < schrift.length; j++) {
        if (schrift[j].right > ort.left + x - rr && schrift[j].left < ort.left + x + rr && schrift[j].bottom > ort.top && schrift[j].top + 4 < ort.top + cy + rr - 1) frei = false;   /* + 4: Luft über den Buchstaben einer Zeile */
      }
      g[i].style.display = frei ? '' : 'none';
    }
  }

  var figuren = [];
  function kacheln() {
    var listen = d.querySelectorAll('ul.liste'), namen = ['schneemann', 'laterne', 'baum', 'geschenke', 'vogel'];
    var mass = { schneemann: [42, 50], laterne: [40, 52], baum: [48, 55], geschenke: [52, 40], vogel: [38, 34] };
    var nr = 0, pfad = location.pathname;
    for (var i = 0; i < pfad.length; i++) nr += pfad.charCodeAt(i);       /* jede Seite beginnt mit einer anderen Figur */
    for (var j = 0; j < listen.length; j++) {
      var li = listen[j].querySelector('li'); if (!li) continue;
      if (j === 0) {
        li.appendChild(neu('span', 'w-schneedecke'));
        kugelbild = kugeln(); li.appendChild(kugelbild);
        continue;
      }
      var kopf = listen[j].previousElementSibling;
      if (!kopf || !/\bthemenkopf\b/.test(kopf.className)) continue;
      var name = namen[nr++ % namen.length], f = neu('img', 'w-figur');
      f.alt = ''; f.width = mass[name][0]; f.height = mass[name][1]; f.src = BILD + 'figur-' + name + '.svg';
      li.appendChild(f); figuren.push([f, kopf]);
    }
  }
  /* Reicht die Überschrift bis unter die Figur (schmales Handy), bleibt die Figur weg */
  function platz() {
    for (var i = 0; i < figuren.length; i++) {
      var r = d.createRange(); r.selectNodeContents(figuren[i][1]);
      figuren[i][0].style.visibility = '';
      figuren[i][0].style.visibility = r.getBoundingClientRect().right + 10 > figuren[i][0].getBoundingClientRect().left ? 'hidden' : '';
    }
  }

  bereit(function () {
    var b = d.body;
    var oben = neu('div', 'w-oben', '<div class="w-girlande"></div><div class="w-leds"></div>' + kranz());
    b.insertBefore(oben, b.firstChild);
    b.insertBefore(neu('div', 'w-himmel', '<div class="w-schnee"><i></i></div><div class="w-schnee w-schnee-2"><i></i></div>'), b.firstChild);
    var kette = oben.querySelector('.w-leds');
    leds(kette); kacheln(); platz(); kugelnPlatz();
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(function () { platz(); kugelnPlatz(); });
    var warten;
    window.addEventListener('resize', function () { clearTimeout(warten); warten = setTimeout(function () { leds(kette); platz(); kugelnPlatz(); }, 150); });
  });
})();
