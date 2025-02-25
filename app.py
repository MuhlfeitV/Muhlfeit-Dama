import pygame
from math import floor
import assets
import colors
import datetime

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

class Button:
    
    def __init__(self, asset, asset_h, x, y):
        self.img = asset
        self.img_h = asset_h
        self.rect = self.img.get_rect()
        self.rect_H = self.img_h.get_rect()
        self.rect.topleft = (x, y)
        self.rect_H.topleft = (x, y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            screen.blit(self.img_h, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.img, (self.rect.x, self.rect.y))

MM_Play = Button(assets.Play, assets.Play_H, 500, 300)
MM_Quit = Button(assets.Quit, assets.Quit_H, 500, 500)
IG_Menu = Button(assets.Quit, assets.Quit_H, 900, 600)

# Usable squares

class Square:

    def __init__(self, xcoordinate, ycoordinate, piececolor, type, available):
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.piececolor = piececolor # 1 = black, 2 = white
        self.type = type
        self.available = available

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
    e = datetime.datetime.now()
    L = [e.strftime("%Y-%m-%d %H:%M:%S"), 
         e.strftime("%d/%m/%Y"), 
         e.strftime("%I:%M:%S %p"), 
         e.strftime("%a, %b %d, %Y")
         ]
    logtext.write("\n")
    logtext.write("--------------\n")
    logtext.write(f"{L}\n")



def forcecheck(blackturn):
    forcelist.clear()
    x = 0
    if blackturn:
        clr = 1
    else:
        clr = 2
    for a in range(len(squarelist)):
        if squarelist[a].piececolor == clr:
                for b in range(len(squarelist)):
                    if squarelist[b].piececolor != 0 and squarelist[b].piececolor != clr:
                        if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                            if squarelist[a].type == 2:
                                if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                                    for c in range(len(squarelist)):
                                        if (
                                            (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                            (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                            (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                            (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                            squarelist[c].piececolor == 0
                                            ):
                                            forcelist.append(a)
                                            forcelist.append(b)
                                            forcelist.append(c)
                                            squarelist[c].available = 2
                                            x = 1
                            else:
                                if blackturn:
                                    if squarelist[a].ycoordinate-squarelist[b].ycoordinate == 1:
                                        for c in range(len(squarelist)):
                                            if (
                                            (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                            (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                            (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                            (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                            squarelist[c].piececolor == 0
                                            ):
                                                forcelist.append(a)
                                                forcelist.append(b)
                                                forcelist.append(c)
                                                squarelist[c].available = 2
                                                x = 1
                                else:
                                    if squarelist[a].ycoordinate-squarelist[b].ycoordinate == -1:
                                        for c in range(len(squarelist)):
                                            if (
                                            (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                            (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                            (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                            (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                            squarelist[c].piececolor == 0
                                            ):
                                                forcelist.append(a)
                                                forcelist.append(b)
                                                forcelist.append(c)
                                                squarelist[c].available = 2
                                                x = 1
    if x == 1:
        return True
    else:
        return False



def postforce(a,blackturn):
    forcelist.clear()
    x = 0
    if blackturn:
        clr = 1
    else:
        clr = 2
    for b in range(len(squarelist)):
        if squarelist[b].piececolor != 0 and squarelist[b].piececolor != clr:
            if abs(squarelist[a].xcoordinate-squarelist[b].xcoordinate) == 1:
                if squarelist[a].type == 2:
                    if abs(squarelist[a].ycoordinate-squarelist[b].ycoordinate) == 1:
                        for c in range(len(squarelist)):
                            if (
                                (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                squarelist[c].piececolor == 0
                                ):
                                forcelist.append(a)
                                forcelist.append(b)
                                forcelist.append(c)
                                squarelist[c].available = 2
                                x = 1
                else:
                    if blackturn:
                        if squarelist[a].ycoordinate-squarelist[b].ycoordinate == 1:
                            for c in range(len(squarelist)):
                                if (
                                (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                squarelist[c].piececolor == 0
                                ):
                                    forcelist.append(a)
                                    forcelist.append(b)
                                    forcelist.append(c)
                                    squarelist[c].available = 2
                                    x = 1
                    else:
                        if squarelist[a].ycoordinate-squarelist[b].ycoordinate == -1:
                            for c in range(len(squarelist)):
                                if (
                                (squarelist[a].xcoordinate-squarelist[b].xcoordinate)*2==squarelist[a].xcoordinate-squarelist[c].xcoordinate and
                                (squarelist[a].ycoordinate-squarelist[b].ycoordinate)*2==squarelist[a].ycoordinate-squarelist[c].ycoordinate and
                                (squarelist[a].xcoordinate-squarelist[c].xcoordinate)!=0 and
                                (squarelist[a].ycoordinate-squarelist[c].ycoordinate)!=0 and
                                squarelist[c].piececolor == 0
                                ):
                                    forcelist.append(a)
                                    forcelist.append(b)
                                    forcelist.append(c)
                                    squarelist[c].available = 2
                                    x = 1
    if x == 1:
        return True
    else:
        return False
            


def availabilitycheck(selsquare, is_selected, blackturn):
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
    for a in range(4):
        if squarelist[a].piececolor == 2:
            squarelist[a].type = 2
    for b in range(28,32,1):
        if squarelist[b].piececolor == 1:
            squarelist[b].type = 2



def click(selsquare,is_selected,blackturn,m,postforceplay,lastmove):
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

def render():
    screen.fill("black")
    if gamestate == 0:
        screen.blit(assets.Menu_BG, (assets.Menu_BG.get_rect().x, assets.Menu_BG.get_rect().y))
        screen.blit(assets.Title, (400,100))
    elif gamestate == 1:
        if winner != None:
            pygame.draw.rect(screen, colors.LSPACEWIN, (0, 0, 800, 800))
            for row in range(0,8):
                for column in range(0,8):
                    if (row + column) % 2 != 0:
                        pygame.draw.rect(screen, colors.DSPACEWIN, (row*100, column*100, 100, 100))    
        else:
            pygame.draw.rect(screen, colors.LSPACE, (0, 0, 800, 800))
            for row in range(0,8):
                for column in range(0,8):
                    if (row + column) % 2 != 0:
                        pygame.draw.rect(screen, colors.DSPACE, (row*100, column*100, 100, 100))
        if debugrender:
            propss = font.render(f"selsquare = {str(selsquare)}", True, colors.WPIECE)
            propfl = font.render(f"forcelist = {str(forcelist)}", True, colors.WPIECE)
            trss = propss.get_rect(center=(1000,200))
            trfl = propss.get_rect(center=(1000,300))
            screen.blit(propss,trss)
            screen.blit(propfl,trfl)
            for a in range(len(squarelist)):
                snum = font.render(str(a), True, colors.WPIECE)
                prop0 = font.render(str(squarelist[a].piececolor), True, colors.DEBUG0)
                prop1 = font.render(str(squarelist[a].type), True, colors.DEBUG1)
                prop2 = font.render(str(squarelist[a].available), True, colors.DEBUG2)
                trn = snum.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+20))
                tr0 = prop0.get_rect(topleft=(squarelist[a].xcoordinate*100+25,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+45,squarelist[a].ycoordinate*100+20))
                tr1 = prop1.get_rect(topleft=(squarelist[a].xcoordinate*100+50,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+70,squarelist[a].ycoordinate*100+20))
                tr2 = prop2.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100+30),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+50))
                screen.blit(snum,trn)
                screen.blit(prop0,tr0)
                screen.blit(prop1,tr1)
                screen.blit(prop2,tr2)
        else:
            for a in range(len(squarelist)):
                x = squarelist[a]
                if x.available == 2:
                    pygame.draw.rect(screen, colors.FORCED, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                if selsquare != None:
                    if x.available == 1:
                        pygame.draw.rect(screen, colors.CANSEL, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                    if x == squarelist[selsquare]:
                        pygame.draw.rect(screen, colors.SELECT, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                if x.piececolor == 1:
                    pygame.draw.circle(screen, colors.BPIECE, (x.xcoordinate*100+50, x.ycoordinate*100+50), 40)
                if x.piececolor == 2:
                    pygame.draw.circle(screen, colors.WPIECE, (x.xcoordinate*100+50, x.ycoordinate*100+50), 40)
                if x.type == 2:
                    pygame.draw.circle(screen, colors.KING, (x.xcoordinate*100+50, x.ycoordinate*100+50), 30)
        if winner == 1:
            text = font.render("Black wins!", True, colors.WPIECE)
        elif winner == 2:
            text = font.render("White wins!", True, colors.WPIECE)
        elif blackturn == True:
            text = font.render("Black's turn!", True, colors.WPIECE)
        else:
            text = font.render("White's turn!", True, colors.WPIECE)
        text_rect = text.get_rect(center=(1000,50))
        screen.blit(text, text_rect)


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
        render()
        if IG_Menu.draw() == True:
            gamestate = 0
    elif gamestate == 0:
        render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if MM_Play.draw() == True:
            gamestate = 1
        if MM_Quit.draw() == True:
            running = False

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit