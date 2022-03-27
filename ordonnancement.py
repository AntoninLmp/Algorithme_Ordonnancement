from ast import Return
from operator import le
from os import TMP_MAX
from pickle import FALSE
from re import L
from turtle import rt
from matplotlib import lines
from matplotlib.pyplot import table
import numpy as np
from prettytable import PrettyTable
import prettytable


# ------------------------------------------------------------
# Affichage d'un tableau de contrainte à l'aide de prettyTable
# ------------------------------------------------------------
def affichageTableau(tableau):
    x = PrettyTable()
    # Nom des colonnes pour le tableau
    x.field_names = ["Tâche", "Durée", "Contraintes"]

    for i in range(0, len(tableau)):
        # Mis des contraintes sous forme de string
        contraintes = ""
        for j in range(0, len(tableau[i][2])):
            contraintes += str(tableau[i][2][j]) + " "
        # Un ligne
        if (contraintes == ""):
            contraintes = "Aucun"
        # Ajout de chaque ligne au tableau
        x.add_row(
            [tableau[i][0], tableau[i][1], contraintes]
        )
    print(x)


# ------------------------------------------------------------
# Affichage de matrice grâce à prettyTable
# ------------------------------------------------------------
# def affichageMatrice(matrice):
#     print("    | ", end="")
#     for i in range(0, len(matrice)):
#         print(i+1, end=" | ")
#     print()
#     print("----|", end="")
#     for i in range(0, len(matrice)):
#         if (i >= 9):
#             print("----", end="|")
#         else:
#             print("---", end="|")
#     # Affichage du corps
#     for i in range(0, len(matrice)):
#         if (i+1 > 9):
#             print("\n "+str(i+1)+" | ", end="")
#         else:
#             print("\n "+str(i+1)+"  | ", end="")
#         for j in range(0, len(matrice[i])):
#             if (j >= 9):
#                 print(matrice[i][j], end="  | ")
#             else:
#                 print(matrice[i][j], end=" | ")
#     print()


def affichageMatricePretty(matrice):
    tab_adj = PrettyTable()

    # Fields
    tab_field_names = ["\\", "α"]
    for i in range(1, len(matrice)-1):
        tab_field_names.append(i)
    tab_field_names.append("ω")
    tab_adj.field_names = tab_field_names

    # Row
    tab_tmp = np.array([])
    tab_tmp = np.append(tab_tmp, 'α')
    for i in range(1, len(matrice)-1):
        tab_tmp = np.append(tab_tmp, i)
    tab_tmp = np.append(tab_tmp, 'ω')

    matrice = np.array(matrice)
    matrice = np.column_stack((tab_tmp, matrice))

    for line in matrice:
        tab_adj.add_row(line)
    print(tab_adj)


def affichageDate(list, nomColonne):
    tableau = PrettyTable()
    # Row
    tab_tmp = np.array(nomColonne)
    list = np.array(list, dtype=object)
    list = np.column_stack((tab_tmp, list))

    for line in list:
        tableau.add_row(line)
    print(tableau)
# ------------------------------------------------------------
# Construction de la matrice d'adjacence
# Entrée: Prend un tableau de contrainte
# Sortie : Renvoie une matrice de n * n, où n est le nombre
# de ligne du tableau de contrainte
# ------------------------------------------------------------


def matriceAdjacence(tableauContraintes):
    # Initialisation de la matrice d'adjacence
    matriceAD = []
    tableauContraintes = np.array(tableauContraintes, dtype=object)
    for i in range(0, len(tableauContraintes)+1):
        # Initialisation et remplissage de chaque ligne de la matrice
        ligneMatrice = [0]
        terminaux = True
        for j in range(0, len(tableauContraintes)):
            # ---------------------------------
            # POUR ALPHA
            if (i == 0):
                terminaux = False
                if (len(tableauContraintes[j][2]) == 0):
                    ligneMatrice.append(1)
                else:
                    ligneMatrice.append(0)
            # ---------------------------------
            elif (tableauContraintes[j][2].__contains__(i)):
                ligneMatrice.append(1)
                terminaux = False
            else:
                ligneMatrice.append(0)
        # ---------------------------------
        # Ajout de w :
        if (terminaux == False):
            ligneMatrice.append(0)
        else:
            ligneMatrice.append(1)
        # ---------------------------------
        # Ajout de la ligne à la matrice
        matriceAD.append(ligneMatrice)
    # Ajout de la ligne w, qui est nulle
    matriceAD.append(np.array([int(0)
                     for i in range(len(tableauContraintes)+2)]))
    return matriceAD


# ------------------------------------------------------------
# Construction de la matrice de valeur
# ------------------------------------------------------------
def matriceValeur(tableauContraintes):
    # Initialisation de la matrice d'adjacence
    matriceAD = []
    tableauContraintes = np.array(tableauContraintes, dtype=object)
    for i in range(0, len(tableauContraintes)+1):
        # Initialisation et remplissage de chaque ligne de la matrice
        ligneMatrice = ['-']
        terminaux = True
        for j in range(0, len(tableauContraintes)):
            # ---------------------------------
            # POUR ALPHA
            if (i == 0):
                terminaux = False
                if (len(tableauContraintes[j][2]) == 0):
                    ligneMatrice.append(0)
                else:
                    ligneMatrice.append('-')
            # ---------------------------------
            elif (tableauContraintes[j][2].__contains__(i)):
                ligneMatrice.append(tableauContraintes[i-1][1])
                terminaux = False
            else:
                ligneMatrice.append('-')
        # ---------------------------------
        # Ajout de w :
        if (terminaux == False):
            ligneMatrice.append('-')
        else:
            ligneMatrice.append(tableauContraintes[i-1][1])
        # ---------------------------------
        # Ajout de la ligne à la matrice
        matriceAD.append(ligneMatrice)
    # Ajout de la ligne w, qui est nulle
    matriceAD.append(np.array([str('-')
                     for i in range(len(tableauContraintes)+2)]))
    return matriceAD


# ------------------------------------------------------------
# Un seul point d'entrée
# ------------------------------------------------------------
def checkUnPointEntree(matrice):
    if (None != matrice):
        entree = -1
        compteurEntree = 0
        for i in range(0, len(matrice)):
            contientUn1 = False
            for j in range(0, len(matrice)):
                if (matrice[j][i] == 1):
                    contientUn1 = True
                    break
            if (contientUn1 == False):
                compteurEntree += 1
                entree = i+1
                print(i+1, " est une entrée")
        if(compteurEntree == 1):
            return True, entree
    return False, entree


# ------------------------------------------------------------
# Un seul point de sortie
# ------------------------------------------------------------
def checkUnPointSortie(matrice):
    if (None != matrice):
        compteurSortie = 0
        sortie = -1
        for i in range(0, len(matrice)):
            contientUn1 = False
            for j in range(0, len(matrice)):
                if (matrice[i][j] == 1):
                    contientUn1 = True
                    break
            if (contientUn1 == False):
                compteurSortie += 1
                sortie = i + 1
                print(i+1, " est une sortie")
        if(compteurSortie == 1):
            return True, sortie
    return False, sortie


# ------------------------------------------------------------
# Fermuture transitive pour détecter un circuit
# ------------------------------------------------------------
def checkCircuit(matrice):
    matriceCp = np.copy(matrice)
    # Trouver le tableau avec les prédécesseurs
    for i in range(len(matriceCp)):
        tableau_pred = []
        tableau_succ = []
        for j in range(len(matriceCp[i])):
            if (matriceCp[j][i] == 1):
                tableau_pred.append(j)
            if (matriceCp[i][j] == 1):
                tableau_succ.append(j)
        # print(tableau_pred, tableau_succ)
        for m in range(len(tableau_pred)):
            for n in range(len(tableau_succ)):
                matriceCp[tableau_pred[m]][tableau_succ[n]] = 1
        # print(matriceCp)
    # Or on sait que le graphe est sans circuit s'il n'y a aucun 1 sur la diagonal de sa fermeture transitive
    for i in range(len(matriceCp)):
        if (matriceCp[i][i] == 1):
            return True, matriceCp
    return False, matriceCp

# ------------------------------------------------------------
# valeurs identiques pour tous les arcs incidents vers l’extérieur à un sommet
# ------------------------------------------------------------


def arcIncidentIdentiques(matriceValeur):
    taille = len(matriceValeur)  # Matrice carré taille de m = taille de n
    for i in range(1, taille):
        valeur = 0
        for j in range(taille):
            if (matriceValeur[i][j] != '-' and valeur == 0):
                # On initialise la valeur de l'arc
                valeur = matriceValeur[i][j]
            elif (matriceValeur[i][j] != valeur and matriceValeur[i][j] != '-'):
                return False
    return True


# ------------------------------------------------------------
# arcs incidents vers l’extérieur au point d’entrée de valeur nulle
# ------------------------------------------------------------


def arcIncidentPointEntree(matriceValeur):
    for i in range(1, len(matriceValeur)):
        if (matriceValeur[0][i] != 0 and matriceValeur[0][i] != '-'):
            return False
    return True


# ------------------------------------------------------------
# Pas d'arc à valeur négative
# ------------------------------------------------------------
# def checkArcValeurNegative(tableauContraintes):
#     if (None != tableauContraintes):
#         for i in range(0, len(tableauContraintes)):
#             # On vérifie que les arcs ne soit pas négatif
#             if(tableauContraintes[i][1] < 0):
#                 return True
#     return False


def checkArcValeurNegative(matriceValeur):
    if (None != matriceValeur):
        for i in range(0, len(matriceValeur)):
            for j in range(len(matriceValeur[i])):
                # On vérifie que les arcs ne soit pas négatif
                if(matriceValeur[i][j] != '-' and matriceValeur[i][j] < 0):
                    return True
    return False
# ------------------------------------------------------------
# Calcul des rangs
# ------------------------------------------------------------


def calculRangs(matrice):
    # Variables utiles
    matriceCopie = np.copy(matrice)
    etatRestant = len(matrice)
    numRang = 0
    tableauRangs = []  # Stocker et pouvoir réutiliser les rangs par la suite

    # Boucles pour le nombre de rangs
    while etatRestant > 0:
        rangAEliminer = []
        print("Les états de RANG "+str(numRang) + " sont : { ", end="")
        # Recherche des lignes a supprimé
        for i in range(0, len(matriceCopie)):
            contientUn1 = False
            nombreDe2 = 0

            for j in range(0, len(matriceCopie)):
                if (matriceCopie[j][i] == 2):
                    nombreDe2 += 1
                # Si on detecte un 1 alors il ne s'agit pas d'un état qui ne possede aucun predecesseur
                if (matriceCopie[j][i] == 1):
                    contientUn1 = True
                    break

            if (contientUn1 == False and nombreDe2 != len(matriceCopie)):
                rangAEliminer.append(i)
                etatRestant -= 1

        # Ici on ne vas pas supprimer le tableau et le recrée par soucis de simplicité car c'est assez laborieux
        # On va remplacer par un 2 toutes les cases de ces états
        tableauRangs.append(list(rangAEliminer))
        for m in range(0, len(rangAEliminer)):
            if(rangAEliminer[m] == 0):
                print("α", end=" ")
            elif(rangAEliminer[m] == len(matrice)-1):
                print("ω", end=" ")
            else:
                print(rangAEliminer[m], end=" ")
            for n in range(0, len(matriceCopie)):
                matriceCopie[rangAEliminer[m]][n] = 2
            for n in range(0, len(matriceCopie)):
                matriceCopie[n][rangAEliminer[m]] = 2
            # affichaeMatrice(matriceCopie)
        rangAEliminer.clear()
        numRang += 1
        print("}")

    return tableauRangs

# ------------------------------------------------------------
# Calcul au plus tôt
# ------------------------------------------------------------


def calculDateAuPlusTot(matriceAdj, tableauContraintes, rang):
    # rang | Tâche+longueur | Précedent(s) | Dates par pred. | Dates au plus tôt
    listDatePlusTot = [[], [], [], [], []]
    # ----------------------------------------
    # LIGNE CONTENANTS "rangs"
    for i in range(0, len(rang)):
        for j in range(0, len(rang[i])):
            listDatePlusTot[0].append(i)

    # ----------------------------------------
    # LIGNES CONTENANT "Tâches et sa longueur"
    for i in range(0, len(rang)):
        taches = []
        for k in range(0, len(rang[i])):
            taches.append(rang[i][k])
            if (rang[i][k] == 0 or rang[i][k] == len(matriceAdj)-1):
                taches.append(0)
            else:
                for j in range(0, len(tableauContraintes)):
                    if (tableauContraintes[j][0] == (rang[i][k])):
                        taches.append(tableauContraintes[j][1])
                        break
            listDatePlusTot[1].append(list(taches))
            taches.clear()

    # ----------------------------------------
    # Calcul des predecesseurs
    for n in range(len(listDatePlusTot[0])):
        i = listDatePlusTot[1][n][0]  # correspond à l'état
        etatPrec = []
        for j in range(len(matriceAdj[i])):
            if(matriceAdj[j][i] == 1):
                etatPrec.append(j)
        # Ajout des prédécesseurs
        listDatePlusTot[2].append(list(etatPrec))
        etatPrec.clear()

    # ----------------------------------------
    # Calcul Dates par predecesseur
    for i in range(len(listDatePlusTot[0])):

        # Dans le cas où cette état n'a pas de prédecesseur
        if(len(listDatePlusTot[2][i]) == 0):
            listDatePlusTot[3].append([0])

        # Autres cas
        else:
            valeur = []
            # Parcours des prédécesseurs
            for j in range(len(listDatePlusTot[2][i])):
                val = 0
                for n in range(len(listDatePlusTot[1])):
                    if (listDatePlusTot[1][n][0] == listDatePlusTot[2][i][j]):
                        valeur.append(
                            listDatePlusTot[1][n][1] + max(listDatePlusTot[3][n]))
            listDatePlusTot[3].append(list(valeur))
            valeur.clear()
    # ----------------------------------------
    # Dates au plus tôt
    for tab in listDatePlusTot[3]:
        listDatePlusTot[4].append(max(tab))
    # ----------------------------------------
    # affichageDate(listDatePlusTot, ['Rangs', 'Tâches et sa longueur',
    #                                 'Predecesseur', 'Date par Pred.', 'Date au plus tôt'])
    return listDatePlusTot


def calculDateAuPlusTard(matriceAdj, tableauContraintes, listDateAuPlusTot):
    # Successeurs, Date par successeur et Date au plus tard
    listDateAuPlusTard = [[], [], []]

    # ----------------------------------------
    # Successeurs
    for loop in range(len(matriceAdj)):
        successeurs = []
        i = listDateAuPlusTot[1][loop][0]
        for j in range(len(matriceAdj)):
            if(matriceAdj[i][j] == 1):
                successeurs.append(j)
        listDateAuPlusTard[0].append(list(successeurs))
        successeurs.clear()
    listDateAuPlusTot.append(listDateAuPlusTard[0])

    # ----------------------------------------

    # Tableau qui contiendra les date au plus tard de chaque états
    for l in range(len(listDateAuPlusTard[0])):
        listDateAuPlusTard[1].append([])

    # Ajout de la date au plus tard de w
    listDateAuPlusTard[1][len(listDateAuPlusTard[1]) -
                          1].append(listDateAuPlusTot[4][len(listDateAuPlusTot[0])-1])
    valeur = []
    compteur = 2
    for i in range(len(listDateAuPlusTot[0])-2, -1, -1):
        # On va partir de la droite et on prend le successeurs de chaque état pour calcul sa date au plus tard
        successeurs = listDateAuPlusTard[0][i]

        for k in range(len(successeurs)):
            for j in range(i, len(listDateAuPlusTard[0])):
                if(successeurs[k] == listDateAuPlusTot[1][j][0]):
                    valeur.append(
                        min(listDateAuPlusTard[1][j]) - listDateAuPlusTot[1][i][1])

        # Ajout des valeurs car plus simple
        for val in valeur:
            listDateAuPlusTard[1][len(
                listDateAuPlusTard[1])-compteur].append(val)
        compteur += 1
        valeur.clear()

    listDateAuPlusTot.append(listDateAuPlusTard[1])
    # ----------------------------------------
    # Dates au plus tôt
    for tab in listDateAuPlusTard[1]:
        listDateAuPlusTard[2].append(min(tab))
    listDateAuPlusTot.append(listDateAuPlusTard[2])
    return listDateAuPlusTot


def calculMarges(listDate):
    listeMarge = []
    for i in range(len(listDate[0])):
        listeMarge.append(listDate[7][i] - listDate[4][i])
    listDate.append(listeMarge)
    return listDate
