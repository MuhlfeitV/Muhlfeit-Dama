import pygame
from math import floor
import colors
import datetime

logtext = open('log.txt', 'w')

# Settings

FPS = 60
pygame.display.set_caption("Průjem")
blackturn = True
penis = False
force = False
moves = 0
debugrender = False

# Usable squares

class Square:

    def __init__(self, xcoordinate, ycoordinate, piececolor, type, available, link, jump):
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.piececolor = piececolor
        self.type = type
        self.available = available
        self.link = link # In case of forced move, the square which the selected piece jumps to
        self.jump = jump # In case of forced move, the square containing the piece which gets jumped over and removed by the selected piece

a1 = Square(0,7,1,1,0,None,None)
a3 = Square(2,7,1,1,0,None,None)
a5 = Square(4,7,1,1,0,None,None)
a7 = Square(6,7,1,1,0,None,None)
b2 = Square(1,6,1,1,0,None,None)
b4 = Square(3,6,1,1,0,None,None)
b6 = Square(5,6,1,1,0,None,None)
b8 = Square(7,6,1,1,0,None,None)
c1 = Square(0,5,1,1,0,None,None)
c3 = Square(2,5,1,1,0,None,None)
c5 = Square(4,5,1,1,0,None,None)
c7 = Square(6,5,1,1,0,None,None)
d2 = Square(1,4,0,0,0,None,None)
d4 = Square(3,4,0,0,0,None,None)
d6 = Square(5,4,0,0,0,None,None)
d8 = Square(7,4,0,0,0,None,None)
e1 = Square(0,3,0,0,0,None,None)
e3 = Square(2,3,0,0,0,None,None)
e5 = Square(4,3,0,0,0,None,None)
e7 = Square(6,3,0,0,0,None,None)
f2 = Square(1,2,2,1,0,None,None)
f4 = Square(3,2,2,1,0,None,None)
f6 = Square(5,2,2,1,0,None,None)
f8 = Square(7,2,2,1,0,None,None)
g1 = Square(0,1,2,1,0,None,None)
g3 = Square(2,1,2,1,0,None,None)
g5 = Square(4,1,2,1,0,None,None)
g7 = Square(6,1,2,1,0,None,None)
h2 = Square(1,0,2,1,0,None,None)
h4 = Square(3,0,2,1,0,None,None)
h6 = Square(5,0,2,1,0,None,None)
h8 = Square(7,0,2,1,0,None,None)

squarelist = [a1,a3,a5,a7,b2,b4,b6,b8,c1,c3,c5,c7,d2,d4,d6,d8,e1,e3,e5,e7,f2,f4,f6,f8,g1,g3,g5,g7,h2,h4,h6,h8]

selsquare = None
is_selected = False
oldss = None

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
                                            squarelist[c].available = 2
                                            squarelist[a].jump = b
                                            squarelist[a].link = c
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
                                                squarelist[c].available = 2
                                                squarelist[a].jump = b
                                                squarelist[a].link = c
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
                                                squarelist[c].available = 2
                                                squarelist[a].jump = b
                                                squarelist[a].link = c
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



def click(selsquare,is_selected,blackturn,m):
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
                    return a,True,blackturn,m
                else:
                    return None,False,blackturn,m
            elif is_selected == True:
                if force:
                  if squarelist[int(selsquare)].link == a:
                    squarelist[a].piececolor,squarelist[a].type,squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type = squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type,squarelist[a].piececolor,squarelist[a].type
                    squarelist[int(squarelist[int(selsquare)].jump)].type = 0
                    squarelist[int(squarelist[int(selsquare)].jump)].piececolor = 0
                    m += 1
                    for x in range(len(squarelist)):
                        squarelist[x].available = 0
                    squarelist[int(selsquare)].link = None
                    squarelist[int(selsquare)].jump = None
                    if forcecheck(a) == True:
                        return None,False,blackturn,m
                    else:
                        return None,False,not blackturn,m
                  else:
                    return None,False,blackturn,m
                elif squarelist[a].available == 1:
                    squarelist[a].piececolor,squarelist[a].type,squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type = squarelist[int(selsquare)].piececolor,squarelist[int(selsquare)].type,squarelist[a].piececolor,squarelist[a].type
                    m += 1
                    return None,False,not blackturn,m
                else: 
                    return None,False,blackturn,m
            break
    if found == False:
        return selsquare,is_selected,blackturn,m
                    


def keycheck(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "ESC"
        elif event.key == pygame.K_p:
            return "Penis"
        elif event.key == pygame.K_d:
            return "Debug"
    else: 
        return False
        


def debuglog(oldss):
    if selsquare != oldss:
        oldss = selsquare
        logtext.write("\n")
        logtext.write(f"Moves completed: {moves}\n")
        squarenames = ["a1","a3","a5","a7","b2","b4","b6","b8","c1","c3","c5","c7","d2","d4","d6","d8","e1","e3","e5","e7","f2","f4","f6","f8","g1","g3","g5","g7","h2","h4","h6","h8"]
        for a in range(len(squarelist)):
            if squarelist[a].link != None:
                logtext.write(f"{squarenames[a]}: Piececolor {squarelist[a].piececolor} | Type {squarelist[a].type} | Available {squarelist[a].available} | Link {squarenames[squarelist[a].link]} | Jump {squarenames[squarelist[a].jump]}\n")
            else:
                logtext.write(f"{squarenames[a]}: Piececolor {squarelist[a].piececolor} | Type {squarelist[a].type} | Available {squarelist[a].available} | Link {squarelist[a].link} | Jump {squarelist[a].jump}\n")
        if is_selected:
            logtext.write(f"selsquare: {squarenames[selsquare]}\n")
        else:
            logtext.write("No selection")
    return oldss

# Render screen

def render():
    screen.fill("black")
    pygame.draw.rect(screen, colors.LSPACE, (0, 0, 800, 800))
    for row in range(0,8):
        for column in range(0,8):
            if (row + column) % 2 != 0:
                pygame.draw.rect(screen, colors.DSPACE, (row*100, column*100, 100, 100))
    if penis == False:
        if debugrender:
            for a in range(len(squarelist)):
                snum = font.render(str(a), True, colors.WPIECE)
                prop0 = font.render(str(squarelist[a].piececolor), True, colors.DEBUG0)
                prop1 = font.render(str(squarelist[a].type), True, colors.DEBUG1)
                prop2 = font.render(str(squarelist[a].available), True, colors.DEBUG2)
                prop3 = font.render(str(squarelist[a].link), True, colors.DEBUG3)
                prop4 = font.render(str(squarelist[a].jump), True, colors.DEBUG4)
                propss = font.render(f"selsquare = {str(selsquare)}", True, colors.WPIECE)
                trn = snum.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+20))
                tr0 = prop0.get_rect(topleft=(squarelist[a].xcoordinate*100+25,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+45,squarelist[a].ycoordinate*100+20))
                tr1 = prop1.get_rect(topleft=(squarelist[a].xcoordinate*100+50,squarelist[a].ycoordinate*100),bottomright=(squarelist[a].xcoordinate*100+70,squarelist[a].ycoordinate*100+20))
                tr2 = prop2.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100+30),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+50))
                tr3 = prop3.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100+55),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+75))
                tr4 = prop4.get_rect(topleft=(squarelist[a].xcoordinate*100,squarelist[a].ycoordinate*100+80),bottomright=(squarelist[a].xcoordinate*100+20,squarelist[a].ycoordinate*100+100))
                trss = propss.get_rect(center=(1000,200))
                screen.blit(snum,trn)
                screen.blit(prop0,tr0)
                screen.blit(prop1,tr1)
                screen.blit(prop2,tr2)
                screen.blit(prop3,tr3)
                screen.blit(prop4,tr4)
                screen.blit(propss,trss)
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
    else:
        pygame.draw.rect(screen, colors.BPIECE, (300, 300, 200, 300))
        pygame.draw.circle(screen, colors.BPIECE, (400, 300), 100)
        pygame.draw.circle(screen, colors.BPIECE, (300, 600), 100)
        pygame.draw.circle(screen, colors.BPIECE, (500, 600), 100)
    if penis:
        text = font.render("Penis", True, colors.WPIECE)
    elif blackturn == True:
        text = font.render("Black's turn!", True, colors.WPIECE)
    else:
        text = font.render("White's turn!", True, colors.WPIECE)
    text_rect = text.get_rect(center=(1000,50))
    screen.blit(text, text_rect)


# Main
openlog()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif keycheck(event) == "ESC":
            running = False
        elif keycheck(event) == "Penis":
            penis = not penis
        elif keycheck(event) == "Debug":
            debugrender = not debugrender
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            selsquare,is_selected,blackturn,moves = click(selsquare,is_selected,blackturn,moves)
            if force == False:
                availabilitycheck(selsquare, is_selected, blackturn)
        kingcheck()
        oldss = debuglog(oldss)
    force = forcecheck(blackturn)
    render()

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit