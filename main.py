import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(75)

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))#and components.Pipes(config.window) ?

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10

    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        # Spawn Ground
        config.ground.draw(config.window)

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 2

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            population.natural_selection()

        clock.tick(500)
        pygame.display.flip()

main()