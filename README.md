#  Emoji Reactions — Instagram-Style Floating Emoji App

A full simulation of Instagram's live emoji reaction system, built for **Windows**.

Tap/click emojis and watch them float upward with physics-based animations, particle trails, and glow effects — just like Instagram Live.

## What's Inside

| Language     | File                        | Purpose                              |
|--------------|-----------------------------|--------------------------------------|
| Python       | `src/python/app.py`         | Windows desktop overlay app (tkinter)|
| Python       | `src/python/reactions.py`   | Emoji physics & animation engine     |
| Python       | `src/python/config.py`      | App configuration loader             |
| HTML         | `src/web/index.html`        | Web-based version (works anywhere)   |
| CSS          | `src/web/css/style.css`     | Animated gradient UI theme           |
| JavaScript   | `src/web/js/app.js`         | Canvas-based reaction engine         |
| JavaScript   | `src/web/js/particles.js`   | Particle trail system                |
| JavaScript   | `src/web/js/audio.js`       | Web Audio API sound effects          |
| JSON         | `config/settings.json`      | Shared configuration                 |
| Batch        | `scripts/run-desktop.bat`   | Launch desktop app                   |
| Batch        | `scripts/run-web.bat`       | Launch web version                   |
| PowerShell   | `scripts/setup.ps1`         | Full Windows setup script            |

## Quick Start

### Option A: Desktop App (Python + tkinter)
```
scripts\run-desktop.bat
```

### Option B: Web Version (Browser)
```
scripts\run-web.bat
```
Then open http://localhost:8080

### Manual Setup
```powershell
# Install Python dependencies
pip install pillow

# Run desktop version
python src/python/app.py

# Or run web version
python -m http.server 8080 --directory src/web
```

## Features

-  6 reaction emojis: ❤️ 😂 😮 😢 😡 👍
-  Physics-based floating animation with randomized paths
-  Particle trail effects behind each emoji
-  Scale pulse on spawn + fade on exit
-  Subtle pop sound effects (web version)
-  Desktop overlay mode (always-on-top transparent window)
-  Responsive web version works on any device
-  Fully configurable via JSON

## Architecture

```
┌──────────────────────────────────────────┐
│           Config (JSON)                  │
├──────────────┬───────────────────────────┤
│  Desktop App │     Web App               │
│  (Python)    │     (HTML/CSS/JS)         │
│              │                           │
│  tkinter GUI │  Canvas Renderer          │
│  ↓           │  ↓                        │
│  Animation   │  requestAnimationFrame    │
│  Engine      │  ↓                        │
│  (reactions  │  Particle System          │
│   .py)       │  (particles.js)           │
│              │  ↓                        │
│              │  Audio Engine             │
│              │  (audio.js)              │
└──────────────┴───────────────────────────┘
```

## License
MIT
