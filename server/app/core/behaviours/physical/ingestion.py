import math
from ....db.mongo import agents, inventories
from ...metrics.physical import ingest_metrics


async def calculate_bmr(agent):
    weight = agent["weight"]
    height = agent["height"]
    age = agent["age"]
    gender = agent["gender"]

    gender_const = ingest_metrics["bmr_const_male"] if gender == "m" else ingest_metrics["bmr_const_female"]
    bmr = (
            ingest_metrics["bmr_weight_co"] * weight
            + ingest_metrics["bmr_height_co"] * height
            - ingest_metrics["bmr_age_co"] * age
            + gender_const
    )
    agent["bmr"] = max(ingest_metrics["bmr_min"], bmr)
    return agent


async def update_metabolism(agent):
    bmr = agent["bmr"]
    prev_metabolism = agent["metabolism"]
    metabolism = (
            ingest_metrics["metabolism_co"] * prev_metabolism
            + ingest_metrics["metabolism_bmr_co"] * bmr
    )
    metabolism = max(
        ingest_metrics["metabolism_min"],
        min(ingest_metrics["metabolism_max"], metabolism)
    )
    agent["metabolism"] = metabolism
    return agent


async def calculate_energy(agent):
    weight = agent["weight"]

    body_fat_fraction = 1 / (1 + math.exp(
        -ingest_metrics["fat_fraction_weight_co"] *
        (weight - ingest_metrics["fat_fraction_weight_avg"])
    ))

    body_fat = body_fat_fraction * weight
    energy_stored = body_fat * ingest_metrics["fat_to_calories"]
    agent["energy_stored"] = energy_stored
    return agent


async def apply_weight_change(agent, calories):
    kcal_per_kg = ingest_metrics["kcal_per_kg_gain"]
    weight_change_kg = calories / kcal_per_kg
    agent["weight"] += weight_change_kg
    return agent


async def calculate_hydration(agent):
    weight = agent["weight"]
    body_hydrate = ingest_metrics["water_fraction_weight_co"] * weight
    agent["body_hydrate"] = body_hydrate
    return agent


async def calculate_max_hungry(agent):
    bmr = agent["bmr"]
    daily_burning_const = ingest_metrics["daily_burn_co"]  # TODO: need to change with task

    daily_burn = daily_burning_const * bmr
    agent["max_hungry"] =  daily_burn
    return agent


async def calculate_max_thirsty(agent):
    metabolism = agent["metabolism"]
    daily_draining_const = ingest_metrics["daily_drain_co"]  # TODO: need to change with climate
    thirsty_metabolism_const = ingest_metrics["thirsty_metabolism_co"]  # TODO: need to change with gender

    daily_drain = daily_draining_const + (metabolism * thirsty_metabolism_const)
    agent["max_thirsty"] = daily_drain
    return agent


async def update_hungry(agent):
    bmr = agent["bmr"]
    daily_burning_const = ingest_metrics["daily_burn_co"]  # TODO: need to change with task
    hourly_burn = daily_burning_const * bmr / 24.0
    agent["hungry"] += hourly_burn
    agent["energy_stored"] -= hourly_burn
    return agent


async def update_thirsty(agent):
    metabolism = agent["metabolism"]
    daily_draining_const = ingest_metrics["daily_drain_co"]  # TODO: need to change with climate
    thirsty_metabolism_const = ingest_metrics["thirsty_metabolism_co"]  # TODO: need to change with gender
    hourly_drain = (daily_draining_const + (metabolism * thirsty_metabolism_const)) / 24.0
    agent["thirsty"] += hourly_drain
    agent["body_hydrate"] -= hourly_drain
    return agent


async def eat(agent, inventory):
    foods = inventory.get("foods", [])
    if not foods:
        return agent, inventory

    # Choose the highest calorie food first
    food = max(foods, key=lambda x: x["cal"])
    food_calories = food["cal"]

    net_calories = food_calories - agent["hungry"]
    agent["hungry"] = max(agent["hungry"] - food_calories, 0)

    if net_calories > 0:
        agent = await apply_weight_change(agent, net_calories)
    elif net_calories < 0:
        agent = await apply_weight_change(agent, net_calories)

    agent = await calculate_energy(agent)

    food["count"] -= 1
    if food["count"] <= 0:
        foods.remove(food)
    inventory["foods"] = foods

    return agent, inventory


async def drink(agent, inventory):
    drinks = inventory.get("drinks", [])
    if not drinks:
        return agent, inventory

    # Choose the highest count drink first
    drink_item = max(drinks, key=lambda x: x["count"])
    drink_calories = drink_item["cal"]

    agent["thirsty"] = max(agent["thirsty"] - drink_item["litres"], 0)
    net_calories = drink_calories - agent["hungry"]
    agent["hungry"] = max(agent["hungry"] - drink_item["cal"], 0)

    if net_calories > 0:
        agent = await apply_weight_change(agent, net_calories)
    elif net_calories < 0:
        agent = await apply_weight_change(agent, net_calories)
    agent = await calculate_energy(agent)

    drink_item["count"] -= 1
    if drink_item["count"] <= 0:
        drinks.remove(drink_item)
    inventory["drinks"] = drinks

    return agent, inventory


async def check_dead(agent):
    if agent["hungry"] > agent["max_hungry"]*2 or agent["thirsty"] > agent["max_thirsty"]*2:
        agent["state"] = "dead"
    return agent


async def ingestion(agent):
    agent = await calculate_bmr(agent)
    agent = await update_metabolism(agent)
    agent = await calculate_energy(agent)
    agent = await calculate_hydration(agent)
    agent = await calculate_max_hungry(agent)
    agent = await calculate_max_thirsty(agent)

    agent = await update_hungry(agent)
    agent = await update_thirsty(agent)

    inventory = await inventories.find_one({"agent": agent["_id"]})
    if not inventory:
        pass
    else:
        performed_action = False

        daily_eat_times = ingest_metrics["daily_eat_times"]
        daily_drink_times = ingest_metrics["daily_drink_times"]

        while agent["hungry"] >= agent["max_hungry"]/daily_eat_times and len(inventory.get("foods", [])) > 0:
            agent, inventory = await eat(agent, inventory)
            performed_action = True
            agent = await calculate_bmr(agent)
            agent = await calculate_max_hungry(agent)
            if inventory.get("foods", []) is None:
                break

        while agent["thirsty"] >= agent["max_thirsty"]/daily_drink_times and len(inventory.get("drinks", [])) > 0:
            agent, inventory = await drink(agent, inventory)
            performed_action = True
            agent = await calculate_energy(agent)
            agent = await calculate_max_thirsty(agent)
            if inventory.get("drinks", []) is None:
                break

        if performed_action:
            agent = await calculate_energy(agent)
            agent = await update_metabolism(agent)

    agent = await check_dead(agent)

    await agents.update_one({"_id": agent["_id"]}, {"$set": agent})
    if inventory:
        await inventories.update_one({"_id": inventory["_id"]}, {"$set": inventory})
