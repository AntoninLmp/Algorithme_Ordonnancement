from A4_Algo_ordonnancement import *

# ------------------------------------------------------------
# Lecture d'un tableau de contrainte et stockage en mémoire
# ------------------------------------------------------------


def lectureTableauContrainte(nomFichier):
    with open(nomFichier, "r") as fichier:
        # Variables de lecture du fichier
        ligneFichier = fichier.readline()
        tableauContrainte = []
        # Lecture du fichier jusqu'a ce qu'il n'y ai plus rien dans le fichier
        while ligneFichier != "":

            # Variables utiles
            ligneTableauContrainte = []
            compteur = 0  # 1 = Tâche, 2 = Durée et 3 = Contraintes
            contraintes = []

            # Analyse d'une ligne
            i = 0
            while i < len(ligneFichier):
                nombre = ""
                while (i < len(ligneFichier) and ligneFichier[i] != " " and ligneFichier[i] != "\n"):
                    nombre += ligneFichier[i]
                    i += 1

                if (nombre != "" and i < len(ligneFichier)):
                    compteur += 1
                    if (compteur >= 3):
                        contraintes.append(int(nombre))
                    else:
                        ligneTableauContrainte.append(int(nombre))
                else:
                    i += 1
            # Ajout du tableau de contraintes
            ligneTableauContrainte.append(contraintes)
            # Ajout de la ligne au tableau finale
            tableauContrainte.append(ligneTableauContrainte)
            # Lecture d'une nouvelle ligne
            ligneFichier = fichier.readline()
        # print(tableauContrainte)
        return tableauContrainte
    return False

# ------------------------------------------------------------
# Ecriture de Trace
# ------------------------------------------------------------


def trace(nomFichier, matriceVal, matriceAdj, tableauRangs, listeCheminsCritique):
    with open(nomFichier, "w") as fichier:
        # Sommets | Arcs | relation
        fichier.write("ETAPE 1 : Création du graphe d’ordonnancement :\n\n")
        fichier.write(str(len(matriceVal)) + " sommets\n")
        compteur = 0
        for i in range(len(matriceVal)):
            for j in range(len(matriceVal)):
                if (matriceVal[i][j] != '-'):
                    compteur += 1
                    fichier.write(str(i) + " => " + str(j) +
                                  " = " + str(matriceVal[i][j]) + "\n")
        fichier.write(str(compteur) + " arcs\n")
        # -------------------------------------------------------------------
        # Matrice d'ajacence et de valeur
        # -------------------------------------------------------------------

        fichier.write("Matrice d'adjacence\n")
        for i in range(len(matriceAdj)):
            if(i == 0):
                fichier.write("   ")
            fichier.write(str(i) + "  ")
        fichier.write("\n")
        for i in range(len(matriceAdj)):
            for j in range(len(matriceAdj)):
                if (j == 0 and i < 10):
                    fichier.write(str(i) + "  ")
                elif(j == 0 and i >= 10):
                    fichier.write(str(i) + " ")
                if (j >= 10):
                    fichier.write(str(matriceAdj[i][j]) + "   ")
                else:
                    fichier.write(str(matriceAdj[i][j]) + "  ")
            fichier.write("\n")
        # -------------------------------------------------------------------
        fichier.write("Matrice des valeurs\n")
        for i in range(len(matriceVal)):
            if(i == 0):
                fichier.write("   ")
            fichier.write(str(i) + "  ")

        fichier.write("\n")
        for i in range(len(matriceVal)):
            for j in range(len(matriceVal)):
                if (j == 0 and i < 10):
                    fichier.write(str(i) + "  ")
                elif(j == 0 and i >= 10):
                    fichier.write(str(i) + " ")
                if (j >= 10):
                    fichier.write(str(matriceVal[i][j]) + "   ")
                else:
                    fichier.write(str(matriceVal[i][j]) + "  ")
            fichier.write("\n")

        # -------------------------------------------------------------------

        boolean, entree = checkUnPointEntree(matriceAdj)
        if (boolean == True):
            fichier.write("Il y a un seul point d'entree, " +
                          str(entree) + "\n")
        else:
            fichier.write("Il y a plusieurs points d'entrée\n")
            return

        boolean, sortie = checkUnPointSortie(matriceAdj)
        if (boolean == True):
            fichier.write("Il y a un seul point de sortie, " +
                          str(sortie) + "\n")
        else:
            fichier.write("Il y a plusieurs points de sortie\n")
            return

        boolean, matriceTrans = checkCircuit(matriceAdj)
        fichier.write("-- Matrice de fermeture transitive --\n")
        for i in range(len(matriceTrans)):
            if(i == 0):
                fichier.write("   ")
            fichier.write(str(i) + "  ")
        fichier.write("\n")
        for i in range(len(matriceTrans)):
            for j in range(len(matriceTrans)):
                if (j == 0 and i < 10):
                    fichier.write(str(i) + "  ")
                elif(j == 0 and i >= 10):
                    fichier.write(str(i) + " ")
                if (j >= 10):
                    fichier.write(str(matriceTrans[i][j]) + "   ")
                else:
                    fichier.write(str(matriceTrans[i][j]) + "  ")
            fichier.write("\n")

        if (boolean == False):
            fichier.write(
                "Il n'y a pas de circuit car la diagonale de la matrice ne comporte aucun 1!\n")
        else:
            fichier.write(
                "Il y a un circuit car la diagonale de la matrice comporte un ou plusieurs 1 !\n")
            return

        arcIncidentIden = arcIncidentIdentiques(matriceVal)
        if(arcIncidentIden == False):
            fichier.write(
                "ERREUR : valeurs NON IDENTIQUES pour tous les arcs incidents vers l’extérieur à un sommet\n")
            return
        else:
            fichier.write("Arc incident identiques donc c'est OK !\n")

        arcIncidentEntreeNull = arcIncidentPointEntree(matriceVal)
        if(arcIncidentEntreeNull == False):
            fichier.write(
                "ERREUR : valeurs NON NULL pour l'arc incident au point d'entree\n")
            return
        else:
            fichier.write(
                "arcs incidents vers l'exterieur au point d'entree de valeur nulle, OK !\n")

        arcNegatif = checkArcValeurNegative(matriceVal)
        if(arcNegatif == True):
            fichier.write("ERREUR : arc NEGATIF !\n")
            return
        else:
            fichier.write(
                "Ce graphe ne contient pas d'arc a valeur negatif, OK!\n")

        fichier.write(
            "\n\nC'est un graphe d'ordonnancement, il repond a toutes les exigences !\n\n")

        fichier.write("Rangs : \n")
        for i in range(len(tableauRangs)):
            fichier.write(tableauRangs[i])

        fichier.write("\nChemins critiques :\n")
        for num in listeCheminsCritique:
            fichier.write(str(num) + " ")
