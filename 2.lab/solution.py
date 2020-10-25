import sys


class cvor:
    def __init__(self, p1, indeks1, p2, indeks2, parent, value, dep):
        self.p1 = p1
        self.indeks1 = indeks1
        self.p2 = p2
        self.indeks2 = indeks2
        self.parent = parent
        self.value = value
        self.dep = dep


def unos_klauzula(putanja_klauzule):
    klauz = list()
    h = open(putanja_klauzule, mode='r', encoding='utf8')
    for line in h:
        line = line.strip()
        if line.startswith("#"):
            continue
        line = line.lower()
        vazna = True
        part = set()
        for one in line.split(" "):
            if one == "v":
                continue
            if one.startswith("~"):
                if one[1:] in part:
                    vazna = False
            else:
                if "~".__add__(one) in part:
                    vazna = False
                    break
            part.add(one)
        if vazna:
            klauz.append(part)
    return klauz


def unos_kor_nar(putanja_kor_nar):
    kor_nar = list()
    h = open(putanja_kor_nar, mode='r', encoding='utf8')
    for line in h:
        line = line.strip()
        if line.startswith("#"):
            continue
        line = line.lower()
        kor_nar.append(line)
    return kor_nar


def set_to_string(klauzula):
    rez = ""
    first = True
    for clan in klauzula:
        if first:
            rez += clan
            first = False
        else:
            rez += " v " + clan
    return rez


def pl_resolve(cv):
    novi = list()
    prva = cv.p1
    druga = cv.p2
    for one in druga:
        jedno = set()
        if one.startswith("~"):
            if one[1:] in prva:
                jedno = prva | druga
                jedno.remove(one)
                jedno.remove(one[1:])
                if len(jedno) == 0:
                    jedno = "NIL"
        else:
            if "~".__add__(one) in prva:
                jedno = prva.union(druga)
                jedno.remove(one)
                jedno.remove("~".__add__(one))
                if len(jedno) == 0:
                    jedno = "NIL"
        tautologija = False
        if len(jedno) != 0:
            for test in jedno:
                if test.startswith("~"):
                    if test[1:] in jedno:
                        tautologija = True
                else:
                    if "~".__add__(test) in jedno:
                        tautologija = True
            if not tautologija:
                novi.append(jedno)
    return novi


def ukloni_redundantne(klauzule):
    velicina = len(klauzule)
    makni = list()
    for i in range(0, velicina):
        prva = klauzule[i]
        for j in range(0, velicina):
            if i == j:
                continue
            druga = klauzule[j]
            if prva.issubset(druga) and prva != druga:
                makni.append(j)
                break
    for one in makni:
        klauzule.pop(one)


def uredi(new, klauzule):
    novo = list()
    velicina = len(klauzule)
    for one in new:
        dodaj = True
        for j in range(0, velicina):
            druga = klauzule[j]
            if druga.issubset(one[0]):
                dodaj = False
                break
        if dodaj:
            novo.append(one)
    return novo


def rezolucija_opovrgavanjem(klauzule, rjecnik, vrij):
    # negiranje ispitnog
    zadnji = klauzule.pop()
    size = 0
    for jedna in zadnji:
        one = set()
        size = size + 1
        if jedna.startswith("~"):
            jedna = jedna[1:]
        else:
            jedna = "~".__add__(jedna)
        one.add(jedna)
        klauzule.append(one)
        rjecnik.update({set_to_string(one): vrij})
        vrij = vrij + 1

    ukloni_redundantne(klauzule)
    stog = list()
    velicina = len(klauzule)
    for d in range(0, velicina - size):
        for indeks in range(0, size):
            stog.append(cvor(klauzule[d], d + 1, klauzule[velicina-indeks-1], velicina - indeks, None, None, 0))
    while 1:
        new = list()
        for p in range(0, len(stog)):
            cv = stog.pop()
            rezolvente = pl_resolve(cv)
            if len(rezolvente) == 1:
                cv.value = rezolvente[0]
            if "NIL" in rezolvente:
                return True, cv,  rjecnik, vrij
            for one_1 in rezolvente:
                new.append((one_1, cv))
        k = 1
        velicina = len(klauzule)
        new = uredi(new, klauzule)
        for one in new:
            if one[0] not in klauzule:
                for m in range(0, velicina):
                    stog.append(cvor(klauzule[m], m + 1, one[0], velicina + k, one[1], None, one[1].dep + 1))
                klauzule.append(one[0])
                k = k + 1
        if k == 1:
            return False, None, rjecnik, vrij


def dodaj(klauzule, one):
    odvojeno = one.split(" ")
    jedno = set()
    for jedan in odvojeno:
        if jedan == "v":
            continue
        elif jedan == "+":
            break
        jedno.add(jedan)
    klauzule.append(jedno)
    return klauzule


def ukloni(klauzule, one):
    odvojeno = one.split(" ")
    jedno = set()
    for jedan in odvojeno:
        if jedan == "v":
            continue
        elif jedan == "-":
            break
        jedno.add(jedan)
    klauzule.remove(jedno)
    return klauzule


def upitaj(klauzule, one, verbose):
    radna = list()
    rj = dict()
    vr = 1
    for jedna in klauzule:
        radna.append(jedna)
        rj.update({set_to_string(jedna): vr})
        vr = vr + 1
    pocetni_ispis = ""
    for u in range(0, len(radna)):
        pocetni_ispis += str(u + 1) + ". "
        fir = True
        for h in radna[u]:
            if fir:
                pocetni_ispis += h
                fir = False
            else:
                pocetni_ispis += " v " + h
        pocetni_ispis += "\n"

    ispitna = one.split(" ")
    ispitni = set()
    pocetno = len(radna)
    for jedno in ispitna:
        if jedno == "v":
            continue
        if jedno == "?":
            break
        ispitni.add(jedno)
    radna.append(ispitni)
    dokazujemo = ""
    first = True
    for z in ispitni:
        if first:
            dokazujemo += z
            first = False
        else:
            dokazujemo += " v " + z

    istinitost_1, cv_1, rj, vr = rezolucija_opovrgavanjem(radna, rj, vr)
    if istinitost_1:
        if verbose:
            ispisi_verbose(cv_1, pocetni_ispis, dokazujemo, ispitni, pocetno, rj, vr)
        else:
            print(dokazujemo, "is true")
    else:
        print(dokazujemo, "is unknown")


def ispisi_verbose(cv, ispisP, dokazujemo, dok, pocetno, rjecnik, vrij):
    ispis = ""
    ispis += ispisP
    i = pocetno
    ispis += "=============\n"
    prvi = True
    for jedan in dok:
        if jedan.startswith("~"):
            jedan = jedan[1:]
        else:
            jedan = "~".__add__(jedan)
        if prvi:
            ispis += str(i + 1).__add__(". ").__add__(jedan)
            prvi = False
        else:
            ispis += "\n".__add__(str(i + 1)).__add__(". ").__add__(jedan)
        i = i + 1
    ispis += "\n" + "=============\n"
    ispis2 = ""
    lista = list()
    while cv.parent is not None:
        lista.append(cv)
        cv = cv.parent
    lista.append(cv)
    for j in range(0, len(lista)):
        jedan = lista[len(lista) - j - 1]
        clan = ""
        if jedan.value == "NIL":
            clan = "NIL"
        else:
            clan = set_to_string(jedan.value)
        rjecnik.update({clan: vrij})
        vrij = vrij + 1
        roditelj1 = str(rjecnik.get(set_to_string(jedan.p1)))
        roditelj2 = str(rjecnik.get(set_to_string(jedan.p2)))
        ispis2 += str(cv.dep + i + 1).__add__(". ").__add__(clan).__add__(" (").__add__(roditelj1).__add__(", ").__add__(roditelj2).__add__(")\n")
        i = i + 1
    ispis += ispis2
    ispis += "=============\n" + dokazujemo + " is true"
    print(ispis)


rjecnik = dict()
input_1 = sys.argv
input_size = len(sys.argv)
podzadatak = input_1[1]
putanja_klauzule = input_1[2]
klauzule = unos_klauzula(putanja_klauzule)
pocetno = len(klauzule) - 1
dok = klauzule.pop()
vrij = 1
for klauzula in klauzule:
    rjecnik.update({set_to_string(klauzula): vrij})
    vrij = vrij + 1
klauzule.append(dok)
dokazujemo = ""
first = True
for z in dok:
    if first:
        dokazujemo += z
        first = False
    else:
        dokazujemo += " v " + z

global putanja_kor_nar
verbose = False
testni = False

if input_size == 4:
    if input_1[3] == "verbose":
        verbose = True
    else:
        putanja_kor_nar = input_1[3]
        testni = True
elif input_size == 5:
    putanja_kor_nar = input_1[3]
    verbose = True
    testni = True

#priprema pocetno zadanog za ispis
ispisP = ""
for i in range(0, pocetno):
    ispisP += str(i + 1) + ". "
    first = True
    for j in klauzule[i]:
        if first:
            ispisP += j
            first = False
        else:
            ispisP += " v " + j
    ispisP += "\n"


if input_1[1] == "resolution":
    istinitost, cv, rjecnik, vrij = rezolucija_opovrgavanjem(klauzule, rjecnik, vrij)
    if istinitost:
        if verbose:
            ispisi_verbose(cv, ispisP, dokazujemo, dok, pocetno, rjecnik, vrij)
        else:
            print(dokazujemo, "is true")
    else:
        print(dokazujemo, "is unknown")

elif input_1[1] == "cooking_test":
    if not testni:
        print("Nije unesena putanja")
        exit(0)
    kor_nar = unos_kor_nar(putanja_kor_nar)
    for one in kor_nar:
        linija = one.split(" ")
        naredba = linija[len(linija)-1]
        if naredba == "+":
            dodaj(klauzule, one)
        elif naredba == "-":
            ukloni(klauzule, one)
        elif naredba == "?":
            upitaj(klauzule, one, verbose)


elif input_1[1] == "cooking_interactive":
    k = 1
    while(k):
        print("Please enter your query:")
        n = input()
        linija = n.split(" ")
        naredba = linija[len(linija) - 1]
        if naredba == "+":
            klauzule = dodaj(klauzule, n)
        elif naredba == "-":
            klauzule = ukloni(klauzule, n)
        elif naredba == "?":
            upitaj(klauzule, n, verbose)
        elif naredba == "exit":
            k = 0
else:
    print("Neispravan unos")
    exit(0)
