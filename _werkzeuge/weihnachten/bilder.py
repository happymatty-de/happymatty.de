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


FIGUREN = {
    'figur-baum': (48, 55, '<g transform="translate(0,3)">' + huegel(24, 49, 19) + '''
<rect x="22" y="41" width="4" height="8" fill="#7A4A21"/>
<path d="M24,19 L41,43 L7,43 Z" fill="#2E8B45"/><path d="M7,43 L41,43 L38.6,39.6 L9.4,39.6 Z" fill="#1F6B34"/>
<path d="M24,11 L37,31 L11,31 Z" fill="#34994D"/><path d="M11,31 L37,31 L34.8,27.6 L13.2,27.6 Z" fill="#237339"/>
<path d="M24,4 L33,19 L15,19 Z" fill="#3BA555"/><path d="M15,19 L33,19 L31,15.7 L17,15.7 Z" fill="#287D3F"/>
<ellipse cx="9.5" cy="42.4" rx="4" ry="1.7" fill="#fff"/><ellipse cx="38.5" cy="42.4" rx="4" ry="1.7" fill="#fff"/>
<ellipse cx="13.2" cy="30.4" rx="3.4" ry="1.5" fill="#fff"/><ellipse cx="34.8" cy="30.4" rx="3.4" ry="1.5" fill="#fff"/>
<ellipse cx="17" cy="18.4" rx="2.8" ry="1.3" fill="#fff"/><ellipse cx="31" cy="18.4" rx="2.8" ry="1.3" fill="#fff"/>
<path d="M24,4 L27.2,9.6 Q25.6,8.6 24,10 Q22.4,8.6 20.8,9.6 Z" fill="#fff"/>
<circle cx="20" cy="25" r="1.9" fill="#E0453A"/><circle cx="29" cy="24" r="1.7" fill="#F4C542"/>
<circle cx="16" cy="37" r="2" fill="#F4C542"/><circle cx="24.5" cy="35.5" r="2" fill="#59A3CD"/><circle cx="32" cy="37.5" r="1.9" fill="#E0453A"/>
<circle cx="23" cy="14.5" r="1.5" fill="#59A3CD"/>
<circle cx="24" cy="3.6" r="6.5" fill="#FFD772" opacity=".28"/>
<path d="M24,-1.2 L25.4,2 L28.9,2.3 L26.2,4.6 L27,8 L24,6.2 L21,8 L21.8,4.6 L19.1,2.3 L22.6,2 Z" fill="#F4C542" stroke="#D9A31C" stroke-width=".5" transform="translate(0,1.6)"/></g>'''),
    'figur-schneemann': (42, 50, huegel(21, 47, 17) + '''
<path d="M11,31 L4,25 M6.4,27 L4.2,29.4 M6.4,27 L7,23.6" stroke="#8A5A2B" stroke-width="1.4" stroke-linecap="round" fill="none"/>
<path d="M31,31 L38,25 M35.6,27 L37.8,29.4 M35.6,27 L35,23.6" stroke="#8A5A2B" stroke-width="1.4" stroke-linecap="round" fill="none"/>
<circle cx="21" cy="35" r="11.5" fill="#fff"/><path d="M29,26.8 A11.5,11.5 0 0 1 21,46.5 A14,14 0 0 0 29,26.8 Z" fill="#D5E3F2"/>
<circle cx="21" cy="18" r="8" fill="#fff"/><path d="M26.6,12.3 A8,8 0 0 1 21,26 A10,10 0 0 0 26.6,12.3 Z" fill="#D5E3F2"/>
<path d="M13.4,22.6 Q21,26.6 28.6,22.6 L28.9,25.6 Q21,29.6 13.1,25.6 Z" fill="#D63A2F"/>
<path d="M25,25.8 L28.6,25 L30.2,33 L26.8,33.6 Z" fill="#C62828"/>
<g transform="rotate(-9 21 11)"><rect x="12" y="9.6" width="18" height="2.5" rx="1.2" fill="#22303F"/><rect x="15.2" y="2.4" width="11.6" height="8" rx="1" fill="#22303F"/><rect x="15.2" y="7.2" width="11.6" height="2.4" fill="#D63A2F"/></g>
<circle cx="18.2" cy="16.8" r="1.15" fill="#22303F"/><circle cx="23.8" cy="16.8" r="1.15" fill="#22303F"/>
<path d="M21,18.6 L28.4,20.2 L21,21.4 Z" fill="#F08A24"/>
<circle cx="17.6" cy="21.4" r=".6" fill="#22303F"/><circle cx="19.2" cy="22.4" r=".6" fill="#22303F"/><circle cx="23" cy="22.5" r=".6" fill="#22303F"/><circle cx="24.6" cy="21.6" r=".6" fill="#22303F"/>
<circle cx="21" cy="32" r="1.25" fill="#22303F"/><circle cx="21" cy="37.4" r="1.25" fill="#22303F"/>'''),
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
    'figur-laterne': (40, 52, '''
<defs><radialGradient id="l-schein"><stop offset="0" stop-color="#FFD772" stop-opacity=".75"/><stop offset=".5" stop-color="#FFC24A" stop-opacity=".28"/><stop offset="1" stop-color="#FFC24A" stop-opacity="0"/></radialGradient>
<radialGradient id="l-glas" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#FFF8DA"/><stop offset="1" stop-color="#F5C24A"/></radialGradient></defs>
<circle cx="20" cy="30" r="20" fill="url(#l-schein)"/>''' + huegel(20, 49, 15) + '''
<path d="M15.6,9.4 Q20,0.6 24.4,9.4" fill="none" stroke="#D9B13A" stroke-width="1.5" stroke-linecap="round"/>
<path d="M11.4,15.6 L20,8.4 L28.6,15.6 Z" fill="#B8891F"/><rect x="10.4" y="15" width="19.2" height="2.6" rx="1" fill="#D9B13A"/>
<rect x="12.6" y="17.6" width="14.8" height="25.4" fill="url(#l-glas)"/>
<rect x="18.2" y="31" width="3.6" height="12" rx=".8" fill="#FFFDF4"/>
<path d="M20,22.4 C22.6,25.8 22.4,29.4 20,30.6 C17.6,29.4 17.4,25.8 20,22.4 Z" fill="#FF9D2E"/><path d="M20,25.4 C21.3,27.2 21.2,29.2 20,29.9 C18.8,29.2 18.7,27.2 20,25.4 Z" fill="#FFE889"/>
<path d="M12.6,17.6 V43 M27.4,17.6 V43 M20,17.6 V21" fill="none" stroke="#A87916" stroke-width="1.6"/>
<rect x="10.4" y="42.6" width="19.2" height="3" rx="1" fill="#D9B13A"/><rect x="12.2" y="45.4" width="15.6" height="1.8" fill="#B8891F"/>
<path d="M9,47.4 L3.4,43.6 M8.2,47.6 L2.4,46.2 M9.6,46.8 L5.6,41.8" stroke="#2E8B45" stroke-width="1.5" stroke-linecap="round" fill="none"/>
<circle cx="9.6" cy="46.4" r="2" fill="#D63A2F"/><circle cx="12" cy="48" r="1.6" fill="#C62828"/>'''),
    'figur-vogel': (38, 34, huegel(19, 31, 13) + '''
<path d="M9,20.6 L1.4,25.4 L3,18.6 Z" fill="#7E6148"/>
<path d="M15.4,27 V31 M20.6,27 V31" stroke="#D9A066" stroke-width="1.3" stroke-linecap="round"/>
<ellipse cx="17" cy="18.6" rx="10.6" ry="9.2" fill="#A98566"/>
<circle cx="24.4" cy="11.6" r="7" fill="#A98566"/>
<path d="M20.2,12.4 C21,8.6 28.6,8 30.6,12 C32.4,16.4 29.4,24 22.6,24.6 C17.8,23.4 18.2,16.6 20.2,12.4 Z" fill="#E8662A"/>
<ellipse cx="17.4" cy="24" rx="7.4" ry="3.6" fill="#F3EBDD"/>
<path d="M6.6,17.4 C9.4,12.8 16.6,13.4 17.8,17.6 C16.6,22.4 9.6,23.4 6.6,17.4 Z" fill="#7E6148"/>
<path d="M30.8,10.6 L36.4,12.4 L30.8,13.8 Z" fill="#F2B134"/>
<circle cx="26.6" cy="9.8" r="1.35" fill="#1B1B1B"/><circle cx="27" cy="9.4" r=".45" fill="#fff"/>'''),
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
