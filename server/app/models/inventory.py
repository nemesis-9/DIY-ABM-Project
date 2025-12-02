def default_inventory(agent, items, x, y, z, active=True):
    return {
        "agent": agent,
        "items": items,
        "pos": {"x": x, "y": y, "z": z},
        "isActive": active,
    }
