# poke-container

A containerized Flask app deployed on Google Cloud Run. Hits the PokéAPI and serves up a random Gen 1 Pokémon with a small frontend — sprite, types, height, weight. Refresh for a new one.

Live: [your-cloud-run-url-here]

---

## What this is

This started as a way to get comfortable with the full container workflow — writing a Dockerfile, building an image, pushing to Google Container Registry, and deploying to Cloud Run. I wanted something that actually made an external API call and served real content rather than just a hello world.

Ended up adding a little frontend to make it worth looking at. Nothing crazy, just enough to make it feel like an actual app.

---

## Stack

- Python / Flask
- Docker
- Google Cloud Run
- Google Container Registry
- GitHub Actions (CI — lint + tests on push)
- PokéAPI

---

## Run it locally

```bash
git clone https://github.com/jiovinejr/poke-container.git
cd poke-container
docker build -t poke-container .
docker run -p 8080:8080 poke-container
```

Then open `http://localhost:8080`.

---

## Deploy

```bash
docker build -t gcr.io/firstcontainerlaunch/poke-container .
docker push gcr.io/firstcontainerlaunch/poke-container

gcloud run deploy poke-container \
  --image gcr.io/YOUR_PROJECT_ID/poke-container \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --port 8080
```

---

## Background

I spent about 10 years in restaurants — bartending, cooking, managing. Left the industry 3 years ago to move into tech. I'm currently working in produce wholesale, managing warehouse operations while building internal tools to modernize how the place runs. Most of what I build day to day is practical stuff the job actually needs.

This project is separate from that — it's here to show I can work with containers and cloud infrastructure, not just scripts and web apps.

---

## CI

GitHub Actions runs on every push to `main` and `develop`. Installs dependencies, lints with flake8, runs pytest. Nothing gets merged without passing.