/* Klang der Weihnachtszeit auf happymatty.de (CLAUDE.md, Abschnitt „Saison“); saison.js lädt diese Datei nach.
   Es erklingt nur, was jemand antippt: Die Lichterkette ist ein Glockenspiel, und auf der Startseite hängt eine
   Glocke, die Jingle Bells spielt (erst klassisch als Glockenspiel, dann mit Bass, Beat und Synthesizer, nach
   einem Drop zum Schluss ein ruhiges Klavier).
   Die Töne entstehen im Browser; nur die Klaviertöne des Schlusses sind Aufnahmen und liegen im Ordner klavier/
   auf dem eigenen Server. Nichts wird gespeichert, nichts von fremden Servern geladen.
   Wichtig: Töne werden erst kurz vor ihrem Einsatz angelegt. Hunderte vorbereitete Tongeber überlasten den Ton
   im Browser, dann knarzt es (so geschehen am 28.11.2026 in Safari). Im Drop spielen Bass und Synthesizer deshalb
   auf wenigen Tongebern, die durchlaufen und je Ton nur neue Stellwerte bekommen. */
(function () {
  var d = document, oben = d.querySelector('.w-oben'), kette = d.querySelector('.w-leds');
  var A = window.AudioContext || window.webkitAudioContext;
  if (!oben || !kette || !A) return;
  var ton = null, haupt = null;
  /* Fassung des Lieds: 1 endet nach dem Kehrreim mit Beat (24 Takte, gut 40 Sekunden);
     2 hängt vier Takte Aufbau und den Drop über den ganzen Kehrreim an (44 Takte, knapp 80 Sekunden);
     3 hat einen kürzeren Aufbau, den Drop nur über die erste Hälfte, einen Schlussschlag und danach ein ruhiges
     Klavier (nachgebildet) mit Glöckchen (gut 70 Sekunden);
     4 ist wie 3, aber der Beat geht ohne Schlussschlag direkt in ein reines Klavier über (berechnete Töne), und
     nach dem Glöckchen kommt ein tiefer Schlussakkord (gut 70 Sekunden);
     5 ist die Fassung für alle (Freigabe Patrick 28.11.2026): wie 4, das Klavier aber aus Aufnahmen eines echten
     Flügels, und nach dem Beat erklingt nur noch Klavier (auch der helle Akkord vor dem Schluss).
     ?klang=1 bis ?klang=4 holen die älteren Fassungen zurück. */
  var WAHL = (/[?&]klang=(\d)/.exec(location.search) || [])[1], FASSUNG = WAHL > 0 && WAHL < 5 ? +WAHL : 5;
  var ruhig = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ausgang(ctx) {                       /* Summe mit sanftem Begrenzer, damit nichts übersteuert */
    var presse = ctx.createDynamicsCompressor(), g = ctx.createGain();
    presse.threshold.value = -16; presse.knee.value = 12; presse.ratio.value = 5; presse.attack.value = 0.004; presse.release.value = 0.16;
    g.gain.value = 0.85; g.connect(presse); presse.connect(ctx.destination);
    return g;
  }
  function audio() {
    if (!ton) { ton = new A(); haupt = ausgang(ton); }
    if (ton.state === 'suspended') ton.resume();
    return ton;
  }

  /* ---------- Instrumente ---------- */
  function huelle(g, t, an, laut, aus) {         /* schnell an, weich aus */
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(laut, t + an); g.gain.exponentialRampToValueAtTime(0.0001, t + an + aus);
  }
  /* Glockenspiel: Grundton und zwei helle Teiltöne, die schneller ausklingen */
  var GLOCKE = [[1, 1, 1.3], [2.76, 0.26, 0.45], [5.4, 0.1, 0.2]];
  function glocke(ctx, ziel, f, t, laut) {
    for (var i = 0; i < GLOCKE.length; i++) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = 'sine'; o.frequency.value = f * GLOCKE[i][0];
      huelle(g, t, 0.003, laut * GLOCKE[i][1], GLOCKE[i][2]);
      o.connect(g); g.connect(ziel); o.start(t); o.stop(t + GLOCKE[i][2] + 0.06);
    }
  }
  /* Synthesizer: Sägezahn oder Rechteck durch einen Tiefpass, der sich schließt (Bass, Arpeggio, zweite Stimme) */
  function synth(ctx, ziel, f, t, dauer, laut, auf, zu, guete, form) {
    var o = ctx.createOscillator(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
    o.type = form || 'sawtooth'; o.frequency.value = f;
    fl.type = 'lowpass'; fl.Q.value = guete; fl.frequency.setValueAtTime(auf, t); fl.frequency.exponentialRampToValueAtTime(zu, t + dauer);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(laut, t + 0.006);
    g.gain.setValueAtTime(laut, t + dauer * 0.55); g.gain.exponentialRampToValueAtTime(0.0001, t + dauer);
    o.connect(fl); fl.connect(g); g.connect(ziel); o.start(t); o.stop(t + dauer + 0.03);
  }
  /* Bassdrum: ein Sinus, der schnell nach unten fällt */
  function kick(ctx, ziel, t, laut) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(165, t); o.frequency.exponentialRampToValueAtTime(48, t + 0.11);
    huelle(g, t, 0.004, laut, 0.28);
    o.connect(g); g.connect(ziel); o.start(t); o.stop(t + 0.32);
  }
  /* Rauschen für Hi-Hat (hell, kurz), Clap (mittig, etwas länger), Wirbel und Becken */
  function rauschen(ctx) {
    if (!ctx.hmRauschen) {
      var b = ctx.createBuffer(1, Math.floor(ctx.sampleRate * 0.6), ctx.sampleRate), x = b.getChannelData(0);
      for (var i = 0; i < x.length; i++) x[i] = Math.random() * 2 - 1;
      ctx.hmRauschen = b;
    }
    return ctx.hmRauschen;
  }
  function zisch(ctx, ziel, t, dauer, laut, art, hz) {
    var q = ctx.createBufferSource(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
    q.buffer = rauschen(ctx); q.loop = true; fl.type = art; fl.frequency.value = hz; fl.Q.value = art === 'bandpass' ? 0.9 : 0.7;
    huelle(g, t, 0.002, laut, dauer);
    q.connect(fl); fl.connect(g); g.connect(ziel); q.start(t, Math.random() * 0.3); q.stop(t + dauer + 0.03);
  }
  function hihat(ctx, ziel, t, laut, offen) { zisch(ctx, ziel, t, offen ? 0.16 : 0.045, laut, 'highpass', 7500); }
  function clap(ctx, ziel, t, laut) { zisch(ctx, ziel, t, 0.15, laut, 'bandpass', 1700); zisch(ctx, ziel, t + 0.012, 0.1, laut * 0.6, 'bandpass', 2300); }
  function trommel(ctx, ziel, t, laut) { zisch(ctx, ziel, t, 0.07, laut, 'bandpass', 1900); zisch(ctx, ziel, t, 0.05, laut * 0.5, 'highpass', 5000); }
  function becken(ctx, ziel, t, laut) { zisch(ctx, ziel, t, 1.3, laut, 'highpass', 5200); }

  /* Klavierklang für den Schluss (Fassung 3), nachgebildet, keine Aufnahme: ein Ton aus zwölf Teiltönen (je höher,
     desto leiser) auf zwei leicht gegeneinander verstimmten „Saiten“. Der Anschlag ist hell und laut, dann wird der
     Ton rasch weicher und klingt langsam aus. */
  function saite(c) {
    if (!c.hmSaite) {
      var st = [0, 1, 0.55, 0.3, 0.2, 0.11, 0.08, 0.05, 0.035, 0.022, 0.015, 0.01, 0.007];
      c.hmSaite = c.createPeriodicWave(new Float32Array(st.length), new Float32Array(st));
    }
    return c.hmSaite;
  }
  function klavier(c, ziel, f, t, dauer, laut) {
    var fl = c.createBiquadFilter(), g = c.createGain();
    fl.type = 'lowpass'; fl.Q.value = 0.5;
    fl.frequency.setValueAtTime(Math.min(9000, f * 10), t); fl.frequency.exponentialRampToValueAtTime(Math.max(600, f * 2.5), t + 0.45);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(laut, t + 0.006);
    g.gain.exponentialRampToValueAtTime(laut * 0.42, t + 0.2); g.gain.exponentialRampToValueAtTime(laut * 0.09, t + dauer * 0.8);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dauer);
    [-2.5, 2.5].forEach(function (cent) {
      var o = c.createOscillator(); o.setPeriodicWave(saite(c)); o.frequency.value = f; o.detune.value = cent;
      o.connect(fl); o.start(t); o.stop(t + dauer + 0.05);
    });
    fl.connect(g); g.connect(ziel);
  }
  function midi(m) { return 440 * Math.pow(2, (m - 69) / 12); }

  /* Klavier für den Schluss von Fassung 4, als reiner Klang ohne Filter und Verzerrer: Jeder Ton wird einmal
     berechnet und dann wie eine Aufnahme abgespielt. Er besteht aus bis zu 16 Teiltönen, leicht gespreizt wie bei
     echten Saiten; die hohen sind leiser und verklingen schneller, jeder Ton hat zwei kaum gegeneinander
     verstimmte, ungleich laute Saiten (sonst löschen sie sich nach zwei Sekunden kurz aus) und einen kurzen, weichen Anschlag. Gerechnet wird mit einem Zeiger, der sich je Abtastwert
     ein Stück dreht (kein Sinus in der Schleife), damit auch ein Handy das nebenher schafft. */
  var FLUEGEL_SEK = 3.2;
  function fluegel(c, m) {
    var bank = c.hmFluegel || (c.hmFluegel = {});
    if (bank[m]) return bank[m];
    var sr = c.sampleRate, f0 = midi(m), n = Math.floor(sr * FLUEGEL_SEK), puffer = c.createBuffer(1, n, sr), x = puffer.getChannelData(0);
    var spreiz = 0.00005 * Math.pow(2, (m - 36) / 12), K = Math.max(4, Math.min(16, Math.floor(9000 / f0))), lage = 261.63 / f0;
    var t1 = 0.42 * Math.pow(lage, 0.35), t2 = 3 * Math.pow(lage, 0.5), k, s, i, spitze = 0;
    for (k = 1; k <= K; k++) {
      var fk = k * f0 * Math.sqrt(1 + spreiz * k * k);
      var a = Math.pow(k, -1.6) * Math.abs(Math.sin(k * Math.PI / 8.3)) * Math.exp(-fk / 4200);
      var d1 = Math.exp(-(1 + 0.3 * (k - 1)) / (sr * t1)), d2 = Math.exp(-(1 + 0.14 * (k - 1)) / (sr * t2));
      for (s = 0; s < 2; s++) {
        var w = 2 * Math.PI * fk * (s ? 1.00005 : 0.99995) / sr, cw = Math.cos(w), sw = Math.sin(w), re = 1, im = 0, st = s ? 0.33 : 0.67, a1 = a * 0.6 * st, a2 = a * 0.4 * st, r;
        for (i = 0; i < n; i++) {
          x[i] += im * (a1 + a2);
          r = re * cw - im * sw; im = re * sw + im * cw; re = r;
          a1 *= d1; a2 *= d2;
        }
      }
    }
    var an = Math.floor(sr * 0.0025), aus = Math.floor(sr * 0.06), tief = 0, hammer = Math.floor(sr * 0.03);
    for (i = 0; i < hammer; i++) { tief += 0.1 * (Math.random() * 2 - 1 - tief); x[i] += tief * 0.12 * Math.exp(-i / (sr * 0.007)); }   /* der Anschlag */
    for (i = 0; i < an; i++) x[i] *= 0.5 - 0.5 * Math.cos(Math.PI * i / an);
    for (i = 0; i < aus; i++) x[n - 1 - i] *= i / aus;
    for (i = 0; i < n; i++) if (Math.abs(x[i]) > spitze) spitze = Math.abs(x[i]);
    for (i = 0; i < n; i++) x[i] *= 0.9 / spitze;
    return (bank[m] = puffer);
  }
  function fluegelTon(c, ziel, m, t, dauer, laut) {
    var q = c.createBufferSource(), g = c.createGain();
    dauer = Math.min(dauer, FLUEGEL_SEK - 0.05);
    q.buffer = fluegel(c, m);
    g.gain.setValueAtTime(laut, t); g.gain.setValueAtTime(laut, t + dauer - 0.3); g.gain.linearRampToValueAtTime(0.0001, t + dauer);
    q.connect(g); g.connect(ziel); q.start(t); q.stop(t + dauer + 0.02);
  }
  /* Klavier aus Aufnahmen (Fassung 5): Töne eines echten Flügels, „Salamander Grand Piano V3“ von Alexander Holm,
     CC BY 3.0 (Quelle und Änderungen in klavier/QUELLE.txt, Namensnennung im Impressum). 14 Töne im Abstand kleiner
     Terzen liegen als MP3 auf dem eigenen Server; die Töne dazwischen entstehen, indem der Nachbarton einen Halbton
     schneller oder langsamer läuft. Geladen wird erst, wenn jemand die Glocke antippt. Fehlt eine Aufnahme (kein
     Netz, alter Browser), spielt an ihrer Stelle der berechnete Ton (fluegel). */
  var AUFNAHME = { 36: ['C2', 0], 43: ['Fs2', 1], 45: ['A2', 0], 48: ['C3', 0], 52: ['Ds3', 1], 53: ['Fs3', -1], 55: ['Fs3', 1], 57: ['A3', 0],
    59: ['C4', -1], 60: ['C4', 0], 64: ['Ds4', 1], 65: ['Fs4', -1], 72: ['C5', 0], 74: ['Ds5', -1], 76: ['Ds5', 1], 79: ['Fs5', 1], 84: ['C6', 0] };
  var aufnahmen = {}, laedt = false;
  function ladeKlavier(c) {
    if (laedt || !window.fetch) return;
    laedt = true;
    var namen = {}, m;
    for (m in AUFNAHME) namen[AUFNAHME[m][0]] = 1;
    Object.keys(namen).forEach(function (name) {
      fetch('/stil/weihnachten/klavier/' + name + '.mp3').then(function (r) { if (!r.ok) throw 0; return r.arrayBuffer(); }).then(function (daten) {
        c.decodeAudioData(daten, function (puffer) {
          var x = puffer.getChannelData(0), i = 0, n = Math.min(x.length, 4000);
          while (i < n && Math.abs(x[i]) < 0.004) i++;          /* die Stille überspringen, die das MP3-Format vorn anfügt */
          aufnahmen[name] = { puffer: puffer, ab: Math.max(0, i - 40) / puffer.sampleRate };
        }, function () {});
      }).catch(function () {});
    });
  }
  function klavierTon(c, ziel, m, t, dauer, laut) {
    var a = AUFNAHME[m], auf = a && aufnahmen[a[0]];
    if (!auf) { fluegelTon(c, ziel, m, t, dauer, laut * 0.4); return; }
    var q = c.createBufferSource(), g = c.createGain(), tempo = Math.pow(2, a[1] / 12);
    dauer = Math.min(dauer, (auf.puffer.duration - auf.ab) / tempo - 0.02);
    q.buffer = auf.puffer; q.playbackRate.value = tempo;
    g.gain.setValueAtTime(laut, t); g.gain.setValueAtTime(laut, t + dauer - 0.35); g.gain.linearRampToValueAtTime(0.0001, t + dauer);
    q.connect(g); g.connect(ziel); q.start(t, auf.ab); q.stop(t + dauer + 0.02);
  }

  /* ---------- Nur für den Drop (Fassung 2) ---------- */
  /* Verzerrer: rundet Spitzen weich ab; Bass und Bassdrum bekommen dadurch Obertöne und klingen auch
     auf kleinen Lautsprechern „fett“ */
  function kurve(staerke) {
    var n = 1024, k = new Float32Array(n), i;
    for (i = 0; i < n; i++) k[i] = Math.tanh(staerke * (i / (n - 1) * 2 - 1)) / Math.tanh(staerke);
    return k;
  }
  /* Das Werk des Drops, einmal je Abspielen: ein Bass (Sägezahn und Sinus) und ein Synthesizer aus drei leicht
     verstimmten Sägezähnen, die durchlaufen; dazu der Verzerrer der Bassdrum und die „Pumpe“, die Bass und
     Synthesizer auf jedem Schlag kurz leiser macht, damit die Bassdrum durchkommt */
  function werk(c, ziel, s) {
    if (s.werk) return s.werk;
    var w = {}, form = c.createWaveShaper(), aus = c.createGain();
    w.pumpe = c.createGain(); w.pumpe.connect(ziel);
    w.druck = c.createWaveShaper(); w.druck.curve = kurve(2.4); aus.gain.value = 0.5; w.druck.connect(aus); aus.connect(ziel);
    w.bo = c.createOscillator(); w.bo.type = 'sawtooth'; w.bs = c.createOscillator(); w.bs.type = 'sine';
    w.bf = c.createBiquadFilter(); w.bf.type = 'lowpass'; w.bf.Q.value = 6; w.bf.frequency.value = 300;
    form.curve = kurve(2); w.bg = c.createGain(); w.bg.gain.value = 0; w.bsg = c.createGain(); w.bsg.gain.value = 0;
    w.bo.connect(w.bf); w.bf.connect(form); form.connect(w.bg); w.bg.connect(w.pumpe); w.bs.connect(w.bsg); w.bsg.connect(w.pumpe);
    w.lf = c.createBiquadFilter(); w.lf.type = 'lowpass'; w.lf.Q.value = 1.5; w.lf.frequency.value = 2400;
    w.lg = c.createGain(); w.lg.gain.value = 0; w.lf.connect(w.lg); w.lg.connect(w.pumpe);
    w.lo = [-11, 0, 11].map(function (cent) { var o = c.createOscillator(); o.type = 'sawtooth'; o.detune.value = cent; o.connect(w.lf); return o; });
    [w.bo, w.bs].concat(w.lo).forEach(function (o) { o.start(); s.dauer.push(o); });
    return (s.werk = w);
  }
  function ein(g, t, dauer, laut, an) {           /* Hüllkurve eines Tons auf einem durchlaufenden Tongeber */
    g.setValueAtTime(0.0001, t); g.linearRampToValueAtTime(laut, t + an);
    g.setValueAtTime(laut, t + dauer * 0.7); g.linearRampToValueAtTime(0.0001, t + dauer);
  }
  function bassTon(w, f, t, dauer, laut, auf) {
    w.bo.frequency.setValueAtTime(f, t); w.bs.frequency.setValueAtTime(f, t);
    w.bf.frequency.setValueAtTime(auf, t); w.bf.frequency.exponentialRampToValueAtTime(260, t + dauer);
    ein(w.bg.gain, t, dauer, laut * BASS, 0.004); ein(w.bsg.gain, t, dauer, laut * SUB, 0.006);
  }
  function leadTon(w, f, t, dauer, laut) {
    w.lo.forEach(function (o) { o.frequency.setValueAtTime(f, t); });
    w.lf.frequency.setValueAtTime(5200, t); w.lf.frequency.exponentialRampToValueAtTime(1500, t + Math.min(dauer, 0.5));
    ein(w.lg.gain, t, dauer, laut, 0.008);
  }
  function pump(w, t) { w.pumpe.gain.setValueAtTime(0.25, t); w.pumpe.gain.linearRampToValueAtTime(1, t + 0.19); }
  /* Die Bassdrum des Drops: fällt tiefer, klingt länger, geht durch den Verzerrer und hat vorn einen Klick */
  function kickFett(c, w, ziel, t, laut) {
    var o = c.createOscillator(), g = c.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(230, t); o.frequency.exponentialRampToValueAtTime(58, t + 0.07); o.frequency.exponentialRampToValueAtTime(44, t + 0.3);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(laut, t + 0.003); g.gain.setValueAtTime(laut, t + 0.1); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.34);
    o.connect(g); g.connect(w.druck); o.start(t); o.stop(t + 0.38);
    zisch(c, ziel, t, 0.014, 0.12, 'highpass', 2500);
  }
  function fall(c, w, t) {                         /* der tiefe Ton, der beim Drop nach unten sackt */
    var o = c.createOscillator(), g = c.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(130, t); o.frequency.exponentialRampToValueAtTime(36, t + 0.9);
    huelle(g, t, 0.01, 0.5, 1.1);
    o.connect(g); g.connect(w.druck); o.start(t); o.stop(t + 1.15);
  }
  /* Aufbau vor dem Drop: Rauschen, das heller und lauter wird, und ein Ton, der nach oben zieht; beide brechen ab */
  function steiger(c, ziel, t, dauer) {
    var q = c.createBufferSource(), fl = c.createBiquadFilter(), g = c.createGain();
    q.buffer = rauschen(c); q.loop = true; fl.type = 'bandpass'; fl.Q.value = 1.4;
    fl.frequency.setValueAtTime(350, t); fl.frequency.exponentialRampToValueAtTime(9000, t + dauer);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(STEIGER, t + dauer); g.gain.linearRampToValueAtTime(0.0001, t + dauer + 0.012);
    q.connect(fl); fl.connect(g); g.connect(ziel); q.start(t); q.stop(t + dauer + 0.03);
  }
  function zieh(c, ziel, t, dauer) {
    var o = c.createOscillator(), fl = c.createBiquadFilter(), g = c.createGain();
    o.type = 'sawtooth'; o.frequency.setValueAtTime(98, t); o.frequency.exponentialRampToValueAtTime(784, t + dauer);
    fl.type = 'lowpass'; fl.frequency.value = 2600; fl.Q.value = 2;
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.09, t + dauer); g.gain.linearRampToValueAtTime(0.0001, t + dauer + 0.012);
    o.connect(fl); fl.connect(g); g.connect(ziel); o.start(t); o.stop(t + dauer + 0.03);
  }
  var BASS = 0.17, SUB = 0.14, LEAD = 0.1, STEIGER = 0.2;   /* Lautstärken im Drop */

  /* ---------- Das Lied ---------- */
  /* Tonleiter der Lichterkette: C-Dur ab c'' (523,25 Hz), von links nach rechts */
  function hoehe(stufe) { return 523.25 * Math.pow(2, ([0, 2, 4, 5, 7, 9, 11][stufe % 7] + 12 * Math.floor(stufe / 7)) / 12); }
  /* Jingle Bells (James Lord Pierpont, 1857, gemeinfrei), der Kehrreim: Stufe der Tonleiter (0 = C) und Dauer in Schlägen */
  var LIED = [[2, 1], [2, 1], [2, 2], [2, 1], [2, 1], [2, 2], [2, 1], [4, 1], [0, 1.5], [1, 0.5], [2, 4],
    [3, 1], [3, 1], [3, 1.5], [3, 0.5], [3, 1], [2, 1], [2, 1], [2, 0.5], [2, 0.5], [2, 1], [1, 1], [1, 1], [2, 1], [1, 2], [4, 2],
    [2, 1], [2, 1], [2, 2], [2, 1], [2, 1], [2, 2], [2, 1], [4, 1], [0, 1.5], [1, 0.5], [2, 4],
    [3, 1], [3, 1], [3, 1.5], [3, 0.5], [3, 1], [2, 1], [2, 1], [2, 0.5], [2, 0.5], [4, 1], [4, 1], [3, 1], [1, 1], [0, 4]];
  var HALB = 26;                                  /* die ersten 26 Töne sind die erste Hälfte (acht Takte) */
  var TEMPO = 136, SCHLAG = 60 / TEMPO;           /* Schläge in der Minute, Dauer eines Schlags in Sekunden */
  /* Akkorde: Basston und vier Töne für das Arpeggio */
  var AKKORD = { C: [130.81, [261.63, 329.63, 392.0, 523.25]], F: [174.61, [261.63, 349.23, 440.0, 523.25]], G: [196.0, [293.66, 392.0, 493.88, 587.33]] };
  var FOLGE = ['C', 'C', 'C', 'C', 'F', 'C', 'G', 'G', 'C', 'C', 'C', 'C', 'F', 'C', 'G', 'C'];   /* je Takt */
  var ARP = [0, 2, 1, 3, 2, 3, 1, 2, 0, 2, 1, 3, 3, 2, 1, 2];
  var ERSTE = 96;                                 /* 24 Takte: 8 klassisch, dann der ganze Kehrreim mit Beat */
  var DROP = 112;                                 /* Fassung 2: vier Takte Aufbau, auf diesem Schlag setzt der Drop ein */

  /* Der Ablauf als Liste: [Schlag, Funktion(ctx, ziel, Zeit, Zustand), Licht]. Licht: eine Stufe der Tonleiter,
     { p: Anteil der Kettenbreite } oder { takt: Nummer des Schlags } (dann blinkt jede zweite Lampe). */
  function ablauf(fassung) {
    var e = [], ende = ERSTE;
    function dazu(schlag, fn, licht) { e.push([schlag, fn, licht]); }
    function melodie(ab, noten) {
      var s = ab;
      noten.forEach(function (n) {
        var stufe = n[0], hier = s, lang = n[1];
        dazu(hier, function (c, z, t) {
          glocke(c, z, hoehe(stufe), t, 0.2);
          if (hier >= 64) {                         /* letzte acht Takte: Glanz eine Oktave höher, dazu eine Synthesizer-Stimme */
            glocke(c, z, hoehe(stufe) * 2, t, 0.05);
            synth(c, z, hoehe(stufe) / 2, t, Math.min(0.5, lang * 0.4), 0.045, 2600, 1100, 2, 'sawtooth');
          }
        }, stufe);
        s += lang;
      });
    }
    melodie(0, LIED.slice(0, HALB));               /* Takte 1 bis 8: klassisch, nur Glockenspiel */
    melodie(32, LIED);                             /* Takte 9 bis 24: der ganze Kehrreim */
    for (var takt = 0; takt < 24; takt++) (function (takt) {
      var a = AKKORD[FOLGE[takt < 8 ? takt : (takt - 8) % 16]], s0 = takt * 4, s, k;
      if (takt >= 4 && takt < 8) {                 /* Takte 5 bis 8: Der Bass setzt weich ein, leise Hi-Hats kommen dazu */
        for (s = 0; s < 4; s++) (function (s) {
          dazu(s0 + s, function (c, z, t) { synth(c, z, a[0], t, 0.34, 0.1 + 0.02 * (takt - 4), 520, 170, 3); });
          dazu(s0 + s + 0.5, function (c, z, t) { hihat(c, z, t, 0.035 + 0.015 * (takt - 4)); });
        })(s);
      }
      if (takt === 6) for (k = 0; k < 8; k++) (function (k) { dazu(s0 + k * 0.5, function (c, z, t) { clap(c, z, t, 0.05 + 0.012 * k); }); })(k);
      if (takt === 7) for (k = 0; k < 16; k++) (function (k) { dazu(s0 + k * 0.25, function (c, z, t) { clap(c, z, t, 0.1 + 0.012 * k); }); })(k);
      if (takt >= 8) {                             /* ab Takt 9: Bassdrum auf jedem Schlag, Clap auf 2 und 4, Bass und Hi-Hat dazwischen */
        for (s = 0; s < 4; s++) (function (s) {
          dazu(s0 + s, function (c, z, t) { kick(c, z, t, 0.6); });
          if (s % 2 === 1) dazu(s0 + s, function (c, z, t) { clap(c, z, t, 0.26); });
          dazu(s0 + s + 0.5, function (c, z, t) {
            synth(c, z, a[0], t, 0.2, 0.2, 1500, 240, 7);
            hihat(c, z, t, 0.11, takt >= 16 && s === 3);
          });
          if (takt >= 16) {                        /* ab Takt 17: schnelle leise Hi-Hats und ein Arpeggio über dem Akkord */
            dazu(s0 + s + 0.25, function (c, z, t) { hihat(c, z, t, 0.04); });
            dazu(s0 + s + 0.75, function (c, z, t) { hihat(c, z, t, 0.04); });
            for (k = 0; k < 4; k++) (function (k) {
              var f = a[1][ARP[s * 4 + k]];
              dazu(s0 + s + k * 0.25, function (c, z, t) { synth(c, z, f, t, 0.1, 0.04, 3000, 900, 3, 'square'); });
            })(k);
          }
        })(s);
      }
    })(takt);
    if (fassung === 2) ende = drop(dazu);
    else if (fassung === 3) ende = drop3(dazu);
    else if (fassung === 4) ende = drop4(dazu);
    else if (fassung === 5) ende = drop5(dazu);
    else dazu(ERSTE, function (c, z, t) {          /* Schluss: ein Schlag und ein C-Dur-Akkord aus Glocken */
      kick(c, z, t, 0.6); [0, 2, 4, 7].forEach(function (st) { glocke(c, z, hoehe(st), t, 0.16); });
    });
    e.sort(function (x, y) { return x[0] - y[0]; });
    return { liste: e, ende: ende };
  }

  /* ---------- Bausteine für Aufbau und Drop ---------- */
  function wirbel(dazu, ab, bis, schritt, l0, l1) {    /* Trommelwirbel, der lauter wird */
    var n = Math.round((bis - ab) / schritt), i;
    for (i = 0; i < n; i++) (function (i) { dazu(ab + i * schritt, function (c, z, t) { trommel(c, z, t, l0 + (l1 - l0) * i / n); }); })(i);
  }
  /* Ein Takt des Drops ab Schlag s0 (nr: Nummer des Takts im Kehrreim): stampfende Bassdrum, Clap auf 2 und 4,
     rollender Bass auf den drei Sechzehnteln zwischen den Schlägen, Hi-Hats (offen auf dem „und“); mit arp dazu das
     Arpeggio, mit fuell auf dem letzten Schlag ein Wirbel statt der Bassdrum */
  function takt(dazu, s0, nr, arp, fuell) {
    var a = AKKORD[FOLGE[nr]], tief = a[0] / 2, s;
    for (s = 0; s < 4; s++) (function (s) {
      if (!(fuell && s === 3)) {
        dazu(s0 + s, function (c, z, t, st) { var w = werk(c, z, st); kickFett(c, w, z, t, 1); pump(w, t); }, { takt: nr * 4 + s });
        if (s % 2 === 1) dazu(s0 + s, function (c, z, t) { clap(c, z, t, 0.3); zisch(c, z, t, 0.16, 0.09, 'highpass', 3500); });
      }
      dazu(s0 + s + 0.25, function (c, z, t, st) { bassTon(werk(c, z, st), tief, t, 0.095, 0.8, 900); hihat(c, z, t, 0.045); });
      dazu(s0 + s + 0.5, function (c, z, t, st) { bassTon(werk(c, z, st), tief, t, 0.095, 1, 2600); hihat(c, z, t, 0.13, true); });
      dazu(s0 + s + 0.75, function (c, z, t, st) { bassTon(werk(c, z, st), s % 2 ? tief * 2 : tief, t, 0.095, 0.8, 1500); hihat(c, z, t, 0.045); });
      if (arp) for (var k = 0; k < 4; k++) (function (k) {
        var f = a[1][ARP[s * 4 + k]];
        dazu(s0 + s + k * 0.25, function (c, z, t, st) { synth(c, werk(c, z, st).pumpe, f, t, 0.1, 0.045, 3000, 900, 3, 'square'); });
      })(k);
    })(s);
  }

  /* Fassung 2: Nach dem Kehrreim hört das Lied nicht auf. Vier Takte Aufbau über G (die Bassdrum schweigt,
     Glocken laufen nach oben, ein Wirbel wird immer schneller, ein Ton zieht hoch, dann ein halber Schlag Stille),
     danach der Drop: der ganze Kehrreim noch einmal, mit stampfender Bassdrum, rollendem tiefen Bass, offenen
     Hi-Hats und der Melodie eine Oktave tiefer auf dem Synthesizer; die Lichterkette blinkt im Takt. */
  function drop(dazu) {
    var k, nr, sch;
    /* Takte 25 und 26: Schlussakkord der ersten Runde, dann wird es leise: Glocken zerlegen G7, darunter ein liegender Bass */
    dazu(ERSTE, function (c, z, t) {
      kick(c, z, t, 0.6); becken(c, z, t, 0.14); [0, 2, 4, 7].forEach(function (st) { glocke(c, z, hoehe(st), t, 0.16); });
      steiger(c, z, t, (DROP - 0.5 - ERSTE) * SCHLAG);
    });
    for (k = 0; k < 14; k++) (function (k) {
      var st = [4, 6, 8, 10][k % 4];
      dazu(ERSTE + 1 + k * 0.5, function (c, z, t) { glocke(c, z, hoehe(st), t, 0.08 + 0.006 * k); }, { p: 0.25 + (k % 4) / 6 });
    })(k);
    dazu(ERSTE, function (c, z, t) { synth(c, z, 98, t, 1.6, 0.13, 420, 150, 3); });
    dazu(ERSTE + 4, function (c, z, t) { synth(c, z, 98, t, 1.6, 0.14, 520, 150, 3); });
    for (k = 0; k < 4; k++) (function (k) { dazu(ERSTE + 4 + k, function (c, z, t) { clap(c, z, t, 0.08 + 0.02 * k); }); })(k);
    /* Takte 27 und 28: Der Wirbel wird schneller, die Glocken laufen die Tonleiter hoch, der Bass pocht */
    wirbel(dazu, ERSTE + 8, ERSTE + 12, 0.5, 0.1, 0.18); wirbel(dazu, ERSTE + 12, ERSTE + 14, 0.25, 0.16, 0.24); wirbel(dazu, ERSTE + 14, DROP - 0.5, 0.125, 0.18, 0.32);
    dazu(ERSTE + 8, function (c, z, t) { zieh(c, z, t, 7.5 * SCHLAG); });
    for (k = 0; k < 15; k++) (function (k) { dazu(ERSTE + 8 + k * 0.5, function (c, z, t) { synth(c, z, 98, t, 0.18, 0.12 + 0.006 * k, 500 + 150 * k, 240, 4); }); })(k);
    for (k = 0; k < 22; k++) (function (k) {
      var st = k < 8 ? k : k - 7, wann = k < 8 ? ERSTE + 8 + k * 0.5 : ERSTE + 12 + (k - 8) * 0.25;
      dazu(wann, function (c, z, t) { glocke(c, z, hoehe(st), t, 0.1 + 0.002 * k); }, { p: k / 21 });
    })(k);
    /* Der Drop */
    dazu(DROP, function (c, z, t, s) { fall(c, werk(c, z, s), t); becken(c, z, t, 0.2); });
    sch = DROP;
    LIED.forEach(function (n) {
      var stufe = n[0], lang = n[1], hier = sch;
      dazu(hier, function (c, z, t, s) {
        var spaet = hier >= DROP + 32;
        leadTon(werk(c, z, s), hoehe(stufe) / 2, t, lang * SCHLAG * 0.88, LEAD);
        glocke(c, z, hoehe(stufe), t, spaet ? 0.2 : 0.15);
        if (spaet) glocke(c, z, hoehe(stufe) * 2, t, 0.045);
      }, stufe);
      sch += lang;
    });
    for (nr = 0; nr < 16; nr++) takt(dazu, DROP + nr * 4, nr, nr >= 8, nr === 7);   /* in der zweiten Hälfte mit Arpeggio */
    wirbel(dazu, DROP + 31, DROP + 32, 0.25, 0.2, 0.32);
    dazu(DROP + 32, function (c, z, t) { becken(c, z, t, 0.18); });
    dazu(DROP + 64, function (c, z, t, s) {        /* Schluss: ein letzter Schlag, Becken, tiefer Bass und der C-Dur-Akkord aus Glocken */
      var w = werk(c, z, s);
      kickFett(c, w, z, t, 0.9); becken(c, z, t, 0.18); bassTon(w, 65.41, t, 1.3, 0.8, 1800); leadTon(w, 261.63, t, 1.3, LEAD * 0.8);
      [0, 2, 4, 7].forEach(function (st) { glocke(c, z, hoehe(st), t, 0.15); });
    });
    return DROP + 64;
  }

  /* Fassung 3, die Grundfassung (Patrick 28.11.2026, auf Fassung 2 aufgebaut): Der Aufbau ist kürzer (zehn Schläge,
     gut vier Sekunden). Der Drop läuft nur einmal durch die erste Hälfte des Kehrreims (acht Takte, in den letzten
     vier mit Arpeggio) und endet mit einem Schlag. Nach kurzem Atemholen spielt ein Klavier allein, etwas langsamer
     und zum Ende hin ruhiger werdend, „Jingle bells, jingle bells, jingle all the way“ und schließt mit E, D, C;
     ganz am Ende erklingt noch einmal der Akkord der Glöckchen als Schlusszeichen. */
  var DROP3 = 106, KLAVIER = 140;
  function ort(b) { var x = Math.max(0, b - 12); return KLAVIER + 1.1 * b + 0.03125 * x * x; }   /* Schlag des Klaviers -> Schlag des Lieds */
  /* rechte Hand: Schlag, Ton (MIDI), Dauer in Schlägen, Stufe für das Licht; linke Hand: Schlag, Ton */
  var RECHTS = [[0, 76, 1, 2], [1, 76, 1, 2], [2, 76, 2, 2], [4, 76, 1, 2], [5, 76, 1, 2], [6, 76, 2, 2],
    [8, 76, 1, 2], [9, 79, 1, 4], [10, 72, 1.5, 0], [11.5, 74, 0.5, 1], [12, 76, 2, 2], [14, 74, 2, 1], [16, 72, 4, 0]];
  var LINKS = [[0, 48], [1, 55], [2, 64], [3, 55], [4, 45], [5, 52], [6, 60], [7, 52], [8, 52], [9, 60], [10, 53], [11, 57],
    [12, 43], [13, 60], [13, 64], [14, 43], [15, 59], [15, 65], [16, 36], [16, 48], [16.1, 60], [16.2, 64], [16.3, 67]];
  function grund(dazu) {                          /* Aufbau und Drop, gemeinsam für die Fassungen 3 und 4 */
    var k, nr, sch;
    /* Aufbau: Schlussakkord der ersten Runde, ein Takt Glocken über G7, dann Wirbel, Lauf nach oben, ein halber Schlag Stille */
    dazu(ERSTE, function (c, z, t) {
      kick(c, z, t, 0.6); becken(c, z, t, 0.14); [0, 2, 4, 7].forEach(function (st) { glocke(c, z, hoehe(st), t, 0.16); });
      steiger(c, z, t, (DROP3 - 0.5 - ERSTE) * SCHLAG); synth(c, z, 98, t, 1.6, 0.13, 420, 150, 3);
    });
    for (k = 0; k < 6; k++) (function (k) {
      var st = [4, 6, 8, 10][k % 4];
      dazu(ERSTE + 1 + k * 0.5, function (c, z, t) { glocke(c, z, hoehe(st), t, 0.09 + 0.01 * k); }, { p: 0.25 + (k % 4) / 6 });
    })(k);
    dazu(ERSTE + 2, function (c, z, t) { clap(c, z, t, 0.09); });
    dazu(ERSTE + 3, function (c, z, t) { clap(c, z, t, 0.12); });
    wirbel(dazu, ERSTE + 4, ERSTE + 6, 0.5, 0.1, 0.18); wirbel(dazu, ERSTE + 6, ERSTE + 8, 0.25, 0.16, 0.24); wirbel(dazu, ERSTE + 8, DROP3 - 0.5, 0.125, 0.18, 0.32);
    dazu(ERSTE + 4, function (c, z, t) { zieh(c, z, t, 5.5 * SCHLAG); });
    for (k = 0; k < 11; k++) (function (k) { dazu(ERSTE + 4 + k * 0.5, function (c, z, t) { synth(c, z, 98, t, 0.18, 0.12 + 0.008 * k, 500 + 200 * k, 240, 4); }); })(k);
    for (k = 0; k < 18; k++) (function (k) {
      var st = k < 4 ? k : k - 3, wann = k < 4 ? ERSTE + 4 + k * 0.5 : ERSTE + 6 + (k - 4) * 0.25;
      dazu(wann, function (c, z, t) { glocke(c, z, hoehe(st), t, 0.1 + 0.002 * k); }, { p: k / 17 });
    })(k);
    /* Der Drop: acht Takte, die erste Hälfte des Kehrreims */
    dazu(DROP3, function (c, z, t, s) { fall(c, werk(c, z, s), t); becken(c, z, t, 0.2); });
    sch = DROP3;
    LIED.slice(0, HALB).forEach(function (n) {
      var stufe = n[0], lang = n[1], hier = sch;
      dazu(hier, function (c, z, t, s) {
        var spaet = hier >= DROP3 + 16;
        leadTon(werk(c, z, s), hoehe(stufe) / 2, t, lang * SCHLAG * 0.88, LEAD);
        glocke(c, z, hoehe(stufe), t, spaet ? 0.2 : 0.15);
        if (spaet) glocke(c, z, hoehe(stufe) * 2, t, 0.045);
      }, stufe);
      sch += lang;
    });
    for (nr = 0; nr < 8; nr++) takt(dazu, DROP3 + nr * 4, nr, nr >= 4, false);
  }
  function drop3(dazu) {
    grund(dazu);
    wirbel(dazu, DROP3 + 31, DROP3 + 32, 0.25, 0.14, 0.26);
    dazu(DROP3 + 32, function (c, z, t, s) {       /* ein letzter Schlag mit Becken und tiefem C; danach schweigen Bass und Synthesizer */
      var w = werk(c, z, s);
      kickFett(c, w, z, t, 0.9); becken(c, z, t, 0.18); bassTon(w, 65.41, t, 1.2, 0.8, 1800); leadTon(w, 261.63, t, 1, LEAD * 0.7);
      s.dauer.forEach(function (o) { try { o.stop(t + 1.5); } catch (e) {} });
    }, { takt: 32 });
    /* Das Klavier allein */
    RECHTS.forEach(function (n) {
      var dauer = n[0] === 16 ? 3.6 : (ort(n[0] + n[2]) - ort(n[0])) * SCHLAG + 0.9;
      dazu(ort(n[0]), function (c, z, t) { klavier(c, z, midi(n[1]), t, dauer, KLAVIER_R); }, n[3]);
    });
    LINKS.forEach(function (n) {
      dazu(ort(n[0]), function (c, z, t) { klavier(c, z, midi(n[1]), t, n[0] >= 16 ? 3.6 : 1.5, n[1] < 46 ? KLAVIER_L * 1.3 : KLAVIER_L); });
    });
    [0, 2, 4, 7].forEach(function (st) { dazu(ort(18), function (c, z, t) { glocke(c, z, hoehe(st), t, 0.15); }, st); });   /* das Glöckchen zum Schluss */
    return ort(18) + 3;
  }
  var KLAVIER_R = 0.13, KLAVIER_L = 0.06;          /* Lautstärke der rechten und der linken Hand */

  /* Fassung 4, die Grundfassung (Patrick 28.11.2026 zu Fassung 3: der Übergang „direkter“, ohne „Klang dazwischen“;
     die ruhige Phase „nahezu reines Klavier“, „Classic, Piano, reiner Klang, nicht verzerrt“, weniger Töne; nach dem
     „Bing“ am Ende noch ein tieferer Akkord). Aufbau und Drop wie in Fassung 3. Der Drop endet mit seinem letzten
     Takt, ohne Wirbel und ohne Schlussschlag; auf dem nächsten Schlag beginnt das Klavier allein (berechnete Töne,
     fluegel), die linke Hand nur noch mit einem Basston und einem Akkord je Takt. Am Ende das Glöckchen und danach
     ein tiefer C-Dur-Akkord auf dem Klavier. */
  var KLAVIER4 = DROP3 + 32;
  function ort4(b) { var x = Math.max(0, b - 12); return KLAVIER4 + 1.1 * b + 0.03125 * x * x; }
  var LINKS4 = [[0, 48], [2, 55], [2, 64], [4, 45], [6, 52], [6, 60], [8, 52], [10, 53], [10, 57],
    [12, 43], [12, 60], [14, 55], [14, 59], [14, 65], [16, 48], [16, 55], [16, 64]];
  var SCHLUSS4 = [36, 43, 48, 52, 55, 60];        /* C, G, c, e, g, c': von unten nach oben leicht gebrochen */
  var FLUEGEL_R = 0.2, FLUEGEL_L = 0.11, FLUEGEL_S = 0.18;
  function toene4() {                             /* alle Töne, die das Klavier braucht (zum Vorausberechnen) */
    var t = {}, i;
    for (i = 0; i < RECHTS.length; i++) t[RECHTS[i][1]] = 1;
    for (i = 0; i < LINKS4.length; i++) t[LINKS4[i][1]] = 1;
    for (i = 0; i < SCHLUSS4.length; i++) t[SCHLUSS4[i]] = 1;
    return Object.keys(t).map(Number);
  }
  function drop4(dazu) {
    grund(dazu);
    dazu(KLAVIER4, function (c, z, t, s) { s.dauer.forEach(function (o) { try { o.stop(t + 0.2); } catch (e) {} }); });   /* Bass und Synthesizer schweigen */
    RECHTS.forEach(function (n) {
      var dauer = n[0] === 16 ? 3.1 : (ort4(n[0] + n[2]) - ort4(n[0])) * SCHLAG + 1.2;
      dazu(ort4(n[0]), function (c, z, t) { fluegelTon(c, z, n[1], t, dauer, FLUEGEL_R); }, n[3]);
    });
    LINKS4.forEach(function (n) { dazu(ort4(n[0]), function (c, z, t) { fluegelTon(c, z, n[1], t, n[0] >= 16 ? 3.1 : 2.4, FLUEGEL_L); }); });
    [0, 2, 4, 7].forEach(function (st) { dazu(ort4(18), function (c, z, t) { glocke(c, z, hoehe(st), t, 0.14); }, st); });      /* das „Bing“ */
    SCHLUSS4.forEach(function (m, i) { dazu(ort4(19.5) + i * 0.09, function (c, z, t) { fluegelTon(c, z, m, t, 3.1, FLUEGEL_S); }); });   /* der tiefe Schlussakkord */
    return ort4(19.5) + 4;
  }

  /* Fassung 5, die Grundfassung (Patrick 28.11.2026 zu Fassung 4: das Klavier klinge „immer noch ziemlich künstlich“
     und „ein bisschen verzerrt“; mit echten Klaviertönen werde es „noch ein bisschen klarer und ruhiger“): alles wie
     Fassung 4, aber das Klavier spielt Aufnahmen eines echten Flügels (klavierTon) und geht am Begrenzer vorbei
     direkt zum Lautsprecher (zustand.rein), damit nichts mehr am Klang zieht. */
  var AUFN_R = 0.5, AUFN_L = 0.3, AUFN_B = 0.32, AUFN_S = 0.36;   /* Lautstärke: rechte Hand, linke Hand, „Bing“, Schlussakkord */
  function drop5(dazu) {
    grund(dazu);
    dazu(KLAVIER4, function (c, z, t, s) { s.dauer.forEach(function (o) { try { o.stop(t + 0.2); } catch (e) {} }); });
    RECHTS.forEach(function (n) {
      var dauer = n[0] === 16 ? 3.5 : (ort4(n[0] + n[2]) - ort4(n[0])) * SCHLAG + 1.4;
      dazu(ort4(n[0]), function (c, z, t, s) { klavierTon(c, s.rein || z, n[1], t, dauer, AUFN_R); }, n[3]);
    });
    LINKS4.forEach(function (n) { dazu(ort4(n[0]), function (c, z, t, s) { klavierTon(c, s.rein || z, n[1], t, n[0] >= 16 ? 3.5 : 2.6, AUFN_L); }); });
    /* das „Bing“: derselbe helle Akkord wie bisher bei den Glöckchen, jetzt auch auf dem Klavier (Patrick 28.11.2026:
       am Ende „nur noch Klavier“); die Lichter leuchten wie bei den Glöckchen mit */
    [72, 76, 79, 84].forEach(function (m, i) { dazu(ort4(18) + i * 0.04, function (c, z, t, s) { klavierTon(c, s.rein || z, m, t, 3.2, AUFN_B); }, [0, 2, 4, 7][i]); });
    SCHLUSS4.forEach(function (m, i) { dazu(ort4(19.5) + i * 0.09, function (c, z, t, s) { klavierTon(c, s.rein || z, m, t, 3.5, AUFN_S); }); });
    return ort4(19.5) + 4;
  }

  /* ---------- Lichterkette und Glocke ---------- */
  var knopf = null, spielt = null;
  function zonen() { return Math.max(8, Math.min(15, Math.floor(kette.clientWidth / 44))); }
  function zone(e) {
    var ort = kette.getBoundingClientRect(), n = zonen();
    return Math.max(0, Math.min(n - 1, Math.floor((e.clientX - ort.left) / ort.width * n)));
  }
  function an(led, ms) { led.classList.add('w-an'); setTimeout(function () { led.classList.remove('w-an'); }, ms); }
  function leuchte(z) {                            /* Die LEDs einer Zone leuchten kurz auf */
    var W = kette.clientWidth, n = zonen(), l = kette.children;
    for (var i = 0; i < l.length; i++) {
      var x = parseFloat(l[i].style.left);
      if (x >= z * W / n && x < (z + 1) * W / n) an(l[i], 260);
    }
  }
  function licht(L) {                              /* Licht zu einem Ton des Lieds (siehe ablauf) */
    if (typeof L === 'number') leuchte(L);
    else if (L.p !== undefined) leuchte(Math.round(L.p * (zonen() - 1)));
    else if (!ruhig) for (var l = kette.children, i = L.takt % 2; i < l.length; i += 2) an(l[i], 110);
  }
  function schlage(z) { var ctx = audio(); glocke(ctx, haupt, hoehe(z), ctx.currentTime + 0.01, 0.22); leuchte(z); }

  function liedAus() {
    if (!spielt) return;
    clearInterval(spielt.takt);
    for (var i = 0; i < spielt.uhren.length; i++) clearTimeout(spielt.uhren[i]);
    var tor = spielt.tor, dauer = spielt.zustand.dauer, rein = spielt.zustand.rein; spielt = null;
    try { tor.gain.setTargetAtTime(0, ton.currentTime, 0.04); rein.gain.setTargetAtTime(0, ton.currentTime, 0.04); } catch (e) {}
    setTimeout(function () {
      try { tor.disconnect(); rein.disconnect(); } catch (e) {}
      dauer.forEach(function (o) { try { o.stop(); } catch (e) {} });
    }, 600);
    if (knopf) { knopf.classList.remove('w-laeutet'); knopf.setAttribute('aria-label', 'Jingle Bells abspielen'); }
  }
  function liedAn() {
    var ctx = audio(), tor = ctx.createGain(); tor.connect(haupt);
    var rein = ctx.createGain(); rein.connect(ctx.destination);                /* am Begrenzer vorbei: für das Klavier aus Aufnahmen */
    var plan = ablauf(FASSUNG), e = plan.liste, t0 = ctx.currentTime + 0.12, i = 0, uhren = [], zustand = { dauer: [], rein: rein }, takt;
    function vor() {                               /* legt nur an, was in der nächsten Drittelsekunde erklingt */
      var bis = ctx.currentTime + (d.hidden ? 1.6 : 0.35);
      while (i < e.length && t0 + e[i][0] * SCHLAG < bis) {
        var wann = t0 + e[i][0] * SCHLAG;
        e[i][1](ctx, tor, wann, zustand);
        if (e[i][2] !== undefined) (function (L) { uhren.push(setTimeout(function () { licht(L); }, Math.max(0, (wann - ctx.currentTime) * 1000))); })(e[i][2]);
        i++;
      }
      if (i >= e.length) { clearInterval(takt); uhren.push(setTimeout(liedAus, Math.max(0, (t0 + (plan.ende + 4) * SCHLAG - ctx.currentTime) * 1000))); }
    }
    takt = setInterval(vor, 60);
    spielt = { tor: tor, takt: takt, uhren: uhren, zustand: zustand };
    vor();
    if (FASSUNG === 5) ladeKlavier(ctx);                        /* die Aufnahmen des Flügels holen (einmal) */
    if (FASSUNG === 4) toene4().forEach(function (m, nr) {      /* die Klaviertöne nach und nach vorausberechnen */
      uhren.push(setTimeout(function () { fluegel(ctx, m); }, 1500 + nr * 280));
    });
    knopf.classList.add('w-laeutet'); knopf.setAttribute('aria-label', 'Jingle Bells anhalten');
  }

  oben.className += ' w-klang';
  kette.addEventListener('click', function (e) { schlage(zone(e)); });
  /* Mit der Maus über die Lichter streichen: Jede neue Zone erklingt. Wer nur zur Leiste des Browsers hochfährt,
     wechselt keine Zone und löst nichts aus. Vor dem ersten Klick auf die Seite lässt der Browser keinen Ton zu. */
  var letzte = -1;
  d.addEventListener('pointerdown', function entsperren() { audio(); d.removeEventListener('pointerdown', entsperren); });
  kette.addEventListener('pointerleave', function () { letzte = -1; });
  kette.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse' || !ton || ton.state !== 'running') return;
    var z = zone(e);
    if (letzte === -1) { letzte = z; return; }
    if (z !== letzte) { letzte = z; schlage(z); }
  });

  /* Nur auf der Startseite: die Glocke in der Mitte der Girlande */
  if (!/^\/(index\.html)?$/.test(location.pathname)) return;
  knopf = d.createElement('button'); knopf.type = 'button'; knopf.className = 'w-glocke'; knopf.setAttribute('aria-label', 'Jingle Bells abspielen');
  knopf.innerHTML = '<svg width="24" height="30" viewBox="0 0 24 30" aria-hidden="true"><defs><linearGradient id="w-gold" x1="0" x2="1" y1="0" y2="0">'
    + '<stop offset="0" stop-color="#F8DC8A"/><stop offset=".5" stop-color="#E3B341"/><stop offset="1" stop-color="#B8891F"/></linearGradient></defs>'
    + '<path d="M12,0 V6" stroke="#D63A2F" stroke-width="1.6"/>'
    + '<path d="M12,7 C7.6,7 6.2,11 6.2,15.4 C6.2,19.4 4.8,21.4 3.4,22.8 H20.6 C19.2,21.4 17.8,19.4 17.8,15.4 C17.8,11 16.4,7 12,7 Z" fill="url(#w-gold)"/>'
    + '<path d="M9.2,10.4 C8,12.4 7.8,15.2 8,18" stroke="#FFF6D2" stroke-width="1.2" stroke-linecap="round" fill="none" opacity=".85"/>'
    + '<rect x="2.6" y="22" width="18.8" height="2.8" rx="1.4" fill="#C9961F"/><circle cx="12" cy="26.8" r="2.1" fill="#B8891F"/>'
    + '<path d="M12,6.4 C8.6,3 5.4,4 6,6.4 C6.6,8.6 10,8 12,6.4 Z M12,6.4 C15.4,3 18.6,4 18,6.4 C17.4,8.6 14,8 12,6.4 Z" fill="#D63A2F" stroke="#8E1B1B" stroke-width=".5"/>'
    + '<circle cx="12" cy="6.4" r="1.3" fill="#E0453A" stroke="#8E1B1B" stroke-width=".5"/></svg>';
  knopf.addEventListener('click', function (e) { e.stopPropagation(); if (spielt) liedAus(); else liedAn(); });
  oben.appendChild(knopf);
})();
