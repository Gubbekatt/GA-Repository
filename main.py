import pygame
from sys import exit
import config
import components
import population
import graphic

pygame.init()
clock = pygame.time.Clock()
population = population.Population(200)


def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))   
def quit_game(generational_fitness_list,death_list,weight_variation_list, generation):
    """Efter avslutad körning av programmet, eller manuell avbrytning, visas samtliga grafer,
        baserat på värderna från population fittnes.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT or generation == 200:
            graphic.plot_score_lists(generational_fitness_list)
            graphic.plot_death(death_list)
            graphic.plot_gene(weight_variation_list)
            pygame.quit()
            exit()
def game_menu(score_value, screen, highscore_value, generation, last_score_value,average_fitness):
    """Under körning av program visas samtliga relevanta värdern: Alla utom average_fittnes reflekterar
    antal frames överlevda. 
    """
    test_font = pygame.font.Font(None, 25)
    
    title_surface=test_font.render("score: " + str(score_value), False,"Gold")
    title_surface_rect=title_surface.get_rect(midleft=(20,25))
    
    title_surface_2 = test_font.render("last score: " + str(last_score_value), False, "Gold")
    title_surface_rect_2 = title_surface_2.get_rect(midleft=(20, 50))
    
    title_surface_3 = test_font.render("generation: " + str(generation), False, "Gold")
    title_surface_rect_3 = title_surface_3.get_rect(midleft=(170, 25))
    
    title_surface_4 = test_font.render("highscore: " + str(highscore_value), False, "Gold")
    title_surface_rect_4 = title_surface_4.get_rect(midleft=(170, 50))
   
    title_surface_5 = test_font.render("average fittnes: " + str(average_fitness), False, "Gold")
    title_surface_rect_5 = title_surface_5.get_rect(midleft=(20, 75))

    #visar samtliga värden
    screen.blit(title_surface_2, title_surface_rect_2)
    screen.blit(title_surface,title_surface_rect)
    screen.blit(title_surface_3, title_surface_rect_3)
    screen.blit(title_surface_4, title_surface_rect_4)
    screen.blit(title_surface_5, title_surface_rect_5)
    
def main():
    """ Detta är den huvudsakliga programmet där alla relevanta mekanismer körs. Den sker dock
        inte i isolation utan bygger på programmets samtliga filer i ett komplex samband
    """
  
    # parametrar som jag använder för att spåra framgången av den nuvarande körning
    pipes_spawn_time = -1
    score = 0
    high_score = 0
    last_score = 0
    average_score = 0

    while True:
        quit_game(population.fitness_list,population.death_place_list,population.weight_st_variation_list,population.generation)
        
        # Ritar ut banans komponenter; Ground, pipes och bakgrund
        config.window.fill((0, 0, 0))
        config.ground.draw(config.window)
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 250
        pipes_spawn_time -= 1.1
        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        # Visar och upptaderar samtliga spelare eller utför den naturlig selektionen; baserat på om alla lever.
        if not population.extinct():
            population.update_live_players()
            score+=1
            game_menu(score, config.window, high_score, population.generation, last_score,average_score)
            
            # manuell trigga selection, vid 7000 frames överlevda
            if pygame.key.get_pressed()[pygame.K_a] or score>=7000:
                for p in population.players:
                    p.alive=False
                    p.death_place=p.lifespan
        else:
            config.pipes.clear()  
            pipes_spawn_time = -1
            population.natural_selection()
            if score>high_score:
                high_score=score
            last_score=score
            score = 0
            average_score=population.median_fitness

       # uptaderar skärmen. Utan nedtryckning visas inget.
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            clock.tick(120 )
            pygame.display.flip()
        else:
            pass
main()
