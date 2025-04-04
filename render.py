import pygame
import colors
import assets

def render(screen,gamestate,debugrender,font,squarelist,selsquare,forcelist,movelist,winner,blackturn,lastmove,gamecolor):
    if gamecolor == 0:
        colors.Dspace = colors.DSPACE_0
        colors.Lspace = colors.LSPACE_0
        colors.Bpiece = colors.BPIECE_0
        colors.Select = colors.SELECT_0
        colors.Cansel = colors.CANSEL_0
        colors.Forced = colors.FORCED_0
    elif gamecolor == 1:
        colors.Dspace = colors.DSPACE_1
        colors.Lspace = colors.LSPACE_1
        colors.Bpiece = colors.BPIECE_1
        colors.Select = colors.SELECT_1
        colors.Cansel = colors.CANSEL_1
        colors.Forced = colors.FORCED_1
    elif gamecolor == 2:
        colors.Dspace = colors.DSPACE_2
        colors.Lspace = colors.LSPACE_2
        colors.Bpiece = colors.BPIECE_2
        colors.Select = colors.SELECT_2
        colors.Cansel = colors.CANSEL_2
        colors.Forced = colors.FORCED_2
    screen.fill("black")
    if gamestate == 0:
        screen.blit(assets.Menu_BG, (assets.Menu_BG.get_rect().x, assets.Menu_BG.get_rect().y))
        screen.blit(assets.Title, (400,100))
    elif gamestate == 1:
        screen.blit(assets.Blackturn, (800,0))
        if winner != None:
            pygame.draw.rect(screen, colors.LSPACEWIN, (0, 0, 800, 800))
            for row in range(0,8):
                for column in range(0,8):
                    if (row + column) % 2 != 0:
                        pygame.draw.rect(screen, colors.DSPACEWIN, (row*100, column*100, 100, 100))    
        else:
            pygame.draw.rect(screen, colors.Lspace, (0, 0, 800, 800))
            for row in range(0,8):
                for column in range(0,8):
                    if (row + column) % 2 != 0:
                        pygame.draw.rect(screen, colors.Dspace, (row*100, column*100, 100, 100))
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
                if len(lastmove) != 0:
                    if a == lastmove[0] or a == lastmove[1]:
                        pygame.draw.rect(screen, colors.LASTMOVE, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                if x.available == 2:
                    pygame.draw.rect(screen, colors.Forced, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                if selsquare != None:
                    if x.available == 1:
                        pygame.draw.rect(screen, colors.Cansel, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                    if x == squarelist[selsquare]:
                        pygame.draw.rect(screen, colors.Select, (x.xcoordinate*100, x.ycoordinate*100, 100, 100))
                if x.piececolor == 1:
                    pygame.draw.circle(screen, colors.Bpiece, (x.xcoordinate*100+50, x.ycoordinate*100+50), 40)
                if x.piececolor == 2:
                    pygame.draw.circle(screen, colors.WPIECE, (x.xcoordinate*100+50, x.ycoordinate*100+50), 40)
                if x.type == 2:
                    pygame.draw.circle(screen, colors.KING, (x.xcoordinate*100+50, x.ycoordinate*100+50), 30)
                for move in range(int(len(movelist)/2)):
                    if a == movelist[move*2]:
                        pygame.draw.rect(screen, colors.Select, (x.xcoordinate*100, x.ycoordinate*100, 100, 100), 5)
        if winner == 1:
            screen.blit(assets.Blackwin, (800,0))
            text = font.render("Black wins!", True, colors.WPIECE)
        elif winner == 2:
            screen.blit(assets.Whitewin, (800,0))
            text = font.render("White wins!", True, colors.WPIECE)
        elif blackturn == True:
            text = font.render("Black's turn!", True, colors.WPIECE)
        else:
            screen.blit(assets.Whiteturn, (800,0))
            text = font.render("White's turn!", True, colors.WPIECE)
        text_rect = text.get_rect(center=(1000,50))
        screen.blit(text, text_rect)