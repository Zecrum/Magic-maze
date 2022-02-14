#### projet python jeu Magic Maze sur ordinateur
#### rendu du 10/01/2020
#### compatible linux & windows
#### Auteurs ####
# LAPLAIGE Alexandre
# GEOFFROY-PITAILLER Quentin
#################

import json
import os
from copy import deepcopy
from random import randint, choice
from time import time

from MM_grille import generer_grille_save
from MM_texte import affichage_texte_base

from upemtk import *

if os.name == 'nt':  # windows
    systeme = '\\'
else:
    systeme = '/'  # linux

police_e = 'Helvetica'  # police du texte

# longueur du plateau
long_i = 10  # horizontale
long_j = 15  # verticale

fic_save = 'save.json'  # fichier de save


def couleur(pion):
    """Renvoie la couleur en anglais du pion (exemple pion=1 -> couleur_pion='yellow')"""
    couleur_pion = ['rien', 'yellow', 'green', 'orange', 'purple', 'black']
    return couleur_pion[pion]


def generer_grille():
    """Affiche tous les éléments visuels au lancement (cases, textes, encadrés...) ;
        Génère les matrices : statut case, position pion, postion objet, postion sortie"""

    ### Couleur des pions
    # 1 = jaune
    # 2 = vert
    # 3 = orange
    # 4 = violet
    ###

    grille_statut = []  ### statut des cases (visibles, invisibles, décors)
    grille_pos_pion = []  ### positions des pions sur le plateau
    grille_pos_mur_vert = []  ###  positions des murs verticaux

    for ind in range(long_j):
        grille_statut.append([])
        grille_pos_pion.append([])
        grille_pos_mur_vert.append([])
        for j in range(long_i):
            grille_statut[ind].append('v')
            grille_pos_pion[ind].append(0)
            grille_pos_mur_vert[ind].append('r')

    grille_pos_objet = deepcopy(grille_pos_pion)  ### positions des objets sur le plateau
    grille_pos_sortie = deepcopy(grille_pos_pion)  ### positions des/la sortie(s) sur le plateau
    grille_pos_mur_horiz = deepcopy(grille_pos_mur_vert)  ### positions des murs horizontaux

    case_decor = [[0, 1], [0, 5], [2, 5], [4, 1], [4, 5], [4, 6], [5, 1], [6, 8], [7, 8], [8, 8], [10, 4], [10, 5],
                  [12, 2], [13, 6], [14, 6], [12, 5], [3, 0], [11, 3], [12, 4], [10, 6], [11, 6], [12, 6], [0, 9],
                  [0,2],[0,3],[0,4],[1,3],[14,8],[13,8], [10,3], [10,1]]
    mur_vert = [[2, 3], [5, 3], [13, 2], [5, 7], [9, 7], [6, 2], [7, 2], [0, 6], [1, 6], [7,0], [10,0],[11,0]]
    mur_hor = [[7, 1], [7, 3], [13, 4], [13, 3], [9, 1], [1, 9], [1, 8], [4, 4], [7,6], [6,0], [10,8]]

    for couple in case_decor:
        grille_statut[couple[0]][couple[1]] = 'd'
    for couple in mur_vert:
        grille_pos_mur_vert[couple[0]][couple[1]] = 'm'
    for couple in mur_hor:
        grille_pos_mur_horiz[couple[0]][couple[1]] = 'm'

    grille_pos_pion[6][4], grille_pos_pion[6][5], grille_pos_pion[7][4], grille_pos_pion[7][5] = 1, 2, 3, 4  # pions
    grille_pos_objet[1][8], grille_pos_objet[12][8], grille_pos_objet[9][2], grille_pos_objet[2][2] = 1, 2, 3, 4  # obj
    grille_pos_sortie[11][5] = 5  # position sortie

    grille_pos_sablier = {'actif': [[0, 7], [14, 7]], 'inactif': []}  # postion case sablier
    for statut, positions in grille_pos_sablier.items():  # placement des cases sablier
        for pos in positions:
            image(120 + 40 * pos[1], 120 + 40 * pos[0], 'image' + systeme + 'sablier.gif', ancrage='center',
                  tag='sablier')

    grille_pos_vortex = {'1': [[0, 6], [2, 8]], '2': [[13, 1], [10, 8]], '3': [[1, 0], [6, 9]], '4': [[14, 3], [3, 8]]}
    ### positions des vortex
    for pion, positions in grille_pos_vortex.items():  # placement des cases vortex
        for pos in positions:
            rectangle(105 + 40 * pos[1], 105 + 40 * pos[0], 95 + 40 * (pos[1] + 1), 95 + 40 * (pos[0] + 1),
                      couleur=couleur(int(pion)), epaisseur='2')

    grille_pos_escalator = {'1': [[12, 3], [11, 4]], '2': [[4, 0], [3, 1]]}  # postion case escalator
    for action, positions in grille_pos_escalator.items():  # placement des cases escalator
        for nb in action:
            image(140 + 40 * grille_pos_escalator[nb][0][1], 100 + 40 * grille_pos_escalator[nb][0][0],
                  'image' + systeme + 'Escalator.gif', ancrage='center',
                  tag='esclator')

    cercle(600, 500, 15, couleur="black", remplissage='yellow', tag="pion_choix_yellow")  # pions pour sélectionner
    cercle(660, 500, 15, couleur="black", remplissage='green', tag="pion_choix_green")  # le choix à jouer
    cercle(720, 500, 15, couleur="black", remplissage='orange', tag="pion_choix_orange")
    cercle(780, 500, 15, couleur="black", remplissage='purple', tag="pion_choix_purple")

    for ind in [1, 2, 3, 4]:  # placement des 4 pions joueur
        mise_a_jour_plateau_pions(grille_pos_pion, ind)

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

            if grille_pos_mur_vert[j][ind] == 'm':
                ligne(140 + 40 * ind, 100 + 40 * j, 140 + 40 * ind, 100 + 40 * (j + 1), couleur="black", epaisseur='5')
            if grille_pos_mur_horiz[j][ind] == 'm':
                ligne(100 + 40 * ind, 140 + 40 * j, 100 + 40 * (ind + 1), 140 + 40 * j, couleur="black", epaisseur='5')

    rectangle(100, 100, 500, 700)  # rectangle englobant les cases

    affichage_texte_base()
    return grille_statut, grille_pos_pion, grille_pos_objet, grille_pos_sortie, grille_pos_mur_vert, grille_pos_mur_horiz, grille_pos_vortex, grille_pos_sablier, grille_pos_escalator


def mise_a_jour_plateau_pions(grille_pos_pion, pion):  # color = 1 ; 2 ; 3 ; 4
    """Met a jour la position des pions du joueur sur le plateau"""

    color = couleur(pion)

    efface("pion_" + color)  # efface l'ancien pion
    for i in range(0, len(grille_pos_pion)):  # boucle sur toutes les cases
        for j in range(0, len(grille_pos_pion[0])):  # ajoute le pion changé
            if grille_pos_pion[i][j] == pion:
                cercle(120 + j * 40, 120 + i * 40, 13, couleur="black", remplissage=color, tag="pion_" + color)
    return


def choix_touche(grille_pos_pion, grille_statut, debug, oldPion, tempsRestant, StatutPartie, nbJoueur, role,
                 grille_pos_mur_vert, grille_pos_mur_horiz, oldjoueur, grille_pos_vortex, objet_recup,
                 grille_pos_sablier, grille_pos_objet, grille_pos_sortie, grille_pos_escalator):
    """Fonction principale qui récupère les saisies utilisateurs puis les traite en envoyant vers d'autres
        fonctions"""

    tempsDebut = time()
    pion = oldPion
    chang_debug = debug
    joueur = oldjoueur
    affichage_pion_choix(oldPion)  # selectionne l'ancien pion choisi
    affichage_joueur_choix(joueur, role)

    while True:
        touche = attente_touche(100)  # attribut la touche (None si rien)
        if (StatutPartie == True) or (StatutPartie == False):  # si partie gagnée ou perdue
            if chang_debug:  # désactive debug si activé
                affichage_mode_debug(False)
            if touche == 'Escape':  # quitte la fenetre
                fermer_jeu()
            return [False, pion, StatutPartie, tempsRestant, nbJoueur, joueur]
        elif (touche is None) and (chang_debug == True):  # si aucune touche et mode debug activé
            aleatoire = mode_debug()  # joue aléatoirement
            pion = aleatoire[0]
            touche = aleatoire[1]
            joueur = nbJoueur[randint(1, len(nbJoueur) - 1)]
            break
        elif touche is None:  # aucune touche
            return [chang_debug, pion, None, tempsRestant - (time() - tempsDebut), nbJoueur, joueur]
        elif touche[-1] in str(nbJoueur) and touche != "0":
            joueur = int(touche[-1])
            affichage_joueur_choix(joueur, role)
        elif touche == 'a':
            if pion == 4:
                pion = 1
            else:
                pion += 1
            affichage_pion_choix(pion)
        elif touche == 'Up' or touche == 'Down' or touche == 'Right' or touche == 'Left':
            break
        elif touche == 'd':
            chang_debug = not chang_debug
            affichage_mode_debug(chang_debug)
            continue
        elif touche == 'v' and 'Vortex' in role[str(joueur)][1]:
            if not objet_recup:
                pos_pion_moove = selection_vortex(grille_pos_vortex, pion)
                if pos_pion_moove is not None:
                    for i in range(0, len(grille_pos_pion)):
                        for j in range(0, len(grille_pos_pion[0])):
                            if grille_pos_pion[i][j] == pion:
                                grille_pos_pion[i][j] = 0
                                grille_pos_pion[pos_pion_moove[0]][pos_pion_moove[1]] = pion
                                mise_a_jour_plateau_pions(grille_pos_pion, pion)
        elif touche == 'e' and 'Escalator' in role[str(joueur)][1]:  # esclator
            grille_pos_pion = action_escalator(pion, grille_pos_escalator, grille_pos_pion)

        elif touche == 'p':
            texte(1000, 50, 'Partie en PAUSE', couleur='red', taille='25', police=police_e, tag='partie_pause')
            partie_en_pause(grille_pos_pion, grille_statut, debug, oldPion, tempsRestant, StatutPartie, nbJoueur, role,
                            grille_pos_mur_vert, grille_pos_mur_horiz, oldjoueur, grille_pos_vortex, objet_recup,
                            grille_pos_sablier, grille_pos_objet, grille_pos_sortie, grille_pos_escalator)
            return [chang_debug, pion, None, tempsRestant, nbJoueur, joueur]
        elif touche == 'Escape':
            fermer_jeu()

    if verif_action_joueur(role, joueur, touche):
        val = changement_matrice_pion(grille_pos_pion, grille_statut, pion, touche, grille_pos_mur_vert,
                                      grille_pos_mur_horiz, grille_pos_sablier, tempsRestant)
        return [chang_debug, pion, None, val[1] - (time() - tempsDebut), nbJoueur, joueur]  # change le temps du sablier

    return [chang_debug, pion, None, tempsRestant - (time() - tempsDebut), nbJoueur, joueur]


def fermer_jeu():
    """Fermer la fenêtre de jeu"""
    ferme_fenetre()
    quit()


def action_escalator(pion, grille_pos_escalator, grille_pos_pion):
    """Action escalator"""
    position = 0
    pos_escalator = 0
    num_escalator = 0

    for i in range(len(grille_pos_pion)):
        for j in range(len(grille_pos_pion[0])):
            if grille_pos_pion[i][j] == pion:
                position = [i, j]
                break

    for nb, valeur in grille_pos_escalator.items():
        for pos in valeur:
            if pos == position:
                pos_escalator = pos
                num_escalator = nb
                break
    if num_escalator == 0:
        return grille_pos_pion

    lst = list(grille_pos_escalator[str(num_escalator)])
    lst.remove(pos_escalator)
    grille_pos_pion[position[0]][position[1]] = 0
    grille_pos_pion[lst[0][0]][lst[0][1]] = pion

    mise_a_jour_plateau_pions(grille_pos_pion, pion)
    return grille_pos_pion


def selection_vortex(grille_pos_vortex, pion):
    """Selectionne le vortex à se TP"""
    vortex = 0
    while True:
        touche = attente_touche(100)
        affichage_selection_vortex(grille_pos_vortex[str(pion)][vortex], pion)
        if touche == 'v':
            if vortex == len(grille_pos_vortex[str(pion)]) - 1:
                vortex = 0
            else:
                vortex += 1
        elif touche in ('Return','KP_Enter'):
            efface('cercle_select_vortex')
            return grille_pos_vortex[str(pion)][vortex]
        elif touche == 'c':
            efface('cercle_select_vortex')
            return
        elif touche == 'Escape':
            fermer_jeu()


def affichage_selection_vortex(coord, pion):
    """affiche un cercle rouge pour choisir le vortex"""
    efface('cercle_select_vortex')
    image(120 + coord[1] * 40, 120 + coord[0] * 40, 'image' + systeme + 'Vortex.gif', ancrage='center',
          tag="cercle_select_vortex")


def test_case_sablier(i, j, grille_pos_sablier, tempsRestant):
    """Test si le sablier est encore utilisable"""
    couple = [i, j]
    if couple in grille_pos_sablier['actif']:
        tempsRestant = 180 - tempsRestant
        grille_pos_sablier["actif"].remove(couple)
        grille_pos_sablier['inactif'].append(couple)
        ligne(105 + 40 * j, 105 + 40 * i, 135 + 40 * j, 95 + 40 * (i + 1), couleur="red", epaisseur='3')
        ligne(105 + 40 * j, 95 + 40 * (i + 1), 135 + 40 * j, 105 + 40 * i, couleur="red", epaisseur='3')
    return [grille_pos_sablier, tempsRestant]


def affichage_pion_choix(pion):
    """Change la position de la flèche en fonction du choix de l'utilisateur"""
    efface('choix_pion')
    lst = [(0, 0), (600, 550), (660, 550), (720, 550), (780, 550)]
    image(lst[pion][0], lst[pion][1], 'image' + systeme + 'choix_fleche.gif', ancrage='center', tag='choix_pion')


def affichage_joueur_choix(joueur, role):
    """Carré montrant le choix du joueur"""
    efface('choix_joueur')
    x = 420
    y = 590
    lst = [(0, 0), (570, 590, 660, 760), (720, 590, 810, 720), (870, 590, 960, 720)]
    nb_img = len(role[str(joueur)][0])
    nb_img += len(role[str(joueur)][1])

    rectangle(x + (joueur * 150), y, x + (joueur * 150 + 90), y + 21 + (nb_img * 46), couleur='green', epaisseur='3',
              tag='choix_joueur')


def changement_matrice_pion(grille_pos_pion, grille_statut, pion, touche, grille_pos_mur_vert, grille_pos_mur_horiz,
                            grille_pos_sablier, tempsRestant):
    """Change la matrice postion pion avec le nouvel emplacement du pion"""
    old_grille = list(grille_pos_pion)
    for i in range(0, len(old_grille)):
        for j in range(0, len(old_grille[0])):
            if (old_grille[i][j] == pion):
                if not verif_mouvement_pion(grille_pos_pion, grille_statut, pion, touche, i, j, grille_pos_mur_vert,
                                            grille_pos_mur_horiz):
                    val = [grille_pos_sablier, tempsRestant]
                    return val
                else:
                    grille_pos_pion[i][j] = 0
                    if touche == 'Up':
                        i -= 1
                    elif touche == 'Down':
                        i += 1
                    elif touche == 'Right':
                        j += 1
                    elif touche == 'Left':
                        j -= 1
                    grille_pos_pion[i][j] = pion

                    mise_a_jour_plateau_pions(grille_pos_pion, pion)
                    val = test_case_sablier(i, j, grille_pos_sablier, tempsRestant)
                    return val
    val = [grille_pos_sablier, tempsRestant]
    return val


def verif_mouvement_pion(grille_pos_pion, grille_statut, pion, touche, i, j, grille_pos_mur_vert, grille_pos_mur_horiz):
    '''Vérifie si le mouvement du pion est possible ; ne pas aller sur un autre pion, sortir du plateau;
        aller sur une cases décor...'''
    if touche == 'Up' and (
            i == 0 or grille_pos_pion[i - 1][j] != 0 or grille_statut[i - 1][j] == 'd' or grille_pos_mur_horiz[i - 1][
        j] == 'm'):
        return False
    elif touche == 'Down' and (
            i == len(grille_pos_pion) - 1 or grille_pos_pion[i + 1][j] != 0 or grille_statut[i + 1][j] == 'd' or
            grille_pos_mur_horiz[i][j] == 'm'):
        return False
    elif touche == 'Right' and (
            j == len(grille_pos_pion[i]) - 1 or grille_pos_pion[i][j + 1] != 0 or grille_statut[i][j + 1] == 'd' or
            grille_pos_mur_vert[i][j] == 'm'):
        return False
    elif touche == 'Left' and (
            j == 0 or grille_pos_pion[i][j - 1] != 0 or grille_statut[i][j - 1] == 'd' or grille_pos_mur_vert[i][
        j - 1] == 'm'):
        return False
    return True


def verif_action_joueur(role, joueur, touche):
    for element in role[str(joueur)]:
        for valeur in element:
            if valeur == touche:
                return True
    return False


def objets_recuperer(grille_pos_pion, grille_pos_objet, recuperer):
    """Test si les 4 pions sont sur sur leur cases objets"""
    lst = []
    if recuperer:
        return True
    for i in range(0, len(grille_pos_pion)):  # boucle sur toutes les cases
        for j in range(0, len(grille_pos_pion[i])):
            if grille_pos_pion[i][j] != grille_pos_objet[i][j]:
                return False
            elif grille_pos_pion[i][j] == grille_pos_objet[i][j] and grille_pos_objet[i][j] != 0:
                lst.append([i, j])

    for couple in lst:
        grille_pos_objet[couple[0]][couple[1]] = 0
    affichage_objet_recup()
    return True


def affichage_objet_recup():
    '''Efface les objets et affiche dans l'encadré les objets récupérés'''
    couleur = ['yellow', 'green', 'orange', 'purple']
    position = [(590, 140), (660, 140), (730, 140), (800, 140)]

    for ind in range(len(couleur)):
        efface('objet_' + couleur[ind])
        image(position[ind][0], position[ind][1], 'image' + systeme + 'objet_' + couleur[ind] + '.gif',
              ancrage='center', tag='objet_recup_' + couleur[ind])


def sortie_pion(grille_pos_pion, grille_pos_sortie, objet_recup):
    """Fait sortir les pions du plateau une fois qu'ils ont récupéré leur objet
        et renvoie la nouvelle matrice"""
    if not objet_recup:
        return False

    for i in range(0, len(grille_pos_sortie)):  # boucle sur toutes les cases
        for j in range(0, len(grille_pos_sortie[i])):
            if grille_pos_sortie[i][j] != 0 and grille_pos_pion[i][j] != 0:
                affichage_pion_sortie(grille_pos_pion[i][j])
                grille_pos_pion[i][j] = 0
                return grille_pos_pion


def affichage_pion_sortie(pion):
    '''Affiche le pion sorti dans l'encadré prévu'''
    for i in range(0, 5):
        if pion == i:
            cercle(520 + i * 70, 290, 18, remplissage=couleur(pion), couleur="black", tag='pion_sorti_' + couleur(pion))
            efface("pion_" + couleur(pion))
            return


def statut_partie(grille_pos_pion, temps):
    '''Voit si la partie est gagné ou perdu en fonction du chronomètre et des pions'''
    if temps >= 0.0:
        for i in range(0, len(grille_pos_pion)):  # boucle sur toutes les cases
            for j in range(0, len(grille_pos_pion[i])):
                if grille_pos_pion[i][j] != 0:
                    return None
        texte(50, 30, chaine='Bravo vous avez gagné !', couleur='Red', taille=35, police=police_e)
        return True
    elif temps < 0.0:
        texte(100, 30, chaine='Perdu Perdu Perdu !', couleur='Blue', taille=35, police=police_e)
        return False


def mode_debug():
    '''Génère un pion est un mouvement pour le mode debug'''
    action = ['Up', 'Down', 'Right', 'Left']
    choix = [randint(1, 4), action[randint(0, 3)]]
    return choix


def affichage_mode_debug(debug):
    """Texte affiché pour le mode debug"""
    if debug:
        texte(10, 710, "Mode debug activé", couleur="red", taille=13, police=police_e, tag='texte_mode_debug')
    else:
        efface('texte_mode_debug')


def chronometre(stop, tempsRestant):
    '''Affiche le temps restant'''
    if stop:
        return
    efface('texte_temps')
    texte(200, 710, 'Temps restant : ' + str(round(tempsRestant, 1)) + ' s', tag="texte_temps", taille=13,
          police=police_e)  # arrondi


def lancement_Partie():
    """"Lance la partie uniquement après avoir appuyé sur 'g'"""
    texte(1000, 150, "Lancez la partie : 'g'", taille=15, police=police_e, couleur='blue', tag='aide_lancement_p')
    while True:
        touche = attente_touche(500)
        if touche is None:
            continue
        elif touche == 'g':
            efface('aide_lancement_p')
            return True
        elif touche == 'Escape':
            fermer_jeu()


def selecteur_mode():
    """Permet de sélectionner le nombre de joueur au début de la partie"""
    joueur = ['0', '1', '2', '3']
    texte(1000, 150, "Choisissez le nombre de joueur : '1, 2 ou 3'", taille=15, police=police_e, couleur='blue',
          tag='aide_selection_j')
    while True:
        touche = attente_touche(500)
        if touche is None:
            continue
        elif touche[-1] in joueur:
            lst = [*range(0, int(touche[-1]) + 1, 1)]
            efface('aide_selection_j')
            return lst
        elif touche == 'Escape':
            fermer_jeu()


def definition_role_joueur(valeur):
    """Définit le rôle des joueurs (actions, mouvements)"""
    mvtPossible = ['Right', 'Left', 'Up', 'Down']
    actionPossible = ['Escalator', 'Vortex']
    nbJoueur = valeur[4][-1]
    role = dict()

    if nbJoueur == 1:
        role['1'] = [mvtPossible, actionPossible]
    elif nbJoueur == 2:
        for joueur in range(1, 3):
            mouvement = []
            action = []
            for select in range(2):
                m = choice(mvtPossible)
                mouvement.append(m)
                mvtPossible.remove(m)
            a = choice(actionPossible)
            action.append(a)
            actionPossible.remove(a)
            role[str(joueur)] = [mouvement, action]
    elif nbJoueur == 3:
        mouvement = []
        action = []
        for select in range(2):
            m = choice(mvtPossible)
            mouvement.append(m)
            mvtPossible.remove(m)
        a = choice(actionPossible)
        action.append(a)
        actionPossible.remove(a)
        role['1'] = [mouvement, action]
        for joueur in range(2, 4):
            mouvement = []
            action = []
            m = choice(mvtPossible)
            mouvement.append(m)
            mvtPossible.remove(m)
            if len(actionPossible) > 0:
                a = choice(actionPossible)
                action.append(a)
                actionPossible.remove(a)
            role[str(joueur)] = [mouvement, action]

    return role


def affichage_role_joueur(role):
    """Affichage des roles de chaque joueur sur le plateau"""

    position_x = 580

    for cle, valeur in role.items():
        position_y = 600
        texte(position_x, position_y, 'Joueur ' + str(cle), taille=12, police=police_e)
        position_y += 40
        position_x += 30
        for mvt in valeur[0]:
            image(position_x, position_y, 'image' + systeme + mvt + '.gif', ancrage='center', tag=mvt + 'mouvement')
            position_y += 40
        for act in valeur[1]:
            image(position_x, position_y, 'image' + systeme + act + '.gif', ancrage='center', tag=mvt + 'mouvement')
            position_y += 40
        position_x += 120


def partie_en_pause(grille_pos_pion, grille_statut, debug, oldPion, tempsRestant, StatutPartie, nbJoueur, role,
                    grille_pos_mur_vert, grille_pos_mur_horiz, oldjoueur, grille_pos_vortex, objet_recup,
                    grille_pos_sablier, grille_pos_objet, grille_pos_sortie, grille_pos_escalator):
    """Met en pause la partie"""
    donne = {'grille_statut': grille_statut,
             'grille_pos_pion': grille_pos_pion,
             'grille_pos_objet': grille_pos_objet,
             'grille_pos_sortie': grille_pos_sortie,
             'grille_pos_mur_vert': grille_pos_mur_vert,
             'grille_pos_mur_horiz': grille_pos_mur_horiz,
             'grille_pos_vortex': grille_pos_vortex,
             'grille_pos_sablier': grille_pos_sablier,
             'debug': debug,
             'oldPion': oldPion,
             'tempsRestant': tempsRestant,
             'StatutPartie': StatutPartie,
             'nbJoueur': nbJoueur,
             'role': role,
             'oldjoueur': oldjoueur,
             'objet_recup': objet_recup,
             'grille_pos_escalator': grille_pos_escalator}

    while True:
        touche = attente_touche(500)
        if touche == 'p':
            efface('partie_pause')
            efface('partie_save')
            break
        elif touche == 's':
            texte(1005, 100, 'Partie sauvegardée', couleur='black', taille='20', police=police_e, tag='partie_save')
            sauvegarde(donne)
        elif touche == 'Escape':
            fermer_jeu()
    return


def sauvegarde(donne):
    """Sauvegarde la partie"""
    with open(fic_save, "w") as fichier:
        json.dump(donne, fichier, indent=4)


def debut_menu():
    """Menu principale au début du jeu"""
    texte(100, 50, "Bienvenue sur Magic Maze, version ordinateur.", taille=15,
          police=police_e, couleur='red', tag='debut_1')
    texte(100, 100, "Tout au long pour quitter le jeu, fait : 'echap'", taille=15, police=police_e, tag='debut_2')
    texte(100, 150, "Tu as plusieurs possibilités :", taille=15,
          police=police_e, tag='debut_3')
    texte(150, 200, "- Tu peux démarrer une nouvelle partie : 'n'", taille=15, police=police_e, tag='debut_4')
    texte(150, 250, "- Tu peux charger la partie sauvegardée : 's'", taille=15, police=police_e, tag='debut_5')
    image(700, 500, 'image' + systeme + 'magic_logo.gif', ancrage='center', tag='debut_logo')

    while True:
        touche = attente_touche(500)
        if touche == 'n':  # nouvelle partie
            result = 'nouvelle_partie'
            break
        elif touche == 's':  # charge la sauvegarde
            result = 'charge_save'
            break
        elif touche == 'Escape':
            fermer_jeu()

    efface_tout()
    return result


if __name__ == "__main__":
    largeurFenetre = 1400
    hauteurFenetre = 890
    cree_fenetre(largeurFenetre, hauteurFenetre)

    debut = debut_menu()
    if debut == 'nouvelle_partie':
        gen_grille = generer_grille()

        grille_statut = gen_grille[0]
        grille_pos_pion = gen_grille[1]
        grille_pos_objet = gen_grille[2]
        grille_pos_sortie = gen_grille[3]
        grille_pos_mur_vert = gen_grille[4]
        grille_pos_mur_horiz = gen_grille[5]
        grille_pos_vortex = gen_grille[6]
        grille_pos_sablier = gen_grille[7]
        grille_pos_escalator = gen_grille[8]

        objet_recup = False
        valeur = [False, 1, None, 180.0, selecteur_mode(), 1]
        ## mode debug ; ancien pion ; stop chrono ; temps restant chrono ; nb joueur ; old Joueur

        role = definition_role_joueur(valeur)
    elif debut == 'charge_save':
        with open(fic_save, "r") as fichier:
            donne = json.load(fichier)

        grille_statut = donne['grille_statut']
        grille_pos_pion = donne['grille_pos_pion']
        grille_pos_objet = donne['grille_pos_objet']
        grille_pos_sortie = donne['grille_pos_sortie']
        grille_pos_mur_vert = donne['grille_pos_mur_vert']
        grille_pos_mur_horiz = donne['grille_pos_mur_horiz']
        grille_pos_vortex = donne['grille_pos_vortex']
        grille_pos_sablier = donne['grille_pos_sablier']
        debug = donne['debug']
        oldPion = donne['oldPion']
        tempsRestant = donne['tempsRestant']
        StatutPartie = donne['StatutPartie']
        nbJoueur = donne['nbJoueur']
        role = donne['role']
        oldjoueur = donne['oldjoueur']
        objet_recup = donne['objet_recup']
        grille_pos_escalator = donne['grille_pos_escalator']
        affichage_texte_base()
        generer_grille_save(grille_statut, grille_pos_pion, grille_pos_objet, grille_pos_sortie, grille_pos_mur_vert,
                            grille_pos_mur_horiz, grille_pos_vortex, grille_pos_sablier, objet_recup,
                            grille_pos_escalator)
        for ind in [1, 2, 3, 4]:  # placement des 4 pions joueur
            mise_a_jour_plateau_pions(grille_pos_pion, ind)
        valeur = [debug, oldPion, StatutPartie, tempsRestant, nbJoueur, oldjoueur]

        if objet_recup:
            affichage_objet_recup()

    affichage_role_joueur(role)
    lancement_Partie()

    while True:
        valeur = choix_touche(grille_pos_pion, grille_statut, valeur[0], valeur[1], valeur[3], valeur[2], valeur[4],
                              role, grille_pos_mur_vert, grille_pos_mur_horiz, valeur[5], grille_pos_vortex,
                              objet_recup, grille_pos_sablier, grille_pos_objet, grille_pos_sortie,
                              grille_pos_escalator)
        objet_recup = objets_recuperer(grille_pos_pion, grille_pos_objet, objet_recup)
        sortie_pion(grille_pos_pion, grille_pos_sortie, objet_recup)
        chronometre(valeur[2], valeur[3])

        if statut_partie(grille_pos_pion, valeur[3]):  # test partie gagné
            valeur = [False, valeur[1], True, valeur[3], valeur[4], valeur[5]]
        elif statut_partie(grille_pos_pion, valeur[3]) is False:  # test partie perdu
            valeur = [False, valeur[1], False, 0, valeur[4], valeur[5]]

    attente_clic()
    ferme_fenetre()
