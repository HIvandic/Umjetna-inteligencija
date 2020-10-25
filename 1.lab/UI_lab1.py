import heapq
class cvor:
    def __init__(self, location, distance, parent):
        self.location = location
        self.distance = distance
        self.parent = parent

class cvor2:
    def __init__(self, location, distance, all, parent):
        self.location = location
        self.distance = distance
        self.all = all
        self.parent = parent

def pretrazi_u_sirinu (pocetno, dictionary, ciljnaD):
    visited = dict()
    opened = list()
    heapq.heapify(opened)
    order = 1
    heapq.heappush(opened, (0, order, pocetno))
    size = 1
    print("Running bfs:")
    while size != 0:
        dep, nmbr, n = heapq.heappop(opened)
        size = size - 1
        if n.location in ciljnaD:
            return len(visited), n
        visited.update({n.location: 0})
        for m in dictionary.get(n.location):
            if m[0] not in visited:
                order = order + 1
                size = size + 1
                heapq.heappush(opened, (dep + 1, order,cvor(m[0], m[1], n)))
    return None, None


def p_sirina(pocetno, dictionary, ciljnaD):
    visited, node = pretrazi_u_sirinu(pocetno, dictionary, ciljnaD)
    if node is None:
        print ("Fail")
    else:
        size = 1
        rj = node
        ispis = rj.location
        while (rj.parent != None):
            size = size + 1
            rj = rj.parent
            vrij = rj.location
            ispis = vrij.__add__("=>\n").__add__(ispis)
        print("States visited = ", str(visited+1)) #+1 jer ne prebroji inace ciljno
        print("Found path of length ", size, ":")
        print(ispis, "\n")


def pretrazi_s_jednolikom_cijenom(pocetno, dictionary, ciljnaD):
    visited = dict()
    opened = list()
    heapq.heapify(opened)
    order = 1
    heapq.heappush(opened, (0, order, pocetno))
    size = 1
    print("Running ucs:")
    while size != 0:
        dist, nmbr, n = heapq.heappop(opened)
        size = size - 1
        if n.location in ciljnaD:
            return len(visited), n
        visited.update({n.location: 0})
        for m in dictionary.get(n.location):
            if m[0] not in visited:
                order = order + 1
                size = size + 1
                dist = int(n.distance) + int(m[1])
                heapq.heappush(opened, (dist, order, cvor(m[0], str(dist), n)))
    return None, None


def p_cijena(pocetno, dictionary, ciljnaD):
    visited, node = pretrazi_s_jednolikom_cijenom(pocetno, dictionary, ciljnaD)
    if node is None:
        print ("Fail")
    else:
        size = 1
        rj = node
        ispis = rj.location
        cost = rj.distance
        while (rj.parent != None):
            size = size + 1
            rj = rj.parent
            vrij = rj.location
            ispis = vrij.__add__("=>\n").__add__(ispis)
        print("States visited = ", str(visited+1)) #+1 jer inace ne prebroji ciljno
        print("Found path of length ", size, " with total cost", cost, ":")
        print(ispis, "\n")


def pretrazi_astar(pocetno, dictionary, ciljnaD, heur):
    closed = dict()
    opened = list()
    heapq.heapify(opened)
    order = 1
    poc = cvor2(pocetno.location, pocetno.distance, heur.get(pocetno.location), None)
    heapq.heappush(opened, (0, order, poc))
    size = 1
    opened2 = dict()
    opened2.update({poc.location: 0})
    print("Running astar:")
    while size != 0:
        dist, nmbr, n = heapq.heappop(opened)
        size = size - 1
        if n.location in ciljnaD:
            return len(closed), n
        closed.update({n.location: 0})
        for m in dictionary.get(n.location):
            if m[0] in closed:
                continue
            nova = int(m[1]) + int(n.distance)
            prije = opened2.get(m[0])
            if prije is not None and prije < nova:
                continue
            dist = nova + int(heur.get(m[0]))
            size = size + 1
            order = order + 1
            opened2.update({m[0]: dist})
            heapq.heappush(opened, (dist, order, cvor2(m[0], str(nova), str(dist), n)))
    return None, None


def p_astar(pocetno, dictionary, ciljnaD, heur):
    closed, node = pretrazi_astar(pocetno, dictionary, ciljnaD, heur)
    if node is None:
        print ("Fail")
    else:
        size = 1
        rj = node
        ispis = rj.location
        cost = rj.distance
        while (rj.parent != None):
            size = size + 1
            rj = rj.parent
            vrij = rj.location
            ispis = vrij.__add__("=>\n").__add__(ispis)
        print("States visited = ", str(closed+1)) #+1 jer inace ne prebroji ciljno
        print("Found path of length ", size, " with total cost", cost, ":")
        print(ispis, "\n")


def add_sorted_2(opened, var):
    index = 0
    if len(opened) < 1:
        opened.append(var)
        return opened
    for element in opened:
        if int(element[1]) > int(var[1]):
            opened.insert(index, var)
            return opened
        index = index + 1
    opened.append(var)
    return opened


def provjera_optimisticnosti(obratno, heur, ciljna, stanja):
    print("Checking if heuristic is optimistic:")
    visited = dict()
    opened = list()
    heapq.heapify(opened)
    order = 1
    size = 0
    help = dict()
    optimisticna = True
    for m in stanja:
        if m in ciljna:
            heapq.heappush(opened, (0, order, m))
            order = order + 1
            size = size + 1
            help.update({m: "0"})
        else:
            help.update({m: str(float('inf'))})
    while size != 0:
        dist, nmbr, n = heapq.heappop(opened)
        size = size - 1
        novo = int(heur.get(n))
        if int(dist) < novo:
            print("[ERR] h(", n, ") > h*: ", str(novo), " > ", dist)
            optimisticna = False
        visited.update({n: 0})
        prijelaz = obratno.get(n)
        if prijelaz is not None:
            for k in prijelaz:
                alt = int(k[1]) + dist
                staro = help.get(k[0])
                if alt < float(staro) and k[0] not in visited:
                    size = size + 1
                    order = order + 1
                    help.update({k[0]: str(alt)})
                    heapq.heappush(opened, (alt, order, k[0]))
    return optimisticna


def provjera_konzistentnosti(dictionary, heur, stanja):
    print("Checking if heuristic is consistent:")
    konzistentna = True
    for m in stanja:
        for k in dictionary.get(m):
            h1 = int(heur.get(m))
            h2 = int(heur.get(k[0]))
            c = int(k[1])
            if h1 > (h2 + c):
                print("[ERR] h(", m, ") > h(", k[0], ") + c: ", h1, " > ", h2, " + ", c)
                konzistentna = False
    return konzistentna

f = open('istra.txt', encoding="utf8")
first = True
second = False
global pocetno
ciljna = list()
ciljnaD = dict()
stanja = list()
dictionary = dict()
obratno = dict()
nmbr = 0
transitions = 0
for line in f:
    line = line.strip()
    if line.startswith("#"):
        continue
    elif first:
        poc = line
        print("Start state: ", poc)
        pocetno = cvor(poc, "0", None)
        first = False
        second = True
    elif second:
        line = line.split(" ")
        for one in line:
            ciljna.append(one)
            ciljnaD.update({one: 0})
        print("End state(s): ", ciljna)
        second = False
    else:
        nmbr = nmbr + 1
        pom = line.split(":")
        desno = pom.pop(1).strip()
        desno = desno.split(" ")
        lista = list()
        stanja.append(pom[0])
        for final in desno:
            pom2 = final.split(",")
            if len(pom2) < 2:
                break
            lista.append((pom2[0], pom2[1]))
            if pom2[0] not in dictionary: #znaci da jos nema zapisa u obratno za taj grad
                obr = list()
                dictionary.update({pom2[0]: obr})
            if pom2[0] not in obratno:
                obr = list()
                obratno.update({pom2[0]: obr})
            obr = obratno.get(pom2[0])
            obr.append((pom[0], pom2[1]))
            obratno.update({pom2[0]: obr})
            transitions = transitions + 1
        dictionary.update({pom[0]: lista})
print("State space size: ", nmbr)
print("Total transitions: ", transitions, "\n")
p_sirina(pocetno, dictionary, ciljnaD)
p_cijena(pocetno, dictionary, ciljnaD)

h = open('istra_pessimistic_heuristic.txt', encoding="utf8")
heur = dict()
for line in h:
    pomocni = line.split(":")
    desno = pomocni.pop(1).strip()
    heur.update({pomocni.pop(0): desno})

p_astar(pocetno, dictionary, ciljnaD, heur)

opt = provjera_optimisticnosti(obratno, heur, ciljna, stanja)
if opt:
    print("Heuristic is optimistic\n")
else:
    print("Heuristic is not optimistic\n")

konz = provjera_konzistentnosti(dictionary, heur, stanja)
if konz:
    print("Heuristic is consistent\n")
else:
    print("Heuristic is not consistent\n")

f.close()
h.close()
