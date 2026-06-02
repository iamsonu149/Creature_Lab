import pygame

from creature import (
    spawn_creature,
    spawn_food,
    create_next_generation,
    update_creatures,
    apply_energy_and_collect_dead,
    handle_creature_eating,
    NUM_CREATURES,
    CREATURE_RADIUS,
    INITIAL_ENERGY,
    ENERGY_LOSS_PER_SECOND,
    MAX_ENERGY,
)

from predator import (
    create_predator,
    next_generation_predator,
    update_predator,
    apply_energy_and_collect_dead_predator,
    handle_predator_eating,
    PREDATOR_COUNT ,
    PREDATOR_RADIUS ,
    PREDATOR_INITIAL_ENERGY ,
    PREDATOR_ENERGY_LOSS_PER_SECOND,
    PREDATOR_MAX_ENERGY,
)

pygame.init()

WIDTH, HEIGHT = 1280, 700
NUM_FOOD = 20
GENERATION_TIME = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creature Evolution")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
generation_timer = 0
generation = 1


creatures = [spawn_creature(WIDTH, HEIGHT, INITIAL_ENERGY) for _ in range(NUM_CREATURES)]
dead_creatures = []
food_list = [spawn_food(WIDTH,HEIGHT) for _ in range(NUM_FOOD)]
       ################# predator ####################
predators = [create_predator(WIDTH,HEIGHT,PREDATOR_INITIAL_ENERGY) for _ in range(PREDATOR_COUNT)]
dead_predators =[]




running = True
while running:
    dt = clock.tick(60) / 1000
    generation_timer += dt

    if len(creatures) == 0 or generation_timer >= GENERATION_TIME:
        generation += 1
        generation_timer = 0
        old_creatures = creatures + dead_creatures
        creatures = create_next_generation(
            old_creatures, NUM_CREATURES, WIDTH, HEIGHT, INITIAL_ENERGY
        )
        dead_creatures = []
        #################### predator ################################
        old_predators = predators + dead_predators
        predators = next_generation_predator(old_predators,PREDATOR_COUNT,WIDTH, HEIGHT,
                                              PREDATOR_INITIAL_ENERGY )
        dead_predators=[]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_creatures(creatures, food_list,predators ,WIDTH, HEIGHT, CREATURE_RADIUS)
    apply_energy_and_collect_dead(creatures, dead_creatures, ENERGY_LOSS_PER_SECOND, dt)
    handle_creature_eating(
        creatures, food_list, CREATURE_RADIUS, spawn_food, max_energy=MAX_ENERGY
    )
    ######################### predator ##############################

    update_predator(predators, creatures, WIDTH, HEIGHT, PREDATOR_RADIUS)
    apply_energy_and_collect_dead_predator(predators, dead_predators, PREDATOR_ENERGY_LOSS_PER_SECOND, dt)
    handle_predator_eating(
        predators, creatures,dead_creatures, PREDATOR_RADIUS,  max_energy=PREDATOR_MAX_ENERGY)


    screen.fill((20, 20, 30))

    for food in food_list:
        pygame.draw.circle(screen, (255, 100, 100), (food[0], food[1]), 5)

    for creature in creatures:
        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (int(creature["x"]), int(creature["y"])),
            CREATURE_RADIUS,
        )

        energy_text = font.render(str(int(creature["energy"])), True, (255, 255, 255))
        screen.blit(energy_text, (creature["x"], creature["y"] - 20))
    ##################### predator #######################
    for predator in predators:
        pygame.draw.circle(screen,(255, 0, 0),
            (int(predator["x"]), int(predator["y"])),
            PREDATOR_RADIUS,
        )
       

    total_score = sum(c["score"] for c in creatures)
    best_score = max((c["score"] for c in creatures), default=0)

    screen.blit(
        font.render(f"Total Food Eaten: {total_score}", True, (255, 255, 255)), (10, 10)
    )
    screen.blit(font.render(f"Best Score: {best_score}", True, (255, 255, 0)), (10, 40))
    screen.blit(
        font.render(f"Creatures Alive: {len(creatures)}", True, (200, 200, 255)), (10, 70)
    )
    screen.blit(font.render(f"Generation: {generation}", True, (180, 255, 180)), (10, 100))

    pygame.display.flip()

pygame.quit()
