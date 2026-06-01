from collections import deque

def genereaza_posibilitati(prod, anulabile):
    # generam toate posibilitatile de a scrie o productie, eliminand lambda unde se poate
    rezultate=[""]
    for ch in prod:
        liste_noi=[]
        for string_vechi in rezultate:
            liste_noi.append(string_vechi+ch) # varianta in care caracterul este pastrat
            if ch in anulabile:
                liste_noi.append(string_vechi)
        rezultate=liste_noi
    return set(r for r in rezultate if r!="") # scapam de spatii

def elimina_lambda():
    d_nou ={}
    for neterm in d:
        if neterm not in d_nou:
            d_nou[neterm]=[]

        for prod in d[neterm]:
            if prod != "lambda":
                combinatii = genereaza_posibilitati(prod, anulabile)
                d_nou[neterm].extend(combinatii)

    for neterm in d_nou:
        d_nou[neterm]=list(set(d_nou[neterm]))

    return d_nou

def gaseste_redenumiri(start_neterm):
    redenum = set()
    coada = deque([start_neterm])
    #BFS
    while coada:
        curent = coada.popleft()
        if curent in d: # neterm are productii
            for prod in d[curent]:
                if len(prod)==1 and prod in Q:
                    if prod not in redenum:
                        redenum.add(prod)
                        coada.append(prod)
    return redenum

def elimina_redenumiri():
    d_fara_reden = {}
    for neterm in d:
        d_fara_reden[neterm] = []
        # gasim neternimalele unitare in care poate ajunge
        redenum = gaseste_redenumiri(neterm)
        redenum.add(neterm)  # pt pastrarea propriilor reguli

        for r in redenum:
            if r in d:
                for prod in d[r]:
                    # prod nu este unitara?
                    if not (len(prod) == 1 and prod in Q):
                        d_fara_reden[neterm].append(prod)

        d_fara_reden[neterm] = list(set(d_fara_reden[neterm]))  # stergem eventualele duplicate
    return d_fara_reden

def gaseste_neutilizabile():
    util = set()
    for neterm in d:
        for prod in d[neterm]:
            if all(ch in E for ch in prod):
                util.add(neterm)
                break # trecem la urm neterm
    modificat = True
    while modificat:
        modificat = False
        for neterm in d:
            if neterm not in util:
                for prod in d[neterm]:
                    if all(ch in E or ch in util for ch in prod):
                        util.add(neterm)
                        modificat = True
                        break
    return util

def gaseste_accesibile(start_sym):
    coada = deque([start_sym])
    accesibile = {start_sym}
    while coada:
        sym = coada.popleft()
        if sym in d:
            for prod in d[sym]:
                for ch in prod:
                    if ch in Q and ch not in accesibile:
                        coada.append(ch)
                        accesibile.add(ch)
    return accesibile

def dictionar_redus(neterminale_bune):
    d_redus = {}
    for neterm in d:
        if neterm in neterminale_bune:
            d_redus[neterm] = []
            for prod in d[neterm]:
                if prod!="" and all(ch in E or ch in neterminale_bune for ch in prod):
                    d_redus[neterm].append(prod)
    return d_redus

def transforma_fnc():
    d_fnc={}
    contor=1
    terminale_noi = {} # pt neterminalele pentru litere mici

    for neterm in d:
        d_fnc[neterm]=[]
        for prod in d[neterm]:
            # cazurile stiute: neterm -> term sau neterm-> {neterm} {neterm}
            if len(prod) == 1 or (len(prod)==2 and all(ch in Q for ch in prod)):
                d_fnc[neterm].append(prod)
                continue

            # inlocuim terminalele din productii lungi
            prod_curatata=[]
            for ch in prod:
                if ch in E: # litera mica intre litere mari
                    if ch not in terminale_noi:
                        term_nou = f"X_{ch}"
                        terminale_noi[ch]=term_nou
                    prod_curatata.append(terminale_noi[ch])
                else:
                    prod_curatata.append(ch)

            # separare neterminale
            if len(prod_curatata)==2:
                d_fnc[neterm].append("".join(prod_curatata))
            else:
                nod_curent=neterm
                while len(prod_curatata)>2:
                    term_nou = f"F{contor}"
                    contor+=1

                    prim=prod_curatata[0]
                    if nod_curent not in d_fnc:
                        d_fnc[nod_curent]=[]
                    d_fnc[nod_curent].append(prim+term_nou)

                    nod_curent=term_nou
                    prod_curatata=prod_curatata[1:] # stergem primul element, e procesat
                if nod_curent not in d_fnc:
                    d_fnc[nod_curent]=[]
                d_fnc[nod_curent].append("".join(prod_curatata))
    for ch, term_nou in terminale_noi.items():
        d_fnc[term_nou]=[ch]
    return d_fnc

with open("FNC.in") as f:
    Q =set(f.readline().split())
    E = set(f.readline().split())
    nr_prod=int(f.readline().strip())
    d={}
    for _ in range(nr_prod):
        neterm, prod = f.readline().strip().split(" ")
        if neterm not in d:
            d[neterm]=[]
        d[neterm].append(prod)
    start_sym = f.readline().strip()
    anulabile=set()
    for neterm in d:
        if "lambda" in d[neterm]:
            anulabile.add(neterm)

    # SIMBOLURI NEUTILIZABILE
    modificat = True
    while modificat:
        modificat=False
        for neterm in d:
            if neterm not in anulabile:
                for prod in d[neterm]:
                    if prod != "lambda" and all(ch in anulabile for ch in prod):
                        # verif daca toate ch din aceasta productie sunt anulabile
                        anulabile.add(neterm)
                        modificat=True
                        break

    # ELIMINAM LAMBDA PRODUCTIILE (empty-productions)
    d=elimina_lambda()

    # ELIMINAM REDENUMIRILE (unit-productions)
    d = elimina_redenumiri()

    # ELIMINAM SIMBOLURILE NEUTILIZABILE SI INACCESIBILE (non-terminating & unreachable)
    util=gaseste_neutilizabile()
    accesibile=gaseste_accesibile(start_sym)

    # REDUCERE DICTIONAR
    neterminale_bune =util.intersection(accesibile)
    if start_sym in neterminale_bune: # pt key error
        d=dictionar_redus(neterminale_bune)

    # SPARGERE PRODUCTII
    d=transforma_fnc()

with open("FNC.out", 'w') as g:
    for neterm in d:
        for prod in sorted(d[neterm]):
            g.write(f"{neterm} -> {prod}\n")