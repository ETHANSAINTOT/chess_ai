#!/usr/bin/env python3

## EPITECH PROJECT, 2025
## G-INN-220:chess_ai
## File description:
## chess_1v1.py

import pygame
import sys
import os

class ChessPiece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.has_moved = False
        self.image = None
        self.load_image()
    
    def load_image(self):
        # Charger l'image correspondant à la pièce
        image_name = f"{self.piece_type}_{self.color}.png"
        try:
            # Supposons que les images sont dans un dossier "assets"
            image_path = os.path.join("assets", image_name)
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (CASE_SIZE, CASE_SIZE))
        except:
            print(f"Impossible de charger l'image: {image_path}")
            # Créer une image de remplacement si l'image ne peut pas être chargée
            self.image = pygame.Surface((CASE_SIZE, CASE_SIZE))
            self.image.fill((255, 0, 0))  # Rouge pour indiquer une erreur
    
    def get_valid_moves(self, board):
        # Cette méthode sera remplacée dans les classes dérivées
        return []

class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__("pawn", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        direction = -1 if self.color == "white" else 1  # Les pions blancs montent, les noirs descendent
        
        # Avancer d'une case
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            valid_moves.append((row + direction, col))
            
            # Avancer de deux cases depuis la position initiale
            if (self.color == "white" and row == 6) or (self.color == "black" and row == 1):
                if board[row + 2*direction][col] is None:
                    valid_moves.append((row + 2*direction, col))
        
        # Capture en diagonale
        for offset in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + offset < 8:
                target = board[row + direction][col + offset]
                if target is not None and target.color != self.color:
                    valid_moves.append((row + direction, col + offset))
        
        # TODO: Ajouter la prise en passant et la promotion
        return valid_moves

class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__("rook", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        
        # Directions: haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    valid_moves.append((r, c))
                elif board[r][c].color != self.color:
                    valid_moves.append((r, c))
                    break  # On s'arrête après avoir capturé une pièce
                else:
                    break  # On s'arrête si on rencontre une pièce de sa couleur
                r, c = r + dr, c + dc
        
        return valid_moves

class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__("knight", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        
        # Les 8 mouvements possibles du cavalier
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    valid_moves.append((r, c))
        
        return valid_moves

class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__("bishop", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        
        # Directions diagonales: haut-gauche, haut-droite, bas-gauche, bas-droite
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    valid_moves.append((r, c))
                elif board[r][c].color != self.color:
                    valid_moves.append((r, c))
                    break  # On s'arrête après avoir capturé une pièce
                else:
                    break  # On s'arrête si on rencontre une pièce de sa couleur
                r, c = r + dr, c + dc
        
        return valid_moves

class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__("queen", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        
        # Toutes les directions (combinaison de la tour et du fou)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Comme la tour
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Comme le fou
        ]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    valid_moves.append((r, c))
                elif board[r][c].color != self.color:
                    valid_moves.append((r, c))
                    break  # On s'arrête après avoir capturé une pièce
                else:
                    break  # On s'arrête si on rencontre une pièce de sa couleur
                r, c = r + dr, c + dc
        
        return valid_moves

class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__("king", color, position)
    
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        
        # Toutes les directions mais un seul pas
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Orthogonales
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
        ]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    valid_moves.append((r, c))
        
        # TODO: Ajouter le roque
        return valid_moves

class ChessGame:
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
        pygame.display.set_caption("Jeu d'Échecs - Mode 1v1")
        
        # Police pour les textes
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        # État du jeu
        self.init_board()
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = "white"  # Les blancs commencent
        self.game_over = False
        self.check_status = {"white": False, "black": False}
        self.winner = None
        self.promotion_message = None
        self.promotion_timer = 0
        
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
        current_player_text = f"Tour: {'Blancs' if self.current_player == 'white' else 'Noirs'}"
        player_surf = self.font.render(current_player_text, True, DARK_BROWN)
        self.screen.blit(player_surf, (self.board_size + 20, 60))
        
        # Afficher un message sur le mode libre
        mode_text = "Mode libre: mouvements"
        mode_text2 = "sans restrictions"
        mode_surf = self.font.render(mode_text, True, DARK_BROWN)
        mode_surf2 = self.font.render(mode_text2, True, DARK_BROWN)
        self.screen.blit(mode_surf, (self.board_size + 20, 90))
        self.screen.blit(mode_surf2, (self.board_size + 20, 110))
        
        # Afficher le statut d'échec (information seulement)
        y_offset = 140
        if self.check_status["white"]:
            check_text = "Info: Blancs en échec"
            check_surf = self.font.render(check_text, True, self.check_color)
            self.screen.blit(check_surf, (self.board_size + 20, y_offset))
            y_offset += 30
        
        if self.check_status["black"]:
            check_text = "Info: Noirs en échec"
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
                winner_text = f"{'Blancs' if self.winner == 'white' else 'Noirs'} ont gagné!"
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
        
        # Vérifier si le clic est dans l'échiquier
        if pos[0] >= self.board_size:
            return "continue"  # Clic dans la zone d'information, ignorer
        
        # Convertir la position du clic en coordonnées du plateau
        col = pos[0] // self.case_size
        row = pos[1] // self.case_size
        
        # Vérifier si une pièce est déjà sélectionnée
        if self.selected_piece:
            # En mode libre, on permet tous les mouvements si c'est le tour du joueur
            # On vérifie juste que la destination n'est pas occupée par une pièce de la même couleur
            destination_piece = self.board[row][col]
            
            if not destination_piece or destination_piece.color != self.selected_piece.color:
                # Mouvement autorisé en mode libre
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.valid_moves = []
                
                # On continue à vérifier l'échec (pour information seulement)
                self.check_for_check()
                
                # Vérifier l'échec et mat (pour information seulement)
                if self.is_checkmate():
                    self.game_over = True
                    self.winner = "white" if self.current_player == "black" else "black"
            else:
                # Clic sur une pièce de même couleur, changer la sélection
                self.selected_piece = destination_piece
                self.valid_moves = self.get_all_possible_moves(destination_piece)  # Tous les mouvements possibles
        else:
            # Aucune pièce sélectionnée, en sélectionner une si possible
            piece = self.board[row][col]
            if piece and piece.color == self.current_player:
                self.selected_piece = piece
                self.valid_moves = self.get_all_possible_moves(piece)  # Tous les mouvements possibles
        
        return "continue"
    
    def get_all_possible_moves(self, piece):
        """
        Retourne tous les mouvements possibles sans restrictions de règles,
        juste en respectant les limites du plateau et la non-capture des pièces amies.
        """
        row, col = piece.position
        possible_moves = []
        
        # Pour les pions
        if piece.piece_type == "pawn":
            direction = -1 if piece.color == "white" else 1
            
            # Avancer d'une case
            if 0 <= row + direction < 8 and self.board[row + direction][col] is None:
                possible_moves.append((row + direction, col))
                
                # Avancer de deux cases depuis la position initiale
                if ((piece.color == "white" and row == 6) or (piece.color == "black" and row == 1)) and \
                   self.board[row + 2*direction][col] is None:
                    possible_moves.append((row + 2*direction, col))
            
            # Capture en diagonale
            for offset in [-1, 1]:
                if 0 <= row + direction < 8 and 0 <= col + offset < 8:
                    target = self.board[row + direction][col + offset]
                    if target is not None and target.color != piece.color:
                        possible_moves.append((row + direction, col + offset))
        
        # Pour les autres pièces, on utilise leur logique standard mais sans vérifier l'échec
        elif piece.piece_type == "rook":
            # Mouvements horizontaux et verticaux
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] is None:
                        possible_moves.append((r, c))
                    elif self.board[r][c].color != piece.color:
                        possible_moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc
        
        elif piece.piece_type == "knight":
            # Les 8 mouvements possibles du cavalier
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] is None or self.board[r][c].color != piece.color:
                        possible_moves.append((r, c))
        
        elif piece.piece_type == "bishop":
            # Mouvements diagonaux
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] is None:
                        possible_moves.append((r, c))
                    elif self.board[r][c].color != piece.color:
                        possible_moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc
        
        elif piece.piece_type == "queen":
            # Combinaison des mouvements de la tour et du fou
            directions = [
                (-1, 0), (1, 0), (0, -1), (0, 1),  # Orthogonales
                (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] is None:
                        possible_moves.append((r, c))
                    elif self.board[r][c].color != piece.color:
                        possible_moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc
        
        elif piece.piece_type == "king":
            # Mouvements du roi (1 case dans toutes les directions)
            directions = [
                (-1, 0), (1, 0), (0, -1), (0, 1),  # Orthogonales
                (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] is None or self.board[r][c].color != piece.color:
                        possible_moves.append((r, c))
        
        return possible_moves
    
    def move_piece(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        
        # Mettre à jour la position de la pièce
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position
        piece.has_moved = True
        
        # Gérer la promotion du pion
        if piece.piece_type == "pawn":
            # Si un pion atteint la rangée opposée, le promouvoir en dame
            if (piece.color == "white" and new_row == 0) or (piece.color == "black" and new_row == 7):
                # Remplacer le pion par une dame
                self.board[new_row][new_col] = Queen(piece.color, (new_row, new_col))
                # Afficher un message temporaire de promotion
                self.promotion_message = f"Promotion du pion en Dame!"
                self.promotion_timer = 100  # Nombre de frames pour afficher le message
        
        # Changer de joueur
        self.current_player = "black" if self.current_player == "white" else "white"
    
    def get_legal_moves(self, piece):
        # Obtenir tous les mouvements valides de la pièce
        moves = piece.get_valid_moves(self.board)
        
        # Filtrer les mouvements qui mettraient le roi en échec
        legal_moves = []
        for move in moves:
            if not self.would_be_in_check_after_move(piece, move):
                legal_moves.append(move)
        
        return legal_moves
    
    def would_be_in_check_after_move(self, piece, move):
        # Simulation du mouvement pour vérifier si le roi serait en échec
        old_row, old_col = piece.position
        new_row, new_col = move
        
        # Sauvegarder l'état actuel
        old_piece_at_target = self.board[new_row][new_col]
        
        # Effectuer le mouvement temporaire
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = move
        
        # Vérifier si le roi est en échec
        king_position = self.find_king(piece.color)
        is_in_check = self.is_position_attacked(king_position, 
                                              "black" if piece.color == "white" else "white")
        
        # Annuler le mouvement temporaire
        self.board[old_row][old_col] = piece
        self.board[new_row][new_col] = old_piece_at_target
        piece.position = (old_row, old_col)
        
        return is_in_check
    
    def find_king(self, color):
        # Trouver la position du roi de la couleur donnée
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type == "king" and piece.color == color:
                    return (row, col)
        return None  # Ne devrait jamais arriver dans une partie normale
    
    def is_position_attacked(self, position, by_color):
        # Vérifier si une position est attaquée par une pièce de la couleur donnée
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == by_color:
                    # Pour éviter la récursion infinie avec la vérification des mouvements du roi
                    if piece.piece_type == "king":
                        # Vérifier manuellement si le roi peut attaquer la position
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
        # Vérifier si l'un des rois est en échec
        white_king_pos = self.find_king("white")
        black_king_pos = self.find_king("black")
        
        self.check_status["white"] = self.is_position_attacked(white_king_pos, "black")
        self.check_status["black"] = self.is_position_attacked(black_king_pos, "white")
    
    def is_checkmate(self):
        # Vérifier s'il y a échec et mat
        color = self.current_player
        
        # Si le roi n'est pas en échec, ce n'est pas un échec et mat
        if not self.check_status[color]:
            return False
        
        # Vérifier si une pièce peut faire un mouvement légal
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    legal_moves = self.get_legal_moves(piece)
                    if legal_moves:
                        return False  # Il y a au moins un mouvement légal, pas d'échec et mat
        
        # Aucun mouvement légal n'est possible et le roi est en échec, c'est un échec et mat
        return True
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        result = self.handle_click(event.pos)
                        if result == "menu":
                            return "menu"
            
            # Dessiner le plateau
            self.draw_board()
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            clock.tick(60)
        
        return "quit"

# Constantes globales
CASE_SIZE = 80
LIGHT_BROWN = (210, 180, 140)  # Marron clair
DARK_BROWN = (139, 69, 19)     # Marron foncé

def main():
    game = ChessGame()
    result = game.run()
    pygame.quit()
    return result

if __name__ == "__main__":
    main()