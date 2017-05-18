

import doctest, random, itertools, os



class Interfaccia:
    """
    Questa classe deve contenere le azioni eseguite in base al tipo di interfaccia implementata
    """

    def inizializza_giocatori(self):
        """metodo che richiede i giocatori e ritorna una loro lista"""
        raise NotImplementedError

    def scelta_dadi(self):
        """metodo che gestisce i lanci di un giocatore"""
        raise NotImplementedError




class Tui(Interfaccia):
    def inizializza_giocatori(self):
        """richiede partecipanti, restituisce lista di giocatori"""
       #numero giocatori
        gioca_num = int(input("inserisci numero giocatori(2-7): "))
        gioca_num = min(max(2, gioca_num), 7)   #no minore di 2, non maggioree di 7
        nomi = []
        giocatori = []
       #input loop nome e età
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
            giocatori.append(G_Umano(nome, eta))
       #restituisco i giocatori
        return giocatori

    def scelta_dadi(self):
        pass







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
    >>> g = Giocatore('rino', 22)
    >>> isinstance(g.eta, int) and 0 <= g.eta <= 100
    True


    """
    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta

    def __repr__(self):
        return '{}("{}", {})'.format(type(self).__name__,self.nome, self.eta)




class G_Umano(Giocatore):
    """se il giocatore è umano, i/o sarà gestita da una interfaccia

    >>> tui = Tui()
    >>> g = G_Umano('aldo', '35')
    >>> g.eta, g.nome
    (35, 'aldo')
    >>> g
    Umano("aldo", 35)

    Età non valida: ValueError
    >>> g = G_Umano('rinco', 'asda')
    Traceback (most recent call last):
    ...
    ValueError: invalid literal for int() with base 10: 'asda'

    """
    def __init__(self, nome, eta=None):
        if eta is None: eta = random.randint(0,100) #età casuale
        else: eta = int(eta)
        super().__init__(nome, eta)
    # def scelta_dadi(self):
    #     risultato = self.ui.lancia_dadi()





class G_Artificiale(Giocatore):
    """se il giocatore è un ia, le azioni saranno calcolate in automatico"""
    pass




class G_Remoto(Giocatore):
    """se il giocatore è remoto l'io sarà gestito da un client, il client dovrà vedere che interfaccia usare"""
    pass




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




class Tavolo():
    """
    Questa classe serve a gestire gli spostamenti sul tavolo

    >>>

    disattivo questo test perché è interattivo, comunuqe inserendo come input
    2, a, 2, b, 3, funziona correttamente
    >> tui = Tui()
    >> tav = Tavolo(tui)
    >> isinstance(tav.giocatori[0], Giocatore)
    True
    >> isinstance(tav.griglia[0], Tessera)
    True
    >> isinstance(tav.dadi[0], Dado)
    True
    """
    def __init__(self, giocatori):
        self.giocatori = self.ordina_giocatori(giocatori)
        self.griglia = self.inizializza_griglia_tessere()
        self.dadi = self.inizializza_dadi()
        # ui.tavolo = self    #dipendenza circolare!

    def inizializza_griglia_tessere(self):
        """Questa funzione genera una lista di tessere"""
        tessere = []
        p = 1
        for v in range (21, 37):
            tessere.append(Tessera(v, int(p)))
            p += 0.25
        return tessere

    def inizializza_dadi(self):
        """Crea una tupla con tutti i dadi in gioco"""
        return tuple(Dado() for i in range(8))

    def ordina_giocatori(self, giocatori):
        """ordina i giocaatori per età"""
        return giocatori.sort(key=lambda giocatore:giocatore.eta)

    def turno(self):
        """restituisce il giocatore del turno corrente fintanto che ci sono tessere nella griglia"""
        giocatore = itertools.cycle(self.giocatori)
        while self.griglia:
            yield next(giocatore)




### programma
if __name__ == "__main__":
    doctest.testmod()                             #eseguo i test
    ui = Tui()                                    #scelgo l'interfaccia
    # tv = Tavolo(ui.inizializza_giocatori())       #inizializzo il tavolo

   #provo a fare un giro di gioco, poi vedrò come e dove piazzarlo
    # for giocatore in tv.turno():
    #     risultato = giocatore.scelta_dadi()







