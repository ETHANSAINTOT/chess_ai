#!/usr/bin/env python3

## EPITECH PROJECT, 2025
## G-INN-220:chess_ai
## File description:
## menu_update.py

import pygame
import sys
import os

# Créer le dossier assets s'il n'existe pas
os.makedirs("assets", exist_ok=True)

# Importer le module du jeu 1v1
import chess_1v1

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (210, 180, 140)
DARK_BROWN = (139, 69, 19)
HOVER_COLOR = (180, 150, 100)
TEXT_COLOR = (50, 30, 10)

# Création de la fenêtre
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Jeu d'Échecs - Menu Principal")

# Police d'écriture
title_font = pygame.font.SysFont("Arial", 48, bold=True)
button_font = pygame.font.SysFont("Arial", 28)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        # Dessiner le bouton avec la couleur appropriée
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, 0, 10)  # Bouton avec coins arrondis
        pygame.draw.rect(surface, DARK_BROWN, self.rect, 2, 10)  # Bordure
        
        # Dessiner le texte du bouton
        text_surface = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

def draw_menu():
    # Remplir l'écran avec une couleur de fond
    screen.fill(LIGHT_BROWN)
    
    # Dessiner le titre
    title_surface = title_font.render("Jeu d'Échecs", True, DARK_BROWN)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH//2, 80))
    screen.blit(title_surface, title_rect)
    
    # Dessiner les boutons
    for button in buttons:
        button.draw(screen)

# Créer les boutons
button_width = 300
button_height = 60
button_spacing = 30
start_y = 180

buttons = [
    Button((WINDOW_WIDTH - button_width) // 2, start_y, 
           button_width, button_height, "1v1", LIGHT_BROWN, HOVER_COLOR),
    Button((WINDOW_WIDTH - button_width) // 2, start_y + button_height + button_spacing, 
           button_width, button_height, "Player vs AI", LIGHT_BROWN, HOVER_COLOR),
    Button((WINDOW_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), 
           button_width, button_height, "Player vs AI Progressive", LIGHT_BROWN, HOVER_COLOR)
]

def main_menu():
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_clicked = True
        
        # Vérifier les survols et les clics de boutons
        for i, button in enumerate(buttons):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                if i == 0:
                    print("Mode 1v1 sélectionné")
                    return "1v1"
                elif i == 1:
                    print("Mode Player vs AI sélectionné")
                    return "player_vs_ai"
                elif i == 2:
                    print("Mode Player vs AI Progressive sélectionné")
                    return "player_vs_ai_progressive"
        
        # Dessiner le menu
        draw_menu()
        
        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)

# Fonction principale
def main():
    running = True
    
    while running:
        game_mode = main_menu()
        
        if game_mode == "1v1":
            print("Lancement du mode 1v1...")
            # Lancer le mode 1v1
            try:
                result = chess_1v1.main()
                if result == "quit":
                    running = False
                # Si result == "menu", on reviendra au menu
            except Exception as e:
                print(f"Erreur lors du lancement du mode 1v1: {e}")
                # En cas d'erreur, on continue à exécuter le menu
        
        elif game_mode == "player_vs_ai":
            # TODO: Implémenter le mode Player vs AI
            print("Mode Player vs AI - Pas encore implémenté")
        
        elif game_mode == "player_vs_ai_progressive":
            # TODO: Implémenter le mode Player vs AI Progressive
            print("Mode Player vs AI Progressive - Pas encore implémenté")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()