"""Aus den Aufnahmen des Salamander Grand Piano (Alexander Holm, CC BY 3.0) die Töne für das Weihnachtslied machen:
je Ton das nähere der beiden Mikrofone nehmen, den Anfang auf den Anschlag legen, auf 3,6 Sekunden kürzen, ausblenden,
alle Töne gleich laut machen, als MP3 (mono, 96 kbit/s) ablegen.
Aufruf: python3 -I wandeln.py <Ordner mit den flac-Dateien> <Zielordner> [nur_pruefen]"""
import subprocess, sys, pathlib, numpy as np
roh, ziel = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); pruefen = len(sys.argv) > 3
SR, SEK = 44100, 3.6
TOENE = {'C2': 'C2v6', 'Fs2': 'Fs2v6', 'A2': 'A2v6', 'C3': 'C3v6', 'Ds3': 'Ds3v6', 'Fs3': 'Fs3v6', 'A3': 'A3v6', 'C4': 'C4v6',
         'Ds4': 'Ds4v6', 'Fs4': 'Fs4v6', 'C5': 'C5v8', 'Ds5': 'Ds5v8', 'Fs5': 'Fs5v8'}
def lesen(datei):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(datei), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype='<f4').reshape(-1, 2).astype(np.float64)
toene = {}
for name, quelle in TOENE.items():
    x = lesen(roh / (quelle + '.flac'))
    # Die beiden Mikrofone hängen über Bass und Diskant. Zusammengelegt löschen sie sich bei manchen Tönen fast aus
    # (c'' um 8 dB), deshalb nur das nähere Mikrofon: der Kanal, der in der ersten Sekunde lauter ist.
    wahl = []
    for k in (0, 1):
        v = x[:, k]; an = int(np.argmax(np.abs(v) > np.abs(v).max() * 10 ** (-46 / 20)))
        a = max(0, an - int(SR * 0.003)); wahl.append((float(np.sqrt(np.mean(v[a:a + SR] ** 2))), k, a))
    eff, k, a = max(wahl)
    m = x[a:a + int(SR * SEK), k].copy() * (0.14 / eff)          # alle Töne in der ersten Sekunde gleich laut
    n = len(m); ein = int(SR * 0.001); m[:ein] *= np.linspace(0, 1, ein)
    aus = int(SR * 0.7); m[n - aus:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, aus))
    toene[name] = m
    print(f'{name:4} aus {quelle:6} Kanal {"LR"[k]} | Beginn {a / SR * 1000:5.1f} ms | Spitze {np.abs(m).max():.2f}')
    if pruefen: continue
    ziel.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-codec:a', 'libmp3lame', '-b:a', '96k',
                    '-map_metadata', '-1', '-id3v2_version', '0', '-write_id3v1', '0', str(ziel / (name + '.mp3'))], input=m.astype('<f4').tobytes(), check=True)
if pruefen: sys.exit()
print('Dateien:', sorted((p.name, p.stat().st_size) for p in ziel.glob('*.mp3')), '| zusammen', sum(p.stat().st_size for p in ziel.glob('*.mp3')), 'Bytes')
