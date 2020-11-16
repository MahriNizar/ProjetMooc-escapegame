from turtle import *
from CONFIGS import *


def lire_matrice(fichier):
    """
    lecture du fichier contenant les données du terrain puis
    transforme les données en liste représentant une matrice
    entrée : fichier contenant les données du terrain
    Résultat : matrice du terrain
    """
    li = []
    with open(fichier, mode="r") as f:  # lit le fichier
        for line in f:
            eph_li = []  # lit chaque ligne du fichier puis crée une liste éphémère
            # retire les espaces contenant dans la ligne
            for j in line.replace(" ", ""):
                if j == "\n":  # condition permettant la suppression des newlines
                    pass
                else:
                    # ajoute chaque paramètre en le transformant en integer puis l'ajoute dans la pré-liste
                    eph_li.append(int(j))
            li.append(eph_li)  # ajoute à la liste finale
    return li


def calculer_pas(matrice):
    """
    Fonction permettant de calculer la dimension donner aux cases pour que le plan tienne dans la zone de fenêtre turtle qu}on définie
    elle divise la largeur et la hauteur de la zone par le nombre de cases qu'elle doit accueillir
    et puis retient la plus faible des valeurs

    """
    case_largeur, case_hauteur = 0, 0  # definit les cases
    for i in matrice:  # calcul le nombre de lignes et de colonnes de la matrice
        case_hauteur += 1
        for j in i:
            case_largeur += 1
    # trouve le nombre de colonnes
    case_largeur = int(case_largeur/case_hauteur)
    plan_hauteur, plan_largeur = 200+240, 50+240  # dimension du plan turtle
    if plan_hauteur/case_hauteur > plan_largeur/case_largeur:  # retient la plus faible des valeurs
        taille_case = plan_largeur/case_largeur
    else:
        taille_case = plan_hauteur/case_hauteur
    return taille_case


def coordonnees(case, pas):
    """
    fonction calculant les coordonnées en pixel turtle, changeant les coordonées de case en coordonées turtle
    """
    co_turtle_or = (-240, 184.74)  # place l'origine
    # calcul les coordonnées grâce aux dimensions de la case (le pas)
    co_turtle_case = (case[1]*pas+co_turtle_or[0], co_turtle_or[1]-case[0]*pas)
    return co_turtle_case


def tracer_carre(dimension):
    """
    Fonction traçant un carré grâce au module turtle
    """
    for i in range(4):
        # for loop créant le carré
        forward(dimension)
        left(90)
    return


def tracer_case(case, couleur, pas):
    """
    Fonction permettant de tracer une case en fonction de coordonnées de pixel turtle qui va placer la structure de notre labyrinthe
    on peut definir la couleur et la taille de la case
    """
    color(couleur)  # définit la couleur
    up()  # relève le stylo
    setpos(case)  # dirige vers les coordonnées
    down()
    begin_fill()  # repose le stylo
    tracer_carre(pas)  # utilise la fonction qui trace un carré
    end_fill()


def deplacer_gauche():
    global matrice, pas, position
    onkeypress(None, "Left")
    posi = deplacer(matrice, position, (-1, 0))
    if (round(posi[0]), round(posi[1])) in liste_couloir:
        # bloque le passage dans les murs
        pos_carre = (posi[0]+pas, posi[1])
        point(position)
        tracer_case(pos_carre, COULEUR_VUE, pas)

    else:
        position = (position[0], position[1]+1)
    onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    global matrice, pas, position
    onkeypress(None, "Right")
    posi = deplacer(matrice, position, (1, 0))
    if (round(posi[0]), round(posi[1])) in liste_couloir:
        # bloque le passage dans les murs
        pos_carre = (posi[0]-pas, posi[1])
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        position = (position[0], position[1]-1)
    onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    global matrice, pas, position
    onkeypress(None, "Up")
    posi = deplacer(matrice, position, (0, -1))
    if (round(posi[0]), round(posi[1])) in liste_couloir:  # bloque le passage dans les murs
        pos_carre = (posi[0], posi[1]-pas)
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        position = (position[0]+1, position[1])
    onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    global matrice, pas, position
    onkeypress(None, "Down")
    posi = deplacer(matrice, position, (0, 1))
    if (round(posi[0]), round(posi[1])) in liste_couloir:
        # bloque le passage dans les murs
        pos_carre = (posi[0], posi[1]+pas)
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        position = (position[0]-1, position[1])
    onkeypress(deplacer_bas, "Down")


def case_importante(position):
    new_position = (round(position[0]), round(position[1]))
    if new_position in liste_couloir:
        res = True
    elif new_position in liste_objet:
        res = case_objet(new_position)
    elif new_position in liste_porte:
        res = case_porte()


def case_porte(position):
    pass


def case_objet(position):
    pass


def afficher_plan(matrice):
    """
    Fonction permettant de tracer le plan du chateau où le personnage
    va se déplacer, de plus ,les appends des listes serviront de marquer les cases 
    importantes pour faciliter le deplacement dans les différentes cases.
    """
    tracer(0)
    pas = calculer_pas(matrice)  # calcule la longueur d'un carré
    # transforme les coordonnées en pixels turtle
    co = coordonnees((0, 0), pas)
    i = 0  # assigne i en tant que comptabilisateur de loop
    for ligne in matrice:
        for colonne in ligne:  # 2 loop qui vont lire toute les données de la matrice
            if colonne == 1:
                tracer_case(co, COULEUR_MUR, pas)
            elif colonne == 0:
                tracer_case(co, COULEUR_CASES, pas)
                liste_couloir.append((round(co[0]), round(co[1])))
            elif colonne == 2:
                tracer_case(co, COULEUR_OBJECTIF, pas)
            elif colonne == 3:
                tracer_case(co, COULEUR_PORTE, pas)
                liste_porte.append(co)
            elif colonne == 4:
                tracer_case(co, COULEUR_OBJET, pas)
                liste_objet.append(co)
            # change les coordonées en avançant dans le plan
            co = (co[0]+pas, co[1])
        i += 1
        co = coordonnees((0, 0), pas)
        co = (co[0], co[1]-pas*i)


def point(case):
    global pas
    co = coordonnees(case, pas)
    co_point = (co[0]+pas/2, co[1]+pas/2)
    up()
    setpos(co_point)
    down()
    dot(pas*RATIO_PERSONNAGE, COULEUR_PERSONNAGE)


def deplacer(matrice, pos, mouvement):
    global pas, position
    position = (position[0] + mouvement[1], position[1] + mouvement[0])
    co_p = coordonnees(position, pas)
    return co_p


position = POSITION_DEPART
liste_couloir, liste_objet, liste_porte = [], [], []
matrice = lire_matrice(fichier_plan)
pas = calculer_pas(matrice)
print(coordonnees((7, 1), pas))

afficher_plan(matrice)
point(position)
listen()
onkeypress(deplacer_gauche, "Left")
onkeypress(deplacer_droite, "Right")
onkeypress(deplacer_haut, "Up")
onkeypress(deplacer_bas, "Down")
mainloop()
