# -*- coding: utf-8 -*-

#####
# Étienne Boutet - boue2327
# Raphael Valois - valr2802
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


#####
# reviser: Fonction utilisée par AC3 afin de réduire le domaine de Xi en fonction des contraintes de Xj.
#
# Xi: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# Xj: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant un booléen indiquant si il y a eu des changements et le csp.
###
def reviser(Xi, Xj, csp):
    revise = False
    for x in csp.domaines[Xi]:
        if not any([x != y for y in csp.domaines[Xj]]):
            csp.domaines[Xi].remove(x)
            revise = True
    return revise, csp


#####
# AC3: Fonction s'occupant de réduire les domaines des variables selon l'algorithme AC3.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant le csp optimisé et un booléen indiquant si aucune contrainte n'est violée.
###
def AC3(csp):
    file_arcs = csp.arcs()

    while file_arcs:
        Xi, Xj = file_arcs.pop()
        revise, csp = reviser(Xi, Xj, csp)
        if revise:
            if len(csp.domaines[Xi]) == 0:
                return csp, False
            else:
                for Xk in csp.contraintes[Xi]:
                    if Xk != Xj:
                        file_arcs.append((Xk, Xi))

    return csp, True

#####
# est_compatible: Fonction vérifiant la légalité d'une affectation.
#
# X: Tuple contenant la position en y et en x de la case concernée par l'affectation.
#
# v: String représentant la valeur (entre [1-9]) concernée par l'affectation.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un booléean indiquant si l'affectation de la valeur v à la case X est légale.
###
def est_compatible(X, v, assignations, csp):
    for cle, valeur in assignations.items():
        if v == valeur and cle in csp.contraintes[X]:
            return False
    return True


#####
# backtrack : Fonction s'occupant de trouver les assignations manquantes de la grille de Sudoku
#             en utilisant l'algorithme de Backtracking Search.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtrack(assignations, csp):
    if len(assignations) == len(csp.variables):
        return assignations

    X = var_non_assignee(assignations, csp)

    for v in valeurs_ordonnees(X, csp):
        if est_compatible(X, v, assignations, csp):
            assignations[X] = v
            csp.domaines[X] = [v]
            csp_prime, ok = AC3(csp.copy())
            if ok:
                resultat = backtrack(assignations, csp_prime)
                if resultat:
                    return resultat
            del assignations[X]

    return False


def var_non_assignee(assignations, csp):
    non_assignees = [v for v in csp.variables if v not in assignations]
    return min(non_assignees, key=lambda var: len(csp.domaines[var]))


def valeurs_ordonnees(variable, csp):
    if len(csp.domaines[variable]) == 1:
        return csp.domaines[variable]
    else:
        return sorted(csp.domaines[variable], key=lambda valeur: nombres_conflits(csp, variable, valeur))


def nombres_conflits(csp, variable, valeur):
    nombre = 0

    for voisin in csp.contraintes[variable]:
        if len(csp.domaines[voisin]) > 1 and valeur in csp.domaines[voisin]:
            nombre += 1

    return nombre


#####
# backtracking_search : Fonction coquille pour la fonction 'backtrack'.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku. Les variables membres sont
#      'variables'   : list de cases (tuple (Y,X)) vides
#      'domaines'    : dict mappant une case à une liste des valeurs possibles
#      'contraintes' : dict mappant une case à une liste de cases dont leur valeur doivent être différentes
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtracking_search(csp):
    return backtrack({}, csp)
