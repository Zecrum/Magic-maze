#### projet python jeu Magic Maze sur ordinateur
#### rendu du 10/01/2020
#### compatible linux & windows
#### Auteurs ####
# LAPLAIGE Alexandre
# GEOFFROY-PITAILLER Quentin
#################

from upemtk import *
import os

# longueur du plateau
long_i = 10  # horizontale
long_j = 15  # verticale

if os.name == 'nt':  # windows
    systeme = '\\'
else:
    systeme = '/'  # linux


def couleur(pion):
    """Renvoie la couleur en anglais du pion (exemple pion=1 -> couleur_pion='yellow')"""
    couleur_pion = ['rien', 'yellow', 'green', 'orange', 'purple', 'black']
    return couleur_pion[pion]


def generer_grille_save(grille_statut, grille_pos_pion, grille_pos_objet, grille_pos_sortie, grille_pos_mur_vert,
                        grille_pos_mur_horiz, grille_pos_vortex, grille_pos_sablier, objet_recup, grille_pos_escalator):
    """Affiche tous les éléments visuels au lancement (cases, textes, encadrés...)"""

    for statut, positions in grille_pos_sablier.items():  # placement des cases sablier
        for pos in positions:
            image(120 + 40 * pos[1], 120 + 40 * pos[0], 'image' + systeme + 'sablier.gif', ancrage='center',tag='sablier')

    for positions in grille_pos_sablier['inactif']:  # placement croix sablier inactif
        ligne(105 + 40 * positions[1], 105 + 40 * positions[0], 135 + 40 * positions[1], 95 + 40 * (positions[0] + 1),
              couleur="red", epaisseur='3')
        ligne(105 + 40 * positions[1], 95 + 40 * (positions[0] + 1), 135 + 40 * positions[1], 105 + 40 * positions[0],
              couleur="red", epaisseur='3')

    for pion, positions in grille_pos_vortex.items():  # placement des cases vortex
        for pos in positions:
            rectangle(105 + 40 * pos[1], 105 + 40 * pos[0], 95 + 40 * (pos[1] + 1), 95 + 40 * (pos[0] + 1),
                      couleur=couleur(int(pion)), epaisseur='2')

    for action, positions in grille_pos_escalator.items():  # placement des cases escalator
        for nb in action:
            image(140 + 40 * grille_pos_escalator[nb][0][1], 100 + 40 * grille_pos_escalator[nb][0][0], 'image' + systeme + 'Escalator.gif', ancrage='center',
                  tag='esclator')

    cercle(600, 500, 15, couleur="black", remplissage='yellow', tag="pion_choix_yellow")  # pions pour sélectionner
    cercle(660, 500, 15, couleur="black", remplissage='green', tag="pion_choix_green")  # le choix à jouer
    cercle(720, 500, 15, couleur="black", remplissage='orange', tag="pion_choix_orange")
    cercle(780, 500, 15, couleur="black", remplissage='purple', tag="pion_choix_purple")


    for ind in range(long_i):
        for j in range(long_j):  # ajoute les objets a recuperer
            if grille_pos_objet[j][ind] != 0:
                color = couleur(grille_pos_objet[j][ind])
                image(120 + ind * 40, 120 + j * 40, 'image' + systeme + 'objet_' + color + '.gif', ancrage='center',
                      tag='objet_' + color)

            if grille_pos_sortie[j][ind] != 0:  # ajoute les(la) cases sorties
                color = couleur(grille_pos_sortie[j][ind])
                image(120 + ind * 40, 120 + j * 40, 'image' + systeme + 'sortie_pion.gif', ancrage='center',
                      tag='sortie_pion')

            if grille_statut[j][ind] == 'v':
                rectangle(100 + 40 * ind, 100 + 40 * j, 100 + 40 * (ind + 1), 100 + 40 * (j + 1), couleur='black')
            elif grille_statut[j][ind] == 'd':
                rectangle(101 + 40 * ind, 101 + 40 * j, 100 + 40 * (ind + 1), 100 + 40 * (j + 1), remplissage='grey',
                          couleur='grey')
            elif grille_statut[j][ind] == 'i':
                rectangle(101 + 40 * ind, 101 + 40 * j, 100 + 40 * (ind + 1), 100 + 40 * (j + 1), remplissage='green',
                          couleur='green')

            if grille_pos_mur_vert[j][ind] == 'm':
                ligne(140 + 40 * ind, 100 + 40 * j, 140 + 40 * ind, 100 + 40 * (j + 1), couleur="black", epaisseur='5')
            if grille_pos_mur_horiz[j][ind] == 'm':
                ligne(100 + 40 * ind, 140 + 40 * j, 100 + 40 * (ind + 1), 140 + 40 * j, couleur="black", epaisseur='5')

    rectangle(100, 100, 500, 700)  # rectangle englobant les cases


    if objet_recup:
        liste_pion = [1,2,3,4]
        for i in range(0, len(grille_pos_pion)):  # boucle sur toutes les cases
            for j in range(0, len(grille_pos_pion[i])):
                if grille_pos_pion[i][j] in liste_pion :
                    liste_pion.remove(grille_pos_pion[i][j])

        for pion_a_sortir in liste_pion:
            affichage_pion_sortie(pion_a_sortir)

    return grille_statut, grille_pos_pion, grille_pos_objet, grille_pos_sortie, grille_pos_mur_vert, grille_pos_mur_horiz, grille_pos_vortex, grille_pos_sablier

def affichage_pion_sortie(pion):
    '''Affiche le pion sorti dans l'encadré prévu'''
    for i in range(0, 5):
        if pion == i:
            cercle(520 + i * 70, 290, 18, remplissage=couleur(pion), couleur="black", tag='pion_sorti_' + couleur(pion))
            efface("pion_" + couleur(pion))