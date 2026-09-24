###########################################################################################################
#                                                                                                         #
#                        ESTRUCTURA LLISTA ENLLAÇADA AMB VECTOR   (EDT)                                   #
#                                                                                                         #
###########################################################################################################


####################################
#                                  #
#           TAD PARTIDA            #
#                                  #
####################################

class Partida:

    # Inicialització del la partida:
    def __init__(self):
        self.Nick	= " "
        self.ID_Nivell = -1
        self.Puntuacio = 0
        self.LlistaMoviments = LOE()
        self.MAP = []

#    OPERACIÓNS DEL TAD PARTIDA    #

def CrearPartida(Partida, Max):

    Partida.LlistaMoviments = CrearLlista(Partida.LlistaMoviments, Max)
    return Partida

####################################
#                                  #
#           TAD MOVIMENT           #
#                                  #
####################################

class Moviment:

    # Inicialització del "node"
    def __init__(self):

        self.ID = 0      # Primary key primera partida (1), segona partida (2) etc.
        self.Turn = -1

        self.PuntsIA = 0
        self.PuntsPlayer = 0

        self.CasellesIA = 0
        self.CasellesPlayer = 0

        self.GuanyaIA = False
        self.GuanyaPLAYER = False
        self.Taules = False
        self.OfegamentIA = False
        self.OfegamentPLAYER = False

        self.Estat = []

        # Seguent node dints de la llista contigua (Emulació de punter)
        self.seg = -1


#           OPERACIONS DEL TAD MOVIMENT           #


####################################
#                                  #
#           TAD LOE               #
#                                  #
####################################

class LOE():

    def __init__(self):

        self.MEMO = []
        self.primer = -1 # Sense nodes
        self.ultim = -1
        self.lliure = 0 # Tots el nodes son lliures


#           OPERACIONS DEL TAD LOE         #


def CrearLlista(LOE, Max):

    # Inicialització de la llista amb elements Jugada
    for x in range(Max):
        LOE.MEMO.append(Moviment())

        # Enllaço totes les posicions.
        LOE.MEMO[x].seg = x + 1

    # L'ultim enllaç apunta a NULL
    LOE.MEMO[- 1].seg = -1

    LOE.primer = -1 # Sense nodes
    LOE.ultim = -1
    LOE.lliure = 0 # Tots el nodes son lliures

    return LOE

def Seguent(LOE, pos):
    return LOE.MEMO[pos].seg

def Inici(LOE):
    return LOE.primer

def Fi(LOE):
    return -1

def LlistaBuida(LOE):
    return LOE.primer == -1

def DonamMovimentLliure(LOE):

    x = LOE.lliure                                 # Agafa la primera pos lliure
    LOE.lliure = LOE.MEMO[LOE.lliure].seg        # Actualitza les posicion lliures
    LOE.MEMO[x].seg = -1                           # La partida surt sense enllaç al següent
    return x

def InserirMoviment(LOE, moviment):

    if LOE.primer == -1:       # Es la primera partida
        LOE.primer = moviment
        LOE.ultim = moviment  
    else: 
        LOE.MEMO[LOE.ultim].seg = moviment     # Enllaço l'ultim node de la llista amb la partida atual
        LOE.ultim = moviment                    # La partida actual passa a ser l'ultima de la llista

def ImprimeixMoviment(LOE, moviment):

    print("")
    print("+ Nº Jugada: " + str(LOE.MEMO[moviment].ID))

    # Controla qui ha jugat
    if LOE.MEMO[moviment].Turn == 1:        
        print("- Ha jugat MAX")
    elif LOE.MEMO[moviment].Turn == 0:      
        print("- Ha jugat MIN")

    # Info caselles + heuristica actual
    print("- PuntsIA: " + str(LOE.MEMO[moviment].PuntsIA))
    print("- PuntsPlayer: " + str(LOE.MEMO[moviment].PuntsPlayer))
    print("- CasellesIA: " + str(LOE.MEMO[moviment].CasellesIA))
    print("- CasellesPlayer "  + str(LOE.MEMO[moviment].CasellesPlayer))
    print("")

    # Controla si sha produït un ofegament
    if LOE.MEMO[moviment].OfegamentIA:
        print("+ S'ha produït l'ofegament de IA")
    elif LOE.MEMO[moviment].OfegamentPLAYER:
        print("+ S'ha produït l'ofegament de PLAYER")

    # Controla l'estat final
    if LOE.MEMO[moviment].GuanyaIA:
        print("+ La partida es resol a favor de IA")
    elif LOE.MEMO[moviment].GuanyaPLAYER:
        print("+ La partida es resol a favor de PLAYER")
    elif LOE.MEMO[moviment].Taules:
        print("+ La partida amb Taules")

    print("")
