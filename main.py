import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(200)

def generate_pipes():
    """
    Lägger till rören till "pipes" listan i config
    """
    config.pipes.append(components.Pipes(config.win_width))#and components.Pipes(config.window) ?

def generate_hinder():
    """
    Lägger till hindren till "hinder" listan i config
    """
    config.hinder.append(components.Hinder(config.win_height))

def quit_game():
    """
    En funktion för att stänga programmet ordentligt
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    """
    Våran huvud-funktion som driver spelet
    """
    pipes_spawn_time = 10

    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        # Spawn Ground
        config.ground.draw(config.window)

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            generate_hinder()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        for h in config.hinder:
            h.draw(config.window)
            h.update()
            if h.offscreen_y == True:
                h.direction *= -1

            if h.offscreen_x == True:
                config.hinder.remove(h)

        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            config.hinder.clear()
            population.natural_selection()

        clock.tick(500)
        pygame.display.flip()

main()
