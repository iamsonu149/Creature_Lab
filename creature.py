import math
import random
import numpy as np

from brain import Brain

WIDTH, HEIGHT = 1280, 700
NUM_CREATURES = 10
CREATURE_RADIUS = 10
INITIAL_ENERGY = 10
ENERGY_LOSS_PER_SECOND = 1
MAX_ENERGY = 150


def spawn_creature(width, height, initial_energy=INITIAL_ENERGY):
    return {
        "x": random.randint(50, width - 50),
        "y": random.randint(50, height - 50),
        "angle": random.uniform(0, 2 * math.pi),
        "speed": 2,
        "score": 0,
        "energy": initial_energy,
        "brain": Brain(),
    }


def create_next_generation(
    old_creatures,
    num_creatures=NUM_CREATURES,
    width=1280,
    height=700,
    initial_energy=INITIAL_ENERGY,
):
    old_creatures = list(old_creatures)
    old_creatures.sort(key=lambda c: c["score"], reverse=True)
    parents = old_creatures[:3]

    if not parents:
        return [spawn_creature(width, height, initial_energy) for _ in range(num_creatures)]

    new_creatures = []
    for _ in range(num_creatures):
        parent = random.choice(parents)
        child = spawn_creature(width, height, initial_energy)
        child["brain"] = parent["brain"].copy()
        child["brain"].mutate(rate=0.5, strength=0.1)
        new_creatures.append(child)
    return new_creatures


def update_creatures(creatures, food_list, width, height, creature_radius):
    for creature in creatures:
        nearest_dist = float("inf")
        food_dx, food_dy = 0, 0

        for food in food_list:
            dx = food[0] - creature["x"]
            dy = food[1] - creature["y"]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < nearest_dist:
                nearest_dist = dist
                food_dx = dx
                food_dy = dy

        target_angle = math.atan2(food_dy, food_dx)
        angle_diff = (target_angle - creature["angle"] + math.pi) % (2 * math.pi) - math.pi
        dist_norm = nearest_dist / math.sqrt(width * width + height * height)
        x_center = (creature["x"] - width / 2) / (width / 2)
        y_center = (creature["y"] - height / 2) / (height / 2)

        inputs = np.array(
            [
                math.cos(angle_diff),
                math.sin(angle_diff),
                dist_norm,
                creature["energy"] / INITIAL_ENERGY,
                x_center,
                y_center,
            ]
        )

        outputs = creature["brain"].think(inputs)
        turn = outputs[0]
        move = (outputs[1] + 1) / 2

        creature["angle"] += turn * 0.2
        creature["x"] += math.cos(creature["angle"]) * move * creature["speed"]
        creature["y"] += math.sin(creature["angle"]) * move * creature["speed"]

        if creature["x"] < creature_radius:
            creature["x"] = creature_radius
            creature["angle"] = math.pi - creature["angle"] + random.uniform(-0.25, 0.25)
        elif creature["x"] > width - creature_radius:
            creature["x"] = width - creature_radius
            creature["angle"] = math.pi - creature["angle"] + random.uniform(-0.25, 0.25)

        if creature["y"] < creature_radius:
            creature["y"] = creature_radius
            creature["angle"] = -creature["angle"] + random.uniform(-0.25, 0.25)
        elif creature["y"] > height - creature_radius:
            creature["y"] = height - creature_radius
            creature["angle"] = -creature["angle"] + random.uniform(-0.25, 0.25)

        creature["x"] = max(creature_radius, min(width - creature_radius, creature["x"]))
        creature["y"] = max(creature_radius, min(height - creature_radius, creature["y"]))


def apply_energy_and_collect_dead(creatures, dead_creatures, energy_loss_per_second, dt):
    for creature in creatures[:]:
        creature["energy"] -= energy_loss_per_second * dt
        if creature["energy"] <= 0:
            dead_creatures.append(creature)
            creatures.remove(creature)


def handle_creature_eating(creatures, food_list, creature_radius, spawn_food, max_energy=None):
    for creature in creatures:
        for food in food_list[:]:
            distance = math.sqrt((creature["x"] - food[0]) ** 2 + (creature["y"] - food[1]) ** 2)
            if distance < creature_radius + 5:
                creature["energy"] += 5
                if max_energy is not None:
                    creature["energy"] = min(max_energy, creature["energy"])
                creature["score"] += 1
                food_list.remove(food)
                food_list.append(spawn_food(WIDTH,HEIGHT))

def spawn_food(WIDTH,HEIGHT):
    return [random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)]
