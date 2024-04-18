import tkinter as tk
from random import randint as rd
import numpy as np
import time

class Sudoku:
    """
    Représente un jeu de Sudoku.

    Attributes:
        master (tk.Tk): Fenêtre principale de l'application.
        difficulty (tk.StringVar): Variable pour le niveau de difficulté.
        radio_frame (tk.Frame): Cadre pour les boutons radio.
        generate_button (tk.Button): Bouton pour générer un nouveau jeu.
        grid (list): Grille de Sudoku.
        solution (list): Solution de la grille de Sudoku.
        start_time (float): Temps de départ du chronomètre.
        elapsed_time (float): Temps écoulé depuis le début du jeu.
        timer_label (tk.Label): Étiquette pour afficher le chronomètre.
        check_button (tk.Button): Bouton pour vérifier la solution.
        quit_button (tk.Button): Bouton pour quitter le jeu.
        restart_button (tk.Button): Bouton pour recommencer le jeu.
        entry_list (list): Liste des Entry de la grille.
        initial_grid (list): Grille initiale avant que l'utilisateur ajoute des valeurs.
    """
    def __init__(self, master):
        """
        Initialise l'interface utilisateur du Sudoku.

        Args:
            master (tk.Tk): Fenêtre principale de l'application.
        """
        self.master = master
        self.master.title("Sudoku")

        # Variables pour le niveau de difficulté
        self.difficulty = tk.StringVar()
        self.difficulty.set("Facile")

        # Boutons radio pour choisir le niveau de difficulté
        self.radio_frame = tk.Frame(master)
        self.radio_frame.grid(row=0, columnspan=4, padx=5, pady=5)
        tk.Radiobutton(self.radio_frame, text="Facile", variable=self.difficulty, value="Facile").pack(side=tk.LEFT)
        tk.Radiobutton(self.radio_frame, text="Moyen", variable=self.difficulty, value="Moyen").pack(side=tk.LEFT)
        tk.Radiobutton(self.radio_frame, text="Difficile", variable=self.difficulty, value="Difficile").pack(side=tk.LEFT)

        # Bouton pour générer le jeu
        self.generate_button = tk.Button(master, text="Générer", command=self.generate_game)
        self.generate_button.grid(row=1, columnspan=4, padx=5, pady=5)

        # Initialisation des variables pour la grille de Sudoku
        self.grid = [[0]*9 for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]

        # Variable pour stocker le temps écoulé
        self.start_time = None
        self.elapsed_time = None

        # Étiquette pour afficher le chronomètre
        self.timer_label = tk.Label(master, text="00:00", font=('Arial', 14))
        self.timer_label.grid(row=13, column=3, columnspan=3, padx=5, pady=5)

    def generate_game(self):
        """
        Génère un nouveau jeu de Sudoku en fonction du niveau de difficulté sélectionné.
        """
        # Démarrer le chronomètre lors de la génération du jeu
        self.start_timer()
        
        self.matrice_d(self.get_difficulty())
        self.draw_grid()
        self.generate_button.grid_forget()
        self.radio_frame.grid_forget()
        
        # Stocker les valeurs initiales de la grille
        self.initial_grid = [[entry.get() for entry in row] for row in self.entry_list]

        # Bouton pour vérifier la solution
        self.check_button = tk.Button(self.master, text="Vérifier",fg='green', command=self.check_solution)
        self.check_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

        # Bouton pour quitter
        self.quit_button = tk.Button(self.master, text="Quitter",fg='red', command=self.master.destroy)
        self.quit_button.grid(row=12, column=7, columnspan=2, padx=5, pady=5)
        
        # Bouton pour remettre la grille de départ
        self.restart_button = tk.Button(self.master, text="Recommencer", fg='blue', command=self.restart_grid)
        self.restart_button.grid(row=12, column=3, columnspan=3, padx=5, pady=5)

        # Mettre à jour le chronomètre toutes les 1000 millisecondes (1 seconde)
        self.update_timer()

    def start_timer(self):
        """
        Enregistre le temps de départ du chronomètre.
        """
        self.start_time = time.time()

    def update_timer(self):
        """
        Met à jour l'affichage du chronomètre.
        """
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            timer_text = "{:02d}:{:02d}".format(minutes, seconds)
            self.timer_label.config(text=timer_text)
            self.master.after(1000, self.update_timer)

    def get_difficulty(self):
        """
        Récupère le niveau de difficulté sélectionné.

        Returns:
            int: Nombre de cases à vider pour créer la grille de Sudoku.
        """
        difficulty_str = self.difficulty.get()
        if difficulty_str == "Facile":
            return 30
        elif difficulty_str == "Moyen":
            return 40
        elif difficulty_str == "Difficile":
            return 50

    def matrice_d(self, nb):
        """
        Génère une matrice de Sudoku en fonction du nombre de cases à vider.

        Args:
            nb (int): Nombre de cases à vider pour créer la grille de Sudoku.
        """
        M = np.zeros((9, 9), dtype=int)
        for i in range(3):
            for u in range(3*i, 3*(i+1)):
                for v in range(3*i, 3*(i+1)):
                    while M[u, v] == 0:
                        n = rd(1, 9)
                        if n not in M[3*i:3*(i+1), 3*i:3*(i+1)]:
                            M[u, v] = n
        self.grid = self.suppr_nb(self.solveur(M),nb)
    
    def nb_zero(self,M):
        """
        Compte le nombre de zéros dans une matrice.

        Args:
            M (numpy.ndarray): Matrice à analyser.

        Returns:
            int: Nombre de zéros dans la matrice.
        """
        nb=0
        for i in range(9):
            for j in range(9):
                if M[i,j]==0:
                    nb+=1
        return nb

    def suppr_nb(self,M,nb):
        """
        Supprime un nombre donné de valeurs dans une matrice.

        Args:
            M (numpy.ndarray): Matrice à modifier.
            nb (int): Nombre de cases à vider.

        Returns:
            numpy.ndarray: Matrice modifiée.
        """
        M2=np.copy(M)
        while self.nb_zero(M2)!=nb:
            i=rd(0,8)
            j=rd(0,8)
            M2[i,j]=0
        return M2

    def solveur(self, M):
        """
        Résout la grille de Sudoku en utilisant la méthode de récursion.

        Args:
            M (numpy.ndarray): Grille de Sudoku à résoudre.

        Returns:
            numpy.ndarray or None: Grille de Sudoku résolue ou None si la grille est insoluble.
        """
        r = self.premierzero(M)
        if r:
            i, j = r
        else:
            return M
        for k in range(1, 10):
            M2 = np.copy(M)
            M2[i, j] = k
            if self.verifie(M2):
                res = self.solveur(M2)
                if res is not None:
                    return res
        return None

    def premierzero(self, M):
        """
        Trouve les coordonnées de la première case vide dans la grille de Sudoku.

        Args:
            M (numpy.ndarray): Grille de Sudoku.

        Returns:
            tuple or False: Coordonnées de la première case vide ou False si la grille est complète.
        """
        for i in range(9):
            for j in range(9):
                if M[i, j] == 0:
                    return i, j
        return False

    def verifie(self, M):
        """
        Vérifie si la grille de Sudoku est valide.

        Args:
            M (numpy.ndarray): Grille de Sudoku à vérifier.

        Returns:
            bool: True si la grille est valide, False sinon.
        """
        for i in range(9):
            vus = []
            for j in range(9):
                if M[i, j] in vus:
                    return False
                if M[i, j] != 0:
                    vus.append(M[i, j])
        for j in range(9):
            vus = []
            for i in range(9):
                if M[i, j] in vus:
                    return False
                if M[i, j] != 0:
                    vus.append(M[i, j])
        for I in range(9):
            vus = []
            for J in range(9):
                i, j = 3*(I//3) + J//3, 3*(I % 3) + J % 3
                if M[i, j] in vus:
                    return False
                if M[i, j] != 0:
                    vus.append(M[i, j])
        return True

    def check_solution(self):
        """
        Vérifie la solution proposée par l'utilisateur et affiche un message approprié.
        """
        self.solution=self.solveur(self.grid)
        user_solution = [[int(entry.get()) if entry.get() != "" else 0 for entry in row] for row in self.entry_list]
        u_s = [[0]*9 for _ in range(9)]
        for I in range(9):
            for J in range(9):
                i, j = 3*(I//3) + J//3, 3*(I % 3) + J % 3
                u_s[i][j]=user_solution[I][J]
        for row in u_s:
            n=False
            if 0 in row:
                n=True
                break
        if n==True:
            if self.verifie(np.array(u_s))==False:
                tk.messagebox.showinfo("Erreur", "Vous avez fait une erreur quelque part.")
            else:
                tk.messagebox.showinfo("Félicitation", "Pour l'instant tout est correct!")
            return
        elif u_s == self.solution.tolist():
            self.stop_timer()
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            timer_text = "{:02d} minutes et {:02d} secondes".format(minutes, seconds)
            tk.messagebox.showinfo("Félicitations", f"Bravo, vous avez résolu le Sudoku en {timer_text}!")
            return
        elif self.verifie(np.array(u_s))==True:
            self.stop_timer()
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            timer_text = "{:02d} minutes et {:02d} secondes".format(minutes, seconds)
            tk.messagebox.showinfo("Félicitations", f"Bravo, vous avez résolu le Sudoku en {timer_text}!")
            return
        tk.messagebox.showerror("Erreur", "La solution est incorrecte.")

    def stop_timer(self):
        """
        Arrête le chronomètre en réinitialisant le temps de départ.
        """
        self.start_time = None

    def draw_grid(self):
        """
        Dessine la grille de Sudoku dans l'interface utilisateur.
        """
        big_frame = tk.Frame(self.master)
        big_frame.grid(row=2, column=0, columnspan=9, rowspan=9)
        
        self.entry_list = []
        
        for i in range(3):
            for j in range(3):
                sub_frame = tk.Frame(big_frame, borderwidth=1, relief="solid")
                sub_frame.grid(row=i*3, column=j*3, rowspan=3, columnspan=3)
        
                sub_entries = []
        
                for row in range(i*3, i*3+3):
                    for col in range(j*3, j*3+3):
                        entry = tk.Entry(sub_frame, width=2, font=('Arial', 18), justify='center')
                        entry.grid(row=row-i*3, column=col-j*3, padx=1, pady=1)
                        num = self.grid[row][col]
                        if num != 0:
                            entry.insert(0, str(num))
                            entry.config(fg='black')
                        else:
                            entry.config(fg='blue')
        
                        sub_entries.append(entry)
        
                self.entry_list.append(sub_entries)
                
    def restart_grid(self):
        """
        Efface uniquement les valeurs ajoutées par l'utilisateur dans la grille de Sudoku.
        """
        for i in range(9):
            for j in range(9):
                if self.initial_grid[i][j] == '' and self.entry_list[i][j].get() != '':
                    self.entry_list[i][j].delete(0, tk.END)

def main():
    root = tk.Tk()
    game = Sudoku(root)
    root.mainloop()

if __name__ == "__main__":
    main()