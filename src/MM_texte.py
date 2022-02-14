#### projet python jeu Magic Maze sur ordinateur
#### rendu du 10/01/2020
#### compatible linux & windows
#### Auteurs ####
# LAPLAIGE Alexandre
# GEOFFROY-PITAILLER Quentin
#################

from upemtk import *

police_e = 'Helvetica'  # police du texte


def affichage_texte_base():
    texte(1200, 540, "Les touches : ", taille=16, police=police_e)
    texte(1180, 580, "Touche 'g' pour lancer la partie", taille=8, police=police_e)  # ajoute 5 textes 'aide'
    texte(1180, 600, "Touche 's' pour sauvegarder", taille=8, police=police_e)
    texte(1180, 620, "Touche 'p' pour mettre sur pause", taille=8, police=police_e)
    texte(1180, 640, "Touche 'e' pour utiliser escalator", taille=8, police=police_e)
    texte(1180, 660, "Touche 'v' pour choisir vortex", taille=8, police=police_e)
    texte(1180, 680, "Touche 'Entrer' pour confirmer vortex", taille=8, police=police_e)
    texte(1180, 700, "Touche 'c' pour annuler le choix vortex", taille=8, police=police_e)
    texte(1180, 720, "Touche 'a' pour changer de pion", taille=8, police=police_e)
    texte(1180, 740, "Flèches directionnelles pour la direction", taille=8, police=police_e)
    texte(1180, 760, "Touche 'd' pour activer/désactiver le debug", taille=8, police=police_e)
    texte(1180, 780, "Touche 'Echap' pour quitter la partie", taille=8, police=police_e)
    rectangle(1170, 530, 1390, 800)  # entouré d'un rectangle

    rectangle(550, 100, 850, 180, couleur='black', epaisseur='2')  # afichage du rectangle recup objet et texte
    texte(550, 70, 'Les objets récupérés sont :', taille=15, police=police_e)

    rectangle(550, 250, 850, 330, couleur='red', epaisseur='2')  # afichage du rectangle pion sorti et texte
    texte(550, 220, 'Les pions sortis sont :', taille=15, couleur='red', police=police_e)

    ligne(900, 50, 900, 550, couleur='black', epaisseur='5')  # trait noir écran
    ligne(898, 550, 1150, 550, couleur='black', epaisseur='5')
    ligne(1150, 548, 1150, 850, couleur='black', epaisseur='5')


