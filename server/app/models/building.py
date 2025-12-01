def house(name, hp, x, y, z):
    return {
        "type": "house",
        "name": name,
        "hp": hp,
        "pos": {"x": x, "y": y, "z": z},
        "occupants": [],
    }
