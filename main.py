import pygame
from sys import exit
from numpy.ma.extras import average
from pygame import K_SPACE
import config
import components
import population
import graphic

pygame.init()
clock = pygame.time.Clock()
population = population.Population(151)


def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))
def quit_game(generational_fitness_list,death_list,weight_variation_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphic.plot_score_lists(generational_fitness_list)
            graphic.plot_death(death_list)
            graphic.plot_gene(weight_variation_list)
            pygame.quit()
            exit()
def game_menu(score_value, screen, highscore_value, generation, last_score_value,average_fitness):
    """ Denna kommer skriva ut min poäng innan jag förlorade (genom att score value är det sista returvärdet av,
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

    title_surface_5 = test_font.render("average fittnes: " + str(average_fitness), False, "Gold")
    title_surface_rect_5 = title_surface_5.get_rect(midleft=(20, 75))
    screen.blit(title_surface_5, title_surface_rect_5)
def main():
    n=1
   # parametrar som jag använder för att spåra framgången
    pipes_spawn_time = -1
    score=0
    high_score=0
    last_score=0
    average_score=0

    while True:
        quit_game(population.fitness_list,population.death_place_list,population.weight_st_variation_list)

        config.window.fill((0, 0, 0))

        # Spawn Ground and pipes
        config.ground.draw(config.window)
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 250
        pipes_spawn_time -= 1.1

        # update players and do selection
        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
        if not population.extinct():
            population.update_live_players()
            score+=1
            game_menu(score, config.window, high_score, population.generation, last_score,average_score)

            # manuell trigga selection
            if pygame.key.get_pressed()[pygame.K_a] or score>=7000:
                for p in population.players:
                    p.alive=False
                    p.death_place=p.lifespan
        else:
            config.pipes.clear()  # kommer detta påverkar ?
            pipes_spawn_time = -1
            population.natural_selection()
            if n==1:
                graphic.plot_death(population.death_place_list)
            n += 1

            # now update the respective scores
            if score>high_score:
                high_score=score
            last_score=score
            score = 0
            average_score=population.median_fitness

        if pygame.key.get_pressed()[K_SPACE]:
            clock.tick(120 )
            pygame.display.flip()
        else:
            pass


main()
