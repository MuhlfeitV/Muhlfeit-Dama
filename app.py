import pygame
from math import floor
import assets
import colors
import datetime
from square import *
from button import *
from render import *

logtext = open('log.txt', 'w')

# Settings

FPS = 60
pygame.display.set_caption("Checkers")
blackturn = True
lastmove = None
postforceplay = False
force = False
moves = 0
debugrender = False
winner = None

# Game States

gamestate = 0
pendingstate = None # For the yes/no box

# 0 Main Menu
# 1 Game PVP
# 2 Game PVCOM

# Buttons

MM_Play = Button(assets.Play, assets.Play_H, 500, 300)
MM_Quit = Button(assets.Quit, assets.Quit_H, 500, 500)
IG_Menu = Button(assets.Quit, assets.Quit_H, 900, 600)

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
    return True, None, False, False, 0, False, None

squarelist = [a1,a3,a5,a7,b2,b4,b6,b8,c1,c3,c5,c7,d2,d4,d6,d8,e1,e3,e5,e7,f2,f4,f6,f8,g1,g3,g5,g7,h2,h4,h6,h8]

selsquare = None
is_selected = False
oldss = None
forcelist = []

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
    squarelist[c].available = 2
    return True



def postforce(a: int, blackturn: bool) -> bool:
    """Check for continuations of a chain of forced moves which the player whose turn it is must choose from. Only checks for piece which has just been moved by the player. Looks for squares with pieces of the opposite colour (index b in squarelist) using function "force_findb(blackturn, force_found, clr, a)."""
    forcelist.clear()
    force_found = 0
    if blackturn:
        clr = 1
    else:
        clr = 2
    force_found = force_findb(blackturn, force_found, clr, a)
    if force_found == True:
        return True
    else:
        return False
            


def availabilitycheck(selsquare: int, is_selected: bool, blackturn: bool):
    """Checks for possible moves of selected piece"""
    for a in range(len(squarelist)):
        if is_selected == False:
            squarelist[a].available = 0
        elif squarelist[a].type != 0:
            continue
        else:
            if blackturn:
                if abs(squarelist[a].xcoordinate-squarelist[selsquare].xcoordinate) == 1:
                    if squarelist[selsquare].type == 2:
                        if abs(squarelist[a].ycoordinate-squarelist[selsquare].ycoordinate) == 1:
                            squarelist[a].available = 1
                            continue
                    else:
                        if (squarelist[a].ycoordinate-squarelist[selsquare].ycoordinate) == -1:
                            squarelist[a].available = 1
                            continue
            else:
                if abs(squarelist[a].xcoordinate-squarelist[selsquare].xcoordinate) == 1:
                    if squarelist[selsquare].type == 2:
                        if abs(squarelist[a].ycoordinate-squarelist[selsquare].ycoordinate) == 1:
                            squarelist[a].available = 1
                            continue
                    else:
                        if (squarelist[a].ycoordinate-squarelist[selsquare].ycoordinate) == 1:
                            squarelist[a].available = 1
                            continue



def kingcheck():
    """Checks for pieces which have reached the last row of the opposite side. If an uncrowned piece is found, it becomes a king."""
    for a in range(4):
        if squarelist[a].piececolor == 2:
            squarelist[a].type = 2
    for b in range(28,32,1):
        if squarelist[b].piececolor == 1:
            squarelist[b].type = 2



def click(selsquare: int, is_selected: bool, blackturn: bool, m: int, postforceplay: bool, lastmove: int):
    """Detects which square the user clicks on."""
    print(f"blackturn = {blackturn}")
    if blackturn == True:
        clr = 1
    else:
        clr = 2
    found = False
    print("click")
    print(f"selsquare {selsquare}")
    print(f"is selected {is_selected}")
    mousex, mousey = pygame.mouse.get_pos()
    fieldx, fieldy = floor(mousex/100),floor(mousey/100)
    for a in range(len(squarelist)):
        if squarelist[a].xcoordinate == fieldx and squarelist[a].ycoordinate == fieldy:
            found = True
            if is_selected == False:
                if squarelist[a].piececolor == clr:
                    return a,True,blackturn,m,postforceplay,lastmove
                else:
                    return None,False,blackturn,m,postforceplay,lastmove
            elif is_selected == True:
                if force or postforceplay:
                    print(len(forcelist)/3)
                    for f in range(int(len(forcelist)/3)):
                        if forcelist[f*3] == selsquare and forcelist[f*3+2] == a:
                            squarelist[a].piececolor,squarelist[a].type,squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type = squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type,squarelist[a].piececolor,squarelist[a].type
                            squarelist[forcelist[f*3+1]].type,squarelist[forcelist[f*3+1]].piececolor = 0,0
                            m += 1
                            kingcheck()
                            for x in range(len(squarelist)):
                                squarelist[x].available = 0
                            if postforce(a,blackturn) == True:
                                return None,False,blackturn,m,True,a
                            else:
                                return None,False,not blackturn,m,False,lastmove
                        else:
                            continue
                    return None,False,blackturn,m,postforceplay,lastmove
                elif squarelist[a].available == 1:
                    squarelist[a].piececolor,squarelist[a].type,squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type = squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type,squarelist[a].piececolor,squarelist[a].type
                    m += 1
                    kingcheck()
                    return None,False,not blackturn,m,postforceplay,lastmove
                else:
                    if squarelist[a].piececolor == clr:
                        for f in range(len(squarelist)):
                            squarelist[f].available = 0
                        return a,True,blackturn,m,postforceplay,lastmove
                    else:
                        return None,False,blackturn,m,postforceplay,lastmove
            break
    if found == False:
        return None,False,blackturn,m,postforceplay,lastmove
                    


def menuclick():
    mousex, mousey = pygame.mouse.get_pos()
    if mousex > 400 and mousex < 800 and mousey > 300 and mousey < 400:
        return "SC_0"
    elif mousex > 400 and mousex < 800 and mousey > 500 and mousey < 600:
        return "QUIT"


def keycheck(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "ESC"
        elif event.key == pygame.K_d:
            return "Debug"
    else: 
        return False
    


def wincheck(blackturn):
    validmoves = 0
    if force == True:
        return None
    elif blackturn == True:
        for a in range(len(squarelist)):
            if squarelist[a].piececolor == 1:
                for b in range(len(squarelist)):
                    if squarelist[b].type == 0:
                        if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                            if squarelist[a].type == 2:
                                if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                                    validmoves += 1
                                else: continue
                            else:
                                if squarelist[a].ycoordinate-squarelist[b].ycoordinate == 1:
                                    validmoves +=1
                                else: continue
                        else: continue
                    else: continue
            else: continue
        if validmoves == 0:
            return 2
        else:
            return None
    elif blackturn == False:
        for a in range(len(squarelist)):
            if squarelist[a].piececolor == 2:
                for b in range(len(squarelist)):
                    if squarelist[b].type == 0:
                        if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                            if squarelist[a].type == 2:
                                if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                                    validmoves += 1
                                else: continue
                            else:
                                if squarelist[b].ycoordinate-squarelist[a].ycoordinate == 1:
                                    validmoves += 1
                                else: continue
                        else: continue
                    else: continue
            else: continue
        if validmoves == 0:
            return 1
        else:
            return None




def debuglog(oldss):
    if selsquare != oldss:
        oldss = selsquare
        logtext.write("\n")
        logtext.write(f"Moves completed: {moves}\n")
        squarenames = ["a1","a3","a5","a7","b2","b4","b6","b8","c1","c3","c5","c7","d2","d4","d6","d8","e1","e3","e5","e7","f2","f4","f6","f8","g1","g3","g5","g7","h2","h4","h6","h8"]
        for a in range(len(squarelist)):
            logtext.write(f"{squarenames[a]}: Piececolor {squarelist[a].piececolor} | Type {squarelist[a].type} | Available {squarelist[a].available}\n")
        if is_selected:
            logtext.write(f"selsquare: {squarenames[selsquare]}\n")
        else:
            logtext.write("No selection")
    return oldss

# Render screen



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
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if winner == None:
                    selsquare,is_selected,blackturn,moves,postforceplay,lastmove = click(selsquare,is_selected,blackturn,moves,postforceplay,lastmove)
                    if force == False:
                        availabilitycheck(selsquare, is_selected, blackturn)
            oldss = debuglog(oldss)
        if postforceplay == False:
            force = forcecheck(blackturn)
        else:
            postforceplay = postforce(lastmove,blackturn)
        winner = wincheck(blackturn)
        render(screen,gamestate,debugrender,font,squarelist,selsquare,forcelist,winner,blackturn)
        if IG_Menu.draw(screen) == True:
            gamestate = 0
    elif gamestate == 0:
        render(screen,gamestate,debugrender,font,squarelist,selsquare,forcelist,winner,blackturn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if MM_Play.draw(screen) == True:
            blackturn, lastmove, postforceplay, force, moves, debugrender, winner = setgame()
            gamestate = 1
        if MM_Quit.draw(screen) == True:
            running = False

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit