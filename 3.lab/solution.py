import sys
import math


class Node:
    def __init__(self, value, children, most):
        self. value = value
        self.children = children
        self.most = most


class ID3:
    def __init__(self, mode, model, max_depth, num_trees, feature_ratio, example_ratio):
        self.mode = mode
        self.model = model
        self.max_depth = max_depth
        self.num_trees = num_trees
        self.feature_ratio = feature_ratio
        self.example_ratio = example_ratio
        self.tree = None

    def fit(self, train_data, names_test):
        # provodi ucenje modela
        mode = self.mode
        y = list() #moguce odluke
        for one in train_data:
            rj = one[len(one)-1]
            if rj not in y:
                y.append(rj)
        y.sort()
        dubina = 0
        rez = id3_alg(train_data, train_data, names_test, y, dubina) #stvaranje stabla odluke
        self.tree = rez
        rj = list()
        rj = ispis(rez, rj, 0) #dohvacanje za ispis
        fir = True
        for i in range(0, len(rj)): #ispis dubine i parametra
            dubina, vrijednost = rj[i]
            if fir:
                fir = False
                print(str(dubina) + ":" + vrijednost, end="")
            else:
                print(", "+str(dubina)+":"+vrijednost, end="")
        print()
        return y #vraca moguce odluke

    def predict(self, test_data, indeksi, y):
        # predvida ciljnu varijablu
        total = 0
        correct = 0
        matrica = list([0] * len(y) * len(y))
        pomocni = dict()
        br = 0
        y.sort()
        for i in range(0, len(y)):
            for j in range(0, len(y)):
                pomocni[(y[i], y[j])] = br #sluzi za odredivanje indeksa u matrici zabune
                br = br + 1
        f = True
        for one in test_data: #ispis predikcije za svaki
            start = self.tree
            while 1:
                vrij = indeksi.get(start.value) #da zna na koju poziciju unutar liste gleda za taj parametar
                if start.children is None: #dolazak do odluke
                    if f:
                        f = False
                        print(start.value, end="")
                    else:
                        print(" " + start.value, end="")
                    matrica[pomocni.get((one[len(one)-1], start.value))] = matrica[pomocni.get((one[len(one)-1], start.value))] + 1
                    total = total + 1
                    if start.value == one[len(one)-1]:
                        correct = correct + 1
                    break
                zastavica = 0
                for i in range(0, len(start.children)):
                    vrsta, cvor = start.children[i]
                    if one[vrij] == vrsta: #trazi poklapanje
                        start = cvor #pomice se na iduci cvor
                        zastavica = 1
                        break
                if zastavica == 0: #ako nije nadeno poklapanje uzima najcescu vrijednost u tom cvoru
                    if f:
                        f = False
                        print(start.most, end="")
                    else:
                        print(" " + start.most, end="")
                    matrica[pomocni.get((one[len(one) - 1], start.most))] = matrica[pomocni.get(
                        (one[len(one) - 1], start.most))] + 1
                    total = total + 1
                    if start.most == one[len(one) - 1]:
                        correct = correct + 1
                    break
        print()
        pr = correct / total
        print("%.5f" % pr)
        for i in range(0, len(y)):
            f1 = True
            for j in range(0, len(y)):
                if f1:
                    f1 = False
                    print(str(matrica[pomocni.get((y[i], y[j]))]), end="")
                else:
                    print(" " + str(matrica[pomocni.get((y[i], y[j]))]), end="")
            print()


def ispis(tree, rj, dubina): #vraca ispis dubine i parametra
    if tree.children is None:
        return rj
    rj.append((dubina, tree.value))
    for one in tree.children:
        if one[1] is not None:
            ispis(one[1], rj, dubina + 1)
    return rj


def id3_alg(D, Dp, X, y, dubina):
    global max_depth, moguce_vrij
    if len(D) == 0: #nema vise train data
        v = argmax_v(Dp, y)
        return Node(v, None, v)
    v = argmax_v(D, y)
    if max_depth != -1 and dubina >= max_depth: #provjera je li dostignuta max dubina (ako je zadana)
        return Node(v, None, v)
    if len(X) == 1 or Dv(D, v): #svi parametri iskoristeni ili svi train data imaju istu vrij
        return Node(v, None, v)
    x, vrij, index = argmax_IG(D, X, y)
    subtrees = list()
    vrij_d = dict()
    for one in moguce_vrij.get(x):
        vrij_d[one] = list()
    for one in D: #sprema sve train data u rjecnik prema vrijednosti trenutnog parametra koji ujedno i uklanja
        v = one[index]
        one.pop(index)
        prev = vrij_d.get(v)
        prev.append(one)
        vrij_d[v] = prev
    for v in moguce_vrij.get(x): #ide po svim vrijednostima za taj parametar
        Dx = vrij_d.get(v)
        new = list()
        for vrijednost in X:
            if vrijednost != x:
                new.append(vrijednost)
        t = id3_alg(Dx, D, new, y, dubina + 1)
        subtrees.append((v, t))
    return Node(x, subtrees, argmax_v(D, y))


def Dv(D, v):
    for one in D:
        if one[len(one) - 1] != v:
            return False
    return True


def argmax_v(D, y):
    values = dict()
    for one in y:
        values[one] = 0
    for one in D:
        key = one[len(one) - 1]
        value = values.get(key)
        value = value + 1
        values[key] = value
    first = True
    max = ("0", -1)
    for one in values: #trazi najcescu odluku
        if first:
            max = (one, values.get(one))
            first = False
        else:
            now = values.get(one)
            if now == max[1]:
                if one < max[0]:
                    max = (one, now)
            if now > max[1]:
                max = (one, now)
    return max[0]


def argmax_IG(D, X, y):
    global mode
    values = dict()
    for one in y:
        values[one] = 0
    for one in D:
        key = one[len(one) - 1]
        value = values.get(key)
        value = value + 1
        values[key] = value
    Ed = 0
    for one in values: #racuna Ed
        value = values.get(one)
        Ed += - value / len(D) * math.log2(value / len(D))
    max, index = -1, 0
    vrij = list()
    svi = list()
    for k in range(0, len(X) - 1): # -1 jer ne gledamo zadnji stupac
        IG = Ed
        d = dict()
        for one in D:
            key = one[k]
            value = d.get(key)
            if value is None:
                value = 0
            value = value + 1
            d[key] = value
        vrijednosti = d.keys()
        for one in vrijednosti:
            rj = dict()
            sum = 0
            for jedan in D:
                if jedan[k] == one:
                    key = jedan[len(jedan) - 1]
                    value = rj.get(key)
                    if value is None:
                        value = 0
                    value = value + 1
                    rj[key] = value
                    sum = sum + 1
            E = 0
            for jedan in rj:
                jedno = rj.get(jedan)
                ukupno = d.get(one)
                E += - jedno / ukupno * math.log2(jedno / ukupno)
            IG = IG - d.get(one) / len(D) * E
        if IG == max:
            if X[k] < X[index]:
                index = k
                vrij = vrijednosti
        if IG > max:
            max = IG
            index = k
            vrij = vrijednosti
        svi.append((IG, X[k]))
    if mode != "test":
        sort = sorted(svi, key=lambda x: x[0], reverse=True)
        for j in range(0, len(sort)):
            current, value = sort[j]
            print("IG(" + value + ")=", end='')
            print("%.4f" % current, end='  ')
        print()
    return X[index], vrij, index


argumenti = sys.argv
if len(argumenti) != 4:
    print("Neispravan broj argumenata")
    exit(0)

# skup podataka za treniranje
d = open(argumenti[1], 'r', encoding='utf8')
names_train = list()
train_data = list()
moguce_vrij = dict()
first = True
for line in d:
    line = line.strip()
    odvojeno = line.split(",")
    if first:
        names_train = odvojeno
        for jed in odvojeno:
            moguce_vrij[jed] = set()
        first = False
    else:
        train_data.append(odvojeno)
        for i in range(0, len(odvojeno)):
            prethodno = moguce_vrij.get(names_train[i])
            prethodno.add(odvojeno[i])
            moguce_vrij[names_train[i]] = prethodno
for every in moguce_vrij:
    val = moguce_vrij.get(every)
    l = list(val)
    l.sort()
    moguce_vrij[every] = l

d.close()

# skup podataka za testiranje
d = open(argumenti[2], 'r', encoding='utf8')
names_test = list()
test_data = list()
indeksi = dict()
first = True
for line in d:
    line = line.strip()
    odvojeno = line.split(",")
    if first:
        names_test = odvojeno
        first = False
        for i in range(0, len(odvojeno) - 1):
            indeksi[odvojeno[i]] = i
    else:
        test_data.append(odvojeno)
d.close()

# konfiguracija
d = open(argumenti[3], 'r', encoding='utf8')
global mode, model
max_depth = -1
num_trees = 1
feature_ratio = example_ratio = "1."
for line in d:
    line = line.strip()
    odvojeno = line.split("=")
    if odvojeno[0] == "mode":
        mode = odvojeno[1]
    elif odvojeno[0] == "model":
        model = odvojeno[1]
    elif odvojeno[0] == "max_depth":
        max_depth = int(odvojeno[1])
    elif odvojeno[0] == "num_trees":
        num_trees = odvojeno[1]
    elif odvojeno[0] == "feature_ratio":
        feature_ratio = odvojeno[1]
    elif odvojeno[0] == "example_ratio":
        example_ratio = odvojeno[1]
d.close()

id3 = ID3(mode, model, max_depth, num_trees, feature_ratio, example_ratio)
y = id3.fit(train_data, names_test)
id3.predict(test_data, indeksi, y)
