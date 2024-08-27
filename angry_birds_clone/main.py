import pygame
from .settings import Settings
from .game_screen import GameScreen
from .menu_screen import MenuScreen
from .defeat_screen import DefeatScreen

def main():
    pygame.init()
    
    settings = Settings()
    settings.restart_game = False
    
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Angry Birds")
    
    menu_screen = MenuScreen(screen, settings)
    game_screen = GameScreen(screen, settings)
    defeat_screen = DefeatScreen(screen, settings)
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if menu_screen.active:
                menu_screen.handle_event(event)
            elif defeat_screen.active:
                defeat_screen.handle_event(event)
            else:
                game_screen.handle_event(event)
        
        if menu_screen.active:
            menu_screen.update()
            menu_screen.draw()
        elif defeat_screen.active:
            defeat_screen.update()
            defeat_screen.draw()
            if settings.restart_game:
                settings.restart_game = False
                game_screen = GameScreen(screen, settings)
                defeat_screen.active = False
        else:
            if not game_screen.update():
                defeat_screen.active = True
            else:
                game_screen.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()