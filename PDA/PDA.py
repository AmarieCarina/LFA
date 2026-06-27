from collections import deque

with open("PDA.in") as f:
    Q=set(f.readline().split())
    Sigma=set(f.readline().split())
    Gamma=set(f.readline().split())
    nr_tranz=int(f.readline())
    t= {}
    for _ in range(nr_tranz):
        stare1, simbol, top_stiva, stare2, litere=f.readline().split()
        if (stare1, simbol, top_stiva) not in t:
            t[(stare1, simbol, top_stiva)]=[]
        t[(stare1, simbol, top_stiva)].append([stare2, litere])
    stare_init=f.readline().strip()
    vf_stiva=f.readline().strip()
    F=set(f.readline().split())
    mod_acceptare=f.readline().strip()
    word=f.readline().strip()

def simuleaza_pda():
    coada = deque([(stare_init, 0, [vf_stiva])]) # tine minte configuratiile de vizitat
    vizitat = set()
    while coada:
        stare, idx, stiva = coada.popleft()

        # am mai trecut o data prin aceeasi configuratie?
        configuratie_curenta = (stare, idx, tuple(stiva))
        if configuratie_curenta in vizitat:
            continue
        vizitat.add(configuratie_curenta)

        # final
        if idx == len(word):
            if mod_acceptare == "stare":
                if stare in F:
                    return True
            elif mod_acceptare == "stiva_vida":
                if len(stiva) == 0:
                    return True
            elif mod_acceptare == "stare si stiva_vida":
                if stare in F and len(stiva) == 0:
                    return True

        top_stiva = stiva[-1] if stiva else None
        simbol_citit = word[idx] if idx < len(word) else None
#         conditii pt stiva vida

        # caz 1:
        # incercam sa consumam o litera din cuvant
        if (stare, simbol_citit, top_stiva) in t:
            #consideram toate tranzitiile cu comfiguratia curenta
            for stare_noua, t_push in t[(stare, simbol_citit, top_stiva)]:
                #generam noua stiva, fara ultimul element
                noua_stiva = list(stiva[:-1]) if stiva else [] # POP
                if t_push != "_":
                    noua_stiva.extend(reversed(list(t_push)))  # PUSH
                # adaugam configuratia pentru testare utlerioara
                coada.append((stare_noua, idx+1, noua_stiva))

        # caz 2:
        # pt tranzitii lambda
        if(stare, "_", top_stiva) in t:
            for stare_noua, t_push in t[(stare, "_", top_stiva)]:
                noua_stiva=list(stiva[:-1]) if stiva else []
                if  t_push != "_":
                    noua_stiva.extend(reversed(list(t_push)))
                coada.append((stare_noua, idx, noua_stiva))
    return False


with open("PDA.out", 'w') as g:
    if simuleaza_pda():
        g.write(f"Cuvantul {word} a fost acceptat.")
    else:
        g.write(f"Cuvantul {word} nu a fost acceptat.")