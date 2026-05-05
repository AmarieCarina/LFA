##precizari : am factu DFA complet inainte de Moore
    # simbolurile din alfabet trebuie sa fie sortate
    # am adaugat stare dead

from collections import deque

### PAS 1 : CALCUL LAMBDA INCHIDERE
def lambda_closure(state, transitions, lambda_symbol="lambda"):
    closure = {state}
    queue = deque([state])
    while queue:
        current = queue.popleft()
        next_states = transitions.get(current, {}).get(lambda_symbol, set())
        for next in next_states:
            if next not in closure:
                closure.add(next)
                queue.append(next)
    return closure


### PAS 2 : SUBSET CONSTRUCTION
def move(states, symbol, transitions):
    result = set()
    for state in states:
        result |= transitions.get(state, {}).get(symbol, set())
    return result


### CITIREA DATELOR
with open("minimizare.in") as f:
    Q = set(f.readline().split())
    E = sorted(list(f.readline().split()))
    if "lambda" in E: E.remove("lambda")

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



### LAMBDA NFA -> DFA
delta2 = {}
        # dictionarul pentru automatul DFA
init = frozenset(lambda_closure(stare_init, delta))
        # starile de la care plecam
queue = deque([init])
        # tinem minte ordinea in care vrem sa analizam submultimile de stari (linii din tabel)
visited = {init}
        # tinem minte daca o stare a fost analizata sau nu (daca am scris deja un rand cu ea, in tabel)
dead = frozenset(["DEAD"])
while queue:
    current = queue.popleft()
            # starile corespondente din DFA(prima coloana din tabel)
    if current not in delta2:
        delta2[current] = {}

    for sym in E:
                # pentru fiecare litera, o coloana noua
        new_states = move(current, sym, delta)
        current_states=set()
                    #submt de stari de analizat (valorile de pe o linie din tabel)
        for state in new_states:
            current_states|=lambda_closure(state, delta)

        target_state = frozenset(current_states) if current_states else dead

        if target_state not in visited:
            queue.append(target_state)
            visited.add(target_state)
            if target_state == dead:
                delta2[dead] = {s: dead for s in E}

                        # adaugam valoarea in noul dictionar
        delta2[current][sym] = target_state

# det stari finale
stari_fin2={stare for stare in visited if stare & stari_fin}

# AFISARE 1
g=open("minimizare.out", 'w')
stare_to_id = {stare: i for i, stare in enumerate(sorted(list(visited), key=lambda x: str(sorted(list(x)))))}
g.write("----------DFA---------\n")
for stare in stare_to_id:
    id_sursa = stare_to_id[stare]
    tip = "finala" if stare in stari_fin2 else "nefinala"

    componente = "{" + ",".join(sorted(list(stare))) + "}"
    g.write(f"Q{id_sursa} {componente} ({tip})\n")

    for sym in E:
        if sym in delta2[stare]:
            destinatie = delta2[stare][sym]
            id_dest = stare_to_id[destinatie]
            g.write(f"  '{sym}' -> Q{id_dest}\n")
    g.write("\n")


### PAS 3 : MINIMIZAREA (ALG. MOORE)
# partition va fi un dictionar: {stare: id_grup}, un grup pentru stari finale, unul pentru restul
partition = {stare: (1 if stare in stari_fin2 else 0) for stare in visited}

while True:
    new_partition = {}
                    # grupam starile care au acelasi grup actual SI merg in aceleasi grupuri pe aceleasi simboluri
    split_map = {}  # asociem ID-uri pentru toate semnaturile gasite

    for stare in visited:
        signatures = []
                    #in ce grupuri ajunge starea curenta pentru fiecare litera
        for sym in E:
            destinatie = delta2.get(stare, {}).get(sym, None)
            signatures.append(partition.get(destinatie, -1))
                    # daca nu exista tranzitie, o consideram un grup special (-1)
        signature = (partition[stare], tuple(signatures))
                    # (grupul_starii_actuale, destinatii)

        if signature not in split_map:
            split_map[signature] = len(split_map)

        new_partition[stare] = split_map[signature]

    if new_partition==partition:
        break
                # partitia nu se mai schimba
    partition = new_partition

# RECONSTRUIRE DFA
# grupam starile din visited dupa id-ul lor final din partition
groups = {}
for stare, group_id in partition.items():
    if group_id not in groups: groups[group_id] = []
    groups[group_id].append(stare)


# AFISARE 2
g.write("-----------DFA minim-----------\n")
for g_id, stari_din_grup in groups.items():
    reprezentant = stari_din_grup[0]
    tip = "finala" if reprezentant in stari_fin2 else "nefinala"

    g.write(f"Q{g_id} ({tip})\n")

    for sym in E:
        destinatie_stare = delta2[reprezentant][sym]
            # Gasim in ce grup se afla starea destinatie
        id_grup_dest = partition[destinatie_stare]
        g.write(f"  '{sym}' -> Q{id_grup_dest}\n")
    g.write("\n")
g.close()