"""
Jeu escape game, projet du cours informatique
Auteurs : Mahri Nizar 495605, Lambrechts Aurelien 513576
Date De commencement : 2 novembre 2020
Date de dernière vérification : 15 novembre 2020
petit jeu escape game où le joueur devra répondre à des questions ainsi que 
se balader dans un labyrinthe
Entrée : Deplacement du personnage (touche directionnels) et reponse aux questions
Résultat : Jeu de reflexion
"""
from turtle import *  # importation des modules
from CONFIGS import *
"""Constantes globales"""
position = POSITION_DEPART  # donnée global de la position originale
liste_couloir, liste_objet, liste_porte, liste_win = [], [
], [], []  # sauvegarde de données grâce à des listes
compt = 0  # comptabilisateur global
"""Definitions des fonctions"""


def lire_matrice(fichier):
    """
    lecture du fichier contenant les données du terrain puis
    transforme les données en liste représentant une matrice
    entrée : fichier contenant les données du terrain
    Résultat : matrice du terrain
    """
    li = []
    with open(fichier, mode="r", encoding="UTF-8") as f:  # lit le fichier
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
    retour : taille de la case

    """
    case_largeur, case_hauteur = 0, 0  # definit les cases
    for i in matrice:  # calcul le nombre de lignes et de colonnes de la matrice
        case_hauteur += 1
        for j in i:
            case_largeur += 1
    # trouve le nombre de colonnes
    case_largeur = int(case_largeur/case_hauteur)
    plan_hauteur = ZONE_PLAN_MAXI[1]-ZONE_PLAN_MINI[1]
    plan_largeur = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[1]
    # dimension du plan turtle
    if plan_hauteur/case_hauteur > plan_largeur/case_largeur:  # retient la plus faible des valeurs
        taille_case = plan_largeur/case_largeur
    else:
        taille_case = plan_hauteur/case_hauteur
    return taille_case


def coordonnees(case, pas):
    """
    fonction calculant les coordonnées en pixel turtle
    retour : les coordonnées réel en coordonnéees pixel turtles
    """

    # place l'origine
    co_turtle_or = (ZONE_PLAN_MINI[0], ZONE_PLAN_MAXI[1]-pas)
    # calcul les coordonnées grâce aux dimensions de la case (le pas)
    co_turtle_case = (case[1]*pas+co_turtle_or[0], co_turtle_or[1]-case[0]*pas)
    return co_turtle_case


def tracer_carre(dimension):
    """
    Fonction traçant un carré grâce au module turtle
    retour : dessin carré
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
    retour : traçage de la case
    """
    color(couleur)  # définit la couleur
    up()  # relève le stylo
    setpos(case)  # dirige vers les coordonnées
    down()
    begin_fill()  # repose le stylo
    tracer_carre(pas)  # utilise la fonction qui trace un carré
    end_fill()


def deplacer_gauche():
    """
    Fonction permettant de deplacer le personnage une case vers la gauche
    retour : effectue le deplacement
    """
    global matrice, pas, position  # matrice global
    onkeypress(None, "Left")
    posi = deplacer((-1, 0))
    # fonction permettant de delimiter les cases en fonction de leur possibilité d'etre traverseée
    if case_importante(posi):
        # bloque le passage dans les murs
        pos_carre = (posi[0]+pas, posi[1])
        point(position)
        tracer_case(pos_carre, COULEUR_VUE, pas)  # trace une case derriere
    else:
        # retourne le mouvement en arrière
        position = (position[0], position[1]+1)
    onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    """
    Fonction permettant de deplacer le personnage une case vers la droite
    retour : effectue le deplacement
    """
    global matrice, pas, position
    onkeypress(None, "Right")
    posi = deplacer((1, 0))
    # fonction permettant de delimiter les cases en fonction de leur possibilité d'etre traverseée
    if case_importante(posi):
        # bloque le passage dans les murs
        pos_carre = (posi[0]-pas, posi[1])
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        # retourne le mouvement en arrière
        position = (position[0], position[1]-1)
    onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    """
    Fonction permettant de deplacer le personnage une case vers le haut
    retour : effectue le deplacement
    """
    global matrice, pas, position
    onkeypress(None, "Up")
    posi = deplacer((0, -1))
    # bloque le passage dans les murs
    # fonction permettant de delimiter les cases en fonction de leur possibilité d'etre traverseée
    if case_importante(posi):
        pos_carre = (posi[0], posi[1]-pas)
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        # retourne le mouvement en arrière
        position = (position[0]+1, position[1])
    onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    """
    Fonction permettant de deplacer le personnage une case vers le bas
    retour : effectue le deplacement
    """
    global matrice, pas, position
    onkeypress(None, "Down")
    posi = deplacer((0, 1))
    # fonction permettant de delimiter les cases en fonction de leur possibilité d'etre traverseée
    if case_importante(posi):
        # bloque le passage dans les murs
        pos_carre = (posi[0], posi[1]+pas)
        tracer_case(pos_carre, COULEUR_VUE, pas)
        point(position)
    else:
        position = (position[0]-1, position[1])
    onkeypress(deplacer_bas, "Down")


def annonce(phrase):
    """
    fonction permettant la création d'annonce simplement en écrivant un message en argument
    """
    remplissage()
    color("black")
    up()
    goto(-240, 235)
    down()
    write(phrase, font=(
        "Arial", 12, "bold"))


def case_importante(position):
    """
    fonction permettant de référencer les cases importantes pour ainsi diriger vers d'autres fonctions en rapport avec la case précise
    si le personnage arrive sur la case victoire alros un message va se lancer
    paramètre : la position qui va être vérifiée en fonction du plan et des différentes listes de données
    retour : va retourner un vrai ou faux permettant le déplacement du personnage
    """
    # ajuste les valeurs arrondi pour faciliter la comparaison
    new_position = (round(position[0]), round(position[1]))
    if new_position in liste_couloir:  # si position est dans le couloir alors mouvement possible
        res = True
    elif new_position in liste_objet:  # si position est objet alors le joueur recupère l'indice et transforme case objet en case couloir
        res = ramasser_objet(new_position)
        liste_objet.remove(new_position)
        liste_couloir.append(new_position)
    elif new_position in liste_porte:
        res = poser_question(new_position)
        if res:
            liste_porte.remove(new_position)
            liste_couloir.append(new_position)
    elif new_position in liste_win:  # quand le joueur arrive dans la case victoire alors enclenchement de la fin de partie
        remplissage()
        up()
        color("red")
        goto(-240, 240)
        down()
        write("Vous avez gagné !", font=("Arial", 30, "bold"))
        res = True
    else:  # mur donc pas de mouvement
        res = False
    return res


def poser_question(position):
    """
    Fonction permettant l'interaction avec le joueur afin de répondre aux questions
    des portes et les débloquant lorsque la réponse est bonne
    paramètre : la position sera transformée en coordonées pixel turtle afin de trouver la question respective dans le dictionnnaire
    retour : un vrai ou faux en fonction de si oui ou non la réponse à bien était donnée
    """
    global pas, compt, dic_portes
    for i in dic_portes .copy():  # crée une copie de dictionnaire afin de modifier le dico global pendant la loop
        zone = coordonnees(i, pas)
        if (round(zone[0]), round(zone[1])) == position:
            # valeur permettant de donner une question ou une réponse
            # question and reponse comprit dans [0] et [1]
            q_and_r = dic_portes.get(i)
            # appel fonction annonce qui indique l'état de la porte
            annonce("Cette porte est fermée")
            rep = textinput("Question : ", q_and_r[0])  # affiche la questions
            listen()
            if rep == q_and_r[1]:  # si la réponse est bonne alors la porte s'ouvre
                res = True
                annonce("La porte s'ouvre !")
                dic_portes.pop(i)
            else:
                res = False  # sinon rien en change
                annonce("Mauvaise réponse")
    return res


def remplissage():
    """
    Fonction permettant de nettoyer l'écran d'affichage en le remplissant de blanc
    """
    color("white")  # dessine un rectangle blanc
    up()
    goto(-245, 260)
    down()
    begin_fill()
    fd(600)
    right(90)
    fd(30)
    right(90)
    fd(600)
    right(90)
    fd(30)
    right(90)
    end_fill()


def ramasser_objet(position):
    """
    fonction permettant le rammassage d'objet ainsi que l'écriture de l'inventaire
    paramètre : la position sera transformée en coordonées pixel turtle afin de trouver l'objet respectif dans le dictionnnaire
    retour : vrai permettant le déplacement
    """
    global pas, compt, dic_objets
    for i in dic_objets .copy():  # crée une copie de dictionnaire afin de modifier le dico global pendant la loop
        # transforme les co du plan en co pixel turtle
        zone = coordonnees(i, pas)
        # compare les coordonnées du fichier objet avec la case sur laquelle le joueur est
        if (round(zone[0]), round(zone[1])) == position:
            color("black")
            indice = dic_objets .get(i)  # marque l'objet du dico
            up()
            goto(80, 140-compt)
            down()
            write(indice, font=("Arial", 15, "italic"))  # écrit l'objet
            annonce(f"Vous avez trouvé : {indice}")  # affiche l'annonce
            compt += 30
            # retire l'item du dico global afin de faciliter le code
            dic_objets .pop(i)
    return True


def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    fonction permettant la création d'un dictionnaire en fonction du fichier objet
    retour : un dictionnaire en fonction du fichier
    """
    li = []
    dic = {}
    with open(fichier_des_objets, mode="r", encoding="UTF-8") as f:
        for line in f:
            # Fait avec une liste temporaire afin de faciliter l'ajout au dico
            li.append(eval(line))
    for i in li:
        dic[i[0]] = i[1]
    return dic


def afficher_plan(matrice):
    """
    Fonction permettant de tracer le plan du chateau où le personnage
    va se déplacer, de plus ,les appends des listes serviront de marquer les cases
    importantes pour faciliter le deplacement dans les différentes cases.
    paramètre : matrice est le plan avec lequel la fonction va suivre le dessin
    retour : mapping du terrain
    """
    global pas
    tracer(0)  # trace automatiquement
    # transforme les coordonnées en pixels turtle
    co = coordonnees((0, 0), pas)
    i = 0  # assigne i en tant que comptabilisateur de loop
    for ligne in matrice:
        for colonne in ligne:  # 2 loop qui vont lire toute les données de la matrice
            if colonne == 1:  # lors de chaque traçage les différentes données des cases seront sauvegardées dans des listes
                tracer_case(co, COULEUR_MUR, pas)
            elif colonne == 0:
                tracer_case(co, COULEUR_CASES, pas)
                liste_couloir.append((round(co[0]), round(co[1])))
            elif colonne == 2:
                tracer_case(co, COULEUR_OBJECTIF, pas)
                liste_win.append((round(co[0]), round(co[1])))
            elif colonne == 3:
                tracer_case(co, COULEUR_PORTE, pas)
                liste_porte.append((round(co[0]), round(co[1])))
            elif colonne == 4:
                tracer_case(co, COULEUR_OBJET, pas)
                liste_objet.append((round(co[0]), round(co[1])))
            # change les coordonées en avançant dans le plan
            co = (co[0]+pas, co[1])
        i += 1
        co = coordonnees((0, 0), pas)  # reset les coordonnées
        co = (co[0], co[1]-pas*i)  # change les composantes en y
    color("darkred")
    up()
    # crée l'affichage Inventaire
    goto((POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1]-35))
    down()
    write("Inventaire :", font=("Arial", 27, 'underline'))


def point(case):
    """
    fonction permettant de gérer la position du personnage ainsi que de tracer le point le représentant
    paramètre : la case definit juste les coordonées du plan normal qui vont etre transformées en coordonnées pixel turtle
    retour : création du personnage
    """
    global pas
    # transforme la case en coordonnées pixels turtle
    co = coordonnees(case, pas)
    # prend l'origine du cercle comme étant le centre de la case
    co_point = (co[0]+pas/2, co[1]+pas/2)
    up()
    setpos(co_point)
    down()
    dot(pas*RATIO_PERSONNAGE, COULEUR_PERSONNAGE)


def deplacer(mouvement):
    """
    Fonction permettant le mouvement du personnage en fonction de la direction, les coordonnées
    seront transformées en coordonnées pixel turtle
    paramètres: matrice pour le plan, mouvement indique dans quel sens le deplacement va se faire
    retour : les coordonnées en fonction des pixels turtle
    """
    global pas, position
    position = (position[0] + mouvement[1], position[1] +
                mouvement[0])  # effectue le mouvement
    co_p = coordonnees(position, pas)
    return co_p


"""Code principal"""

dic_objets, dic_portes = creer_dictionnaire_des_objets(
    fichier_objets), creer_dictionnaire_des_objets(fichier_questions)  # donnée globale du dictionnaire
matrice = lire_matrice(fichier_plan)  # donnée globale du plan du chateau
pas = calculer_pas(matrice)  # donnée globale du pas (taille d'un carré)

afficher_plan(matrice)  # appel de la fonction permettant d'afficher le plan
point(position)  # appel  à la fonction permettant l'apparition du personnage
listen()  # écoute du clavier
onkeypress(deplacer_gauche, "Left")
onkeypress(deplacer_droite, "Right")
onkeypress(deplacer_haut, "Up")
onkeypress(deplacer_bas, "Down")
mainloop()
