class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen. http://code.activestate.com/recipes/134892/"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


#ho dovuto backuotare i \, potrei usare le raw string togliendo le interruzioni
#di riga \ e ottenendo un \n in più alla fine
layout_low = """\
`1234567890-=
qwertyuiop[]
asdfghjkl;'\\
<zxcvbnm,./\
"""
layout_upp = """\
~!@#$%^&*()_+
QWERTYUIOP{}
ASDFGHJKL:"|
>ZXCVBNM<>?\
"""
#alcuni tasti richiedono di digitare il carattere seguente
#per comparire, ho messo sempre lo spazio
layout_alt_low = """\
`¹²³4€^789°¯=
qwè®tyùìòp[]
àséfghúíó"'\\
|áx©vbñm«»/\
"""
#gli spazi significano assenza di carattere
layout_alt_upp = """\
~   $  &*(  +
QWÈ TYÙÌÒP{}
ÀSÉFGHÚÍÓ" |
¦ÁX VBÑM  ?\
"""
#layout tastiera notebook
nb_layout = [layout_low, layout_upp, layout_alt_low, layout_alt_upp]



wlow = (
""" `1234567890  """ + "\n"
"""  qwertyuiop\ """ + "\n"
"""  asdfghjkl   """ + "\n"
"""  zxcvbnm,.;' """ + "\n"
"""   -=     []/ """
)
wupp = (
""" ~!@#$%^&*()  """ + "\n"
"""  QWERTYUIOP| """ + "\n"
"""  ASDFGHJKL   """ + "\n"
"""  ZXCVBNM<>:" """ + "\n"
"""   _+     {}? """
)
waltlow = (
""" `¹²³4€^789°  """ + "\n"
"""  qwè®tyùìòp\ """ + "\n"
"""  àséfghúíó   """ + "\n"
"""  áx©vbñm«»"' """ + "\n"
"""   ¯=     []/ """
)
waltupp = (
""" ~   $  &*(   """ + "\n"
"""  QWÈ TYÙÌÒP| """ + "\n"
"""  ÀSÉFGHÚÍÓ   """ + "\n"
"""  ÁX VB M  "  """ + "\n"
"""    +     {}? """
)
#layout tastiera wireless
wi_layout = [wlow, wupp, waltlow, waltupp]



def indice_tasto(tasto, layout):
    """restituisce l'indice di un tasto presente (e non spazio) altrimenti None"""
    if tasto != " " and tasto in layout:
        linee = layout.splitlines()
        c, l =  [(l.index(tasto), linee.index(l)) for l in linee if tasto in l][0]
        return c,l
    else:
        return None

def tasto_indice(indice, layout):
    """restituisce il tasto di un indice se valido (e non spazio) altrimenti None"""
    tasto = None
    c, l = indice
    linee = layout.splitlines()
    if 0 <= l < len(linee) and 0 <= c < len(linee[l]):
        tasto = linee[l][c]
        tasto = tasto if tasto != " " else None
    return tasto

def traduci_tasto(tasto, layout1, layout2):
    """restituisce il tasto corrispondente di un alto layout altrimenti quello inserito"""
    indice = indice_tasto(tasto, layout1)
    trad = tasto_indice(indice, layout2) if indice else tasto
    return trad

def traduci_testo(testo, layout1, layout2):
    """traduce la stringa  o la lista passata lasciando invariati i caratteri
    per cui non è presente una traduzione"""
    traduz = ""
    for lettera in testo:
        let = traduci_tasto(lettera, layout1, layout2)
        traduz += let if let else lettera
    return traduz

def multi_layout(testo, *layout):
    """restituisce una lista di lettere univoche tradotte in più layout
    partendo dai caratteri passati in ingresso, comprse quelle iniziali
    """
    lettere = set(testo)
    layout1 = layout[0]
    for layoutn in layout[1:]:
        traduzione = traduci_testo(testo, layout1, layoutn)
        lettere.update(traduzione)
    return list(lettere)


def numero_complementare(base, numero):
    """restituisce il complemento di un numero"""
    return base-numero

def complemento_di_una_serie(serie, numero):
    """restituisce il complemento di un numero rispetto al numero massimo di una lista"""
    massimo = max(serie)
    #~ complem = [numero_complementare(massimo, numero) for numero in serie]
    return numero_complementare(massimo, numero)

def indice_speculare_ascisse(indice, layout):
    """restituisce l'indice di un tasto complementatato in orizzontale"""
    linee = layout.splitlines()
    c, l = indice
    lunghezze = [len(linea) for linea in linee]
    c_compl = complemento_di_una_serie(lunghezze, c)-1 #gli indici partono da 0
    return c_compl, l

def tasti_speculari_ascisse(tasti, layout):
    tasti_speculari = []
    for tasto in tasti:
        indice = indice_tasto(tasto, layout)
        if indice:
            indice_speculare = indice_speculare_ascisse(indice, layout)
            tasto_speculare = tasto_indice(indice_speculare, layout)
            if tasto_speculare:
                tasti_speculari.append(tasto_speculare)
    return tasti_speculari



from random import choice, randint
def tasti_limitrofi(iniz_tst=None, distanza=0, layout=layout_low):
    """restituisce una lista di tasti a partire da quello iniziale
    specificato per la distanza specificata (a rombo).
    Se non si specifica un tasto, viene scelto random.
    """
    linee = layout.splitlines()
    lettere = set()
    if iniz_tst is None:
            iniz_tst = choice(layout.replace('\n', '').replace(' ', ''))
    try:                #se è un indice
        tasto = tasto_indice(iniz_tst, layout)
        iniz_ind = iniz_tst #si può andare out of range in orizzontale,
        iniz_tst = tasto    #forse è corretto per layout non quadrati
    except ValueError:  #se è una lettera
        iniz_ind = indice_tasto(iniz_tst, layout)
    if iniz_ind:
        for dis in range(distanza+1):
            for col in [dis, -dis]:
                for lin in range(-abs(distanza-dis), abs(distanza-dis)+1):
                    l = lin+iniz_ind[1]
                    l = l if l >= 0 and l < len(linee) else iniz_ind[1]
                    c = col+iniz_ind[0]
                    c = c if c >= 0 and c < len(linee[l]) else iniz_ind[0]
                    lettera = tasto_indice((c, l), layout)
                    if lettera:
                        lettere.add(lettera)
    return list(lettere)

def tasti_asse(iniz_tst=None, distanza=0, layout=layout_low, asse='v'):
    """restituisce una lista di caratteri in base al tasto iniziale (iniz_tst)
    specificato (che può essere una lettera, None per una lettera casuale
    o direttamente un indice). Se la distanza è un numero naturale i tasti
    restituiti saranno a partire dalla distanza specificata fino al iniz_tst.
    Se la distanza è una coppia di valori il primo sarà la distanza fino ad
    arrivare alla tasto iniziale, il secondo la distanza dal tasto iniziale
    a quelli seguenti.
    L'asse di riferimento può assumere valori 'v' o 'y' per verticale o
    'o' o 'x' per orizzontale.
    """
    linee = layout.splitlines()
    lettere = set()
    if iniz_tst is None:
            iniz_tst = choice(layout.replace('\n', '').replace(' ', ''))
    try:                #se è un indice
        tasto = tasto_indice(iniz_tst, layout)
        iniz_ind = iniz_tst #si può andare out of range in orizzontale,
        iniz_tst = tasto    #forse è corretto per layout non quadrati
    except ValueError:  #se è una lettera
        iniz_ind = indice_tasto(iniz_tst, layout)
    if iniz_ind:
        c, l = iniz_ind
        if   asse == 'v' or asse == 'y':
            limite = len(linee)
            indice = {'indipe':c, 'dipend':l}
        elif asse == 'o' or asse == 'x':
            limite = len(linee[l])
            indice = {'dipend':c, 'indipe':l}
        try:
            n_min = max(indice['dipend'] - distanza[0], 0)
            n_max = min(indice['dipend'] + distanza[1] + 1, limite)
        except TypeError:
            n_min = max(indice['dipend'] - distanza, 0)
            n_max = indice['dipend'] + 1
        for n in range(n_min, n_max):
            indice['dipend'] = n
            lettera = tasto_indice(indice.values(), layout)
            if lettera:
                lettere.add(lettera)
    return list(lettere)


def parola_casuale(lettere, lunghezza=1):
    """restituisce nua parola di lunghezza determinata generata
    casualmente prendendo lettere dalla lista o stringa specificata
    attualmente se il numero di caratteri è ripetuto c'è più possibilità
    che escano, altrimenti si potrebbe usare un set
    """
    return ''.join([choice(lettere) for l in range(lunghezza)])

def parole_casuali(lettere, lunghezza=1, numero=1):
    """restituisce un numero di parole casuali generate dalle lettere
    specificate, le lettere possono essere sia una lista che una stringa,
    la lunghezza e il numero possono essere sia un numero intero che
    gli estremi di un numero randomico
    """
    lun = lunghezza
    num = numero
    if isinstance(numero, tuple):
        num = randint(*numero)
    parole = []
    for p in range(num):
        if isinstance(lunghezza, tuple):
            lun = randint(*lunghezza)
        parola = parola_casuale(lettere, lun)
        parole.append(parola)
    return parole



def crea_esercizi(layout):
    linee = layout.splitlines()
    indici = []
    for l, lin in enumerate(linee):
        for c, col in enumerate(lin):
            indici.append((c,l))
    indici_sin = [i for i in indici if i[0] <= max(map(lambda j: j[0], filter(lambda y: y[1] == i[1], indici)))//2]
    #~ indici_des = [indice_speculare_ascisse(i, layout) for i in indici_sin]

    #esercizi sulle righe
    esercizi1 = []
    for l in range(len(linee)):
        es_riga = []
        riga = filter(lambda i: i[1] == l, indici_sin)
        for i in riga:
            i_sp = indice_speculare_ascisse(i, layout)
            tasto1 = tasto_indice(i, layout)
            if tasto1: es_riga.append([tasto1])
            tasto2 = tasto_indice(i_sp, layout)
            if tasto2: es_riga.append([tasto2])
            if tasto1 and tasto2: es_riga.append([tasto1, tasto2])
            serie1 = tasti_asse(i, i[0], layout, 'o')
            if len(serie1) > 1: es_riga.append(serie1)
            #~ serie2 = tasti_speculari_ascisse(serie1, layout)
            serie2 = tasti_asse(i_sp, (0,i[0]), layout, 'o')
            if len(serie2) > 1: es_riga.append(serie2)
            if len(serie1) + len(serie2) > 2: es_riga.append(serie1 + serie2)
            #~ print([tasto1, tasto2, [tasto1, tasto2], serie1, serie2, serie1 + serie2])
        if es_riga: esercizi1 += es_riga #esercizi1.append(es_riga)
        #~ print(); print(es_riga); print(); print(); print()

    #esercizi sulle colonne
    esercizi2 = []
    flag =  [True]
    c = 0
    while any(flag):
        flag = []
        es_col = []
        for l in range(len(linee)):
            i = (c,l) if (c,l) in indici_sin else None
            flag.append(bool(i))
            if i:
                i_sp = indice_speculare_ascisse(i, layout)
                tasto1 = tasto_indice(i, layout)
                if tasto1: es_col.append([tasto1])
                tasto2 = tasto_indice(i_sp, layout)
                if tasto2: es_col.append([tasto2])
                if tasto1 and tasto2: es_col.append([tasto1, tasto2])
                serie1 = tasti_asse(i, i[1], layout, 'v')
                if len(serie1) > 1: es_col.append(serie1)
                serie2 = tasti_asse(i_sp, i[1], layout, 'v')
                if len(serie2) > 1: es_col.append(serie2)
                if len(serie1) + len(serie2) > 2: es_col.append(serie1 + serie2)
                #~ print([tasto1, tasto2, [tasto1, tasto2], serie1, serie2, serie1 + serie2])
        if es_col: esercizi2 += es_col #esercizi2.append(es_col)
        c += 1
        #~ print(); print(es_col); print(); print()
    #~ print(esercizi2)

    #esercizi a rombi
    esercizi3 = []
    indice_medio_s = indici_sin[len(indici_sin)//2]
    indice_medio_d = indice_speculare_ascisse(indice_medio_s, layout)
    #~ tasto_medio = tasto_indice(indice_medio, layout)
    distanza = sum(indice_medio_s)
    for d in range(distanza+1):
        es_romb = []
        ts = tasti_limitrofi(indice_medio_s, d, layout)
        td = tasti_limitrofi(indice_medio_d, d, layout)
        es_romb.append(ts)
        es_romb.append(td)
        es_romb.append(ts+td)
        if es_romb: esercizi3 += es_romb #esercizi3.append(es_romb)

    return esercizi1 + esercizi2 + esercizi3

def test_parole(parole):
    fine = False
    for indovina in parole:
        if fine: break
        parola = ""
        print(f'inserisci la parola {indovina} (spazio per terminare)')
        while not fine:
            lettera = getch()
            fine = lettera == " "
            parola += lettera
            if not indovina.startswith(parola):
                parola = ""
            lung = len(parola)
            print(" " * lung + indovina[lung:])
            if parola == indovina:
                break




if __name__ == "__main__":
    pass

    comb_wlow = crea_esercizi(layout_low)
    comb_all  = [multi_layout(lettere, *wi_layout) for lettere in comb_wlow]

    paro_wlow = [parole_casuali(lettere, (2,4) , 10) for lettere in comb_wlow]
    #~ paro_all  = [parole_casuali(lettere, (1,4) , 4) for lettere in comb_all]

    inizio = input(f"{len(paro_wlow)-1}, esercizi, inserisci il numero da cui vuoi iniziare, default 0: ")
    print()
    try:
        inizio = int(inizio)
    except ValueError:
        inizio = 0

    for c, parole in enumerate(paro_wlow[inizio:]):
        esercizio = f"# Esercizio: {inizio+c} lettere: {''.join(comb_wlow[inizio+c])} #"
        print(f"#" * len(esercizio) + '\n' +
              esercizio             + '\n' +
              f"#" * len(esercizio) + '\n'
             )
        test_parole(parole)



    #~ print(multi_layout('abc', *wi_layout))
    #~ print([multi_layout(lettere, *wi_layout) for lettere in [['a'], ['b'], ['c']]])

    #~ comb_wlow = crea_esercizi(wlow)
    #~ comb_all  = [multi_layout(lettere, *wi_layout) for lettere in comb_wlow]
    #~ for w,a in zip(comb_wlow, comb_all):
        #~ print(w)
        #~ print(a)
        #~ print()



    #~ [print(w, "\n") for w in crea_esercizi(wlow)] #lista
    #~ print(len(crea_esercizi(wlow))) #con wlow es1 = 5righe, es2 = 6colonne, es3 = 6ingrandimenti
    #~ print(len(set(crea_esercizi(wlow)[-1]))) #caratteri ultimo esercizio, tasti_limitrofi è ok?
    #~ print(tasti_asse('\\', (0,1), wlow, 'o'))
    #~ print(tasti_asse('=', 0, wlow, 'o'))
    #~ print(tasti_asse((4,4), 0, wlow, 'o'))
    #~ print(tasti_asse((4,4), 4, wlow, 'o'))
    #~ print(indice_speculare_ascisse((4,4),wlow))


    #~ lettere1 = tasti_asse('w', 1, wlow, 'o')
    #~ lettere2 = tasti_speculari_ascisse(lettere1, wlow)
    #~ parole1 = parole_casuali(lettere1, (2,4), 10)
    #~ parole2 = parole_casuali(lettere2, (2,4), 10)
    #~ parole3 = parole_casuali(lettere1+lettere2, (2,4), 10)
    #~ test_parole(parole1)
    #~ test_parole(parole2)
    #~ test_parole(parole3)


    #~ lettere1 = tasti_asse('w', 1, wlow, 'v')
    #~ lettere2 = tasti_speculari_ascisse(lettere1, wlow)
    #~ print(lettere1, lettere2)
    #~ lettere1 = tasti_limitrofi('w', 1, wlow)
    #~ lettere2 = tasti_speculari_ascisse(lettere1, wlow)
    #~ print(lettere1, lettere2)
    #~ lettere1 = tasti_asse('w', (1,1), wlow, 'v') + tasti_asse('w', (1,1), wlow, 'o')
    #~ lettere2 = tasti_speculari_ascisse(lettere1, wlow)
    #~ print(lettere1, lettere2)




    #~ lettere = tasti_verticali('a', (0,0), wlow)
    #~ print(lettere)
    #~ lettere = tasti_asse('g', 1, wlow, 'o')
    #~ print(lettere)
    #~ lettere = tasti_asse('g', (0,1), wlow, 'o')
    #~ print(lettere)
    #~ lettere = tasti_limitrofi(None, 1, wlow)
    #~ parole = parole_casuali(lettere, (2,4), (6,10))
    #~ test_parole(parole)




    #~ print(tasto_indice(indice_speculare_ascisse(indice_tasto('6', wlow), wlow), wlow))

    #~ print(len(layout_low), len(layout_upp), len(layout_alt_low), len(layout_alt_upp))
    #~ print([len(l) for l in nb_layout])
    #~ print([len(l) for l in wi_layout])
    #~ for i in range(100): print("\n", tasti_limitrofi(None, 3, layout_alt_upp))
    #~ print(parola_casuale("zurro", 10))
    #~ print(parole_casuali("zurro", 5, 3))
    #~ print(parole_casuali("zurro", (1,5), (5,10)))



    #~ test_parole(parole_casuali("zurro", (1,5), (5,10)))
    #~ test_parole(parole_casuali(tasti_limitrofi('a', 1), (1,5), (5,10)))
    #~ test_parole(parole_casuali(tasti_limitrofi(None, 1), (1,5), (5,10)))

    #~ print(traduci_tasto('b', layout_low, layout_upp))
    #~ print(traduci_testo('baB Ì ì Beo', layout_low, layout_upp))
    #~ print(traduci_testo(['a', 'b', 'c'], layout_low, layout_upp))


    #~ caratteri = tasti_limitrofi('a', 1)
    #~ caratteri = list(caratteri) + list(traduci_testo(caratteri, layout_low, layout_upp))
    #~ print(caratteri)
    #~ test_parole(parole_casuali(caratteri, (1,5), (5,10)))

    #~ lts = [layout_low, layout_upp, layout_alt_low, layout_alt_upp]
    #~ caratteri = "as"
    #~ caratteri = multi_layout(caratteri, *lts)
    #~ test_parole(parole_casuali(caratteri, (1,5), (5,10)))






#~ ####################
#~ # CODICI NON USATI #
#~ ####################


#~ def tasti_limitrofi(iniz_tst=None, distanza=0, layout=layout_low):
    #~ """restituisce una lista di tasti a partire da quello iniziale
    #~ specificato per la distanza specificata (a rombo).
    #~ Se non si specifica un tasto, viene scelto random.
    #~ """
    #~ if iniz_tst is None:
        #~ iniz_tst = choice(layout.replace('\n', '').replace(' ', ''))
    #~ linee = layout.splitlines()
    #~ iniz_ind = indice_tasto(iniz_tst, layout)
    #~ lettere = set()
    #~ if iniz_ind:
        #~ for dis in range(distanza+1):
            #~ for col in [dis, -dis]:
                #~ for lin in range(-abs(distanza-dis), abs(distanza-dis)+1):
                    #~ l = lin+iniz_ind[1]
                    #~ l = l if l >= 0 and l < len(linee) else iniz_ind[1]
                    #~ c = col+iniz_ind[0]
                    #~ c = c if c >= 0 and c < len(linee[l]) else iniz_ind[0]
                    #~ lettera = tasto_indice((c, l), layout)
                    #~ if lettera:
                        #~ lettere.add(lettera)
    #~ return list(lettere)










#~ def tasti_verticali(iniz_tst=None, distanza=0, layout=layout_low):
    #~ if iniz_tst is None:
        #~ iniz_tst = choice(layout.replace('\n', '').replace(' ', ''))
    #~ linee = layout.splitlines()
    #~ iniz_ind = indice_tasto(iniz_tst, layout)
    #~ lettere = set()
    #~ if iniz_ind:
        #~ c, l = iniz_ind
        #~ y_min = max(0, l-distanza)
        #~ y_max = min(len(linee), l+distanza)
        #~ for y in range(y_min, y_max):
            #~ lettera = tasto_indice((c,y), layout)
            #~ if lettera:
                #~ lettere.add(lettera)
    #~ return list(lettere)

#~ def tasti_verticali(iniz_tst=None, distanza=0, layout=layout_low):
    #~ if iniz_tst is None:
        #~ iniz_tst = choice(layout.replace('\n', '').replace(' ', ''))
    #~ linee = layout.splitlines()
    #~ iniz_ind = indice_tasto(iniz_tst, layout)
    #~ lettere = set()
    #~ if iniz_ind:
        #~ c, l = iniz_ind
        #~ try:
            #~ y_min = max(l - distanza[0], 0)
            #~ y_max = min(l + distanza[1], len(linee))
        #~ except TypeError:
            #~ y_min = max(l - distanza, 0)
            #~ y_max = l+1
        #~ for y in range(y_min, y_max):
            #~ lettera = tasto_indice((c,y), layout)
            #~ if lettera:
                #~ lettere.add(lettera)
    #~ return list(lettere)







    #~ fine = False
    #~ while not fine:
        #~ indovina = parola_casuale(tasti_limitrofi('a', 1), 4)
        #~ parola = ""
        #~ print(f'inserisci la parola {indovina}, spazio per terminare')
        #~ while not fine:
            #~ lettera = getch()
            #~ fine = lettera == " "
            #~ parola += lettera
            #~ if not indovina.startswith(parola):
                #~ parola = ""
            #~ lung = len(parola)
            #~ print(" " * lung + indovina[lung:])
            #~ if parola == indovina:
                #~ break



    #~ azzecca = False
    #~ indovina = "acca"
    #~ parola = ""
    #~ print(indovina)
    #~ while not azzecca:
        #~ lettera = getch()
        #~ parola += lettera
        #~ if not indovina.startswith(parola):
            #~ parola = ""
        #~ lung = len(parola)
        #~ print(" " * lung + indovina[lung:])
        #~ if parola == indovina:
            #~ exit()




#~ #old layout
#~ wlow = """\
#~ `1234567890
 #~ qwertyuiop\\
 #~ asdfghjkl
 #~ zxcvbnm,.;'
  #~ -=     []/\
#~ """
#~ wupp = """\
#~ ~!@#$%^&*()
 #~ QWERTYUIOP|
 #~ ASDFGHJKL
 #~ ZXCVBNM<>:"
  #~ _+     {}?\
#~ """
#~ waltlow = """\
#~ `¹²³4€^789°
 #~ qwè®tyùìòp\\
 #~ àséfghúíó
 #~ áx©vbñm«»"'
  #~ ¯=     []/\
#~ """
#~ #layout tastiera wireless
#~ waltupp = """\
#~ ~   $  &*(
 #~ QWÈ TYÙÌÒP|
 #~ ÀSÉFGHÚÍÓ
 #~ ÁX VB M  "
   #~ +     {}?\
#~ """
