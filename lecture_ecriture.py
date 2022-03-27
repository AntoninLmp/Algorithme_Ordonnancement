
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
        print(tableauContrainte)
        return tableauContrainte
    return False

# ------------------------------------------------------------
# Ecriture de Trace
# ------------------------------------------------------------


def trace():

    return 0
