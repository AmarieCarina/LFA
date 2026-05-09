def union(r1,r2):
    if r1 == "": return r2
    if r2 == "": return r1
    if r1 == r2: return r1
    return f"({r1}+{r2})"

def concat(r1,r2):
    if r1 == "lambda":  return r2
    if r2 == "lambda":  return r1
    if r1 == "" or r2 == "": return ""
    return f"{r1}.{r2}"

def star(r):
    if r == "lambda" or r=="":
        return f"lambda"
    return f"({r})*"

### CITIREA DATELOR
with open("RegEx.in") as f:
    Q = set(f.readline().split())
    E = sorted(list(f.readline().split()))
    nr_tranzitii = int(f.readline())
    delta = {}
    for _ in range(nr_tranzitii):
        tranzitie = f.readline().split()
        cheie = tranzitie[0]
        cheie2 = tranzitie[1]
        val = tranzitie[2]
        if cheie not in delta:
            delta[cheie] = {}
        if cheie2 not in delta[cheie]:
            delta[cheie][cheie2] = {val}
        else:
            delta[cheie][cheie2].add(val)
    stare_init = f.readline().strip()
    stari_fin = set(f.readline().split())

# PAS 1: TRECEREA LA AUTOMAT FINIT EXTINS
efa = {} # dictionar in care cheia este tuplul (stare_sosire, stare_plecare), iar valoarea este simbolul
for state in delta:
    for sym in delta[state]:
        for substate in delta[state][sym]:
            pair = (state, substate)
            current_regex = "lambda" if sym =="lambda" else sym
            if pair not in efa:
                efa[pair]=current_regex
            else:
                #print(f"Union pentru {state} -> {substate}: {efa[pair]} + {current_regex}")
                efa[pair] = union(efa[pair], current_regex)

#PAS 2 SI 3: STAREA INITIALA SI FINALA DIN AFE
efa[("start", stare_init)] = "lambda"
for stare in stari_fin:
    efa[(stare, "fin")] = "lambda"

#PAS 4: ELIMINAREA STARILOR DIN Q
for to_del in Q:
    # cautam predecesori si succesori
    pred=set()
    succ=set()
    self_loop = "" # pentru formula de mai tarziu
    for stare in efa:
        # in pred si succ nu poate fi starea de sters
        if stare[1] == to_del and stare[0]!=to_del:
            pred.add(stare[0])
        if stare[0] == to_del and stare[1]!=to_del:
            succ.add(stare[1])
        if stare==(to_del,to_del):
            self_loop=efa[(stare[0],stare[1])]
    # print(to_del, pred, succ, self_loop)

    for p in pred:
        for q in succ:
            if (p,q) in efa:
                #p si q au legatura
                regex=union(  efa[(p,q)],   concat(    efa[(p,to_del)], concat(  star(self_loop),  efa[(to_del,q)])))
                efa[(p,q)] = regex
            else:
                # p si q nu au legatura
                regex=concat(efa[(p,to_del)], concat(star(self_loop),efa[(to_del,q)]))
                efa[(p,q)] = regex

    # stergem toate tuplurile care contin cheia de sters
    key_to_del = [pair for pair in efa if to_del in pair]
    for k in key_to_del :
        del efa[k]
with open("RegEx.out", 'w') as g:
    g.write(efa[("start", "fin")])
