/* Saison auf happymatty.de (CLAUDE.md, Abschnitt „Saison“).
   Weihnachtszeit: vom 24. November bis einschließlich 6. Januar bekommt <html> die Klasse „weihnachten“,
   und die Seite wird geschmückt; das Aussehen steht in saison.css, die Bilder liegen in /stil/weihnachten/.
   Es wird nichts gespeichert und nichts von fremden Servern geladen.
   Zum Prüfen lässt sich das Datum in der Adresse vorgeben: ?datum=2026-12-06 */
(function () {
  var d = document, html = d.documentElement, suche = location.search;
  var heute = new Date(), probe = /[?&]datum=(\d{4})-(\d\d)-(\d\d)/.exec(suche);
  if (probe) heute = new Date(+probe[1], +probe[2] - 1, +probe[3], 12);
  var monat = heute.getMonth() + 1, tag = heute.getDate();
  var weihnachten = (monat === 11 && tag >= 24) || monat === 12 || (monat === 1 && tag <= 6);
  if (weihnachten) html.className += (html.className ? ' ' : '') + 'weihnachten';
  var mit = probe ? 'datum=' + probe[1] + '-' + probe[2] + '-' + probe[3] : '';
  if (!weihnachten && !mit) return;

  function bereit(f) { if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', f); else f(); }

  /* Ein Probedatum wandert über die Links der Seite mit */
  if (mit) bereit(function () {
    var a = d.querySelectorAll('a[href^="/"]');
    for (var i = 0; i < a.length; i++) {
      var h = a[i].getAttribute('href');
      if (!/\.pdf$|\?/.test(h)) a[i].setAttribute('href', h + '?' + mit);
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
  function trifft(a, b, luft) { return a.right + luft > b.left && a.left - luft < b.right && a.bottom + luft > b.top && a.top - luft < b.bottom; }
  /* Rechtecke der Schrift in einem Element, Zeile für Zeile; „ohne“ wird übergangen */
  function schrift(e, ohne) {
    var aus = [], k = e.childNodes;
    for (var i = 0; i < k.length; i++) {
      if (k[i] === ohne) continue;
      var r = d.createRange(); r.selectNodeContents(k[i]);
      var z = r.getClientRects(); for (var j = 0; j < z.length; j++) if (z[j].width > 1) aus.push(z[j]);
    }
    return aus;
  }

  /* Wie viele Adventssonntage waren schon? Der vierte Advent ist der letzte Sonntag bis zum 24. Dezember. */
  function advent(h) {
    var jahr = h.getMonth() === 0 ? h.getFullYear() - 1 : h.getFullYear();
    var vierter = 24 - new Date(jahr, 11, 24).getDay(), n = 0;
    for (var i = 0; i < 4; i++) if (h >= new Date(jahr, 11, vierter - 7 * (3 - i))) n++;
    return n;
  }

  /* Adventskranz: Er steht rechts auf der Linie der Kopfzeile. Trägt die Kopfzeile dort Schrift
     (Thema, Teilthema) oder reicht der Zurück-Link bis dorthin, steht er rechts auf der Fußlinie. */
  var kranzbild = null;
  function kranz() {
    var n = advent(heute), t = '', dauer = [1.9, 1.5, 2.3, 1.7], start = [0.3, 1.1, 0.7, 1.6];
    for (var i = 0; i < 4; i++) {
      var an = i < n, hoch = an ? 22 - 2 * (n - i - 1) : 22;
      t += '<span class="w-kerze" style="left:' + (26 + 24 * i) + 'px;height:' + hoch + 'px">'
        + (an ? '<u></u><b style="animation-duration:' + dauer[i] + 's;animation-delay:-' + start[i] + 's"><i></i></b>' : '') + '</span>';
    }
    return neu('span', 'w-kranz', t + '<span class="w-kranz-gruen"></span>');
  }
  function kranzPlatz() {
    var kopf = d.querySelector('.kopf'), fuss = d.querySelector('footer');
    if (!kranzbild) return;
    if (kopf) {
      kranzbild.className = 'w-kranz w-kranz-kopf';
      if (kranzbild.parentNode !== kopf) kopf.appendChild(kranzbild);
      var ort = kranzbild.getBoundingClientRect(), stoert = schrift(kopf, kranzbild), frei = true, i;
      var dazu = d.querySelectorAll('.logo,.zurueck');
      for (i = 0; i < dazu.length; i++) stoert.push(dazu[i].getBoundingClientRect());
      for (i = 0; i < stoert.length; i++) if (trifft(stoert[i], ort, 5)) frei = false;
      if (frei) return;
    }
    if (fuss) { kranzbild.className = 'w-kranz w-kranz-fuss'; fuss.appendChild(kranzbild); }
    else if (kranzbild.parentNode) kranzbild.parentNode.removeChild(kranzbild);
  }

  /* Feine Lichterkette: kleine LEDs in der Girlande, jede funkelt in ihrem eigenen Takt */
  function leds(box) {
    var W = box.clientWidth, t = '', schritt = 12.5, k0 = Math.ceil(W / 2 / schritt);
    for (var k = -k0; k < k0; k++) {
      var x = W / 2 + (k + 0.5) * schritt;
      if (x < 4 || x > W - 4) continue;
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
    return neu('span', 'w-kugeln', '<svg width="88" height="48" viewBox="0 0 88 48">' + t + '</svg>');
  }
  function kugelnPlatz() {
    if (!kugelbild) return;
    var teile = kugelbild.parentNode.querySelectorAll('.titel,.text,.unterzeile'), zeilen = [], i, j;
    for (i = 0; i < teile.length; i++) zeilen = zeilen.concat(schrift(teile[i]));
    var ort = kugelbild.getBoundingClientRect(), g = kugelbild.querySelectorAll('g');
    for (i = 0; i < g.length; i++) {
      var x = KUGELN[i][0], rr = KUGELN[i][2] + 2, cy = KUGELN[i][1] + 3.4 + KUGELN[i][2], frei = true;
      for (j = 0; j < zeilen.length; j++) {
        if (zeilen[j].right > ort.left + x - rr && zeilen[j].left < ort.left + x + rr && zeilen[j].bottom > ort.top
          && zeilen[j].top + 4 < ort.top + cy + rr - 1) frei = false;   /* + 4: Luft über den Buchstaben einer Zeile */
      }
      g[i].style.display = frei ? '' : 'none';
    }
  }

  /* Figuren sitzen rechts oben auf einer Kachel: auf der ersten Kachel unter jeder weiteren Überschrift
     und auf der Startseite auf den Klassen-Kacheln BF2 (Laterne) und BGY (Geschenke). */
  var figuren = [], MASS = { schneemann: [42, 50], laterne: [40, 52], baum: [48, 55], geschenke: [52, 40], vogel: [38, 34] };
  function figur(li, name, kopf) {
    if (!li) return;
    var f = neu('img', 'w-figur'); f.alt = ''; f.width = MASS[name][0]; f.height = MASS[name][1]; f.src = BILD + 'figur-' + name + '.svg';
    li.appendChild(f); figuren.push([f, kopf]);
  }
  function kacheln() {
    var listen = d.querySelectorAll('ul.liste'), namen = ['schneemann', 'laterne', 'baum', 'geschenke', 'vogel'];
    var nr = 0, pfad = location.pathname;
    for (var i = 0; i < pfad.length; i++) nr += pfad.charCodeAt(i);       /* jede Seite beginnt mit einer anderen Figur */
    for (var j = 0; j < listen.length; j++) {
      var li = listen[j].querySelector('li'); if (!li) continue;
      if (j === 0) { li.appendChild(neu('span', 'w-schneedecke')); kugelbild = kugeln(); li.appendChild(kugelbild); continue; }
      var kopf = listen[j].previousElementSibling;
      if (kopf && /\bthemenkopf\b/.test(kopf.className)) figur(li, namen[nr++ % namen.length], kopf);
    }
    var klassen = d.querySelector('ul.klassen');
    if (klassen) {
      var kl = klassen.querySelectorAll('li'), ueber = klassen.previousElementSibling;
      figur(kl[1], 'laterne', ueber); figur(kl[2], 'geschenke', ueber);
    }
  }
  /* Reicht die Überschrift bis unter die Figur (schmales Handy), bleibt die Figur weg */
  function platz() {
    for (var i = 0; i < figuren.length; i++) {
      var f = figuren[i][0], kopf = figuren[i][1], frei = true;
      f.style.visibility = '';
      if (kopf) { var z = schrift(kopf), ort = f.getBoundingClientRect(); for (var j = 0; j < z.length; j++) if (trifft(z[j], ort, 6)) frei = false; }
      f.style.visibility = frei ? '' : 'hidden';
    }
  }

  /* Der Weihnachtsmann fährt mit Schlitten und zwei Rentieren langsam über die Fußlinie, immer wieder */
  function rentier(x, rot) {
    return '<g transform="translate(' + x + ',0)"><g class="w-trab' + (rot ? ' w-trab-2' : '') + '">'
      + '<path d="M7,20 L4,28.6 M9.4,20 L10,28.6 M19,20 L18.4,28.6 M21,19.6 L25,28" stroke="#7E5A3C" stroke-width="1.7" stroke-linecap="round" fill="none"/>'
      + '<ellipse cx="4.4" cy="15.2" rx="2" ry="1.4" fill="#F3EBDD" transform="rotate(-30 4.4 15.2)"/>'
      + '<ellipse cx="14" cy="17.4" rx="9.4" ry="4.5" fill="#A9744A"/><ellipse cx="14" cy="19.8" rx="6.2" ry="1.9" fill="#C79A6C"/>'
      + '<path d="M18.6,15.4 L22.8,8.4 L26.6,10 L24,19.4 Z" fill="#A9744A"/>'
      + '<path d="M24.6,6.2 L23.4,1.4 M24.1,3.9 L21.6,2.6 M23.8,2.7 L25.5,0.9 M26.2,6 L27,1.8 M26.7,3.5 L28.8,2.4" stroke="#E3C9A0" stroke-width="1.1" stroke-linecap="round" fill="none"/>'
      + '<ellipse cx="23.5" cy="6.2" rx="1.7" ry=".9" fill="#8C5E3A" transform="rotate(-35 23.5 6.2)"/>'
      + '<ellipse cx="26.6" cy="8.3" rx="3.7" ry="2.6" fill="#A9744A" transform="rotate(-12 26.6 8.3)"/>'
      + '<ellipse cx="29.2" cy="9" rx="1.9" ry="1.6" fill="#C79A6C"/>'
      + (rot ? '<circle cx="30.9" cy="8.6" r="3.4" fill="#FF6B5E" opacity=".35"/><circle cx="30.9" cy="8.6" r="1.4" fill="#F0453A"/>' : '<circle cx="30.8" cy="8.7" r="1.1" fill="#3A2A22"/>')
      + '<circle cx="26.9" cy="7.4" r=".6" fill="#1B1B1B"/>'
      + '<path d="M20.4,13.2 L24.8,15.6" stroke="#D63A2F" stroke-width="1.7" stroke-linecap="round"/><circle cx="22.8" cy="16.2" r="1" fill="#F4C542"/>'
      + '</g></g>';
  }
  function schlitten() {
    var t = '<svg width="116" height="30" viewBox="0 0 116 30">'
      + '<path d="M27.5,14 L66,14.4 L98,14.4" stroke="#D9B13A" stroke-width=".8" fill="none"/>'
      + '<path d="M2,27.7 L30,27.7 C35.4,27.7 37.6,24.4 35.8,21.2 M10,27.7 V23 M25,27.7 V23" stroke="#D9B13A" stroke-width="1.6" stroke-linecap="round" fill="none"/>'
      + '<ellipse cx="9.4" cy="10.6" rx="5.2" ry="5.8" fill="#8A5A2B"/><path d="M7.6,5.6 L11.4,5.2 L10.2,3.2 L8.6,3.4 Z" fill="#6E4520"/>'
      + '<ellipse cx="18.6" cy="13" rx="5.2" ry="5.8" fill="#D63A2F"/>'
      + '<path d="M19.6,11.4 L27.4,14" stroke="#D63A2F" stroke-width="2.6" stroke-linecap="round"/><circle cx="27.6" cy="14" r="1.5" fill="#fff"/>'
      + '<circle cx="19.8" cy="6.8" r="3.1" fill="#F2C9A5"/>'
      + '<path d="M17,7 C16.6,11.6 22.6,12.6 23,7.6 C21.6,9 18.6,8.8 17,7 Z" fill="#fff"/>'
      + '<path d="M16.6,5.2 L23,4.6 C21,1.2 17.6,0.6 14.4,2.4 C15.8,2.8 16.4,3.8 16.6,5.2 Z" fill="#D63A2F"/>'
      + '<rect x="16.2" y="4.3" width="7" height="1.7" rx=".85" fill="#fff"/><circle cx="14.2" cy="2.6" r="1.4" fill="#fff"/>'
      + '<path d="M3.6,23.4 L3.6,14.6 C3.6,12.4 5,11.6 7,11.8 L8.4,12 L8.4,17.6 L26.4,17.6 L30,13 L33.4,13 L30.6,23.4 Z" fill="#C62828"/>'
      + '<path d="M3.6,14.6 C3.6,12.4 5,11.6 7,11.8 L8.4,12 M26.4,17.6 L30,13 L33.4,13" stroke="#F4C542" stroke-width="1" stroke-linecap="round" fill="none"/>'
      + '<rect x="3.6" y="21.6" width="27.4" height="1.8" fill="#8E1B1B"/>'
      + rentier(44, false) + rentier(78, true) + '</svg>';
    return neu('div', 'w-bahn', '<div class="w-schlitten">' + t + '</div>');
  }

  /* Der Smiley im Logo trägt eine Weihnachtsmütze */
  function muetze() {
    return neu('span', 'w-muetze', '<svg width="27" height="21" viewBox="0 0 27 21">'
      + '<path d="M4.6,15 C4.8,6.4 9.6,2.4 15.4,2.6 C20.6,2.8 23.2,6.4 24,10 C21.8,8 19.6,8 18.4,9.4 C19.6,11.4 20,13.2 20.2,15 Z" fill="#D63A2F"/>'
      + '<path d="M15.4,2.6 C20.6,2.8 23.2,6.4 24,10 C21.8,8 19.6,8 18.4,9.4 C18,6.4 17,4.2 15.4,2.6 Z" fill="#B3211F"/>'
      + '<rect x="2" y="13.6" width="20.6" height="5.6" rx="2.8" fill="#fff" stroke="#D5E3F2" stroke-width=".6"/>'
      + '<circle cx="24" cy="11" r="2.9" fill="#fff" stroke="#D5E3F2" stroke-width=".6"/></svg>');
  }

  bereit(function () {
    var b = d.body, fuss = d.querySelector('footer'), logo = d.querySelector('.logo');
    var oben = neu('div', 'w-oben', '<div class="w-girlande"></div><div class="w-leds"></div>');
    b.insertBefore(oben, b.firstChild);
    b.insertBefore(neu('div', 'w-himmel', '<div class="w-schnee"><i></i></div><div class="w-schnee w-schnee-2"><i></i></div>'), b.firstChild);
    var kette = oben.querySelector('.w-leds');
    if (logo) logo.appendChild(muetze());
    if (fuss) fuss.appendChild(schlitten());
    kranzbild = kranz();
    leds(kette); kacheln();
    function ordnen() { kranzPlatz(); platz(); kugelnPlatz(); }
    ordnen();
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(ordnen);
    var warten;
    window.addEventListener('resize', function () { clearTimeout(warten); warten = setTimeout(function () { leds(kette); ordnen(); }, 150); });
  });
})();
