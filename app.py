import pygame
from math import floor
import assets
import colors
import datetime
from square import *
from button import *
from render import *
from random import randint

logtext = open('log.txt', 'w')

# Settings

FPS = 60
pygame.display.set_caption("CheckersVM")
pygame.display.set_icon(assets.Icon)
blackturn = True
lastmove = []
postforceplay = False
force = False
moves = 0
debugrender = False
winner = None
gamemode = 0
gamecolor = 0
menuclick = False

# Game States

gamestate = 0
gamescreen = 0
pendingstate = None # For the yes/no box

# 0 Main Menu
# 1 Game PVP
# 2 Game PVCOM

# Buttons

MM_Play = Button(assets.Play, assets.Play_H, 500, 300)
MM_Settings = Button(assets.Settings, assets.Settings_H, 500, 450)
MM_Quit = Button(assets.Quit, assets.Quit_H, 500, 600)
IG_Quit = Button(assets.Quit, assets.Quit_H, 900, 650)
SET_PvP = Button(assets.PvP, assets.PvP_H, 500, 300)
SET_PvC = Button(assets.PvC, assets.PvC_H, 500, 300)
SET_CvC = Button(assets.CvC, assets.CvC_H, 500, 300)
SET_Back = Button(assets.Back, assets.Back_H, 500, 600)
SET_Col0 = Button(assets.Clr0, assets.Clr0, 400, 450)
SET_Col0_Sel = Button(assets.Clr0_sel, assets.Clr0_sel, 400, 450)
SET_Col1 = Button(assets.Clr1, assets.Clr1, 550, 450)
SET_Col1_Sel = Button(assets.Clr1_sel, assets.Clr1_sel, 550, 450)
SET_Col2 = Button(assets.Clr2, assets.Clr2, 700, 450)
SET_Col2_Sel = Button(assets.Clr2_sel, assets.Clr2_sel, 700, 450)

# Usable squares

a1 = Square(0,7,1,1,0)
a3 = Square(2,7,1,1,0)
a5 = Square(4,7,1,1,0)
a7 = Square(6,7,1,1,0)
b2 = Square(1,6,1,1,0)
b4 = Square(3,6,1,1,0)
b6 = Square(5,6,1,1,0)
b8 = Square(7,6,1,1,0)
c1 = Square(0,5,1,1,0)
c3 = Square(2,5,1,1,0)
c5 = Square(4,5,1,1,0)
c7 = Square(6,5,1,1,0)
d2 = Square(1,4,0,0,0)
d4 = Square(3,4,0,0,0)
d6 = Square(5,4,0,0,0)
d8 = Square(7,4,0,0,0)
e1 = Square(0,3,0,0,0)
e3 = Square(2,3,0,0,0)
e5 = Square(4,3,0,0,0)
e7 = Square(6,3,0,0,0)
f2 = Square(1,2,2,1,0)
f4 = Square(3,2,2,1,0)
f6 = Square(5,2,2,1,0)
f8 = Square(7,2,2,1,0)
g1 = Square(0,1,2,1,0)
g3 = Square(2,1,2,1,0)
g5 = Square(4,1,2,1,0)
g7 = Square(6,1,2,1,0)
h2 = Square(1,0,2,1,0)
h4 = Square(3,0,2,1,0)
h6 = Square(5,0,2,1,0)
h8 = Square(7,0,2,1,0)

def setgame():
    """Resets game to its move 0 state"""
    global selsquare
    selsquare = None
    squarelist[0] = Square(0,7,1,1,0)
    squarelist[1] = Square(2,7,1,1,0)
    squarelist[2] = Square(4,7,1,1,0)
    squarelist[3] = Square(6,7,1,1,0)
    squarelist[4] = Square(1,6,1,1,0)
    squarelist[5] = Square(3,6,1,1,0)
    squarelist[6] = Square(5,6,1,1,0)
    squarelist[7] = Square(7,6,1,1,0)
    squarelist[8] = Square(0,5,1,1,0)
    squarelist[9] = Square(2,5,1,1,0)
    squarelist[10] = Square(4,5,1,1,0)
    squarelist[11] = Square(6,5,1,1,0)
    squarelist[12] = Square(1,4,0,0,0)
    squarelist[13] = Square(3,4,0,0,0)
    squarelist[14] = Square(5,4,0,0,0)
    squarelist[15] = Square(7,4,0,0,0)
    squarelist[16] = Square(0,3,0,0,0)
    squarelist[17] = Square(2,3,0,0,0)
    squarelist[18] = Square(4,3,0,0,0)
    squarelist[19] = Square(6,3,0,0,0)
    squarelist[20] = Square(1,2,2,1,0)
    squarelist[21] = Square(3,2,2,1,0)
    squarelist[22] = Square(5,2,2,1,0)
    squarelist[23] = Square(7,2,2,1,0)
    squarelist[24] = Square(0,1,2,1,0)
    squarelist[25] = Square(2,1,2,1,0)
    squarelist[26] = Square(4,1,2,1,0)
    squarelist[27] = Square(6,1,2,1,0)
    squarelist[28] = Square(1,0,2,1,0)
    squarelist[29] = Square(3,0,2,1,0)
    squarelist[30] = Square(5,0,2,1,0)
    squarelist[31] = Square(7,0,2,1,0)
    return True, [], False, False, 0, False, None

squarelist = [a1,a3,a5,a7,b2,b4,b6,b8,c1,c3,c5,c7,d2,d4,d6,d8,e1,e3,e5,e7,f2,f4,f6,f8,g1,g3,g5,g7,h2,h4,h6,h8]

selsquare = None
is_selected = False
oldmoves = 0
forcelist = []
movelist = []

# pygame setup
pygame.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
running = True



def openlog():
    """Opens game log and writes current date and time"""
    e = datetime.datetime.now()
    L = [e.strftime("%Y-%m-%d %H:%M:%S"), 
         e.strftime("%d/%m/%Y"), 
         e.strftime("%I:%M:%S %p"), 
         e.strftime("%a, %b %d, %Y")
         ]
    logtext.write("\n")
    logtext.write("--------------\n")
    logtext.write(f"{L}\n")



def forcecheck(blackturn: bool) -> bool:
    """Check for any forced moves which the player whose turn it is must choose from. Searches for all squares (index a in squarelist) with pieces matching the colour of the current player. Once found, looks for squares with pieces of the opposite colour (index b in squarelist) using function "force_findb(blackturn, force_found, clr, a)."
    """
    forcelist.clear()
    force_found = False
    if blackturn:
        clr = 1
    else:
        clr = 2
    for a in range(len(squarelist)):
        if squarelist[a].piececolor == clr:
                force_found = force_findb(blackturn, force_found, clr, a)
    if force_found == True:
        return True
    else:
        return False



def force_findb(blackturn: bool, force_found: bool, clr: int, a: int) -> bool:
    """Searches for all squares (index b in squarelist) with pieces of the opposite colour to square with index a in squarelist. Once found, compares coordinates of both squares to see if piece on square b is in position to potentially be jumped by piece on square A, then calls function "force_findc(a, b, force_found)."
    """
    for b in range(len(squarelist)):
        if squarelist[b].piececolor != 0 and squarelist[b].piececolor != clr:
            if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                if squarelist[a].type == 2:
                    if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                        force_found = force_findc(a, b, force_found)
                else:
                    if blackturn:
                        if squarelist[a].ycoordinate-squarelist[b].ycoordinate == 1:
                            force_found = force_findc(a, b, force_found)
                    else:
                        if squarelist[a].ycoordinate-squarelist[b].ycoordinate == -1:
                            force_found = force_findc(a, b, force_found)
    return force_found



def force_findc(a: int, b: int, force_found: bool) -> bool:
    """Searches for square (index c in squarelist) which piece on square A will jump if it jumps over square B. If this square exists and is unoccupied, calls function "addforcedmove(a, b, c)."""
    for c in range(len(squarelist)):
        if (
        (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
        (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
        (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
        (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
        squarelist[c].piececolor == 0
        ):
            force_found = addforcedmove(a, b, c)
    return force_found
            


def addforcedmove(a: int, b: int, c: int) -> bool:
    """
    Adds valid forced move to the list of possible forced moves (by appending indexes of squares A, B, C to forcelist), visually marks square C and returns True so player can now only choose from forced moves (square with index a in squarelist)."""
    forcelist.append(a)
    forcelist.append(b)
    forcelist.append(c)
    return True



def postforce(a: int, blackturn: bool) -> bool:
    """Check for continuations of a chain of forced moves which the player whose turn it is must choose from. Only checks for piece which has just been moved by the player. Looks for squares with pieces of the opposite colour (index b in squarelist) using function "force_findb(blackturn, force_found, clr, a)."""
    global selsquare
    forcelist.clear()
    force_found = 0
    if blackturn:
        clr = 1
    else:
        clr = 2
    force_found = force_findb(blackturn, force_found, clr, a)
    if force_found == True:
        if gamemode == 0 or (gamemode == 1 and blackturn):
            selsquare = a
        findmoves(blackturn)
        return True
    else:
        return False
            


def availabilitycheck(selsquare: int):
    """Checks for possible moves of selected piece"""
    clearavailability()
    if len(forcelist) == 0:
        for x in range(int(len(movelist)/2)):
            if movelist[x*2] == selsquare:
                squarelist[movelist[x*2+1]].available = 1
    else:
        for x in range(int(len(movelist)/2)):
            squarelist[movelist[x*2+1]].available = 2



def kingcheck():
    """Checks for pieces which have reached the last row of the opposite side. If an uncrowned piece is found, it becomes a king."""
    for a in range(4):
        if squarelist[a].piececolor == 2:
            squarelist[a].type = 2
    for b in range(28,32,1):
        if squarelist[b].piececolor == 1:
            squarelist[b].type = 2



def click():
    """Detects which square the player has clicked on."""
    global selsquare
    valid = False
    mousex, mousey = pygame.mouse.get_pos()
    fieldx, fieldy = floor(mousex/100),floor(mousey/100)
    for a in range(len(squarelist)):
        if squarelist[a].xcoordinate == fieldx and squarelist[a].ycoordinate == fieldy:
            select(a)
            valid = True
    if valid == False:
        if not postforceplay:
            selsquare = None




def select(a):
    """Selects the square which has been clicked on by the user if it contains a piece with a legal movement opportunity."""
    global selsquare
    global lastmove
    valid = False
    if selsquare == None:
        lastmove.clear()
        for x in range(int(len(movelist)/2)):
            if a == movelist[x*2]:
                selsquare = a
                valid = True
                break
    else:
        for x in range(int(len(movelist)/2)):
            if selsquare == movelist[x*2] and a == movelist[x*2+1]:
                move(selsquare,a)
                if not postforceplay:
                    selsquare = None
                valid = True
                break
            elif a == movelist[x*2]:
                selsquare = a
                valid = True
                break
        if valid == False:
            if not postforceplay:
                selsquare = None

       
    
def move(a,b):
    """Executes a legal move."""
    global moves
    global blackturn
    global lastmove
    global postforceplay
    if force:
        for x in range(int(len(forcelist)/3)):
            if a == forcelist[x*3] and b == forcelist[x*3+2]:
                squarelist[forcelist[x*3+1]].type, squarelist[forcelist[x*3+1]].piececolor = 0,0
                squarelist[a].piececolor,squarelist[a].type,squarelist[b].piececolor,squarelist[b].type = squarelist[b].piececolor,squarelist[b].type,squarelist[a].piececolor,squarelist[a].type
                moves += 1
                kingcheck()
                lastmove = [a,b]
                if postforce(b,blackturn) == False:
                    blackturn = not blackturn
                    postforceplay = False
                else:
                    postforceplay = True
                break
    else:
        for x in range(int(len(movelist)/2)):
            if a == movelist[x*2] and b == movelist[x*2+1]:
                squarelist[a].piececolor,squarelist[a].type,squarelist[b].piececolor,squarelist[b].type = squarelist[b].piececolor,squarelist[b].type,squarelist[a].piececolor,squarelist[a].type
                moves += 1
                lastmove = [a,b]
                blackturn = not blackturn
                break



def clearavailability():
    """Clears the availability value of all squares on the board."""
    for x in range(len(squarelist)):
        squarelist[x].available = 0



def keycheck(event):
    """Checks for key presses."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "ESC"
        elif event.key == pygame.K_d:
            return "Debug"
    else: 
        return False
    


def findmoves(blackturn: bool):
    """Finds all of active player's legal moves."""
    global movelist
    movelist.clear()
    if len(forcelist)!=0:
        addlegalmove_forced()
    elif blackturn:
        for a in range(len(squarelist)):
            if squarelist[a].piececolor == 1:
                for b in range(len(squarelist)):
                    if squarelist[b].type == 0:
                        if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                            if squarelist[a].type == 2:
                                if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                                    addlegalmove(a,b)
                                else: continue
                            else:
                                if squarelist[a].ycoordinate-squarelist[b].ycoordinate == 1:
                                    addlegalmove(a,b)
                                else: continue
                        else: continue
                    else: continue
            else: continue
    else:
        for a in range(len(squarelist)):
            if squarelist[a].piececolor == 2:
                for b in range(len(squarelist)):
                    if squarelist[b].type == 0:
                        if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                            if squarelist[a].type == 2:
                                if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                                    addlegalmove(a,b)
                                else: continue
                            else:
                                if squarelist[b].ycoordinate-squarelist[a].ycoordinate == 1:
                                    addlegalmove(a,b)
                                else: continue
                        else: continue
                    else: continue
            else: continue                   



def addlegalmove(a: int, b: int):
    """Adds a move to the list of legal moves."""
    movelist.append(a)
    movelist.append(b)
    


def addlegalmove_forced():
    """Copies list of forced moves into the list of legal moves."""
    for x in range(int(len(forcelist)/3)):
        movelist.append(forcelist[x*3])
        movelist.append(forcelist[x*3+2])



def wincheck(blackturn):
    """Checks for win condition. (If the active player doesn't have any possible legal moves, their opponent wins)"""
    if len(movelist)==0:
        if blackturn: return 2
        else: return 1
    else: return None



def cpumove():
    """Makes a random move"""
    choice = randint(0, len(movelist)/2-1)
    move(movelist[choice*2],movelist[choice*2+1])



def debuglog(oldmoves):
    """Logs the current state of the board."""
    if moves != oldmoves:
        oldmoves = moves
        logtext.write("\n")
        logtext.write(f"Moves completed: {moves}\n")
        squarenames = ["a1","a3","a5","a7","b2","b4","b6","b8","c1","c3","c5","c7","d2","d4","d6","d8","e1","e3","e5","e7","f2","f4","f6","f8","g1","g3","g5","g7","h2","h4","h6","h8"]
        for a in range(len(squarelist)):
            logtext.write(f"{squarenames[a]}: Piececolor {squarelist[a].piececolor} | Type {squarelist[a].type} | Available {squarelist[a].available}\n")
        if selsquare != None:
            logtext.write(f"selsquare: {squarenames[selsquare]}\n")
        else:
            logtext.write("No selection")
    return oldmoves



# Main
openlog()
while running:
    if gamestate == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif keycheck(event) == "ESC":
                running = False
            elif keycheck(event) == "Debug":
                debugrender = not debugrender
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and winner == None:
                if gamemode == 1 and not blackturn:
                    cpumove()
                elif gamemode == 2:
                    cpumove()
                else:
                    click()
            oldmoves = debuglog(oldmoves)
        kingcheck()
        if postforceplay == False:
            force = forcecheck(blackturn)
        findmoves(blackturn)
        availabilitycheck(selsquare)
        winner = wincheck(blackturn)
        render(screen,gamestate,debugrender,font,squarelist,selsquare,forcelist,movelist,winner,blackturn,lastmove,gamecolor)
        if IG_Quit.draw(screen) == True:
            gamestate = 0
            gamescreen = 0
    elif gamestate == 0:
        render(screen,gamestate,debugrender,font,squarelist,selsquare,forcelist,movelist,winner,blackturn,lastmove,gamecolor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                menuclick = True
            else:
                menuclick = False
        if gamescreen == 0:
            if MM_Play.draw(screen) == True and menuclick:
                blackturn, lastmove, postforceplay, force, moves, debugrender, winner = setgame()
                gamestate = 1
                gamescreen = 0
            if MM_Settings.draw(screen) == True and menuclick:
                menuclick = False
                gamescreen = 1
            if MM_Quit.draw(screen) == True and menuclick:
                menuclick = False
                running = False
        elif gamescreen == 1:
            if gamemode == 0:
                if SET_PvP.draw(screen) == True and menuclick:
                    gamemode = 1
                    menuclick = False
            elif gamemode == 1:
                if SET_PvC.draw(screen) == True and menuclick:
                    gamemode = 2
                    menuclick = False
            elif gamemode == 2:
                if SET_CvC.draw(screen) == True and menuclick:
                    gamemode = 0
                    menuclick = False
            if gamecolor == 0:
                if SET_Col0_Sel.draw(screen) == True and menuclick:
                    gamecolor = 0
                    menuclick = False
                elif SET_Col1.draw(screen) == True and menuclick:
                    gamecolor = 1
                    menuclick = False
                elif SET_Col2.draw(screen) == True and menuclick:
                    gamecolor = 2
                    menuclick = False
            elif gamecolor == 1:
                if SET_Col0.draw(screen) == True and menuclick:
                    gamecolor = 0
                    menuclick = False
                elif SET_Col1_Sel.draw(screen) == True and menuclick:
                    gamecolor = 1
                    menuclick = False
                elif SET_Col2.draw(screen) == True and menuclick:
                    gamecolor = 2
                    menuclick = False
            elif gamecolor == 2:
                if SET_Col0.draw(screen) == True and menuclick:
                    gamecolor = 0
                    menuclick = False
                elif SET_Col1.draw(screen) == True and menuclick:
                    gamecolor = 1
                    menuclick = False
                elif SET_Col2_Sel.draw(screen) == True and menuclick:
                    gamecolor = 2
                    menuclick = False
            if SET_Back.draw(screen) == True and menuclick:
                gamescreen = 0
                menuclick = False
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit