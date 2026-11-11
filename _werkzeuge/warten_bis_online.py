#!/usr/bin/env python3
"""Wartet, bis GitHub Pages den aktuellen Stand von main veröffentlicht hat.
Aufruf nach dem Hochladen:  python3 _werkzeuge/warten_bis_online.py
Gibt „online“ aus, wenn die Veröffentlichung für den letzten Commit erfolgreich war,
sonst den Fehler. Wartet höchstens 10 Minuten."""
import json, subprocess, sys, time

repo = 'happymatty-de/happymatty.de'
sha = subprocess.run(['git', 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
start = time.time()
while time.time() - start < 600:
    out = subprocess.run(['gh', 'api', f'repos/{repo}/actions/runs?per_page=10&head_sha={sha}'],
                         capture_output=True, text=True).stdout
    runs = [r for r in json.loads(out or '{}').get('workflow_runs', []) if r.get('name') == 'pages build and deployment']
    if runs:
        r = runs[0]
        if r['status'] == 'completed':
            dauer = int(time.time() - start)
            if r['conclusion'] == 'success':
                print(f'online ({sha[:7]}, nach {dauer} s Wartezeit)'); sys.exit(0)
            # Manchmal bricht GitHub nur den Nebenauftrag „report-build-status“ ab und meldet dann
            # „failure“, obwohl die Seite veröffentlicht ist (Anlass 11.11.2026). Maßgeblich ist „deploy“.
            jobs = subprocess.run(['gh', 'api', f"repos/{repo}/actions/runs/{r['id']}/jobs"],
                                  capture_output=True, text=True).stdout
            if any(j.get('name') == 'deploy' and j.get('conclusion') == 'success'
                   for j in json.loads(jobs or '{}').get('jobs', [])):
                print(f'online ({sha[:7]}, nach {dauer} s Wartezeit; nur der Statusbericht von GitHub schlug fehl)'); sys.exit(0)
            print(f"Veröffentlichung {r['conclusion']} ({sha[:7]})"); sys.exit(1)
    time.sleep(10)
print(f'nach 10 Minuten noch nicht online ({sha[:7]})'); sys.exit(2)
