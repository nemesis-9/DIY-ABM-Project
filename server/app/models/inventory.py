def default_inventory(agent, foods, drinks, x, y, z, active=True):
    return {
        "agent": agent,
        "foods": foods,
        "drinks": drinks,
        "pos": {"x": x, "y": y, "z": z},
        "isActive": active,
    }
