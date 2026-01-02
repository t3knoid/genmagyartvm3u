# 📺 genmagyartvm3u  

### _Hungarian TV M3U Generator (Django-based scraper)_

`genmagyartvm3u` is a lightweight Django application that scrapes live Hungarian TV stream metadata from **mediaklikk.hu** and exposes it as an **M3U playlist**. The generated playlist can be consumed by IPTV clients such as **Kodi’s PVR IPTV Simple Client**, VLC, or any M3U‑compatible player. Originally built for Heroku, the project can now be deployed on any container‑friendly platform or run locally with minimal setup.

---

## 🚀 Features

- Scrapes Hungarian TV channels from **mediaklikk.hu**
- Generates a valid **M3U playlist** endpoint
- Simple Django app — no frontend, no database complexity
- Works with IPTV clients (Kodi, VLC, etc.)
- Deployable to Heroku or container platforms
- Lightweight runtime (Python + Django)

---

## 📦 Architecture Overview

| Component | Purpose |
|----------|---------|
| `manage.py` | Django entrypoint |
| `m2tv/` | Scraper logic for mediaklikk.hu |
| `magyartv/` | Django app exposing the M3U endpoint |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version pin (Heroku legacy) |
| `Procfile` | Heroku web process definition |
| `db.sqlite3` | Local dev DB (not required in production) |

---

## 🧰 Installation & Local Development

### 1. Clone the repository
```bash
git clone https://github.com/t3knoid/genmagyartvm3u.git
cd genmagyartvm3u
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Django server
```bash
python manage.py runserver
```

### 5. Access the M3U feed
```
http://localhost:8000/m3u
```

---

## 🌐 Deployment Options

### Option A — Heroku (legacy workflow)
Heroku support remains, but the platform no longer offers free dynos.

```bash
heroku create
heroku buildpacks:set heroku/python
heroku config:set DISABLE_COLLECTSTATIC=1
git push heroku master
heroku ps:scale web=1
```

### Option B — Container Deployment (recommended)
A modern Dockerfile could be added, but here’s the minimal runtime:

- Python 3.12+
- Django
- Gunicorn (optional)
- No persistent DB required

---

## 📄 M3U Output Format

The application returns a standard M3U playlist:

```
#EXTM3U
#EXTINF:-1 tvg-id="m1" group-title="Hungary",M1
https://stream-url...
```

Channel metadata is scraped dynamically from mediaklikk.hu.

---

## 🧪 Testing the Feed

You can test the generated playlist using:

- **VLC** → Media → Open Network Stream → paste the `/m3u` URL  
- **Kodi** → PVR IPTV Simple Client → Configure → M3U Playlist URL  
- **ffplay**  
  ```bash
  ffplay $(curl -s http://localhost:8000/m3u | grep -v '#')
  ```
