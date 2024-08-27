import pygame

class DefeatScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.active = False
        self.font_title = pygame.font.SysFont(None, int(settings.screen_width * 0.08))
        self.font_button = pygame.font.SysFont(None, int(settings.screen_width * 0.05))
        self.text_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.button_color = (128, 0, 0)
        self.button_hover_color = (180, 0, 0)
        self.restart_button = self.font_button.render("Reiniciar", True, self.text_color)
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.center = (settings.screen_width // 2, settings.screen_height * 0.75)
        self.title = "Você Perdeu!"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button_rect.collidepoint(mouse_pos):
                self.active = False
                self.settings.restart_game = True

    def draw(self):
        self.screen.fill(self.bg_color)
        
        title_surface = self.font_title.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height * 0.3))
        self.screen.blit(title_surface, title_rect)
        
        pygame.draw.rect(self.screen, self.button_color, self.restart_button_rect.inflate(20, 10))
        self.screen.blit(self.restart_button, self.restart_button_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.restart_button_rect.collidepoint(mouse_pos):
            self.restart_button = self.font_button.render("Reiniciar", True, self.text_color, self.button_hover_color)
        else:
            self.restart_button = self.font_button.render("Reiniciar", True, self.text_color, self.button_color)