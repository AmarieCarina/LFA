with open("DFA.in", 'r') as f:
    #preluare date din fisier:
    nrStari=int(f.readline())
    Q=set(f.readline().split())
    nrTranzitii=int(f.readline())
    delta={}
    for _ in range(nrTranzitii):
        tranzitie=f.readline().split()
        cheie1=tranzitie[0]
        val=tranzitie[1]
        cheie2=tranzitie[2]
        if cheie1 not in delta:
            delta[cheie1]={}
        delta[cheie1][cheie2]=val
    q0 = f.readline().strip()
    nrStariFinale=f.readline()
    F = set(f.readline().split())
    nrCuvinte=int(f.readline())
    cuvinte=f.readlines()
    for i in range(len(cuvinte)):
        cuvinte[i]=cuvinte[i].strip()

def verif(cuvant):
    tranzitii=[]
    stareCurenta = q0
    for simbol in cuvant:
        if simbol in delta[stareCurenta]:
            #pentru memorarea tranzitiilor:
            stareUrmatoare = delta[stareCurenta][simbol]
            tranzitii.append(f"({stareCurenta}, {simbol}) -> {stareUrmatoare}")
            stareCurenta = stareUrmatoare
    if stareCurenta in F:
        print(cuvant)
        for tranzitie in tranzitii:
            print(tranzitie)
        print()
        return "DA"
    else:
        return "NU"

with open("DFA.out", 'w') as g:
    for cuvant in cuvinte:
        g.write(cuvant+" "+verif(cuvant)+"\n")
    #afisarea alfabetului:
    sigma = set([k for subdict in delta.values() for k in subdict.keys()])
    print("Alfabetul folosit: "+str(sigma))