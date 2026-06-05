# N5LCC Ham Radio Club Calendar

No login required to view or add events.
Built with Flask + SQLite3 + FullCalendar.js + Bootstrap 5.

## Run Locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py

Open http://localhost:5000

## Project Structure

    hamcal/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    └── templates/
        └── index.html

---

## Deploy to Fly.io

### 1 — Install flyctl

    curl -L https://fly.io/install.sh | sh
    source ~/.bashrc
    fly auth login

### 2 — Create Dockerfile in hamcal/

    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    ENV EVENTS_DB=/data/events.db
    EXPOSE 8080
    CMD ["python", "app.py"]

### 3 — Two changes to app.py

Change the DB line to:

    DB = os.environ.get("EVENTS_DB", os.path.join(os.path.dirname(__file__), "events.db"))

Change the port from 5000 to 8080:

    app.run(debug=False, host="0.0.0.0", port=8080)

### 4 — Launch on Fly.io

    fly launch
    # App name: n5lcc-calendar
    # Region:   dfw  (closest to New Orleans)
    # Postgres: No
    # Deploy now: No

### 5 — Create a persistent volume (keeps events.db across deploys)

    fly volumes create hamcal_data --size 1 --region dfw

### 6 — Add volume mount to fly.toml

Add this block to the fly.toml that fly launch created:

    [[mounts]]
      source      = "hamcal_data"
      destination = "/data"

Also confirm internal_port is 8080 in fly.toml:

    [[services]]
      internal_port = 8080
      protocol      = "tcp"
      [[services.ports]]
        port = 80
        handlers = ["http"]
        force_https = true
      [[services.ports]]
        port = 443
        handlers = ["tls", "http"]

### 7 — Deploy

    fly deploy
    fly logs

Your app will be live at https://YOUR-APP-NAME.fly.dev

### Custom Domain (optional)

    fly certs add yourcallsign.yourdomain.com

Fly.io handles SSL automatically via Let's Encrypt.

---

## Useful Commands

    fly logs           # live logs
    fly ssh console    # shell into running container
    fly status         # check app health
    fly deploy         # redeploy after code changes
    fly volumes list   # check persistent volumes

---

## Cost (Fly.io free tier covers this entirely)

    App: shared-cpu-1x   ~$0 (free tier)
    Volume: 1GB          ~$0.15/mo