#!/usr/bin/env python3
"""Bilder der Weihnachtszeit (Saison, siehe CLAUDE.md): erzeugt alles in stil/weihnachten/.

Aufruf im Hauptordner:  python3 _werkzeuge/weihnachten/bilder.py
Braucht playwright (pip install playwright) und einen Chrome (/usr/bin/google-chrome) für die
drei PNG-Kacheln; die SVG-Dateien schreibt das Skript selbst.

  girlande.png      Tannengirlande, kachelbar (350 x 36), liegt am oberen Rand jeder Seite
  kranz.png         Tannengrün vor den Füßen der vier Adventskerzen (124 x 20)
  schnee.png        Schneeflocken, kachelbar (420 x 560)
  schneedecke.svg   Schnee auf der ersten Kachel einer Seite, kachelbar (200 x 24)
  figur-*.svg       kleine Figuren, die auf der ersten Kachel unter einer Überschrift sitzen

Die drei Kugeln an der ersten Kachel zeichnet saison.js selbst.

Ändert sich ein Bild, bekommt es einen neuen Dateinamen (oder ?v=2 in saison.css und saison.js):
Die Browser halten Bilder lange im Zwischenspeicher.
"""
import asyncio, math, pathlib

ZIEL = pathlib.Path(__file__).resolve().parent.parent.parent / 'stil' / 'weihnachten'

PNG_SEITE = r'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}div{line-height:0}svg{display:block}</style></head><body>
<div id="girlande"></div><div id="kranz"></div><div id="schnee"></div>
<script>
var NS='http://www.w3.org/2000/svg';
function el(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
var seed=11;function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
var GRUEN=[[['#123A22','#17472A'],1.7],[['#1F5D2B','#2A7332'],1.5],[['#35873A','#4A9B46'],1.3]];
function beere(svg,x,y,r){el('circle',{cx:x,cy:y,r:r,fill:'#C62828'},svg);el('circle',{cx:x-r*0.3,cy:y-r*0.33,r:r*0.3,fill:'#fff',opacity:'.6'},svg)}

/* Girlande: zwei Bögen je Kachel, Aufhängung in der Kachelmitte (dort sitzen auf der Seite die Kerzen) */
(function(){
  var TW=350,H=36,seg=175,sag=10,y0=2;seed=11;
  function T(x){return (((x%seg)+seg)%seg)/seg}
  function Y(x){var t=T(x);return y0+sag*(1-(2*t-1)*(2*t-1))}
  function A(x){var t=T(x);return Math.atan(sag*(-2*(2*t-1))*2/seg)}
  var svg=el('svg',{width:TW,height:H,viewBox:'0 0 '+TW+' '+H},document.getElementById('girlande'));
  var linien=[],lang=[[9,16,2.3],[8,13,2.9],[6,10,4.1]];
  GRUEN.forEach(function(L,i){for(var x=0;x<TW;x+=lang[i][2]){var y=Y(x),a=A(x);for(var s=-1;s<=1;s+=2){
    var w=a+s*(0.45+rnd()*0.95)+(rnd()<0.5?0:Math.PI),len=lang[i][0]+rnd()*(lang[i][1]-lang[i][0]);var ey=y+Math.sin(w)*len;if(ey<-1)ey=-1;
    linien.push([x,y,x+Math.cos(w)*len,ey,L[0][rnd()<0.5?0:1],L[1]]);}}});
  [-TW,0,TW].forEach(function(o){
    var g=el('g',{'stroke-linecap':'round',fill:'none',transform:'translate('+o+',0)'},svg);
    if(o===0){var p='';for(var x=-4;x<=TW+4;x+=4)p+=(p?'L':'M')+x+','+Y(x).toFixed(1);el('path',{d:p,stroke:'#143D22','stroke-width':'3'},g);}
    linien.forEach(function(l){el('line',{x1:l[0].toFixed(1),y1:l[1].toFixed(1),x2:l[2].toFixed(1),y2:l[3].toFixed(1),stroke:l[4],'stroke-width':l[5]},g)});
  });
  [[31.5,1.2],[98.8,4.1],[233.4,3.3],[300.7,2.2]].forEach(function(b){beere(svg,b[0],(Y(b[0])+2+b[1]).toFixed(1),3)});
})();

/* Tannengrün des Adventskranzes: ein dichtes, flaches Polster, an den Enden auslaufend */
(function(){
  var W=124,H=20;seed=23;
  var svg=el('svg',{width:W,height:H,viewBox:'0 0 '+W+' '+H},document.getElementById('kranz'));
  function yc(x){return 12-2.5*Math.sin(Math.PI*(x-6)/112)}
  var g=el('g',{'stroke-linecap':'round',fill:'none'},svg);
  var p='';for(var x=10;x<=114;x+=4)p+=(p?'L':'M')+x+','+yc(x).toFixed(1);el('path',{d:p,stroke:'#143D22','stroke-width':'5'},g);
  var lang=[[6,10,1.9],[5,9,2.4],[4,7,3.3]];
  GRUEN.forEach(function(L,i){for(var x=6;x<=118;x+=lang[i][2]){var f=Math.min(1,(x-2)/16,(122-x)/16),y=yc(x);for(var s=-1;s<=1;s+=2){
    var w=s*(0.5+rnd()*1.0)+(rnd()<0.5?0:Math.PI),len=(lang[i][0]+rnd()*(lang[i][1]-lang[i][0]))*(0.55+0.45*f);
    var ey=Math.max(0.6,Math.min(H-0.6,y+Math.sin(w)*len));
    el('line',{x1:x.toFixed(1),y1:y.toFixed(1),x2:(x+Math.cos(w)*len).toFixed(1),y2:ey.toFixed(1),stroke:L[0][rnd()<0.5?0:1],'stroke-width':L[1]},g);}}});
  [[15,13],[38,11.5],[86,11.5],[109,13]].forEach(function(b){beere(svg,b[0],b[1],2.6)});
  /* rote Schleife in der Mitte */
  var s=el('g',{},svg);
  el('path',{d:'M62,11 C56,5 50,6 51,10.5 C52,14.5 58,13.5 62,11 Z',fill:'#D63A2F',stroke:'#8E1B1B','stroke-width':'.7'},s);
  el('path',{d:'M62,11 C68,5 74,6 73,10.5 C72,14.5 66,13.5 62,11 Z',fill:'#D63A2F',stroke:'#8E1B1B','stroke-width':'.7'},s);
  el('path',{d:'M61,11.5 L56.5,19 L59.5,18 L61.5,19.5 Z M63,11.5 L67.5,19 L64.5,18 L62.5,19.5 Z',fill:'#C62828',stroke:'#8E1B1B','stroke-width':'.6'},s);
  el('circle',{cx:62,cy:11.2,r:2.3,fill:'#E0453A',stroke:'#8E1B1B','stroke-width':'.7'},s);
})();

/* Schnee */
(function(){
  seed=5;var SW=420,SH=560;var svg=el('svg',{width:SW,height:SH,viewBox:'0 0 '+SW+' '+SH},document.getElementById('schnee'));
  for(var i=0;i<22;i++){var x=rnd()*SW,y=rnd()*SH,r=0.9+rnd()*2.1,a=(0.4+rnd()*0.55).toFixed(2);
    [-SW,0,SW].forEach(function(ox){[-SH,0,SH].forEach(function(oy){el('circle',{cx:(x+ox).toFixed(1),cy:(y+oy).toFixed(1),r:r.toFixed(2),fill:'#fff',opacity:a},svg)})});}
})();
</script></body></html>'''


def svg(b, h, inhalt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{b}" height="{h}" viewBox="0 0 {b} {h}">'
            + inhalt.strip().replace('\n', '') + '</svg>\n')


def schneedecke():
    """Schnee, der auf der Oberkante einer Kachel liegt; die Kante der Kachel liegt bei y = 9."""
    B, H, P = 200, 24, 2 * math.pi / 200
    def oben(x):
        return 4.6 + 1.5 * math.sin(P * 3 * x + 1) + 0.9 * math.sin(P * 7 * x + 0.4)
    def unten(x):
        y = 12.6 + 1.5 * math.sin(P * 2 * x + 0.5) + 1.1 * math.sin(P * 5 * x + 2)
        for mitte, tief, breit in ((38, 3.4, 5.0), (96, 4.4, 4.2), (151, 3.0, 5.5)):
            y += tief * math.exp(-((x - mitte) / breit) ** 2)
        return y
    xs = list(range(0, B + 1, 2))
    rand = ' '.join(f'L{x},{unten(x):.1f}' for x in reversed(xs))
    form = f'M0,{oben(0):.1f} ' + ' '.join(f'L{x},{oben(x):.1f}' for x in xs[1:]) + ' ' + rand + ' Z'
    schatten = 'M' + ' L'.join(f'{x},{unten(x) - 0.6:.1f}' for x in xs)
    return svg(B, H, f'<path d="{form}" fill="#fff"/><path d="{schatten}" fill="none" stroke="#BCD2E8" stroke-width="1.3"/>')


def huegel(cx, y, rx):
    """Kleiner Schneehügel, auf dem eine Figur steht."""
    return (f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="3.6" fill="#fff"/>'
            f'<ellipse cx="{cx + rx * 0.25:.1f}" cy="{y + 1.2}" rx="{rx * 0.6:.1f}" ry="1.6" fill="#D5E3F2"/>')


RUHE = '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'


def dreh(x, y, klasse, inhalt):
    '''Gruppe, die sich um den Punkt (x, y) bewegt: Die Animation der Klasse dreht, staucht oder schiebt um diesen Punkt.'''
    return f'<g transform="translate({x},{y})"><g class="{klasse}"><g transform="translate({-x},{-y})">{inhalt}</g></g></g>'


def lage(tx=0, ty=0, dreh_=0, sx=1, sy=1):
    """Eine Lage für die Bewegung: verschoben, gedreht, gestaucht (immer dieselbe Folge, damit der Browser weich überblendet)."""
    return f'translate({tx}px,{ty}px) rotate({dreh_}deg) scale({sx},{sy})'


def schneemann():
    """Der schmelzende Schneemann (36 x 48). Jedes Teil hat vier Lagen: steht, halb geschmolzen, Haufen, Schwung beim Aufrichten."""
    dauer = 24   # Sekunden je Runde: etwa 5 stehen, 11 schmelzen, knapp 6 liegen, 2,5 aufrichten
    teile = {    # Klasse: (halb geschmolzen, Haufen, Schwung, Ruhelage)
        'u': (lage(0, 0, 0, 1.2, .76), lage(0, 0, 0, 1.42, .5), lage(0, 0, 0, .97, 1.05), lage()),                 # untere Kugel
        'm': (lage(.6, 6, 0, 1.16, .82), lage(1.4, 13.4, 0, 1.34, .62), lage(0, -.9, 0, .97, 1.05), lage()),       # mittlere Kugel
        'k': (lage(-1, 10, -6, 1.1, .88), lage(-2.2, 20.2, -14, 1.22, .74), lage(0, -1.6, 3, .98, 1.04), lage()),  # Kopf
        'c': (lage(-.6, 9.6, -3, 1.12, .86), lage(-3, 19.4, -6, 1.3, .62), lage(0, -1.3, 2), lage()),              # Schal
        'e1': (lage(-1.3, 10.2), lage(-2.4, 20), lage(0, -1.6), lage()),                                           # Augen
        'e2': (lage(-.5, 11.6), lage(-1.2, 22), lage(.2, -1.6), lage()),
        'd1': (lage(-1.6, 10.2), lage(-4.3, 18.3), lage(0, -1.6), lage()),                                         # Mund
        'd2': (lage(-1.1, 10.8), lage(-3.3, 19.8), lage(0, -1.6), lage()),
        'd3': (lage(-.8, 10.4), lage(-2.4, 19.2), lage(0, -1.6), lage()),
        'd4': (lage(-.2, 11.4), lage(0, 20.8), lage(0, -1.6), lage()),
        'n': (lage(.9, 11.2, 26), lage(4.4, 22.9, 52), lage(0, -1.6, -7), lage()),                                 # Möhre
        'b1': (lage(2.6, 7.4), lage(11.4, 18.4), lage(0, -.9), lage()),                                            # Knöpfe
        'b2': (lage(-1.6, 6.6), lage(-5.6, 15.6), lage(0, -.9), lage()),
        'b3': (lage(.6, 4), lage(2.2, 9.6), lage(0, -.3), lage()),
        'h': (lage(-2.4, 10.6, -22), lage(-9.4, 29.8, -62), lage(0, -2.2, -3), lage(0, 0, -9)),                    # Hut
        'l': (lage(-1, 6.4, -18), lage(-3.4, 15.9, -46), lage(0, -.9, 10), lage()),                                # Arme
        'r': (lage(1, 6.4, 18), lage(3.4, 15.9, 46), lage(0, -.9, -10), lage()),
    }
    klassen = list(teile) + ['p']
    stil = (','.join('.' + k for k in klassen)
            + f'{{animation-duration:{dauer}s;animation-timing-function:ease-in-out;animation-iteration-count:infinite}}'
            + ''.join(f'.{k}{{animation-name:{k}}}' for k in klassen))
    for k, (halb, haufen, schwung, ruhe) in teile.items():
        stil += (f'@keyframes {k}{{0%,6%{{transform:{ruhe};animation-timing-function:ease-in}}'
                 f'30%{{transform:{halb};animation-timing-function:ease-out}}'
                 f'52%,76%{{transform:{haufen}}}81.5%{{transform:{schwung}}}86%,100%{{transform:{ruhe}}}}}')
    stil += '@keyframes p{0%,10%{transform:scale(.3,1);opacity:0}52%,76%{transform:scale(1,1);opacity:.95}85%,100%{transform:scale(.3,1);opacity:0}}'

    def punkt(k, x, y, r):
        return dreh(x, y, k, f'<circle cx="{x}" cy="{y}" r="{r}" fill="#22303F"/>')

    return ('<style>' + stil + RUHE + '</style>'
            + huegel(18, 45, 13)
            + dreh(18, 45.8, 'p', '<ellipse cx="18" cy="45.8" rx="16.4" ry="2.4" fill="#A9D0F0"/>')
            + dreh(11.4, 24.6, 'l', '<path d="M11.4,24.6 L5.8,20 M7.8,21.6 L6,23.4 M7.8,21.6 L8.2,19" stroke="#8A5A2B" stroke-width="1.3" stroke-linecap="round" fill="none"/>')
            + dreh(24.6, 24.6, 'r', '<path d="M24.6,24.6 L30.2,20 M28.2,21.6 L30,23.4 M28.2,21.6 L27.8,19" stroke="#8A5A2B" stroke-width="1.3" stroke-linecap="round" fill="none"/>')
            + dreh(18, 45.2, 'u', '<circle cx="18" cy="35.6" r="9.6" fill="#fff"/><path d="M24.8,28.8 A9.6,9.6 0 0 1 18,45.2 A11.8,11.8 0 0 0 24.8,28.8 Z" fill="#D5E3F2"/>')
            + dreh(18, 23.8, 'm', '<circle cx="18" cy="23.8" r="7.2" fill="#fff"/><path d="M23.1,18.7 A7.2,7.2 0 0 1 18,31 A9,9 0 0 0 23.1,18.7 Z" fill="#D5E3F2"/>')
            + punkt('b1', 18, 23, 1.05) + punkt('b2', 18, 27, 1.05) + punkt('b3', 18, 34, 1.15)
            + dreh(18, 19.5, 'c', '<path d="M12.7,16.8 Q18,19.8 23.3,16.8 L23.6,19.2 Q18,22.4 12.4,19.2 Z" fill="#D63A2F"/><path d="M20.4,19.9 L23,19.2 L24.3,25 L21.8,25.5 Z" fill="#C62828"/>')
            + dreh(18, 13.4, 'k', '<circle cx="18" cy="13.4" r="5.5" fill="#fff"/><path d="M21.9,9.5 A5.5,5.5 0 0 1 18,18.9 A6.9,6.9 0 0 0 21.9,9.5 Z" fill="#D5E3F2"/>')
            + punkt('e1', 16, 12.2, .95) + punkt('e2', 20.1, 12.2, .95)
            + punkt('d1', 15.5, 15.6, .5) + punkt('d2', 16.9, 16.4, .5) + punkt('d3', 19.2, 16.4, .5) + punkt('d4', 20.6, 15.6, .5)
            + dreh(18, 13.9, 'n', '<path d="M18,12.8 L24.6,14.3 L18,15.1 Z" fill="#F08A24"/>')
            + dreh(18, 8.8, 'h', '<rect x="11.6" y="7.7" width="12.8" height="2.2" rx="1.1" fill="#22303F"/><rect x="13.8" y="1.6" width="8.4" height="6.6" rx=".9" fill="#22303F"/><rect x="13.8" y="5.4" width="8.4" height="1.9" fill="#D63A2F"/>'))


# Die Figuren bewegen sich ganz leicht; die Bewegung steht in der SVG-Datei selbst (als Bild eingebunden läuft sie mit).
FIGUREN = {
    # Tannenbaum: geschwungene Zweige, Lametta, Lichter, die abwechselnd funkeln, der Stern leuchtet
    'figur-baum': (48, 55, '<style>.a{animation:f 2.6s ease-in-out infinite}.b{animation:f 2.6s ease-in-out -1.3s infinite}'
                           '.g{animation:g 3.2s ease-in-out infinite alternate}'
                           '@keyframes f{0%,100%{opacity:.35}50%{opacity:1}}@keyframes g{from{opacity:.45}to{opacity:1}}' + RUHE + '</style>'
                           '<defs><radialGradient id="b-stern"><stop offset="0" stop-color="#FFE9A0" stop-opacity=".95"/><stop offset=".45" stop-color="#FFD772" stop-opacity=".4"/><stop offset="1" stop-color="#FFD772" stop-opacity="0"/></radialGradient></defs>'
                           '<g transform="translate(0,3)">' + huegel(24, 49, 19) + '''
<rect x="22" y="41" width="4" height="8" fill="#7A4A21"/>
<path d="M24,19 L42,43.4 Q37.4,41 33,43.4 Q28.6,41 24,43.4 Q19.4,41 15,43.4 Q10.6,41 6,43.4 Z" fill="#23803C"/>
<path d="M24,11 L38,31.4 Q34.4,29.2 31,31.4 Q27.6,29.2 24,31.4 Q20.4,29.2 17,31.4 Q13.6,29.2 10,31.4 Z" fill="#2E9449"/>
<path d="M24,4 L34,19.4 Q31.4,17.6 29,19.4 Q26.6,17.6 24,19.4 Q21.4,17.6 19,19.4 Q16.6,17.6 14,19.4 Z" fill="#3BA858"/>
<path d="M24,19 L29.5,26.4 Q24,30 18.5,26.4 Z" fill="#1F6B34" opacity=".55"/><path d="M24,11 L28.6,17.6 Q24,20.6 19.4,17.6 Z" fill="#237339" opacity=".55"/>
<path d="M12.4,35.4 Q24,41 35.6,35" fill="none" stroke="#F4C542" stroke-width="1.1" stroke-linecap="round"/>
<path d="M15.4,24.4 Q24,29 32.6,24" fill="none" stroke="#F4C542" stroke-width="1.1" stroke-linecap="round"/>
<path d="M19,13.6 Q24,16.6 29,13.4" fill="none" stroke="#F4C542" stroke-width="1" stroke-linecap="round"/>
<ellipse cx="8" cy="42.6" rx="3.6" ry="1.5" fill="#fff"/><ellipse cx="40" cy="42.6" rx="3.6" ry="1.5" fill="#fff"/>
<ellipse cx="12" cy="30.6" rx="3" ry="1.3" fill="#fff"/><ellipse cx="36" cy="30.6" rx="3" ry="1.3" fill="#fff"/>
<ellipse cx="16" cy="18.6" rx="2.4" ry="1.1" fill="#fff"/><ellipse cx="32" cy="18.6" rx="2.4" ry="1.1" fill="#fff"/>
<circle cx="18.6" cy="33.4" r="2.1" fill="#E0453A"/><circle cx="30.4" cy="38.6" r="2.1" fill="#59A3CD"/><circle cx="28.4" cy="22.6" r="1.9" fill="#E0453A"/><circle cx="21" cy="22" r="1.7" fill="#59A3CD"/>
<g fill="#FFF3C4"><circle class="a" cx="14.6" cy="37.2" r="1.3"/><circle class="b" cx="24" cy="38.6" r="1.3"/><circle class="a" cx="33.6" cy="36.6" r="1.3"/>
<circle class="b" cx="17.6" cy="26" r="1.2"/><circle class="a" cx="24.6" cy="27.2" r="1.2"/><circle class="b" cx="31" cy="25.6" r="1.2"/>
<circle class="a" cx="21.4" cy="15" r="1.1"/><circle class="b" cx="26.8" cy="14.8" r="1.1"/></g>
<circle class="g" cx="24" cy="4" r="9" fill="url(#b-stern)"/>
<path d="M24,-2.2 L25.7,1.6 L29.8,2 L26.7,4.7 L27.6,8.8 L24,6.7 L20.4,8.8 L21.3,4.7 L18.2,2 L22.3,1.6 Z" fill="#F7CB4D" stroke="#D9A31C" stroke-width=".5" transform="translate(0,1)"/></g>'''),

    # Schneemann aus drei Kugeln: Er schmilzt langsam zu einem Haufen. Die Kugeln sacken ineinander und werden breit,
    # Augen, Mund, Knöpfe und Möhre rutschen jedes für sich weg, der Hut gleitet zur Seite, eine Pfütze entsteht.
    # So bleibt er eine Weile liegen, dann richtet er sich mit einem kleinen Schwung wieder auf (kein Sprung am Ende).
    'figur-schneemann': (36, 48, schneemann()),

    'figur-geschenke': (52, 40, huegel(26, 37, 23) + '''
<rect x="20" y="14" width="13" height="23" fill="#2E8B45"/><rect x="19" y="11" width="15" height="4" rx=".8" fill="#3BA555"/><rect x="25" y="11" width="3" height="26" fill="#F4C542"/>
<rect x="4" y="16" width="22" height="21" fill="#C62828"/><rect x="2.6" y="12" width="24.8" height="5.2" rx="1" fill="#E0453A"/>
<rect x="13.4" y="12" width="3.4" height="25" fill="#F4C542"/>
<path d="M15,11.6 C11,4.6 5.6,6.4 7.2,10 C8.4,12.6 12.6,12.4 15,11.6 Z" fill="#F4C542" stroke="#C99A16" stroke-width=".6"/>
<path d="M15,11.6 C19,4.6 24.4,6.4 22.8,10 C21.6,12.6 17.4,12.4 15,11.6 Z" fill="#F4C542" stroke="#C99A16" stroke-width=".6"/>
<circle cx="15" cy="11.4" r="2" fill="#FFD95A" stroke="#C99A16" stroke-width=".6"/>
<rect x="31" y="23" width="17" height="14" fill="#2B8CC9"/><rect x="30" y="19.6" width="19" height="4.4" rx=".9" fill="#59A3CD"/>
<rect x="38" y="19.6" width="3" height="17.4" fill="#fff"/><rect x="31" y="28.6" width="17" height="2.6" fill="#fff"/>
<path d="M39.5,19.4 C37,14.6 33,16 34.2,18.4 C35,20 37.8,20 39.5,19.4 Z M39.5,19.4 C42,14.6 46,16 44.8,18.4 C44,20 41.2,20 39.5,19.4 Z" fill="#fff" stroke="#C9D9EA" stroke-width=".5"/>'''),

    # Laterne: Nur die Flamme der Kerze bewegt sich; der Schein um die Laterne steht ruhig auf hellster Stufe
    # (Patrick 28.11.2026: kein pulsierendes Licht)
    'figur-laterne': (40, 52, '<style>.f{animation:f 1.3s ease-in-out infinite alternate}'
        '@keyframes f{from{transform:scale(1.06,.9) skewX(-5deg)}to{transform:scale(.92,1.14) skewX(5deg)}}' + RUHE + '</style>'
        '<defs><radialGradient id="l-schein"><stop offset="0" stop-color="#FFD772" stop-opacity=".75"/><stop offset=".5" stop-color="#FFC24A" stop-opacity=".28"/><stop offset="1" stop-color="#FFC24A" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="l-glas" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#FFF8DA"/><stop offset="1" stop-color="#F5C24A"/></radialGradient></defs>'
        '<circle cx="20" cy="30" r="20" fill="url(#l-schein)"/>' + huegel(20, 49, 15) + '''
<path d="M15.6,9.4 Q20,0.6 24.4,9.4" fill="none" stroke="#D9B13A" stroke-width="1.5" stroke-linecap="round"/>
<path d="M11.4,15.6 L20,8.4 L28.6,15.6 Z" fill="#B8891F"/><rect x="10.4" y="15" width="19.2" height="2.6" rx="1" fill="#D9B13A"/>
<rect x="12.6" y="17.6" width="14.8" height="25.4" fill="url(#l-glas)"/>
<rect x="18.2" y="31" width="3.6" height="12" rx=".8" fill="#FFFDF4"/>'''
        + dreh(20, 30.6, 'f', '<path d="M20,22.4 C22.6,25.8 22.4,29.4 20,30.6 C17.6,29.4 17.4,25.8 20,22.4 Z" fill="#FF9D2E"/><path d="M20,25.4 C21.3,27.2 21.2,29.2 20,29.9 C18.8,29.2 18.7,27.2 20,25.4 Z" fill="#FFE889"/>') + '''
<path d="M12.6,17.6 V43 M27.4,17.6 V43 M20,17.6 V21" fill="none" stroke="#A87916" stroke-width="1.6"/>
<rect x="10.4" y="42.6" width="19.2" height="3" rx="1" fill="#D9B13A"/><rect x="12.2" y="45.4" width="15.6" height="1.8" fill="#B8891F"/>
<path d="M9,47.4 L3.4,43.6 M8.2,47.6 L2.4,46.2 M9.6,46.8 L5.6,41.8" stroke="#2E8B45" stroke-width="1.5" stroke-linecap="round" fill="none"/>
<circle cx="9.6" cy="46.4" r="2" fill="#D63A2F"/><circle cx="12" cy="48" r="1.6" fill="#C62828"/>'''),

    # Rotkehlchen mit Bommelmütze: hüpft ab und zu zweimal kurz und wippt mit dem Schwanz
    'figur-vogel': (40, 38, '<style>.v{animation:v 5.4s ease-in-out infinite}.t{animation:t 5.4s ease-in-out infinite}'
        '@keyframes v{0%,80%,100%{transform:translateY(0)}84%{transform:translateY(-2.6px)}88%{transform:translateY(0)}92%{transform:translateY(-1.7px)}96%{transform:translateY(0)}}'
        '@keyframes t{0%,34%,46%,100%{transform:rotate(0deg)}38%{transform:rotate(-14deg)}42%{transform:rotate(4deg)}}' + RUHE + '</style>'
        + huegel(20, 35, 14)
        + '<g class="v">'
        + dreh(10, 23.6, 't', '<path d="M10,22 L1,25.8 L2.6,21.4 L0.8,18.6 L10,19.6 Z" fill="#6E5540"/>') + '''
<path d="M16.4,30.6 V35 M21.8,30.6 V35 M14.6,35 H18 M20,35 H23.4" stroke="#D9A066" stroke-width="1.2" stroke-linecap="round" fill="none"/>
<ellipse cx="18.4" cy="22.6" rx="10.8" ry="9.2" fill="#A58160"/>
<circle cx="25.6" cy="15.4" r="7" fill="#A58160"/>
<path d="M20.6,16.6 C21,11.6 28.8,10.6 31.4,14.6 C32.8,17.2 32.2,20.6 30.6,23.4 C28.4,27.6 23.8,29.4 20.8,28 C17.6,25.2 19,20.2 20.6,16.6 Z" fill="#E9692C"/>
<path d="M24.4,15.6 C26.4,13.4 29.6,13.8 30.6,16 C30.2,19.4 27.6,22 24.8,22.4 C23,20.6 23,17.8 24.4,15.6 Z" fill="#F4905A" opacity=".8"/>
<ellipse cx="18" cy="28.2" rx="7.2" ry="3.4" fill="#F5EEE2"/>
<path d="M7.4,21.6 C10.2,16.4 17.8,16.6 19.4,21.2 C18.2,26.6 11.2,27.8 7.4,21.6 Z" fill="#7C6048"/>
<path d="M10.4,21.4 C12.8,19.6 15.6,19.8 17.6,21.4 M10,23.6 C12.6,22.6 15.2,22.8 17.2,24" stroke="#5F4937" stroke-width=".7" stroke-linecap="round" fill="none"/>
<path d="M31.8,14 L37.4,15.8 L31.8,17.2 Z" fill="#F2B134"/><path d="M31.8,15.7 L36.4,15.8" stroke="#B9801A" stroke-width=".5"/>
<circle cx="28.2" cy="13.4" r="1.4" fill="#1B1B1B"/><circle cx="28.6" cy="13" r=".45" fill="#fff"/>
<path d="M19.8,11.4 C20.4,5.4 25.4,2 30.2,5.2 C28.2,5.6 27.6,7 28,8.8 Z" fill="#D63A2F"/>
<path d="M19.2,12.6 L28.6,9.6" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><circle cx="30.8" cy="4.8" r="2" fill="#fff"/></g>'''),
}


async def pngs():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 900, 'height': 900}, device_scale_factor=2)
        await pg.set_content(PNG_SEITE)
        await pg.wait_for_timeout(300)
        for name in ('girlande', 'kranz', 'schnee'):
            await pg.locator(f'#{name} svg').screenshot(path=str(ZIEL / f'{name}.png'), omit_background=True)
        await b.close()


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / 'schneedecke.svg').write_text(schneedecke(), encoding='utf-8')
    for name, (b, h, inhalt) in FIGUREN.items():
        (ZIEL / f'{name}.svg').write_text(svg(b, h, inhalt), encoding='utf-8')
    asyncio.run(pngs())
    for f in sorted(ZIEL.iterdir()):
        print(f'{f.name:22} {f.stat().st_size:>7} Bytes')


if __name__ == '__main__':
    main()
