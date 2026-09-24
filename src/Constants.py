###########################################################################################################
#                                                                                                         #
#                               INICIALITZACIÓ DE LES CONSTANTS                                           #
#                                                                                                         #
###########################################################################################################

BLACK = (0,0,0)      # Defincio del color negre
GREY = (120,120,120) # Defincio del color gris
RED = (255,0,0)      # Defincio del color vermell
YELLOW = (255,255,0) # Defincio del color groc
GREEN = (0,128,0)    # Defincio del color verd
WHITE = (255,255,255)# Defincio del color blanc
BLUE = (0,0,255)     # Defincio del color blau

ROW_COUNT = 6    # Numero de files del tauler
COLUMN_COUNT = 8    # Numero de columnes del tauler
SQUARESIZE = 100 # Quadrats de 100 pixels quadrats
RADIUS = int(SQUARESIZE/2 - 5) # Radi fitxa

PLAYER = 0           # Codi del jugador huma
AI = 1               # Codi del jugador AI

EMPTY = 0            # Codi de posicio lliure
PLAYER_PIECE = 1     # Codi de posicio jugador huma
PLAYER_PAINTED = 3   # Codi de posicio pintada per huma

AI_PIECE = 2         # Codi de posicio jugador AI
AI_PAINTED = 4       # Codi de posicio pintada per AI 
WINNER_PIECE = 5     # Codi de posicio guanyadora
BURNED = 6           # Codi de posicio cremada no jugable

MAX_JUGADES = ROW_COUNT * COLUMN_COUNT # Màxim nombre de jugades LOE MAX
DEPH_LEVEL = 9   # Profunditat de l'arbre base
BURNED_POSITIONS = 10 # Nombre de posicions cremades
