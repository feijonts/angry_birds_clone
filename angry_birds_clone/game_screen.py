import pygame
import random
import math
import os
import sys

class Bird:
    def __init__(self, image_path, screen, settings):
        image_full_path = os.path.join(os.path.dirname(__file__), image_path)
        self.original_image = pygame.image.load(image_full_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(100, screen.get_height() - 100))
        self.screen = screen
        self.settings = settings
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.is_dragging = False
        self.is_launched = False
        self.hit_pig = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.start_pos = pygame.math.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
                self.is_launched = True
                self.hit_pig = False
                end_pos = pygame.math.Vector2(event.pos)
                direction_vector = self.start_pos - end_pos
                force_magnitude = direction_vector.length()

                if force_magnitude > self.settings.max_force:
                    direction_vector = direction_vector.normalize() * self.settings.max_force

                self.velocity = direction_vector * 0.3
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            current_pos = pygame.math.Vector2(event.pos)
            self.position = self.start_pos + (current_pos - self.start_pos)
            self.position.x = min(max(self.position.x, 50), 150)
            self.position.y = min(max(self.position.y, self.screen.get_height() - 150), self.screen.get_height() - 50)
            self.rect.center = (int(self.position.x), int(self.position.y))

    def apply_gravity(self, planets):
        for planet in planets:
            direction = planet.position - self.position
            distance = direction.length()
            if distance < planet.influence_radius:
                if distance == 0:
                    continue
                direction = direction.normalize()
                force_magnitude = planet.gravity_strength * 50 / distance

                random_offset = random.uniform(-0.5, 0.5)
                force_direction = pygame.math.Vector2(direction.x, direction.y + random_offset).normalize()
                
                force = force_direction * force_magnitude
                if planet.is_repulsive:
                    force = -force

                self.velocity += force * 0.5

    def update(self, planets, pigs):
        if self.is_launched:
            self.acceleration = pygame.math.Vector2(0, 0.5)
            self.apply_gravity(planets)

            self.velocity += self.acceleration
            self.velocity *= 0.99
            self.position += self.velocity
            self.angle = (self.angle - self.velocity.x * 2) % 360

            self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
            self.image = pygame.transform.rotate(self.original_image, self.angle)

            for pig in pigs:
                if self.rect.colliderect(pig.rect):
                    pigs.remove(pig)
                    self.hit_pig = True

            if self.rect.right < 0 or self.rect.left > self.screen.get_width() or \
               self.rect.bottom < 0 or self.rect.top > self.screen.get_height():
                if not self.hit_pig:
                    self.settings.lives -= 1
                self.settings.attempts -= 1
                self.reset_position()

    def reset_position(self):
        self.position = pygame.math.Vector2(100, self.screen.get_height() - 100)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.rect.center = (100, self.screen.get_height() - 100)
        self.is_launched = False

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

class Planet:
    def __init__(self, image_path, position, gravity_strength, is_repulsive, screen):
        image_full_path = os.path.join(os.path.dirname(__file__), image_path)
        self.image = pygame.image.load(image_full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.position = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(center=self.position)
        self.gravity_strength = gravity_strength
        self.is_repulsive = is_repulsive
        self.influence_radius = 50
        self.screen = screen

    def draw(self):
        red_transparent = pygame.Surface((self.influence_radius * 2, self.influence_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(red_transparent, (255, 0, 0, 100), (self.influence_radius, self.influence_radius), self.influence_radius)
        self.screen.blit(red_transparent, (self.position.x - self.influence_radius, self.position.y - self.influence_radius))
        self.screen.blit(self.image, self.rect.topleft)

class Pig:
    def __init__(self, image_path, position, screen):
        image_full_path = os.path.join(os.path.dirname(__file__), image_path)
        self.image = pygame.image.load(image_full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.position = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(center=self.position)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

class GameScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.bird = Bird(os.path.join('assets', 'bird.png'), screen, settings)
        self.planets = self.create_planets()
        self.pigs = self.create_pigs()
        self.heart_image = pygame.image.load(os.path.join('assets', 'heart.png')).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        self.settings.attempts = len(self.pigs) * 2
        self.settings.lives = len(self.pigs) * 2

    def create_planets(self):
        planets = []
        num_planets = random.randint(1, 2)
        min_distance = 200
        for _ in range(num_planets):
            valid_position = False
            while not valid_position:
                x = random.randint(self.settings.screen_width // 4, self.settings.screen_width - 100)
                y = random.randint(50, self.settings.screen_height - 150)
                valid_position = all(math.hypot(x - planet.position.x, y - planet.position.y) > min_distance for planet in planets)
            gravity_strength = random.uniform(1, 3)
            is_repulsive = random.choice([True, False])
            planets.append(Planet(os.path.join('assets', 'planet.png'), (x, y), gravity_strength, is_repulsive, self.screen))
        return planets

    def create_pigs(self):
        pigs = []
        num_pigs = random.randint(2, 4)
        min_distance = 100
        spawn_height_start = int(self.settings.screen_height * 2 / 3)  # Spawns no terço inferior da tela
        for _ in range(num_pigs):
            valid_position = False
            while not valid_position:
                x = random.randint(self.settings.screen_width // 3, self.settings.screen_width - 50)
                y = random.randint(spawn_height_start, self.settings.screen_height - 50)
                valid_position = all(math.hypot(x - pig.position.x, y - pig.position.y) > min_distance for pig in pigs)
            pigs.append(Pig(os.path.join('assets', 'porco.png'), (x, y), self.screen))
        return pigs

    def handle_event(self, event):
        self.bird.handle_event(event)

    def update(self):
        self.bird.update(self.planets, self.pigs)
        if not self.pigs:
            self.restart_game()
        if self.settings.lives <= 0:
            return False
        return True

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        for planet in self.planets:
            planet.draw()
        for pig in self.pigs:
            pig.draw()
        self.bird.draw()
        self.draw_lives()

    def draw_lives(self):
        for i in range(self.settings.lives):
            x = 10 + i * 40
            self.screen.blit(self.heart_image, (x, 10))

    def restart_game(self):
        self.planets = self.create_planets()
        self.pigs = self.create_pigs()
        self.settings.attempts = len(self.pigs) * 2
        self.settings.lives = len(self.pigs) * 2
        self.bird.reset_position()