###########################################################################################################
#                                                                                                         #
#                                           LLIBRERIES                                                    #
#                                                                                                         #
###########################################################################################################

import numpy as np
import random
import pygame
from pygame import mixer 
import math
import sys
import os

## Llibreries pròpies ##
import TADS
import Constants

###########################################################################################################
#                                                                                                         #
#                                     DEFINICIO DE MODULS  (IA)                                           #
#                                                                                                         #
###########################################################################################################


def Nivells(nivell):
    
    if nivell == 1:
        depth = 5
        guess = True
        burned = math.floor((Constants.COLUMN_COUNT*Constants.ROW_COUNT) / 10) - 1
    elif nivell == 2:
        depth = 6
        guess = False
        burned = math.floor((Constants.COLUMN_COUNT*Constants.ROW_COUNT) / 10) - 1
    elif nivell == 3:
        depth = 9
        guess = False    # Utilitzem floor per tal de poder jugar bé sense cremades al tauler 3x3
        burned = math.floor((Constants.COLUMN_COUNT*Constants.ROW_COUNT) / 10)
    elif nivell == 4:
        depth = Constants.DEPH_LEVEL
        guess = False
        burned = Constants.BURNED_POSITIONS
    elif nivell == 5:
        depth = 50
        guess = False
        burned = 9


    return depth, guess, burned
    

def crear_tauler(burned): # Crea la matriu de mida files per columnes, que utilitzarem per identificar els estats
    board = np.zeros((Constants.ROW_COUNT,Constants.COLUMN_COUNT), dtype='int16')

    Recount = burned
    while Recount > 0:

        row = random.randint(0,Constants.ROW_COUNT-1)     # Selecciona fila a l'atzar
        col = random.randint(0,Constants.COLUMN_COUNT-1)  # Selecciona columna a l'atzar
        if board[row][col] != Constants.BURNED:   # Si la posició no esta ja cremada afegeix pos cremada
            board[row][col] = Constants.BURNED
            Recount -= 1 


    return board


def moure_fitxa(board, row, col, piece):  # Segons l estat i el moviment, replanteja el seguent estat
    for c in range(Constants.COLUMN_COUNT):
        for r in range(Constants.ROW_COUNT):
            if board[r][c] == piece: # Segons la fitxa moguda, s'assigna valor al tauler
                if piece == Constants.PLAYER_PIECE:
                    board[r][c] = Constants.PLAYER_PAINTED
                elif piece == Constants.PLAYER_PAINTED:
                    board[r][c] = Constants.PLAYER_PIECE
                elif piece == Constants.AI_PIECE:
                    board[r][c] = Constants.AI_PAINTED
                elif piece == Constants.AI_PAINTED:
                    board[r][c] = Constants.AI_PIECE
    board[row][col] = piece


def es_posicio_valida(board, row, col, player): # Avalua, segons l estat, si el moviment del jugador indicat compleix les restriccions (NO cal que estigui lliure)
    valid = 0
    if (board[row][col] != Constants.EMPTY): # Posicio ocupada pel propi jugador, o pel contrari
        valid = 0
    elif ((row < Constants.ROW_COUNT-1) and (board[row+1][col] == player)) or ((row > 0) and (board[row-1][col] == player)): # Jugador en la mateixa columna, fila anterior o posterior
        valid = 1
    elif ((col < Constants.COLUMN_COUNT-1) and (board[row][col+1] == player)) or ((col > 0) and (board[row][col-1] == player)): # Jugador en la mateixa fila, columna anterior o posterior
        valid = 1
    return valid


def mostra_tauler(board): # Mostra el tauler per consola
    print(np.flip(board, 0))


def jugada_guanyadora(board, player): # Avalua algunes de les condiciona d'aturada
    winning = False
    painted = 0
    pair = False

    for c in range(Constants.COLUMN_COUNT): # Compta fitxes de cada jugador, de forma separada
        for r in range(Constants.ROW_COUNT):
            if  (player == Constants.PLAYER_PIECE) and (board[r][c] == Constants.PLAYER_PAINTED):
                painted+=1
            elif (player == Constants.AI_PIECE) and (board[r][c] == Constants.AI_PAINTED):
                painted+=1

    if (Constants.COLUMN_COUNT*Constants.COLUMN_COUNT) % 2 == 0: # Cal tenir en compte si el num de posicions es parell o imparell per calcular si posicio guanyadora (+1 o no)
        pair = True

    if (painted >= (Constants.COLUMN_COUNT*Constants.ROW_COUNT)/2 and not pair) or (painted == ((Constants.COLUMN_COUNT*Constants.ROW_COUNT)/2) and pair): # Si comptador de pintades igual o major a la meitat de les posicions
        winning = True  # Verifica posicio guanyadora

    if  (player == Constants.PLAYER_PIECE): # Si l'altre jugador esta ofegat guanya jugador contrari
        if len(recupera_posicions_valides(board, Constants.AI_PIECE)) == 0:
            winning = True
    elif len(recupera_posicions_valides(board, Constants.PLAYER_PIECE)) == 0:
            winning = True

    return winning


def es_node_terminal(board):
    return jugada_guanyadora(board, Constants.PLAYER_PIECE) or jugada_guanyadora(board, Constants.AI_PIECE) or len(recupera_posicions_valides(board, Constants.PLAYER_PIECE)) == 0 or len(recupera_posicions_valides(board, Constants.AI_PIECE)) == 0


def recupera_posicions_valides(board, player):
    posicions_valides = []
    for col in range(Constants.COLUMN_COUNT):
        for row in range(Constants.ROW_COUNT):
            if es_posicio_valida(board, row, col, player):
                posicions_valides.append([Constants.ROW_COUNT-row-1,col])
    return posicions_valides


def avalua_estat(board, piece, heatmap):
    
    # Heuristica proposada basada en el % de guanyar o perdre (Risc)
    PlayerPoints = 0
    IntelPoints = 0
    for c in range(Constants.COLUMN_COUNT): # Compta la puntuació de les fitxes de cada jugador, de forma separada
        for r in range(Constants.ROW_COUNT):
            if (board[r][c] == Constants.PLAYER_PAINTED):
                PlayerPoints += heatmap[r][c]
            elif (board[r][c] == Constants.AI_PAINTED):
                IntelPoints += heatmap[r][c]
            elif (board[r][c] == Constants.AI_PIECE): #Depenent a qui li toca sumarà la fitxa en la que es troba
                IntelPoints += heatmap[r][c]
            elif (board[r][c] == Constants.PLAYER_PIECE):
                 PlayerPoints += heatmap[r][c]
    
    if PlayerPoints > IntelPoints:
        score = -1
    elif PlayerPoints < IntelPoints:
        score = 1
    else:               # Si estan en taules % mes alt de guanyar a qui li toca.
        if piece == Constants.AI_PIECE:
            score = 1
        else:
            score = -1

    return score # Retorna puntuacio de l'estat


#############################
#                           #
#         MINIMAX           #
#                           #
#############################
def minimax(board, depth, alpha, beta, maximizingPlayer, heatmap):

    if maximizingPlayer:
        posicions_valides = recupera_posicions_valides(board, Constants.AI_PIECE)
    else:
        posicions_valides = recupera_posicions_valides(board, Constants.PLAYER_PIECE)

    es_terminal = es_node_terminal(board) # Comprova si hi ha alguna jugada no guanyadora possible
    if depth == 0 or es_terminal: # La profunditat es decreixent, comenca a #DEPTH i resta un nivell fins a zero
        if es_terminal: 
            if jugada_guanyadora(board, Constants.AI_PIECE):
                return (None, None, 2 + depth, 2 + depth, 0)
            elif jugada_guanyadora(board, Constants.PLAYER_PIECE):
                return (None, None, -2 - depth, 0, 2 + depth)
            else: # Joc acabat, no hi ha mes moviments valids pendents (taules)
                return (None, None, 0 + depth, 0, 0)
        else: # Maxim nivell de produnditat, no terminal
            if maximizingPlayer:
                new_score = avalua_estat(board, Constants.AI_PIECE, heatmap)
            else:
                new_score = avalua_estat(board, Constants.PLAYER_PIECE, heatmap)
            return (None, None, new_score, new_score, new_score)

    if maximizingPlayer:
        value = float('-inf')
        position = random.choice(posicions_valides) # Trio una posicio a l'atzar com a inicialitzacio
        for pos in posicions_valides: # Recorro totes les posicions valides
            b_copy = board.copy()     # Preparo nou tauler        

            moure_fitxa(b_copy, Constants.ROW_COUNT-pos[0]-1, pos[1], Constants.AI_PIECE)   # Mou a nova posicio valida, dins del nou tauler
            temp = minimax(b_copy, depth-1, alpha, beta, False, heatmap)

            new_score = temp[2]
            if new_score > value:
                value = new_score
                position = pos

            # Poda α-β.
            if new_score >= alpha:
                alpha = new_score

            # Si alfa és superor a beta deixem d'evaluar la resta
            if alpha > beta: 
                break
            
        return position[0], position[1], value, alpha, beta
    else:
        value = float('inf')
        position = random.choice(posicions_valides) # Trio una posicio valida com inicialitzacio
        for pos in posicions_valides:
            b_copy = board.copy()        

            moure_fitxa(b_copy, Constants.ROW_COUNT-pos[0]-1, pos[1], Constants.PLAYER_PIECE)
            temp = minimax(b_copy, depth-1, alpha, beta, True, heatmap) # Recupera nomes valor minimax
            
            new_score = temp[2]
            if new_score < value:
                value = new_score
                position = pos

            # Poda α-β.
            if new_score <= beta:
                beta = new_score

            # Si alfa és superor a beta deixem d'evaluar la resta
            if beta < alpha: 
                break

        return position[0], position[1], value, alpha, beta

def dibuixa_tauler(board, screen, height, col_count, row_count, visualitzar): # Dibuixa tauler via GUI

    dirname = os.path.dirname(__file__)  # Les imatges les he ficat a una subcarpeta per temes d'organització            
    pygame.display.update()

    brick = pygame.image.load(os.path.join(dirname,'img\\Caixa01.png'))
    brick2 = pygame.image.load(os.path.join(dirname,'img\\Caixa02.png'))
    brick3 = pygame.image.load(os.path.join(dirname,'img\\Caixa03.png'))
    IA_Radio = pygame.image.load(os.path.join(dirname,'img\\Fixa_IA.png'))
    PL_Radio = pygame.image.load(os.path.join(dirname,'img\\Fixa_PL.png'))
    Dots = pygame.image.load(os.path.join(dirname,'img\\Pos_valida_fame.png'))
    Red_block = pygame.image.load(os.path.join(dirname,'img\\Rastre_Vermell.png'))
    Yellow_block = pygame.image.load(os.path.join(dirname,'img\\Rastre_groc.png'))
    Fixa_Win = pygame.image.load(os.path.join(dirname,'img\\Fixa_Win.png'))
    floor1 = pygame.image.load(os.path.join(dirname,'img\\Placa01.png'))
    rej = pygame.image.load(os.path.join(dirname,'img\\Placa02.png'))

    flag_rejilla = 0 
    flag_caixa = 1

    for c in range(col_count):
        for r in range(row_count):

            # MAPEADO
            flag_rejilla += 1

            if flag_rejilla == 10:
                flag_rejilla = 0
                screen.blit(rej, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            else:
                screen.blit(floor1, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))

            # PIZAS		
            if board[r][c] == Constants.PLAYER_PIECE:
                screen.blit(PL_Radio, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            elif board[r][c] == Constants.AI_PIECE: 
                screen.blit(IA_Radio, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            elif board[r][c] == Constants.PLAYER_PAINTED: 
                screen.blit(Red_block, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            elif board[r][c] == Constants.AI_PAINTED: 
                screen.blit(Yellow_block, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            elif board[r][c] == Constants.WINNER_PIECE: 
                screen.blit(Fixa_Win, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            elif board[r][c] == Constants.BURNED: 

                if flag_caixa == 0:
                    flag_caixa += 1
                    screen.blit(brick, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
                elif flag_caixa == 1:
                    flag_caixa += 1
                    screen.blit(brick2, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
                else:
                    flag_caixa = 0
                    screen.blit(brick3, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))

            # A la visualització no volem els dots
            elif not visualitzar:
                if ((r < Constants.ROW_COUNT-1) and (board[r+1][c] == Constants.PLAYER_PIECE)) or ((r > 0) and (board[r-1][c] == Constants.PLAYER_PIECE)): # Jugador en la mateixa columna, fila anterior o posterior
                    screen.blit(Dots, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
                elif ((c < Constants.COLUMN_COUNT-1) and (board[r][c+1] == Constants.PLAYER_PIECE)) or ((c > 0) and (board[r][c-1] == Constants.PLAYER_PIECE)): # Jugador en la mateixa fila, columna anterior o posterior
                    screen.blit(Dots, (c*Constants.SQUARESIZE,height-(r*Constants.SQUARESIZE)-Constants.SQUARESIZE))
            
    pygame.display.update()


##########################################
#                                        #
#         HEURIÍSTICA PROPOSADA          #
#                                        #
##########################################
def heuristica_heatmap(): # Crea la matriu de mida files per columnes que utilitzarem com heatmap
    
    print("---Heatmap---")
    heatmap = crear_tauler(0)
    LowerRow = 0                
    UpperRow = Constants.ROW_COUNT -1    
    LowerCol = 0
    UpperCol = Constants.COLUMN_COUNT -1

    # Calcula el nombre d'iteracions que necessitem, el menor dels dos dividit per dos
    if Constants.COLUMN_COUNT < Constants.ROW_COUNT: 
        BaseCase = Constants.COLUMN_COUNT / 2
    else:
        BaseCase = Constants.ROW_COUNT /2
    
    # Per cada profunditat augmentarem el valor
    Espiral_recursiva(heatmap, LowerRow, UpperRow, LowerCol, UpperCol, 1, BaseCase)
    mostra_tauler(heatmap)
    print("-------------")
    print("")
    return heatmap

# Retorna el nombre de caselles lliures per a un estat determinat del joc
def info_caselles(board, heatmap):

    empty = 0
    ai_painted = 0
    player_painted = 0

    # Punts de cada jugador en el estat actual sense tindre en conte el invrement de nivell
    ai_points = 0
    player_points = 0


    for c in range(Constants.COLUMN_COUNT): # Compta la puntuació de les fitxes de cada jugador, de forma separada
        for r in range(Constants.ROW_COUNT):
            if (board[r][c] == Constants.EMPTY):   # Hem de buscar on es la fitxa guanyadora
                empty +=1
            if (board[r][c] == Constants.AI_PAINTED): 
                ai_points += heatmap[r][c]
                ai_painted +=1
            if (board[r][c] == Constants.PLAYER_PAINTED): 
                player_painted += 1
                player_points += heatmap[r][c]
    
    return empty, ai_painted, player_painted, ai_points, player_points


##########################################
#                                        #
#      DISENY PUNTUACIONS HEATMAP        #
#                                        #
##########################################
def Espiral_recursiva(board, LowerRow, UpperRow, LowerCol, UpperCol, value, BaseCase):

    if BaseCase > 0: # Cas recursiu

        x = LowerRow
        y = LowerCol
        while y <= UpperCol:    # Emplena de la esquina superior esquerra a la superior dreta
            board[x][y] = value
            y += 1

        LowerRow += 1   # Incrementem posició de la fila ja que l'hem emplenat tota

        x = LowerRow
        y = UpperCol
        while x <= UpperRow:        # Emplena de la esquina suerior dreta (-1 d'avants) fins a la esquina inferior dreta
            board[x][y] = value
            x += 1
        
        UpperCol -=1        # Decrementem la columna, tota la columna ja esta printejada

        x = UpperRow
        y = UpperCol
        while y >= LowerCol:        # Emplena des de l'esquina inferior dreta (-1 d'avants) fins a la esuina inferior esquerra
            board[x][y] = value
            y -= 1
        
        UpperRow -= 1  # eliminem la fila superior ()

        x = UpperRow
        y = LowerCol
        while x >= LowerRow:        # Emplena des de l'esquina inferior esquerra (-1 d'avants) fins l'esquina superior esquerra (-1 del principi)
            board[x][y] = value
            x -= 1

        LowerCol +=1

        # repetim el procediment dreta, abaix, esquerra, dalt, per cada nivell mes de profunditat augmentarem els punts
        Espiral_recursiva(board, LowerRow, UpperRow, LowerCol, UpperCol, value + 1, BaseCase - 1)



###########################################################################################################
#                                                                                                         #
#                                     LÒGICA DEL JOC SPLATOON                                             #
#                                                                                                         #
###########################################################################################################

def joc(nivell, Part):
    depth, guess, burned = Nivells(nivell)
    guess_flag = 1
    num_jugada = 0


    # Crea tauler de joc
    if nivell == 1 or nivell == 2 or nivell == 3 or nivell == 5:

        board = crear_tauler(burned) # Crea tauler de joc
        print(" Profunditat: " + str(depth))
        print(" Component aleatori: " + str(guess))
        print(" Caselles cremades : " + str(burned))
        print()

    else:

        board = crear_tauler(Constants.BURNED_POSITIONS)      # Versió genrèrica 

    # Pygame Diseny gràfic window
    pygame.init() 
    pygame.display.set_caption("Splatoon")

    # Per tal de organitzar el projecte he posat les imatges en una subcarpeta
    dirname = os.path.dirname(__file__)              
    filename = os.path.join(dirname, 'img\\joystick.png')

    icon = pygame.image.load(filename)            # Carrega les imatges que utilitzarà el nostre joc
    # pygame.display.set_icon(icon)

    # El nostre joc tindrà musica
    mixer.music.load(os.path.join(dirname,'audio\\Start.ogg'))
    mixer.music.play()                    # (-1) indica play on loop

    width = Constants.COLUMN_COUNT * Constants.SQUARESIZE
    height = Constants.ROW_COUNT * Constants.SQUARESIZE
    size = (width, height)
    myfont = pygame.font.SysFont("monospace", 40)

    # TODO: Cal reprogramar qui gaunya el torn inicial
    turn = random.randint(0,1)


    # TODO: Cal reprogramar la situacio inicial de les fitxes
    while True:

        start = [random.randint(0,Constants.ROW_COUNT-1),random.randint(0,Constants.COLUMN_COUNT-1)]

        if board[start[0], start[1]] != Constants.BURNED:
            moure_fitxa(board, start[0], start[1], Constants.AI_PIECE) # Posiciona fitxa IA
            break

    while True:

        start = [random.randint(0,Constants.ROW_COUNT-1),random.randint(0,Constants.COLUMN_COUNT-1)]
        
        # TODO: Les posicions assignades han de ser aleatories i exclussives
        if board[start[0], start[1]] != Constants.BURNED and board[start[0], start[1]] != Constants.AI_PIECE:
            moure_fitxa(board, start[0], start[1], Constants.PLAYER_PIECE) # Posiciona fitxa IA
            break

    """
    turn = 1              #----- (Proves caixa blanca) -----
    start = [0,2]
    moure_fitxa(board, start[0], start[1], PLAYER_PIECE) # Posiciona fitxa humana
    start = [2,1]
    moure_fitxa(board, start[0], start[1], AI_PIECE) # Posiciona fitxa IA
    screen = pygame.display.set_mode(size)
    dibuixa_tauler(board, screen, height)
    """

    screen = pygame.display.set_mode(size)
    dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

    # Inicialització de la heurística heatmap
    heatmap = heuristica_heatmap()
    pygame.display.update()

    # Estat inicial Hem de enviar el board a MySQL
    mostra_tauler(board)
    # Part.MAP = board.copy()

    # PUNTERS #
    EstatInicial = TADS.DonamMovimentLliure(Part.LlistaMoviments)       # Agafem nou node per emmagatzemar la partida de IA
    
    TADS.InserirMoviment(Part.LlistaMoviments, EstatInicial)
    Part.LlistaMoviments.MEMO[EstatInicial].Estat = board.copy()
    # PUNTERS #
    TADS.ImprimeixMoviment(Part.LlistaMoviments, EstatInicial)
    print("-------------")

    ##########################################
    #                                        #
    #           LÒGICA DEL JOC               #
    #                                        #
    ##########################################
    game_over = False
    while not game_over: # Mentre hi ha partida

        if turn == Constants.PLAYER and not game_over:      # Espera la jugada humana

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    posx = event.pos[0] # Recupera la posicio (columna) clicada
                    posy = event.pos[1] # Recupera la posicio (fila) clicada

                    mixer.music.load(os.path.join(dirname,'audio\\PL_Move.wav'))
                    mixer.music.play()                    # (-1) indica play on loop

                    row = int(math.floor((Constants.ROW_COUNT*Constants.SQUARESIZE-posy)/Constants.SQUARESIZE)) # Cal invertir el calcul d'y!
                    col = int(math.floor(posx/Constants.SQUARESIZE))

                    if es_posicio_valida(board, row, col, Constants.PLAYER_PIECE):
                        
                        num_jugada += 1
                        moure_fitxa(board, row, col, Constants.PLAYER_PIECE)
                        dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

                        pos_val_PL = recupera_posicions_valides(board, Constants.PLAYER_PIECE)
                        pos_val_IA = recupera_posicions_valides(board, Constants.AI_PIECE)
                        info = info_caselles(board, heatmap) # return empty, ai_painted, player_painted, ai_points, player_points
                        pos_lliures = info[0]

                        # PUNTERS # 
                        PartidaPlayer = TADS.DonamMovimentLliure(Part.LlistaMoviments)       # Agafem nou node per emmagatzemar la partida de PLAYER
                        Part.LlistaMoviments.MEMO[PartidaPlayer].ID = num_jugada
                        

                        # PUNTERS #

                        if not pos_val_PL and pos_lliures == 0: # SI JA NO QUEDEN CASELLES LLIURES

                            if info[1] > info[2]:

                                # PUNTERS #
                                Part.LlistaMoviments.MEMO[PartidaPlayer].GuanyaIA = True
                                # PUNTERS #

                                label = myfont.render("Guanya IA!", 1, Constants.WHITE) 
                                screen.blit(label, (40,10))

                                mixer.music.load(os.path.join(dirname,'audio\\AI_Win.mp3'))
                                mixer.music.play()

                                pygame.display.flip()
                                game_over = True

                            if info[1] < info[2]:

                                # PUNTERS #
                                Part.LlistaMoviments.MEMO[PartidaPlayer].GuanyaPLAYER = True
                                # PUNTERS #

                                moure_fitxa(board, row, col, Constants.WINNER_PIECE)
                                dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)
                                label = myfont.render("Guanya PLAYER!", 1, Constants.WHITE) 
                                screen.blit(label, (40,10))

                                mixer.music.load(os.path.join(dirname,'audio\\PL_Win.wav'))
                                mixer.music.play()

                                pygame.display.flip()
                                game_over = True

                            else:

                                # PUNTERS #
                                Part.LlistaMoviments.MEMO[PartidaPlayer].Taules = True
                                # PUNTERS #

                                label = myfont.render("Empat!", 1, Constants.WHITE)
                                screen.blit(label, (40,10))

                                mixer.music.load(os.path.join(dirname,'audio\\PL_Win.wav'))
                                mixer.music.play()

                                pygame.display.flip()
                                game_over = True

                        elif not pos_val_IA and pos_lliures > 0: # PLAYER OFEGA A IA

                            # PUNTERS #
                            Part.LlistaMoviments.MEMO[PartidaPlayer].GuanyaPLAYER = True
                            Part.LlistaMoviments.MEMO[PartidaPlayer].OfegamentIA = True
                            # PUNTERS #

                            moure_fitxa(board, row, col, Constants.WINNER_PIECE)
                            dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

                            mixer.music.load(os.path.join(dirname,'audio\\PL_Win.wav'))
                            mixer.music.play()

                            label = myfont.render("Ofegament IA!", 1, Constants.WHITE)
                            screen.blit(label, (40,10))
                            pygame.display.flip()
                            game_over = True


                        # PUNTERS #
                        Part.LlistaMoviments.MEMO[PartidaPlayer].Turn = turn
                        Part.LlistaMoviments.MEMO[PartidaPlayer].CasellesIA = info[1]
                        Part.LlistaMoviments.MEMO[PartidaPlayer].CasellesPlayer = info[2]
                        Part.LlistaMoviments.MEMO[PartidaPlayer].PuntsIA = info[3] * nivell
                        Part.LlistaMoviments.MEMO[PartidaPlayer].PuntsPlayer = info[4] * nivell
                        Part.LlistaMoviments.MEMO[PartidaPlayer].Estat = board.copy()
                        # PUNTERS #

                        # Flag control de qu li toca
                        turn += 1            
                        turn = turn % 2

                        TADS.InserirMoviment(Part.LlistaMoviments, PartidaPlayer)
                        TADS.ImprimeixMoviment(Part.LlistaMoviments, PartidaPlayer)
                        mostra_tauler(board)
                        print("-------------")
                        print("")
                        # PUNTERS #

                    
        if turn == Constants.AI and not game_over: # Espera la jugada d'IA

            # Declaro variables
            row = None
            col = None

            # Flag pel component aleatori
            num_jugada += 1 

            # Joc amb component aleatori
            if guess:

                if guess_flag == 1:   # Una jugada si

                    posicions_valides = recupera_posicions_valides(board, Constants.AI_PIECE)
                    position = random.choice(posicions_valides)
                    row = position[0]
                    col = position[1]
                    
                else: # Una altra no

                    guess_flag == 1
                    row, col, minimax_score, alpha, beta = minimax(board, depth, float('-inf'), float('inf'), True, heatmap)
                    guess_flag == 1

            else: # Joc sense component aleatori

                row, col, minimax_score, alpha, beta = minimax(board, depth, float('-inf'), float('inf'), True, heatmap) # Al tanto amb aquest - + infinits!

            pygame.time.wait(500)
            mixer.music.load(os.path.join(dirname,'audio\\AI_Move.ogg'))
            mixer.music.play()

            if row is not None: 
                moure_fitxa(board, Constants.ROW_COUNT-row-1, col, Constants.AI_PIECE)
            else:
                pos_val_IA = recupera_posicions_valides(board, Constants.AI_PIECE) # SOL BUG 01: EMPAT AMB MOVIMENT IA
                position = random.choice(pos_val_IA)
                row = position[0]
                col = position[1]
                moure_fitxa(board, Constants.ROW_COUNT-row-1, col, Constants.AI_PIECE)

            for event in pygame.event.get():     # Bucle d'events, requisit pel bon funcionament de Pygame window
                if event.type == pygame.QUIT:
                    run = False
            
            dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

            pos_val_PL = recupera_posicions_valides(board, Constants.PLAYER_PIECE)
            pos_val_IA = recupera_posicions_valides(board, Constants.AI_PIECE)
            info = info_caselles(board, heatmap) # return empty, ai_painted, player_painted, ai_points, player_points
            pos_lliures = info[0]

            # PUNTERS #
            PartidaIA = TADS.DonamMovimentLliure(Part.LlistaMoviments)       # Agafem nou node per emmagatzemar la partida de IA
            Part.LlistaMoviments.MEMO[PartidaIA].ID = num_jugada
            Part.LlistaMoviments.MEMO[PartidaIA].Turn = turn
            Part.LlistaMoviments.MEMO[PartidaIA].CasellesIA = info[1]
            Part.LlistaMoviments.MEMO[PartidaIA].CasellesPlayer = info[2]
            Part.LlistaMoviments.MEMO[PartidaIA].PuntsIA = info[3] * nivell
            Part.LlistaMoviments.MEMO[PartidaIA].PuntsPlayer = info[4] * nivell
            # PUNTERS #


            if not pos_val_IA and pos_lliures == 0: # SI JA NO QUEDEN CASELLES LLIURES

                if info[1] > info[2]:

                    # PUNTERS #
                    Part.LlistaMoviments.MEMO[PartidaIA].GuanyaIA = True
                    # PUNTERS #

                    moure_fitxa(board, row, col, Constants.WINNER_PIECE)
                    dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

                    label = myfont.render("Guanya IA!", 1, Constants.WHITE) 
                    screen.blit(label, (40,10))
            

                    mixer.music.load(os.path.join(dirname,'audio\\AI_Win.mp3'))
                    mixer.music.play()

                    pygame.display.flip()
                    game_over = True

                if info[1] < info[2]:

                    # PUNTERS #
                    Part.LlistaMoviments.MEMO[PartidaIA].GuanyaPLAYER = True
                    # PUNTERS #

                    label = myfont.render("Guanya PLAYER!", 1, Constants.WHITE) 
                    screen.blit(label, (40,10))

                    mixer.music.load(os.path.join(dirname,'audio\\PL_Win.wav'))
                    mixer.music.play()

                    pygame.display.flip()
                    game_over = True

                else:

                    # PUNTERS #
                    Part.LlistaMoviments.MEMO[PartidaIA].Taules = True
                    # PUNTERS #

                    label = myfont.render("Empat!", 1, Constants.WHITE)
                    screen.blit(label, (40,10))
                    pygame.display.flip()
                    game_over = True
            
            if not pos_val_PL and pos_lliures > 0: # IA OFEGA A PLAYER
                
                # PUNTERS #
                Part.LlistaMoviments.MEMO[PartidaIA].GuanyaIA = True
                Part.LlistaMoviments.MEMO[PartidaIA].OfegamentPLAYER = True
                # PUNTERS #

                moure_fitxa(board, Constants.ROW_COUNT-row-1, col, Constants.WINNER_PIECE) # Cal invertir els rows BUG 03
                dibuixa_tauler(board, screen, height, Constants.COLUMN_COUNT, Constants.ROW_COUNT, False)

                label = myfont.render("Ofegament PLAYER!", 1, Constants.WHITE)
                screen.blit(label, (40,10))

                mixer.music.load(os.path.join(dirname,'audio\\AI_Win.mp3'))
                mixer.music.play()

                pygame.display.flip()
                game_over = True

            # PUNTERS #
            Part.LlistaMoviments.MEMO[PartidaIA].Estat = board.copy()
            TADS.InserirMoviment(Part.LlistaMoviments, PartidaIA)
            TADS.ImprimeixMoviment(Part.LlistaMoviments, PartidaIA)
            mostra_tauler(board)
            print("-------------")
            print("")
            # PUNTERS #

            # Flag control de qu li toca
            turn += 1            
            turn = turn % 2

        if game_over:  
            pygame.time.wait(5000)      # Finalització de la partida
            pygame.display.quit()
            pygame.quit()
            return Part                 # Retorna la parida generada # Part EDT + Per SQL

# Andormix 