from pickle import TRUE
from secrets import choice
from types import TracebackType
from lecture_ecriture import *
from ordonnancement import *

print("--------------------------------------------")
print("                 Bonjour                    ")
print("--------------------------------------------")

print("Ce programme sert à analyser des graphes !")

numbFichier = 1
while (numbFichier != -1):
    print("Quel fichier voulez vous analyser ?")
    numbFichier = int(input())
    try:
        fichierTest = "Fichiers_Tests/table " + str(numbFichier) + ".txt"
        nomTrace = "Fichiers_Traces/trace_" + str(numbFichier) + ".txt"

        with open(fichierTest, "r") as f:
            print("Ce fichier existe, Analysons le !")
        print("---------------------------------------------------------")
        print("\t1. Affichage du Tableau de contraintes")
        print("---------------------------------------------------------")
        tableauContraintes = lectureTableauContrainte(fichierTest)
        affichageTableau(tableauContraintes)
        f.close()
        print("---------------------------------------------------------")
        print("\t2. Calcul de la matrice d'Adjacence et affichage")
        print("---------------------------------------------------------")
        matriceAdj = matriceAdjacence(tableauContraintes)
        affichageMatricePretty(matriceAdj)
        print("---------------------------------------------------------")
        print("\t3. Calcul de la matrice des valeurs et affichage")
        print("---------------------------------------------------------")
        matrice_valeur = matriceValeur(tableauContraintes)
        affichageMatricePretty(matrice_valeur)
        print("---------------------------------------------------------")
        print("\t4. Vérification des propriétés nécessaire")
        print("---------------------------------------------------------")
        print("\n\t- Un seul point d'entrée ? ", end="")
        # True pour que cela soit correct
        entree, num_entree = checkUnPointEntree(matriceAdj)
        print(num_entree, " est une entree")
        print("\n\t- Un seul point de sortie ? ", end="")
        # True pour que cela soit correct
        sortie, num_sortie = checkUnPointSortie(matriceAdj)
        print(num_sortie, " est une sortie")
        # ----------------------------------------------------------------
        print("\n\t- Le graphe contient-il un circuit ? ", end="")
        circuit, matriceTransitive = checkCircuit(matriceAdj)
        if(circuit == True):
            print(
                "ERREUR : Il y a un CIRCUIT dans ce graphe ! L'ordonnancement n'est pas possible !")
            # Ecriture de la trace du fichier
            trace(nomTrace, matrice_valeur, matriceAdj, None)
            continue
        else:
            print("OK, Le graphe ne contient pas de circuit ! ")
        # ----------------------------------------------------------------
        print("\n\t- Arc incident indetiques ? ", end="")
        arcIncidentIden = arcIncidentIdentiques(matrice_valeur)
        if(arcIncidentIden == False):
            print(
                "ERREUR : valeurs NON IDENTIQUES pour tous les arcs incidents vers l’extérieur à un sommet")
            # Ecriture de la trace du fichier
            trace(nomTrace, matrice_valeur, matriceAdj, None)
            continue
        else:
            print("OK, Les valeurs des arcs incidents sont identiques ! ")
        # ----------------------------------------------------------------
        print("\n\t- Arc incident entree nulle ? ", end="")
        arcIncidentEntreeNull = arcIncidentPointEntree(matrice_valeur)
        if(arcIncidentEntreeNull == False):
            print(
                "ERREUR : valeurs NON NULL pour l'arc incident au point d'entree")
            # Ecriture de la trace du fichier
            trace(nomTrace, matrice_valeur, matriceAdj, None)
            continue
        else:
            print("OK, Valeurs null pour l'arc incident au point d'entrée ! ")
        # ----------------------------------------------------------------
        print("\n\t- Arc à valeur Négative ? ", end="")
        # False pour que cela soit correct
        arcNegatif = checkArcValeurNegative(matrice_valeur)
        if(arcIncidentEntreeNull == False):
            print(
                "ERREUR : arc NEGATIF")
            # Ecriture de la trace du fichier
            trace(nomTrace, matrice_valeur, matriceAdj, None)
            continue
        else:
            print("OK ! ")

        print("---------------------------------------------------------")
        print("\t5. Calcul des rangs ")
        print("---------------------------------------------------------")
        listRangs, tableauTracesRangs = calculRangs(matriceAdj)
        print("---------------------------------------------------------")
        print("\t6. Calcul Date aux plus tôt Et aux plus tard")
        print("---------------------------------------------------------")
        listDateAuPlusTot = calculDateAuPlusTot(
            matriceAdj, tableauContraintes, listRangs)
        listePlusTotPlusTard = calculDateAuPlusTard(
            matriceAdj, tableauContraintes, listDateAuPlusTot)

        print("---------------------------------------------------------")
        print("\t7. Calcul des Marges")
        print("---------------------------------------------------------")
        listeComplete = calculMarges(listePlusTotPlusTard)

        affichageDate(listeComplete, ['Rangs', 'Tâches et sa longueur', 'Predecesseur', 'Date par Pred.',
                                      'Date au plus tôt', 'Successeurs', 'Date par Succ.', 'Date au plus tard', 'Marge'])

        # Ecriture de la trace du fichier
        trace(nomTrace, matrice_valeur, matriceAdj, tableauTracesRangs)
    except FileNotFoundError as e:
        if (numbFichier == -1):
            print("Au revoir !")
        else:
            print("Ce fichier n'existe pas, veuillez réessayer !")
