import random, pygame, sys
from pygame.locals import *

FPS = 30
Boxsize = 40
Gapsize = 10
BoardWidth = 10
BoardHeight = 10
XMargin = 70#int((WindowWidth - (BoardWidth * (Boxsize + Gapsize)))/2)
YMargin = 70#int((WindoHeight - (BoardHeight * (Boxsize + Gapsize)))/2)

WindowWidth = XMargin*2 + (BoardWidth * (Boxsize + Gapsize))
WindoHeight = YMargin*2 + (BoardHeight * (Boxsize + Gapsize))

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
FstColor = NAVYBLUE
bxColor = GRAY
RbxColor = WHITE
Hcolor = YELLOW
Mine = RED

FontSize = 15

Textcolor = BLACK

colors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, NAVYBLUE, GRAY, WHITE)

NumMine = 10

LClick = 1
RClick = 3

def main():
    global FPSclock, DISPLAYSURF, Reveald, copyR, BaseFont, mainBoard, NmMin, MC_SURF, MineCountRect, Flgcnt, Over
    pygame.init()
    FPSclock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WindowWidth, WindoHeight))
    MouseX = 0
    MouseY = 0
    BaseFont = pygame.font.Font('freesansbold.ttf', FontSize)
    pygame.display.set_caption("Minesweeper")
    mainBoard = GetRandomizedBoard()
    Surround(mainBoard)
    RevealedBoxes = generateRevedBoxesData(False)
    copyR = RevealedBoxes
    DISPLAYSURF.fill(FstColor)
    #startGameAnimation(mainBoard)
    Reveald = False
    NmMin = NumMine
    Flgcnt = 0
    Over = False

    MC_SURF, MineCountRect = Texting("Mines Left: ", WHITE, FstColor, WindoHeight - 150, WindowWidth - 60)

    while True:
        MLClick = False
        MRClick = False
        #mainBoard[1][3].InIsMine(False)
        DISPLAYSURF.fill(FstColor)
        drawBoard(mainBoard, RevealedBoxes)
        MNUM_SURF, MNUM_RECT = Texting(str(NmMin - Flgcnt), WHITE, FstColor, WindoHeight - 65, WindowWidth - 60)
        DISPLAYSURF.blit(MNUM_SURF, MNUM_RECT)
        Solved = Solver(mainBoard, NmMin, RevealedBoxes)

        if Solved != 0:
            if Solved == 2:
                END_SURF, ENDRECT = Texting("Game Over", RED, WHITE, 60, 10)
            if Solved == 1:
                END_SURF, ENDRECT = Texting("Mines Swept. Congratulations!", GREEN, FstColor, 50, 20)
            DISPLAYSURF.blit(END_SURF,ENDRECT)
            Over = True
            Flgcnt = NmMin

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                MouseX, MouseY = event.pos
            elif event.type == MOUSEBUTTONUP and Over == False:
                MouseX, MouseY = event.pos
                if event.button == LClick:
                    MLClick = True
                if event.button == RClick:
                    MRClick = True
            elif (event.type == KEYUP and event.key == K_a):
                if Reveald == False:
                    RevealAll(RevealedBoxes)
                    Reveald = True
                    Flgcnt = 10
                if Reveald == True:
                    RevealedBoxes = copyR
                    Reveald = False

        boxX, boxY = getBoxAtPixel(MouseX, MouseY)
        if boxX != None and boxY != None:
            if not RevealedBoxes[boxX][boxY]:
                drawHighlightBox(boxX, boxY)
            if not RevealedBoxes[boxX][boxY] and MLClick:
                Rboxes = []
                RevealedBoxes[boxX][boxY] = True
                RevealedBoxes = RevealChain(mainBoard, boxX, boxY, RevealedBoxes)
                #for l in range(len(Rboxes)):
                    #J , R = Rboxes[l]
                    #RevealedBoxes[J][R] = True
                print("LCLick")
            if not RevealedBoxes[boxX][boxY] and MRClick:
                if mainBoard[boxX][boxY].IsFlagged() == False:
                    mainBoard[boxX][boxY].InIsFlagged(True)
                    Flgcnt = Flgcnt + 1
                elif mainBoard[boxX][boxY].IsFlagged() == True:
                    mainBoard[boxX][boxY].InIsFlagged(False)
                    Flgcnt = Flgcnt - 1
        pygame.display.update()
        FPSclock.tick(FPS)

def GetRandomizedBoard():
    board = []
    NM = NumMine
    for i in range(BoardWidth):
        columns = []
        for z in range(BoardHeight):
            print (board)
            j = mineSpot()
            columns.append(j)
            columns[z].InIsMine(False)
        board.append(columns)
    while NM > 0:
        #print(NM)
        x = random.randrange(0, BoardWidth, 1)
        y = random.randrange(0, BoardHeight, 1)
        if (board[x][y].IsMine() == False):
            board[x][y].InIsMine(True)
            NM = NM - 1
    return board

def generateRevedBoxesData(num):
    boxes = []
    for i in range(BoardWidth):
        boxes.append([num] * BoardHeight)
    return boxes

def LeftTopBoxCoord(x, y):
    L = x * (Boxsize + Gapsize) + XMargin
    T = y * (Boxsize + Gapsize) + YMargin
    return (L, T)

def getBoxAtPixel(x, y):
    for BoxX in range(BoardWidth):
        for BoxY in range(BoardHeight):
            left, top = LeftTopBoxCoord(BoxX, BoxY)
            Rectbox = pygame.Rect(left, top, Boxsize, Boxsize)
            if Rectbox.collidepoint(x, y):
                return (BoxX, BoxY)
    return (None, None)

def drawBoard(board, reveal):
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            L, T = LeftTopBoxCoord(x, y)
            if not reveal[x][y]:
                if board[x][y].IsFlagged() == False:
                    pygame.draw.rect(DISPLAYSURF, bxColor, (L, T, Boxsize, Boxsize))
                if board[x][y].IsFlagged() == True:
                    pygame.draw.rect(DISPLAYSURF, Hcolor, (L, T, Boxsize, Boxsize))
            else:
                if board[x][y].IsMine() == False:
                    pygame.draw.rect(DISPLAYSURF, RbxColor, (L, T, Boxsize, Boxsize))
                    if (board[x][y].NumAdj() != 0):
                        Texter = BaseFont.render(str(board[x][y].NumAdj()), True, Textcolor)
                        Trect = Texter.get_rect()
                        Trect.center = L + int(Boxsize / 2), T + int(Boxsize / 2)
                        DISPLAYSURF.blit(Texter, Trect)
                else:
                    pygame.draw.rect(DISPLAYSURF, Mine, (L, T, Boxsize, Boxsize))
    DISPLAYSURF.blit(MC_SURF, MineCountRect)

def Surround(board):
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            val = MinSurround(board, x, y)
            #print(val)
            board[x][y].InNumAdj(val)

def MinSurround(board, x, y):
    num = 0
    #print(x, y)
    if (x != 0):
        if (board[x-1][y ].IsMine() == True):
            num = num + 1
    if (x != BoardWidth - 1):
        if (board[x + 1][y].IsMine() == True):
            num = num + 1
    if (y != 0):
        if (board[x][y - 1].IsMine() == True):
            num = num + 1
    if (y != BoardHeight - 1):
        if (board[x][y + 1].IsMine() == True):
            num = num + 1
    if (x != 0 and y != 0):
        if (board[x - 1][y - 1].IsMine() == True):
            num = num + 1
    if (x != BoardWidth - 1 and y != 0):
        if (board[x+1][y - 1].IsMine() == True):
            num = num + 1
    if (x != 0 and y != BoardHeight - 1):
        if (board[x-1][y + 1].IsMine() == True):
            num = num + 1
    if (x != BoardWidth - 1 and y != BoardHeight - 1):
        if (board[x+1][y + 1].IsMine() == True):
            num = num + 1
    #print(num)
    return num

def drawHighlightBox(x, y):
    L, T = LeftTopBoxCoord(x, y)
    pygame.draw.rect(DISPLAYSURF, Hcolor, (L - 5, T - 5, Boxsize + 10, Boxsize + 10), 3)

def RevealAll(list):
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            list[x][y] = True
    return list

def RevealChain(board, x, y, reve):
    Reva = reve
    if board[x][y].IsMine() == False:
        if board[x][y].NumAdj() == 0:
            Reva[x][y]=True
            if (x != 0 and Reva[x-1][y]==False):
                RevealChain(board,x-1,y,Reva)
            if (x != BoardWidth - 1 and Reva[x+1][y]==False):
                RevealChain(board, x + 1, y, Reva)
            if (y != 0 and Reva[x][y-1]==False):
                RevealChain(board, x, y-1, Reva)
            if (y != BoardHeight - 1 and Reva[x][y+1]==False):
                RevealChain(board, x, y+1, Reva)
            if (x != 0 and y != 0 and Reva[x-1][y-1]==False):
                RevealChain(board, x - 1, y-1, Reva)
            if (x != BoardWidth - 1 and y != 0 and Reva[x+1][y-1]==False):
                RevealChain(board, x + 1, y-1, Reva)
            if (x != 0 and y != BoardHeight - 1 and Reva[x-1][y+1]==False):
                RevealChain(board, x - 1, y+1, Reva)
            if (x != BoardWidth - 1 and y != BoardHeight - 1 and Reva[x+1][y+1]==False):
                RevealChain(board, x + 1, y+1, Reva)
        else:
            Reva[x][y] = True
    return Reva


def RevealAdjBox(board, x, y, Rev):
    Reveal = []
    Reveal = RevealChain(board, x, y)
    end = True
    while (end == True):
        Nbox = []
        for i in range(len(Reveal)):
            J, R = Reveal[i]
            Rev[J][R] = True
        for l in range(len(Reveal)):
            J, R = Reveal[l]
            Nbox = RevealChain(board,J,R)
            if (Nbox[0] == False):
                l = len(Reveal)
                end = False
    return Rev

def Texting(text, color, backcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BaseFont.render(text, True, color, backcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def Solver(board, nMine, rev):
    counter = 0
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            if (rev[x][y] == True):
                if board[x][y].IsMine() == True:
                    return 2
            if (rev[x][y] == False):
                counter = counter + 1
    if counter == nMine:
        #print(counter)
        return 1
    else:
        return 0

class mineSpot:
    def __init__(self):
        self.Nam = 0
        self.Im = False
        self.Fl = False

    def NumAdj(self):
        return self.Nam
    def InNumAdj(self, NM):
        self.Nam = NM

    def IsMine(self):
        return self.Im
    def InIsMine(self, num):
        self.Im = num

    def IsFlagged(self):
        return self.Fl
    def InIsFlagged(self, val):
        self.Fl = val

if __name__ == "__main__":
    main()

