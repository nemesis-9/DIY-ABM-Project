def default_agent(
        name, age, gender, x: int, y: int, z: int,
        weight, height, hp):
    return {
        "name": name,
        "age": age,
        "gender": gender,

        "pos": {"x": x, "y": y, "z": z},
        "state": "alive",

        "weight": weight,
        "height": height,

        "bmr": 0,
        "metabolism": 0,
        "energy_stored": 0,
        "body_hydrate": 0,
        "hungry": 10,
        "thirsty": 10,
        "max_hungry": 0,
        "max_thirsty": 0,

        "hp": hp,
        "skills": {"farm": 1, "build": 0}
    }
