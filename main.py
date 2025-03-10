import brain
import pygame
from population import Population
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(200)

def game_menu(score_value, screen, highscore_value, generation, last_score_value):
    """
    Denna kommer skriva ut min poäng innan jag förlorade (genom att score value är det sista returvärdet av,
    display score, detta görs endast om score har ett värde, annars skrivs ett välkomst-meddelande
    """
    test_font = pygame.font.Font(None, 25)
    title_surface=test_font.render("score: " + str(score_value), False,"Gold")
    title_surface_rect=title_surface.get_rect(midleft=(20,25))
    screen.blit(title_surface,title_surface_rect)

    title_surface_2 = test_font.render("last score: " + str(last_score_value), False, "Gold")
    title_surface_rect_2 = title_surface_2.get_rect(midleft=(20, 50))
    screen.blit(title_surface_2, title_surface_rect_2)

    title_surface_3 = test_font.render("generation: " + str(generation), False, "Gold")
    title_surface_rect_3 = title_surface_3.get_rect(midleft=(170, 25))
    screen.blit(title_surface_3, title_surface_rect_3)

    title_surface_4 = test_font.render("highscore: " + str(highscore_value), False, "Gold")
    title_surface_rect_4 = title_surface_4.get_rect(midleft=(170, 50))
    screen.blit(title_surface_4, title_surface_rect_4)



def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))#and components.Pipes(config.window) ?

def generate_hinder():
    config.hinder.append(components.Hinder(config.win_height))

def quit_game(score_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(score_list)
            pygame.quit()
            exit()


def main():
    pipes_spawn_time = 10
    score = 0
    highscore = 0
    last_score = 0
    score_list=[]
    while True:
        quit_game(score_list)

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
            # print(population.players[0].brain.nodes[12].output_value)
            score += 1
            game_menu(score, config.window, highscore, population.generation, last_score)
        else:
            config.pipes.clear()
            config.hinder.clear()
            population.natural_selection()
            if score > highscore:
                highscore = score
            last_score = score
            score_list.append(score)
            score = 0

        clock.tick(120)
        pygame.display.flip()


main()

