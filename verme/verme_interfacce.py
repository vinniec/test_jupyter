import doctest, random, itertools, os


class Interfaccia:
    """
    Questa classe deve contenere le azioni eseguite in base al tipo
    di interfaccia implementata

    >>> i = Interfaccia()
    >>> i.inizializza_dadi()
    (Dado(6), Dado(6), Dado(6), Dado(6), Dado(6), Dado(6), Dado(6), Dado(6))
    >>> len(i.inizializza_dadi())
    8
    """


    def inizializza_dadi(self):
        """Crea una tupla con tutti i dadi in gioco"""
        return tuple(Dado() for i in range(8))

    def inizializza_tessere(self):
        """
        metodo che restituisce le tessere ordinate per la grigla sul tavolo
        può richiedere la scelta delle immagini?
        """
        tessere = []
        p = 1
        for v in range (21, 37):
            tessere.append(Tessera(v, int(p)))
            p += 0.25
        return tessere

    def inizializza_giocatori(self):
        """metodo che richiede i giocatori e ritorna una loro lista"""
        raise NotImplementedError

    def scelta_dadi(self):
        """metodo che gestisce i lanci di un giocatore"""
        raise NotImplementedError


# In[4]:

class Tui(Interfaccia):
    def inizializza_giocatori(self):
        """richiede partecipanti, restituisce lista di giocatori ordinati per età"""
        gioca_num = int(input("inserisci numero giocatori(2-7): "))
        gioca_num = min(max(2, gioca_num), 7)   #no minore di 2, non maggioree di 7
        nomi = []
        giocatori = []
        while len(giocatori) < gioca_num:
            nome = input("inserisci nome giocatore: ")
            if nome in nomi:
                print("Giocatore già esistente, usare un altro nome")
                continue
            nomi.append(nome)
            while True:
                eta  = input("inserisci la sua età o niente per random: ")
                try:
                    eta = int(eta)
                except ValueError:
                    if eta == "":                     #se non si specifica l'età
                        eta = random.randint(0,100)   #viene estratta random
                        print("Età random: {} anni".format(eta))
                finally:
                    if isinstance(eta, int): break
                    else: print("età sbagliata, ritenta")
            giocatori.append(Giocatore(nome, eta))
        giocatori.sort(key=lambda giocatore:giocatore.eta)
        return giocatori


# In[5]:

class Gui(Interfaccia):
    """
        Esempio di come potrebbe funzionare gui, ad esempio ho reimplementato i metodi
        per le tessere e i dadi così da aggiungergli le immagini

        Aggiunge le immagini ai dadi
        >>> g = Gui()
        >>> d = g.inizializza_dadi()
        >>> fd = ('dado_gif/1.gif', 'dado_gif/2.gif', 'dado_gif/3.gif', 'dado_gif/4.gif', 'dado_gif/5.gif', 'dado_gif/6.gif')
        >>> all(dado.facced == fd for dado in d)
        True
        >>> from os.path import isfile
        >>> all([isfile(dado) for dado in fd])
        True

        Riesce ad utilizzare il metodo della classe padre per generare la lista tessere
        >>> g = Gui()
        >>> t = g.inizializza_tessere()
        >>> t
        [Tessera(21, 1), Tessera(22, 1), Tessera(23, 1), Tessera(24, 1), Tessera(25, 2), Tessera(26, 2), Tessera(27, 2), Tessera(28, 2), Tessera(29, 3), Tessera(30, 3), Tessera(31, 3), Tessera(32, 3), Tessera(33, 4), Tessera(34, 4), Tessera(35, 4), Tessera(36, 4)]

        E inoltre gli aggiunge dei path validi per le immagini
        >>> from os.path import isfile
        >>> all([isfile(tes.immagine) for tes in t])
        True
    """
    def inizializza_dadi(self):
        dadi = super().inizializza_dadi()
        facced = tuple(os.path.join("dado_gif/", str(f) + ".gif") for f in dadi[0].faccev)
        for dado in dadi:
            dado.facced = facced
        return dadi


    def inizializza_tessere(self):
        tessere = super().inizializza_tessere()
        for tessera in tessere:
            tessera.immagine = os.path.join("tessere_gif/", str(tessera.valore) + ".gif")
        return tessere


# In[6]:

class Giocatore():
    """
    Questa classe rappresenta un giocatore

    Istanziando il giocatore bisogna specificare il nome e l'età (facoltativa)
    >>> g = Giocatore('aldo', 14)
    >>> g.nome  #il nome del giocatore
    'aldo'
    >>> g.eta   #la sua età
    14

    Senza età viene assegnata un età casuale da 0 a 100
    >>> g = Giocatore('rino')
    >>> isinstance(g.eta, int) and 0 <= g.eta <= 100
    True

    Età non valida: ValueError
    >>> g = Giocatore('rinco', 'asda')
    Traceback (most recent call last):
    ...
    ValueError: invalid literal for int() with base 10: 'asda'

    Età valida
    >>> g = Giocatore('rinco', '134')
    >>> g.eta
    134
    """
    def __init__(self, nome, eta=None):
        self.nome = nome
        if eta is None: self.eta = random.randint(0,100) #età casuale
        else: self.eta = int(eta)

    def __repr__(self):
        return 'Giocatore("{}", {})'.format(self.nome, self.eta)


# In[7]:

class Tessera():
    """
    Questa classe rappresenta una tessera

    >>> t = Tessera(21, 1)
    >>> t
    Tessera(21, 1)
    """
    def __init__(self, valore, punti):
        self.valore = int(valore)
        self.punti = int(punti)

    def __repr__(self):
        return "Tessera({}, {})".format(self.valore, self.punti)


# In[8]:

class Dado():
    """
    Questa classe rappresenta un dado

    >>> d = Dado(6)
    >>> d.faccev
    (1, 2, 3, 4, 5, 6)

    >>> d.lancia() in [1,2,3,4,5,6]
    True
    """
    def __init__(self, facce=6):
        self.faccev = tuple(range(1, facce+1))

    def __repr__(self):
        return "Dado({})".format(len(self.faccev))

    # def lancia(self, numero=1):
    #     """Lancia il dado n volte"""
    #     return [random.choice(self.faccev) for n in range(numero)]

    def lancia(self):
        """lancia il dado una sola volta"""
        return random.choice(self.faccev)


# In[9]:

class Tavolo():
    """
    Questa classe serve a gestire gli spostamenti sul tavolo

    disattivo questo test perché è interattivo, comunuqe inserendo come input
    2, a, 2, b, 3, funziona correttamente
    >> tui = Tui()
    >> tav = Tavolo(tui)
    >> isinstance(tav.giocatori[0], Giocatore)
    True
    >> isinstance(tav.griglia[0], Tessera)
    True
    """
    def __init__(self, interf=Interfaccia()):
        self.giocatori = interf.inizializza_giocatori()
        self.griglia = interf.inizializza_tessere()
        #self.griglia = self.inizializza_griglia_tessere()


    def inizializza_griglia_tessere(self):
        """Questa funzione genera una lista di tessere"""
        tessere = []
        p = 1
        for v in range (21, 37):
            tessere.append(Tessera(v, int(p)))
            p += 0.25
        return tessere

    def gioca(self):
        for giocatore in itertools.cycle(self.giocatori):
            yield giocatore


# In[10]:

### doctest


# In[11]:

doctest.testmod()

tav = Tavolo(Tui())
for g in tav.gioca():
    input(g)
