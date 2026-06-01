def afiseaza_rezultat(mat, word, start_sym):
    n = len(word)
    with open("CYK.out", 'w') as g:
        if start_sym in mat[n-1][0]:
            g.write("DA")
        else:
            g.write("NU")
        g.write("\nTabela CYK:\n")
        for l in range(n-1, -1, -1):
            rand=[]
            for i in range(n-l):
                celula=mat[l][i]
                if len(celula)==0:
                    rand.append("-")
                else:
                    rand.append(",".join(sorted(list(celula))) if celula else "-")
            g.write("   |   ".join(rand)+"\n")

        g.write("-" * (n*7)+"\n")
        g.write("   |   ".join(list(word)))

with open("CYK.in") as f:
    Q = set(f.readline().split())
    E = set(f.readline().split())
    nr_prod = int(f.readline().strip())
    d = {}
    for _ in range(nr_prod):
        neterm, prod = f.readline().strip().split(" ")
        if neterm not in d:
            d[neterm] = []
        d[neterm].append(prod)
    start_sym = f.readline().strip()
    word = f.readline().strip()
n = len(word)

# initializam tabela pt PD
mat = [[set() for _ in range(n)] for _ in range(n)]

# primul rand din matrice
for i in range(n):
    for neterm in d:
        if word[i] in d[neterm]:
            mat[0][i].add(neterm)

for l in range(1,n): # randul din mat
    for i in range(n-l): # coloana (matrice triunghiulara)
        for k in range(l): # punct de taiere al cuvantului
            celula_stanga = mat[k][i] # urca pe verticala
            celula_dreapta=mat[l-k-1][i+k+1] # coboara pe diagonala (dreapta-jos)

            for B in celula_stanga:
                for C in celula_dreapta:
                    pereche = B+C

                    for neterm in d:
                        if pereche in d[neterm]:
                            mat[l][i].add(neterm)
afiseaza_rezultat(mat, word, start_sym)