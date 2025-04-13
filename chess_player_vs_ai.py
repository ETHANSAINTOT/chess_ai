#!/usr/bin/env python3

## EPITECH PROJECT, 2025
## G-INN-220:chess_ai
## File description:
## chess_1v1.py

import pygame
import sys
import os
import random
import time
from threading import Thread

# Importer les pièces d'échecs du module 1v1
from chess_1v1 import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King, CASE_SIZE, LIGHT_BROWN, DARK_BROWN

class ChessAIGame:
    def __init__(self):
        # Initialisation de pygame
        pygame.init()
        
        # Dimensions
        self.case_size = CASE_SIZE
        self.board_size = 8 * self.case_size
        
        # Ajout d'une zone d'information sur le côté
        self.info_width = 200
        self.window_size = (self.board_size + self.info_width, self.board_size)
        
        # Couleurs
        self.light_brown = LIGHT_BROWN
        self.dark_brown = DARK_BROWN
        self.highlight_color = (100, 255, 100)  # Vert clair pour les mouvements possibles
        self.check_color = (255, 0, 0)  # Rouge pour indiquer échec
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Jeu d'Échecs - Mode Joueur vs IA")
        
        # Police pour les textes
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        # État du jeu
        self.init_board()
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = "white"  # Les blancs (joueur) commencent
        self.game_over = False
        self.check_status = {"white": False, "black": False}
        self.winner = None
        self.promotion_message = None
        self.promotion_timer = 0
        
        # Variables spécifiques à l'IA
        self.ai_thinking = False
        self.ai_message = ""
        self.ai_difficulty = "medium"  # Par défaut: facile, medium, difficile
        self.skill_description = ""
        self.skill_description_entered = False
        self.input_active = True
        self.text_input = ""
        self.input_rect = pygame.Rect(50, 200, 500, 50)
        
        # Pour le suivi du temps de réflexion de l'IA
        self.ai_think_time_min = 1.0  # Temps minimum de réflexion en secondes
        self.ai_think_time_max = 3.0  # Temps maximum de réflexion en secondes
    
    def init_board(self):
        # Initialisation du plateau (None = case vide)
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Placement des pions
        for col in range(8):
            self.board[1][col] = Pawn("black", (1, col))
            self.board[6][col] = Pawn("white", (6, col))
        
        # Placement des tours
        self.board[0][0] = Rook("black", (0, 0))
        self.board[0][7] = Rook("black", (0, 7))
        self.board[7][0] = Rook("white", (7, 0))
        self.board[7][7] = Rook("white", (7, 7))
        
        # Placement des cavaliers
        self.board[0][1] = Knight("black", (0, 1))
        self.board[0][6] = Knight("black", (0, 6))
        self.board[7][1] = Knight("white", (7, 1))
        self.board[7][6] = Knight("white", (7, 6))
        
        # Placement des fous
        self.board[0][2] = Bishop("black", (0, 2))
        self.board[0][5] = Bishop("black", (0, 5))
        self.board[7][2] = Bishop("white", (7, 2))
        self.board[7][5] = Bishop("white", (7, 5))
        
        # Placement des reines
        self.board[0][3] = Queen("black", (0, 3))
        self.board[7][3] = Queen("white", (7, 3))
        
        # Placement des rois
        self.board[0][4] = King("black", (0, 4))
        self.board[7][4] = King("white", (7, 4))
    
    def draw_board(self):
        # Dessiner l'échiquier
        for row in range(8):
            for col in range(8):
                # Alternance des couleurs
                if (row + col) % 2 == 0:
                    color = self.light_brown
                else:
                    color = self.dark_brown
                
                # Position de la case
                rect = pygame.Rect(col * self.case_size, row * self.case_size, 
                                  self.case_size, self.case_size)
                pygame.draw.rect(self.screen, color, rect)
                
                # Dessiner la pièce sur cette case
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(piece.image, rect)
        
        # Surligner la pièce sélectionnée
        if self.selected_piece:
            row, col = self.selected_piece.position
            rect = pygame.Rect(col * self.case_size, row * self.case_size, 
                              self.case_size, self.case_size)
            # Dessiner un contour plus épais
            pygame.draw.rect(self.screen, self.highlight_color, rect, 3)
            
            # Surligner les mouvements valides
            for move_row, move_col in self.valid_moves:
                rect = pygame.Rect(move_col * self.case_size, move_row * self.case_size, 
                                  self.case_size, self.case_size)
                # Dessiner un cercle au centre de la case pour indiquer un mouvement possible
                pygame.draw.circle(self.screen, self.highlight_color, 
                                  rect.center, self.case_size // 6)
        
        # Dessiner la zone d'information
        self.draw_info_panel()
    
    def draw_info_panel(self):
        # Zone d'information sur le côté droit
        info_rect = pygame.Rect(self.board_size, 0, self.info_width, self.board_size)
        pygame.draw.rect(self.screen, LIGHT_BROWN, info_rect)
        pygame.draw.line(self.screen, DARK_BROWN, (self.board_size, 0), 
                        (self.board_size, self.board_size), 2)
        
        # Afficher le titre
        title = self.title_font.render("JEU D'ÉCHECS", True, DARK_BROWN)
        self.screen.blit(title, (self.board_size + 20, 20))
        
        # Afficher le joueur actuel
        current_player_text = f"Tour: {'Joueur (Blanc)' if self.current_player == 'white' else 'IA (Noir)'}"
        player_surf = self.font.render(current_player_text, True, DARK_BROWN)
        self.screen.blit(player_surf, (self.board_size + 20, 60))
        
        # Afficher le niveau de difficulté de l'IA
        diff_text = f"Niveau IA: {self.ai_difficulty}"
        diff_surf = self.font.render(diff_text, True, DARK_BROWN)
        self.screen.blit(diff_surf, (self.board_size + 20, 90))
        
        # Message de l'IA
        if self.ai_thinking:
            ai_text = "IA réfléchit..."
            ai_surf = self.font.render(ai_text, True, (0, 0, 200))  # Bleu
            self.screen.blit(ai_surf, (self.board_size + 20, 120))
        elif self.ai_message:
            ai_surf = self.font.render(self.ai_message, True, (0, 0, 200))  # Bleu
            self.screen.blit(ai_surf, (self.board_size + 20, 120))
        
        # Afficher le statut d'échec
        y_offset = 150
        if self.check_status["white"]:
            check_text = "Joueur: Échec au roi!"
            check_surf = self.font.render(check_text, True, self.check_color)
            self.screen.blit(check_surf, (self.board_size + 20, y_offset))
            y_offset += 30
        
        if self.check_status["black"]:
            check_text = "IA: Échec au roi!"
            check_surf = self.font.render(check_text, True, self.check_color)
            self.screen.blit(check_surf, (self.board_size + 20, y_offset))
            y_offset += 30
        
        # Afficher le message de promotion (si présent)
        if self.promotion_message and self.promotion_timer > 0:
            self.promotion_timer -= 1
            promo_surf = self.font.render(self.promotion_message, True, (0, 128, 0))  # Vert
            self.screen.blit(promo_surf, (self.board_size + 20, y_offset))
            y_offset += 30
        
        # Afficher le gagnant ou la fin de partie
        if self.game_over:
            if self.winner:
                winner_text = f"{'Joueur' if self.winner == 'white' else 'IA'} a gagné!"
                game_over_surf = self.title_font.render(winner_text, True, DARK_BROWN)
                self.screen.blit(game_over_surf, (self.board_size + 20, y_offset))
                y_offset += 40
            else:
                draw_text = "Match nul!"
                game_over_surf = self.title_font.render(draw_text, True, DARK_BROWN)
                self.screen.blit(game_over_surf, (self.board_size + 20, y_offset))
                y_offset += 40
                
            # Bouton pour revenir au menu
            back_text = "Retour au menu"
            back_surf = self.font.render(back_text, True, DARK_BROWN)
            back_rect = pygame.Rect(self.board_size + 20, self.board_size - 50, 160, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), back_rect, 0, 5)
            pygame.draw.rect(self.screen, DARK_BROWN, back_rect, 2, 5)
            self.screen.blit(back_surf, (back_rect.x + 20, back_rect.y + 5))
            
            # Bouton pour rejouer
            replay_text = "Nouvelle partie"
            replay_surf = self.font.render(replay_text, True, DARK_BROWN)
            replay_rect = pygame.Rect(self.board_size + 20, self.board_size - 100, 160, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), replay_rect, 0, 5)
            pygame.draw.rect(self.screen, DARK_BROWN, replay_rect, 2, 5)
            self.screen.blit(replay_surf, (replay_rect.x + 20, replay_rect.y + 5))
    
    def draw_skill_input(self):
        # Remplir l'écran avec une couleur de fond
        self.screen.fill(LIGHT_BROWN)
        
        # Dessiner le titre
        title = self.title_font.render("Niveau aux échecs", True, DARK_BROWN)
        self.screen.blit(title, (250, 100))
        
        # Instructions
        instruction = self.font.render("Décrivez votre niveau aux échecs en quelques mots:", True, DARK_BROWN)
        self.screen.blit(instruction, (100, 160))
        
        # Boîte de saisie
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 0, 5)
        pygame.draw.rect(self.screen, DARK_BROWN, self.input_rect, 2, 5)
        
        # Texte saisi
        input_surface = self.font.render(self.text_input, True, DARK_BROWN)
        self.screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 15))
        
        # Bouton de validation
        validate_rect = pygame.Rect(250, 270, 100, 40)
        validate_color = (100, 200, 100) if len(self.text_input) > 5 else (150, 150, 150)
        pygame.draw.rect(self.screen, validate_color, validate_rect, 0, 5)
        pygame.draw.rect(self.screen, DARK_BROWN, validate_rect, 2, 5)
        validate_text = self.font.render("Valider", True, DARK_BROWN)
        self.screen.blit(validate_text, (validate_rect.x + 20, validate_rect.y + 10))
        
        # Instructions supplémentaires
        examples = [
            "Exemples de descriptions:",
            "- \"Je suis débutant, je connais à peine les règles\"",
            "- \"Je joue occasionnellement avec des amis\"",
            "- \"Je suis un joueur de club, j'ai un classement ELO\"",
            "- \"Grand maître international\""
        ]
        
        for i, example in enumerate(examples):
            example_surf = self.font.render(example, True, DARK_BROWN)
            self.screen.blit(example_surf, (100, 330 + i * 30))
    
    def handle_skill_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si le clic est sur le bouton de validation
            validate_rect = pygame.Rect(250, 270, 100, 40)
            if validate_rect.collidepoint(event.pos) and len(self.text_input) > 5:
                self.skill_description = self.text_input
                self.skill_description_entered = True
                self.determine_ai_difficulty()
                return
            
            # Vérifier si le clic est dans la zone de saisie
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
        
        elif event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN and len(self.text_input) > 5:
                    self.skill_description = self.text_input
                    self.skill_description_entered = True
                    self.determine_ai_difficulty()
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    # Limiter la longueur du texte à 40 caractères
                    if len(self.text_input) < 40:
                        self.text_input += event.unicode
    
    def determine_ai_difficulty(self):
        """
        Détermine la difficulté de l'IA basée sur la description du joueur.
        Dans une vraie implémentation, vous pourriez utiliser une API externe,
        mais ici nous utilisons une logique simple basée sur des mots-clés.
        """
        description = self.skill_description.lower()
        
        # Mots-clés pour différents niveaux
        beginner_keywords = ["débutant", "novice", "apprendre", "règles", "commence", "nul", "perds"]
        intermediate_keywords = ["occasion", "amateur", "moyen", "intermédiaire", "parfois"]
        advanced_keywords = ["avancé", "club", "tournoi", "elo", "compétition", "fort", "expert"]
        master_keywords = ["maître", "professionnel", "champion", "international", "fide"]
        
        # Compter les occurrences de chaque catégorie
        beginner_count = sum(1 for word in beginner_keywords if word in description)
        intermediate_count = sum(1 for word in intermediate_keywords if word in description)
        advanced_count = sum(1 for word in advanced_keywords if word in description)
        master_count = sum(1 for word in master_keywords if word in description)
        
        # Déterminer la difficulté en fonction du plus grand nombre d'occurrences
        max_count = max(beginner_count, intermediate_count, advanced_count, master_count)
        
        if max_count == beginner_count and beginner_count > 0:
            self.ai_difficulty = "facile"
            self.ai_think_time_min = 0.5
            self.ai_think_time_max = 1.5
        elif max_count == intermediate_count and intermediate_count > 0:
            self.ai_difficulty = "moyen"
            self.ai_think_time_min = 1.0
            self.ai_think_time_max = 2.0
        elif max_count == advanced_count and advanced_count > 0:
            self.ai_difficulty = "difficile"
            self.ai_think_time_min = 1.5
            self.ai_think_time_max = 3.0
        elif max_count == master_count and master_count > 0:
            self.ai_difficulty = "expert"
            self.ai_think_time_min = 2.0
            self.ai_think_time_max = 4.0
        else:
            # Par défaut si aucun mot-clé n'est trouvé
            self.ai_difficulty = "moyen"
            self.ai_think_time_min = 1.0
            self.ai_think_time_max = 2.0
        
        self.ai_message = f"Difficulté ajustée à: {self.ai_difficulty}"
    
    def handle_click(self, pos):
        if self.game_over:
            # Gestion des clics sur les boutons de fin de partie
            if self.board_size <= pos[0] <= self.window_size[0]:
                # Bouton "Retour au menu"
                if self.board_size - 50 <= pos[1] <= self.board_size - 20:
                    return "menu"
                # Bouton "Nouvelle partie"
                elif self.board_size - 100 <= pos[1] <= self.board_size - 70:
                    self.__init__()  # Réinitialiser le jeu
                    return "continue"
            return "continue"
        
        # Si c'est le tour de l'IA ou si l'IA réfléchit, ignorer les clics
        if self.current_player == "black" or self.ai_thinking:
            return "continue"
        
        # Vérifier si le clic est dans l'échiquier
        if pos[0] >= self.board_size:
            return "continue"  # Clic dans la zone d'information, ignorer
        
        # Convertir la position du clic en coordonnées du plateau
        col = pos[0] // self.case_size
        row = pos[1] // self.case_size
        
        # Vérifier si une pièce est déjà sélectionnée
        if self.selected_piece:
            # Vérifier si le mouvement est valide
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.valid_moves = []
                
                # Vérifier les conditions d'échec après le mouvement
                self.check_for_check()
                
                # Vérifier l'échec et mat
                if self.is_checkmate():
                    self.game_over = True
                    self.winner = "white"  # Le joueur a gagné
                elif not self.game_over:
                    # C'est maintenant le tour de l'IA
                    self.ai_thinking = True
                    # Lancer l'IA dans un thread séparé pour ne pas bloquer l'interface
                    t = Thread(target=self.ai_make_move)
                    t.daemon = True
                    t.start()
            else:
                # Clic sur une autre case, annuler la sélection ou sélectionner une autre pièce
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    self.selected_piece = piece
                    self.valid_moves = self.get_legal_moves(piece)
                else:
                    self.selected_piece = None
                    self.valid_moves = []
        else:
            # Aucune pièce sélectionnée, en sélectionner une si possible
            piece = self.board[row][col]
            if piece and piece.color == self.current_player:
                self.selected_piece = piece
                self.valid_moves = self.get_legal_moves(piece)
        
        return "continue"
    
    def ai_make_move(self):
        """
        Méthode exécutée dans un thread séparé pour faire jouer l'IA.
        """
        # Simuler un temps de réflexion pour l'IA
        think_time = random.uniform(self.ai_think_time_min, self.ai_think_time_max)
        time.sleep(think_time)
        
        # Choisir un mouvement selon la difficulté
        move = self.choose_ai_move()
        
        # Effectuer le mouvement
        if move:
            piece, (to_row, to_col) = move
            self.move_piece(piece, (to_row, to_col))
            
            # Vérifier les conditions d'échec après le mouvement
            self.check_for_check()
            
            # Vérifier l'échec et mat
            if self.is_checkmate():
                self.game_over = True
                self.winner = "black"  # L'IA a gagné
        else:
            # Aucun mouvement possible, l'IA a perdu
            self.game_over = True
            self.winner = "white"
        
        self.ai_thinking = False
        self.ai_message = "IA a joué"
    
    def choose_ai_move(self):
        """
        Choisi un coup pour l'IA en fonction de la difficulté.
        """
        # Collecter tous les mouvements possibles pour l'IA (pièces noires)
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == "black":
                    legal_moves = self.get_legal_moves(piece)
                    for move in legal_moves:
                        all_moves.append((piece, move))
        
        if not all_moves:
            return None  # Aucun mouvement possible
        
        # Différents algorithmes selon la difficulté
        if self.ai_difficulty == "facile":
            # Mouvement aléatoire avec probabilité élevée (80%)
            # ou mouvement intelligent basique (20%)
            if random.random() < 0.8:
                return random.choice(all_moves)
            else:
                return self.choose_basic_strategic_move(all_moves)
        
        elif self.ai_difficulty == "moyen":
            # Mouvement aléatoire avec probabilité moyenne (40%)
            # ou mouvement intelligent basique (60%)
            if random.random() < 0.4:
                return random.choice(all_moves)
            else:
                return self.choose_basic_strategic_move(all_moves)
        
        elif self.ai_difficulty == "difficile":
            # Mouvement aléatoire avec faible probabilité (10%)
            # ou mouvement intelligent avancé (90%)
            if random.random() < 0.1:
                return random.choice(all_moves)
            else:
                return self.choose_advanced_strategic_move(all_moves)
        
        elif self.ai_difficulty == "expert":
            # Toujours choisir le meilleur mouvement disponible
            return self.choose_advanced_strategic_move(all_moves)
        
        # Par défaut, retourner un mouvement aléatoire
        return random.choice(all_moves)
    
    def choose_basic_strategic_move(self, all_moves):
        """
        Stratégie de base pour l'IA: capture si possible, sinon mouvement aléatoire.
        """
        # Vérifier s'il y a des mouvements qui permettent de capturer une pièce
        capture_moves = []
        for piece, move in all_moves:
            row, col = move
            if self.board[row][col] is not None:
                # Évaluer la valeur de la pièce capturée
                captured_piece = self.board[row][col]
                value = self.get_piece_value(captured_piece)
                capture_moves.append((piece, move, value))
        
        if capture_moves:
            # Prendre la capture qui offre la pièce de plus grande valeur
            capture_moves.sort(key=lambda x: x[2], reverse=True)
            return (capture_moves[0][0], capture_moves[0][1])
        
        # Si pas de capture, choisir un mouvement aléatoire
        return random.choice(all_moves)
    
    def choose_advanced_strategic_move(self, all_moves):
        """
        Stratégie avancée pour l'IA: évaluer chaque mouvement et choisir le meilleur.
        """
        best_move = None
        best_score = float('-inf')
        
        for piece, move in all_moves:
            # Simuler le mouvement
            old_row, old_col = piece.position
            to_row, to_col = move
            captured_piece = self.board[to_row][to_col]
            
            # Effectuer le mouvement temporairement
            self.board[old_row][old_col] = None
            self.board[to_row][to_col] = piece
            old_position = piece.position
            piece.position = (to_row, to_col)
            
            # Évaluer la position
            score = self.evaluate_board()
            
            # Annuler le mouvement
            piece.position = old_position
            self.board[old_row][old_col] = piece
            self.board[to_row][to_col] = captured_piece
            
            # Mettre à jour le meilleur mouvement
            if score > best_score:
                best_score = score
                best_move = (piece, move)
        
        return best_move
    
    def evaluate_board(self):
        """
        Évalue la position actuelle du plateau du point de vue de l'IA (noir).
        Une valeur positive indique un avantage pour l'IA.
        """
        score = 0
        
        # Valeur des pièces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    value = self.get_piece_value(piece)
                    if piece.color == "black":
                        score += value
                    else:
                        score -= value
        
        # Bonus pour le contrôle du centre
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            piece = self.board[row][col]
            if piece:
                if piece.color == "black":
                    score += 0.5
                else:
                    score -= 0.5
        
        # Bonus pour les pièces développées (simplifié)
        for col in range(8):
            # Vérifier si les pions ont été déplacés
            if self.board[1][col] is None or self.board[1][col].piece_type != "pawn":
                score += 0.2  # Bonus pour les pions développés
            
            if self.board[6][col] is None or self.board[6][col].piece_type != "pawn":
                score -= 0.2  # Malus pour les pions adverses développés
        
        return score
    
    def get_piece_value(self, piece):
        """
        Retourne la valeur d'une pièce d'échecs.
        """
        if piece is None:
            return 0
        
        if piece.piece_type == "pawn":
            return 1
        elif piece.piece_type == "knight" or piece.piece_type == "bishop":
            return 3
        elif piece.piece_type == "rook":
            return 5
        elif piece.piece_type == "queen":
            return 9
        elif piece.piece_type == "king":
            return 100  # Valeur élevée pour le roi
        
        return 0
    
    def move_piece(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position
        piece.has_moved = True
        if piece.piece_type == "pawn":
            if (piece.color == "white" and new_row == 0) or (piece.color == "black" and new_row == 7):
                self.board[new_row][new_col] = Queen(piece.color, (new_row, new_col))
                self.promotion_message = f"Promotion du pion en Dame!"
                self.promotion_timer = 100
        self.current_player = "black" if self.current_player == "white" else "white"
    
    def get_legal_moves(self, piece):
        moves = piece.get_valid_moves(self.board)
        legal_moves = []
        for move in moves:
            if not self.would_be_in_check_after_move(piece, move):
                legal_moves.append(move)
        return legal_moves
    
    def would_be_in_check_after_move(self, piece, move):
        old_row, old_col = piece.position
        new_row, new_col = move
        old_piece_at_target = self.board[new_row][new_col]
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = move
        king_position = self.find_king(piece.color)
        is_in_check = self.is_position_attacked(king_position, 
                                              "black" if piece.color == "white" else "white")
        self.board[old_row][old_col] = piece
        self.board[new_row][new_col] = old_piece_at_target
        piece.position = (old_row, old_col)
        return is_in_check
    
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type == "king" and piece.color == color:
                    return (row, col)
        return None
    
    def is_position_attacked(self, position, by_color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == by_color:
                    if piece.piece_type == "king":
                        king_row, king_col = piece.position
                        pos_row, pos_col = position
                        if abs(king_row - pos_row) <= 1 and abs(king_col - pos_col) <= 1:
                            return True
                    else:
                        moves = piece.get_valid_moves(self.board)
                        if position in moves:
                            return True
        return False
    
    def check_for_check(self):
        white_king_pos = self.find_king("white")
        black_king_pos = self.find_king("black")
        self.check_status["white"] = self.is_position_attacked(white_king_pos, "black")
        self.check_status["black"] = self.is_position_attacked(black_king_pos, "white")
    
    def is_checkmate(self):
        color = self.current_player
        if not self.check_status[color]:
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    legal_moves = self.get_legal_moves(piece)
                    if legal_moves:
                        return False
        return True
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            if not self.skill_description_entered:
                self.draw_skill_input()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                    self.handle_skill_input(event)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            result = self.handle_click(event.pos)
                            if result == "menu":
                                return "menu"
                self.draw_board()
            pygame.display.flip()
            clock.tick(60)
        return "quit"

def main():
    game = ChessAIGame()
    result = game.run()
    pygame.quit()
    return result

if __name__ == "__main__":
    main()





