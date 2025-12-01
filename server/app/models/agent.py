def default_agent(name, age: int, x: int, y: int, z: int, hunger_max: int, metabolism: int, hp: int, inventory):
    return {
        "name": name,
        "age": age,
        "pos": {"x": x, "y": y, "z": z},
        "state": "alive",
        "hunger": 10,
        "hunger_max": hunger_max,
        "metabolism": metabolism,
        "hp": hp,
        "skills": {"farm": 1, "build": 0},
        "inventory": inventory
    }
