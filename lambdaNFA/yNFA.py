with open("yNFA.in", 'r') as f:
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
        if cheie2 not in delta[cheie1]:
            delta[cheie1][cheie2]=[val]
        else:
            delta[cheie1][cheie2].append(val)
    q0 = f.readline().strip()
    nrStariFinale=f.readline()
    F = set(f.readline().split())
    nrCuvinte=int(f.readline())
    cuvinte=f.readlines()
    for i in range(len(cuvinte)):
        cuvinte[i]=cuvinte[i].strip()

def lambda_inchidere(stari_initiale, delta):
    inchidere=set(stari_initiale)
    stiva=list(stari_initiale)
    while stiva:
        stare_curenta=stiva.pop()
        for stare_urmatoare in delta.get(stare_curenta,{}).get('lambda', []):
            if stare_urmatoare not in inchidere:
                inchidere.add(stare_urmatoare)
                stiva.append(stare_urmatoare)
    return inchidere

def verif(cuvant):
    stari_curente=set(lambda_inchidere({q0},delta))
    for simbol in cuvant:
        stari_noi=set()
        for stare in stari_curente:
            stari_noi.update(delta.get(stare,{}).get(simbol, []))
        stari_curente=lambda_inchidere(stari_noi, delta)
    if stari_curente & F:
        return "DA"
    return "NU"

with open("yNFA.out", 'w') as g:
    for cuvant in cuvinte:
        g.write(cuvant+" "+verif(cuvant)+"\n")
    sigma = set([k for subdict in delta.values() for k in subdict.keys()])
    print("Alfabetul folosit: " + str(sigma))