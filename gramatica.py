#proceseaza sirul de simboluri in neterminal + continuare
def parse_symbols(s, N, T):
    symbols = []
    i = 0
    while i < len(s):
        matched = False
        # testam potrivirea cea mai "lunga"
        for length in range(max(len(sym) for sym in N | T), 0, -1):
            candidate = s[i:i + length]
            if candidate in N or candidate in T:
                symbols.append(candidate)
                i += length
                matched = True
                break
        if not matched:
            symbols.append(s[i])  # fallback: single char
            i += 1
    return symbols


#### CITIRE DATE
with open("gramatica.in") as f:
    N = set(f.readline().split())
    T = set(f.readline().split())
    nr_prod = int(f.readline())
    productii = {}
    for _ in range(nr_prod):
        prod=f.readline().split()
        neterm = prod[0]
        sir = prod[1] if prod[1] != "lambda" else ""
        if neterm not in productii:
            productii[neterm]=[]
        productii[neterm].append(sir)
    start=f.readline().strip()
    lungime=int(f.readline())


############## Algoritm BFS #############
cuvinte_valide = set()
vizitat = set()
vizitat.add(start)
queue = [start]
# incepem de la simbolul de start

while queue:
    curent = queue.pop()

    simboluri = parse_symbols(curent, N, T)

    # impartire simboluri
    nr_terminale = sum(1 for s in simboluri if s in T)
    nr_neterminale = sum(1 for s in simboluri if s in N)

    # prea multe neterminale
    if nr_terminale > lungime:
        continue

    # fara neterminale
    if nr_neterminale == 0:
        if nr_terminale == lungime:
            cuvinte_valide.add(curent)
        continue

    # procesam neterminalul cel mai la stanga
    for i, simbol in enumerate(simboluri):
        #primul neterminal
        if simbol in N:
            prefix = "".join(simboluri[:i]) # ce era inaintea lui
            sufix = "".join(simboluri[i + 1:]) # ce era dupa el

            for inlocuitor in productii.get(simbol, []):
                nou_sir = prefix + inlocuitor + sufix

                # simbolurile noi de procesat
                nou_simboluri = parse_symbols(nou_sir, N, T)

                nr_term_nou = sum(1 for s in nou_simboluri if s in T)

                if nr_term_nou <= lungime and nou_sir not in vizitat:
                    vizitat.add(nou_sir)
                    queue.append(nou_sir)
            break

with open("gramatica.out", 'w') as g:
    if not cuvinte_valide:
        g.write("NU EXISTA")
    else:
        for cuvant in sorted(cuvinte_valide):
            g.write(cuvant if cuvant != "" else "lambda")

