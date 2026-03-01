donnees = [
 ("Sara", "Math", 12, "G1"),
 ("Sara", "Info", 14, "G1"),
 ("Ahmed", "Math", 9, "G2"),
 ("Adam", "Chimie", 18, "G1"),
 ("Sara", "Math", 11, "G1"),
 ("Bouchra", "Info", "abc", "G2"),
 ("", "Math", 10, "G1"),
 ("Yassine", "Info", 22, "G2"),
 ("Ahmed", "Info", 13, "G2"),
 ("Adam", "Math", None, "G1"),
 ("Sara", "Chimie", 16, "G1"),
 ("Adam", "Info", 7, "G1"),
 ("Ahmed", "Math", 9, "G2"),
 ("Hana", "Physique", 15, "G3"),
 ("Hana", "Math", 8, "G3"),
]

# PARTIE 1 : Validation

def valider(enregistrement):
    nom, matiere, note, groupe = enregistrement

    if nom == "" or matiere == "" or groupe == "":
        return False, "champ vide"

    try:
        note = float(note)
    except:
        return False, "note non numerique"

    if note < 0 or note > 20:
        return False, "note hors intervalle"

    return True, note


def nettoyer_donnees(donnees):
    valides = []
    erreurs = []
    doublons = set()
    deja_vu = set()

    for ligne in donnees:

        if ligne in deja_vu:
            doublons.add(ligne)
        else:
            deja_vu.add(ligne)

            ok, resultat = valider(ligne)

            if ok:
                nom, matiere, _, groupe = ligne
                valides.append((nom, matiere, resultat, groupe))
            else:
                erreurs.append({"ligne": ligne, "raison": resultat})

    return valides, erreurs, doublons

# PARTIE 2 : Structuration

def structurer(valides):
    matieres = set()
    etudiants = {}
    groupes = {}

    for nom, matiere, note, groupe in valides:

        matieres.add(matiere)

        if nom not in etudiants:
            etudiants[nom] = {}

        if matiere not in etudiants[nom]:
            etudiants[nom][matiere] = []

        etudiants[nom][matiere].append(note)

        if groupe not in groupes:
            groupes[groupe] = set()

        groupes[groupe].add(nom)

    return matieres, etudiants, groupes

# PART 3 : 

def somme_recursive(liste):
    if liste == []:
        return 0
    return liste[0] + somme_recursive(liste[1:])


def moyenne(liste):
    if liste == []:
        return 0
    return somme_recursive(liste) / len(liste)


def calculer_stats(etudiants):
    stats = {}

    for nom in etudiants:
        toutes_notes = []
        moyennes_matieres = {}

        for matiere in etudiants[nom]:
            notes = etudiants[nom][matiere]
            moyennes_matieres[matiere] = moyenne(notes)

            for n in notes:
                toutes_notes.append(n)

        stats[nom] = {
            "moyenne_generale": moyenne(toutes_notes),
            "moyennes_par_matiere": moyennes_matieres,
            "min": min(toutes_notes) if toutes_notes else None,
            "max": max(toutes_notes) if toutes_notes else None
        }

    return stats

# PARTIE 4 : Anomalies

def analyser(etudiants, matieres, groupes, stats):
    alertes = {
        "notes_multiples": [],
        "profils_incomplets": [],
        "groupes_faibles": [],
        "ecarts_importants": []
    }

    # notes multiples
    for nom in etudiants:
        for matiere in etudiants[nom]:
            if len(etudiants[nom][matiere]) > 1:
                alertes["notes_multiples"].append((nom, matiere))

    # profils incomplets
    for nom in etudiants:
        if len(etudiants[nom]) < len(matieres):
            alertes["profils_incomplets"].append(nom)

    # groupes faibles
    for groupe in groupes:
        notes_groupe = []

        for nom in groupes[groupe]:
            if nom in stats:
                if stats[nom]["min"] is not None:
                    notes_groupe.append(stats[nom]["min"])
                if stats[nom]["max"] is not None:
                    notes_groupe.append(stats[nom]["max"])

        if notes_groupe != []:
            moy = sum(notes_groupe) / len(notes_groupe)
            if moy < 10:
                alertes["groupes_faibles"].append(groupe)

    # ecarts importants
    for nom in stats:
        mini = stats[nom]["min"]
        maxi = stats[nom]["max"]

        if mini is not None and maxi is not None:
            if maxi - mini > 10:
                alertes["ecarts_importants"].append(nom)

    return alertes


# PROGRAMME PRINCIPAL

if __name__ == "__main__":

    valides, erreurs, doublons = nettoyer_donnees(donnees)

    matieres, etudiants, groupes = structurer(valides)

    stats = calculer_stats(etudiants)

    alertes = analyser(etudiants, matieres, groupes, stats)

    print("Valides :", len(valides))
    print("Erreurs :", len(erreurs))
    print("Doublons :", doublons)

    print("Alertes :", alertes)
