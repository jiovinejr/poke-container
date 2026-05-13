import requests
import random


def fetch_pokemon():
    # Pick a random pokemon from the first 151
    pokemon_id = random.randint(1, 151)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "sprite": data["sprites"]["front_default"],
            "types": [t["type"]["name"].capitalize() for t in data["types"]],
            "height": data["height"] / 10,  # convert to meters
            "weight": data["weight"] / 10,  # convert to kg
        }
    return None