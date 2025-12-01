def default_agent(name, age, x, y, z):
    return {
        "name": name,
        "age": age,
        "pos": {"x": x, "y": y, "z": z},
        "state": "alive",
        "hunger": 10,
        "hp": 100,
        "skills": {"farm": 1, "build": 0},
        "inventory": {"food": 2}
    }
