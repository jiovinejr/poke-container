import os
from flask import Flask, render_template_string
from src.api import fetch_pokemon

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>PokéContainer</title>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --red: #E3350D;
      --dark: #1a1a2e;
      --card: #16213e;
      --accent: #f5c518;
      --text: #e0e0e0;
      --muted: #888;
    }

    body {
      background-color: var(--dark);
      background-image: radial-gradient(circle at 20% 50%, #0f3460 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, #1a0a2e 0%, transparent 40%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: 'DM Sans', sans-serif;
      color: var(--text);
      padding: 2rem;
    }

    header {
      text-align: center;
      margin-bottom: 2.5rem;
    }

    header h1 {
      font-family: 'Press Start 2P', monospace;
      font-size: clamp(1rem, 3vw, 1.5rem);
      color: var(--accent);
      text-shadow: 3px 3px 0 var(--red);
      letter-spacing: 2px;
      line-height: 1.6;
    }

    header p {
      margin-top: 0.75rem;
      color: var(--muted);
      font-size: 0.85rem;
    }

    .card {
      background: var(--card);
      border: 2px solid #ffffff10;
      border-radius: 20px;
      padding: 2.5rem 3rem;
      max-width: 400px;
      width: 100%;
      text-align: center;
      box-shadow: 0 0 60px #e3350d22, 0 20px 40px #00000066;
      animation: fadeUp 0.6s ease forwards;
      opacity: 0;
      transform: translateY(20px);
    }

    @keyframes fadeUp {
      to { opacity: 1; transform: translateY(0); }
    }

    .pokeball-ring {
      width: 160px;
      height: 160px;
      border-radius: 50%;
      border: 4px solid var(--red);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem;
      background: radial-gradient(circle, #ffffff0a, transparent);
      box-shadow: 0 0 30px #e3350d44;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 20px #e3350d44; }
      50% { box-shadow: 0 0 40px #e3350d99; }
    }

    .pokeball-ring img {
      width: 120px;
      height: 120px;
      image-rendering: pixelated;
      filter: drop-shadow(0 4px 12px #00000088);
    }

    .pokemon-number {
      font-family: 'Press Start 2P', monospace;
      font-size: 0.6rem;
      color: var(--muted);
      margin-bottom: 0.4rem;
    }

    .pokemon-name {
      font-family: 'Press Start 2P', monospace;
      font-size: clamp(1rem, 4vw, 1.4rem);
      color: #fff;
      margin-bottom: 1rem;
      line-height: 1.5;
    }

    .types {
      display: flex;
      gap: 0.5rem;
      justify-content: center;
      margin-bottom: 1.5rem;
    }

    .type-badge {
      padding: 0.3rem 0.9rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      background: #ffffff15;
      border: 1px solid #ffffff25;
    }

    .stats {
      display: flex;
      justify-content: center;
      gap: 2rem;
      border-top: 1px solid #ffffff10;
      padding-top: 1.25rem;
    }

    .stat label {
      display: block;
      font-size: 0.7rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 0.2rem;
    }

    .stat span {
      font-size: 1rem;
      font-weight: 600;
      color: var(--accent);
    }

    .refresh-btn {
      margin-top: 2rem;
      padding: 0.75rem 2rem;
      background: var(--red);
      color: white;
      border: none;
      border-radius: 999px;
      font-family: 'Press Start 2P', monospace;
      font-size: 0.6rem;
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
      letter-spacing: 1px;
      transition: transform 0.1s, box-shadow 0.1s;
      box-shadow: 0 4px 0 #8a1f08;
    }

    .refresh-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 0 #8a1f08;
    }

    .refresh-btn:active {
      transform: translateY(2px);
      box-shadow: 0 2px 0 #8a1f08;
    }

    footer {
      margin-top: 2rem;
      font-size: 0.75rem;
      color: var(--muted);
    }
  </style>
</head>
<body>

  <header>
    <h1>POKÉ<br>CONTAINER</h1>
    <p>A containerized Pokémon API — running on Cloud Run</p>
  </header>

  {% if pokemon %}
  <div class="card">
    <div class="pokeball-ring">
      <img src="{{ pokemon.sprite }}" alt="{{ pokemon.name }}" />
    </div>
    <div class="pokemon-number">#{{ '%03d' % pokemon.id }}</div>
    <div class="pokemon-name">{{ pokemon.name }}</div>
    <div class="types">
      {% for t in pokemon.types %}
      <span class="type-badge">{{ t }}</span>
      {% endfor %}
    </div>
    <div class="stats">
      <div class="stat">
        <label>Height</label>
        <span>{{ pokemon.height }}m</span>
      </div>
      <div class="stat">
        <label>Weight</label>
        <span>{{ pokemon.weight }}kg</span>
      </div>
    </div>
  </div>
  <a href="/" class="refresh-btn">NEW POKEMON</a>
  {% else %}
  <div class="card">
    <p style="color: var(--red);">Failed to fetch Pokémon. Try again!</p>
    <a href="/" class="refresh-btn">RETRY</a>
  </div>
  {% endif %}

  <footer>poke-container &bull; Cloud Run &bull; PokéAPI</footer>

</body>
</html>
"""


@app.route("/")
def index():
    pokemon = fetch_pokemon()
    return render_template_string(HTML, pokemon=pokemon)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)