import pygame, sys, random
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
inf = pygame.display.Info()
tel_width = inf.current_w
tel_hight = inf.current_h
tela = pygame.display.set_mode((tel_width-100,tel_hight-100))

programIcon = pygame.image.load('nave.png')
programIcon = pygame.transform.scale(programIcon,(20,20))

pygame.display.set_icon(programIcon)
pygame.display.set_caption('Invaders °o°')

pygame.mixer.music.load('Juhani Junkala [Retro Game Music Pack] Level 3.wav')
disparo = pygame.mixer.Sound('shoot02wav-14562.wav')

# jogador -------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

class player(pygame.sprite.Sprite):
        def __init__(self,x,y,width,height,color,life,alive):
            super().__init__()
            self.alive = alive
            self.x = x
            self.y = y
            self.image = pygame.image.load('nave.png')
            self.image = pygame.transform.scale(self.image,(72,72))
            self.speed = 7
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.life = life
            self.mask = pygame.mask.from_surface(self.image)
        def show_life(self):
                for i in range(self.life):
                        pygame.draw.rect(tela,(220,25,200),(self.rect.x+20+12*i,self.rect.y+70,10,10))        

# Inimigos ------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
class enemy(pygame.sprite.Sprite):
        
        def __init__(self,x,y,speed,sprite_inimigo,shoot_count_down,life):
                
                super().__init__()
                self.image = pygame.image.load(sprite_inimigo)
                self.image = pygame.transform.scale(self.image,(72,72))
                self.image = pygame.transform.rotate(self.image,180)
                self.x = x
                self.y = y
                self.rect = self.image.get_rect(topleft = (self.x,self.y))
                self.speed = speed
                self.shoot_count_down = shoot_count_down
                self.life = life
                self.mask = pygame.mask.from_surface(self.image)

        def mov(self):
            global hive_mind_turning
            self.rect.x += self.speed
            if self.rect.x+72>=tel_width-100 or self.rect.x <= 0 or hive_mind_turning == True:
                    self.speed *= -1

        def shot(self):
                if self.shoot_count_down == 0:
                    projetil_enemy = enemy_bullet((self.rect.x+36),(self.rect.y+40),5)
                    projetil_enemy.update()
                    projeteis_enemy.add(projetil_enemy)
                    self.shoot_count_down = random.randint(50,500)
                else:
                    self.shoot_count_down -=1
        def show_life(self):
                global enemy_count
                for i in range(self.life):
                        pygame.draw.rect(tela,(12,255,50),(self.rect.x+i*12,self.rect.y-7,10,10))
                        enemy_count += 1

def thinking(group,think):
            global hive_mind_turning
            if think == 0:
                pass
            elif think == 1:
                if hive_mind_turning == True:
                    pass
                else:
                    for i in group:
                        if i.rect.x+72+i.speed>=tel_width-100 or i.rect.x+i.speed <= 0:
                            hive_mind_turning = True
                            pass

# tiro --------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
class bullet(pygame.sprite.Sprite):

        def __init__(self,x,y,speed):

                super().__init__()
                self.image = pygame.image.load('bullet_player.png')
                self.image = pygame.transform.scale(self.image,(16,36))
                self.x = x
                self.y = y
                self.rect = self.image.get_rect(center = (self.x,self.y))
                self.speed = speed
                self.mask = pygame.mask.from_surface(self.image)
                        
        def update(self):
                self.rect.y -= self.speed
                if self.rect.y <=-25:
                        self.kill()

# tiro do inimigo --------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
fonte_Titulo=pygame.font.Font('freesansbold.ttf',32)
pontos=0
#show_points = "Points: " + str(pontos)
#pontuacao = fonte_Titulo.render(show_points,True,(0,255,0),(30,30,30))
#area_pont = pontuacao.get_rect()
#area_pont.center = (tel_width-250,tel_hight-150)

def point_count():
    global pontos
    word = str(pontos)
    show_points = "Points: " + word
    pontuacao = fonte_Titulo.render(show_points,True,(0,255,0),(30,30,30))
    area_pont = pontuacao.get_rect()
    area_pont.center = (tel_width-250,tel_hight-150)
    tela.blit(pontuacao,area_pont)

def to_kill(person, projectile):
    global pontos, damege_cool_down
    if pygame.Rect.colliderect(person.rect,projectile.rect):
            if pygame.sprite.collide_mask(person, projectile):
                projectile.kill()
                
                if type(person).__name__ == "player" and damege_cool_down <= 0:
                    damege_cool_down = 200
                    person.life -= 1
                if type(person).__name__ != "player":
                    person.life -= 1
                    
                if person.life == 0:
                        if jogador.life == 0:
                                jogador.alive = False
                                person.kill()
                        elif person.life == 0:
                                pontos += 10
                                person.kill()
                

def Death(A,K):
        for i in A:
                for j in K:
                        to_kill(i,j)
                        
class enemy_bullet(pygame.sprite.Sprite):

        def __init__(self,x,y,speed):

                super().__init__()
                self.image = pygame.image.load('bullet_player.png')
                self.image = pygame.transform.scale(self.image,(16,36))
                self.image = pygame.transform.rotate(self.image,180)
                self.x = x
                self.y = y
                self.rect = self.image.get_rect(center = (self.x,self.y))
                self.speed = speed
                self.mask = pygame.mask.from_surface(self.image)
                        
        def update(self):
                self.rect.y += self.speed
                if self.rect.y >= (tel_hight + 25):
                        self.kill()


                

# sair ------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
def sair():
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# pause -----------------------------------------------
cool_down_pause = 10
def pause():
        pygame.mixer.music.pause()
        global cool_down_pause
        cool_down_pause = 20
        pausado = True

        while pausado:

                tela.fill((0,0,0))

                selector.rect.midtop= pygame.mouse.get_pos()

                key = pygame.key.get_pressed()
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            


          
                
                if cool_down_pause > 0:
                        cool_down_pause -= 1

                if cool_down_pause <=0:
                        if key[pygame.K_p]:
                                pausado = False
                

                #tela.fill((0,0,0))
                tela.blit(background_normal,(0,0))
                    
                projeteis.draw(tela)

                projeteis_enemy.draw(tela)

                for i in inimigo_group_2:   
                        i.show_life()
                for i in inimigo_group_1:   
                        i.show_life()

                point_count()
                    
                jogadores.draw(tela)
                jogador.show_life()
                            
                inimigo_group_1.draw(tela)
                inimigo_group_2.draw(tela)
                        
                pygame.draw.rect(tela,(15,25,15),(int(tel_width/3),int(tel_hight/5),500,500))

                tela.blit(pauseLabel,(int(tel_width/2),int(tel_hight/3)))

                m_print.draw(tela)
                pygame.display.flip()

        pygame.mixer.music.unpause()
        cool_down_pause = 40
         
# controles --------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
cool_down = 100
damege_cool_down = 100
cool_down_pause = 0
def moviment():
    global cool_down,damege_cool_down,cool_down_pause

    if damege_cool_down >0:
        damege_cool_down -= 1

    tecla = pygame.key.get_pressed()
    
    if tecla[pygame.K_LEFT] and jogador.rect.x >= 0:
            jogador.rect.x-=jogador.speed

    if tecla[pygame.K_RIGHT] and jogador.rect.x <= tel_width-72:
        jogador.rect.x+=jogador.speed
        
    if tecla[pygame.K_z]:
        jogador.speed = 15
        
    else:
        jogador.speed = 7
        
    if (tecla[pygame.K_x] and cool_down == 0) or tecla[pygame.K_a]:
            
            projetil = bullet((jogador.rect.x+36),(jogador.rect.y+40),17)
            projetil.update()
            projeteis.add(projetil)
            cool_down = 10
            pygame.mixer.Sound.play(disparo)
            
    elif cool_down > 0:
            cool_down -= 1

            
    if tecla[pygame.K_p] and cool_down_pause<=0:
            pause()
    elif cool_down_pause > 0:
            cool_down_pause -= 1
            
            
    
            
    
#defininfo jogador --------------------------------------------
jogador = player(100,(tel_hight-200),64,32,(255,0,0),3,True)
jogadores = pygame.sprite.Group()
jogadores.add(jogador)


#definindo inimigo e grupos --------------------------------------------
inimigo_group_1 = pygame.sprite.Group()
inimigo_group_2 = pygame.sprite.Group()

for i in range(0,5,1):
        inimigo_group_1.add(enemy((75+i*75),100,5,'enemy-1.png',50*(1.5+i),3))
for i in range(0,5,1):
        inimigo_group_2.add(enemy(75+i*75,250,8,'enemy-2.png',50*(1.5+i),1))



#definindo projeteis -------------------------------------------------
projeteis = pygame.sprite.Group()
projeteis_enemy = pygame.sprite.Group()
background_normal = pygame.image.load('space.png')

# mouse -------------------------------------------------------------------

class cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bullet_player.png')
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect =  self.image.get_rect()
        
m_print = pygame.sprite.Group()
selector = cursor()
m_print.add(selector)
pygame.mouse.set_visible(False)

# menu ----------------------------------------------------------------------
#-------------------------------------------------------------------------------------

fonte_Titulo=pygame.font.Font('freesansbold.ttf',32)
titulo_jogo = fonte_Titulo.render("Invaders",True,(0,255,0),(0,0,128))
controles = fonte_Titulo.render("Controles",True,(255,255,25),(128,0,128))
Scores = fonte_Titulo.render("Scores",True,(255,255,25),(128,0,128))
Creditos = fonte_Titulo.render("Creditos",True,(255,255,25),(128,0,128))
area_titulo = titulo_jogo.get_rect()
area_titulo.center = (tel_width/2,(tel_hight/4))
start_button_logo = fonte_Titulo.render("Start",True,(255,255,25),(128,0,128))
pauseLabel = fonte_Titulo.render("Pause",True,(255,255,25),(128,0,128))

class button():
    def __init__(self,text,x,y):
        self.text = fonte_Titulo.render(text,True,(255,255,25),(128,0,128))
        self.x = x
        self.y = y
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.blit(self.text,(0,0))
        self.rectangle = self.surface.get_rect()
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.rect = Rect(self.x-2,self.y-2,self.width+4, self.height+4)
        self.color_bg = (0,50,200)
    def on_click(self,event):
        funciona = False
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x,y):    
                self.color_bg = (255,0,0)
                if pygame.mouse.get_pressed()[0]:
                    funciona = True
            else:
                    self.color_bg = (0,50,200)
        return funciona
    def draw(self,x,y,pos):
        self.x = x
        self.y = y
        self.rectangle = self.surface.get_rect()
        if self.rectangle.collidepoint(pos):
            color_bg = (0,50,200)
        else:
            color_bg = (255,0,0)
        pygame.draw.rect(tela,color_bg,(self.x-2,self.y-2,self.width+4,self.height+4))
        tela.blit(self.surface,(x,y))

'''
def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
'''

starting = button("Start",(int(tel_width/8)*3),(int(tel_hight/16)*6))
Scores_button = button("Pontuações",int(tel_width/8)*3,int(tel_hight/16)*8)
creditos = button("Créditos",(int(tel_width/8)*3),int(tel_hight/16)*9)
controles = button("Controles",(int(tel_width/8)*3),int(tel_hight/16)*7)
retornar_menu = button("Voltar ao menu",(int(tel_width/8)*3),int(tel_hight/16)*13)

def Scores():
        pontos_salvos = open("pontos_salvos.txt", "r")
        score = fonte_Titulo.render(pontos_salvos.readline(),True,(255,200,255))
        in_score = True
        while in_score:
                tela.fill((0,0,0))
                selector.rect.center = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                 if retornar_menu.rect.collidepoint(selector.rect.midtop):
                                # if pygame.Rect.colliderect(Scores_button.rect,selector.rect):
                                         in_score = False            
                tela.blit(score,(int(tel_width/2), int(tel_hight/4)))
                
                pygame.draw.rect(tela,retornar_menu.color_bg,(retornar_menu.x-2,retornar_menu.y-2,retornar_menu.width+4, retornar_menu.height+4))
                tela.blit(retornar_menu.surface,(retornar_menu.x,retornar_menu.y))

                m_print.draw(tela)
                pygame.display.flip()

                
def controles_top():
        in_controles = True
        movimentos = open("Movimentos.txt", "r")
        mvmnts1 = fonte_Titulo.render(movimentos.readline(),True,(255,200,255))
        mvmnts2 = fonte_Titulo.render(movimentos.readline(),True,(255,200,255))
        mvmnts3 = fonte_Titulo.render(movimentos.readline(),True,(255,200,255))
        mvmnts4 = fonte_Titulo.render(movimentos.readline(),True,(255,200,255))
        mvmnts5 = fonte_Titulo.render(movimentos.readline(),True,(255,200,255))
        while in_controles:
                tela.fill((0,0,0))
                selector.rect.center = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
#                                 if (retornar_menu.x<selector.rect.x+selector.point<retornar_menu.x+retornar_menu.width) and (retornar_menu.y<selector.rect.y<retornar_menu.y+retornar_menu.height+25):
                                  if retornar_menu.rect.collidepoint(selector.rect.midtop):
                                         in_controles = False
                        
                        
                tela.blit(mvmnts1,(20, int(tel_hight/16)*4))
                tela.blit(mvmnts2,(20, int(tel_hight/16)*5))
                tela.blit(mvmnts3,(20, int(tel_hight/16)*6))
                tela.blit(mvmnts4,(20, int(tel_hight/16)*7))
                tela.blit(mvmnts5,(20, int(tel_hight/16)*8))
                

                
                pygame.draw.rect(tela,retornar_menu.color_bg,(retornar_menu.x-2,retornar_menu.y-2,retornar_menu.width+4, retornar_menu.height+4))
                tela.blit(retornar_menu.surface,((int(tel_width/8)*3),(int(tel_hight/16)*13)))


                m_print.draw(tela)
                pygame.display.flip()

def Credits():
    
        in_credits = True
        cred = open("Creditos.txt", "r")
        cr1 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr2 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr3 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr4 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr5 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr6 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        cr7 = fonte_Titulo.render(cred.readline(),True,(255,200,255))
        while in_credits:
                tela.fill((0,0,0))
                selector.rect.center = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                 if retornar_menu.rect.collidepoint(selector.rect.midtop):
                                         in_credits = False            
                tela.blit(cr1,(20, int(tel_hight/16)*4))
                tela.blit(cr2,(20, int(tel_hight/16)*5))
                tela.blit(cr3,(20, int(tel_hight/16)*6))
                tela.blit(cr4,(20, int(tel_hight/16)*7))
                tela.blit(cr5,(20, int(tel_hight/16)*8))
                tela.blit(cr6,(20, int(tel_hight/16)*9))
                tela.blit(cr7,(20, int(tel_hight/16)*10))


                pygame.draw.rect(tela,(255,0,0),(retornar_menu.x-2,retornar_menu.y-2,retornar_menu.width+4, retornar_menu.height+4))
                tela.blit(retornar_menu.surface,((int(tel_width/8)*3),(int(tel_hight/16)*13)))


                m_print.draw(tela)
                pygame.display.flip()

def reset():
    level = 0
    if not ganhou_jogo:
        jogador = player(100,(tel_hight-200),64,32,(255,0,0),3,True)
        jogadores.add(jogador)    
    jogador.rect.x = 100
    jogador.life = 3
    pontos = 0
    for i in inimigo_group_1:
        i.kill()
    for i in inimigo_group_2:
        i.kill()
    for i in projeteis_enemy:
        i.kill()
    for i in projeteis:
        i.kill()    

def menu():
        in_menu = True
        while in_menu:
                tela.fill((0,0,0))
                selector.rect.midtop= pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #if (starting.x<=selector.rect.x+selector.point<=starting.x+starting.width) and (starting.y<=selector.rect.y<=starting.y+starting.height+25):
                            if starting.rect.collidepoint(selector.rect.midtop):
                                in_menu = False
                                pygame.mixer.music.play(-1)
                            if Scores_button.rect.collidepoint(selector.rect.midtop):
                                Scores()
                            if creditos.rect.collidepoint(selector.rect.midtop):                                
                                Credits()
                            if controles.rect.collidepoint(selector.rect.midtop):
                                controles_top()


                tela.blit(titulo_jogo,area_titulo)

                #pygame.draw.rect(tela,(255,0,0),(starting.x-2,starting.y-2,starting.width+4, starting.height+4))
                #tela.blit(starting.surface,((int(tel_width/8)*3),(int(tel_hight/16)*6)))
                starting.draw(int(tel_width/8)*3,(int(tel_hight/16)*6),selector.rect.midtop)

                
                #pygame.draw.rect(tela,(255,0,0),(controles.x-2,controles.y-2,controles.width+4, controles.height+4))
                #tela.blit(controles.surface,(int(tel_width/8)*3,int(tel_hight/16)*7))
                controles.draw(int(tel_width/8)*3,int(tel_hight/16)*7,selector.rect.midtop)
                
                #pygame.draw.rect(tela,(255,0,0),(Scores_button.x-2,Scores_button.y-2,Scores_button.width+4, Scores_button.height+4))
                #tela.blit(Scores_button.surface,(int(tel_width/8)*3,int(tel_hight/16)*8))
                Scores_button.draw(int(tel_width/8)*3,int(tel_hight/16)*8,selector.rect.midtop)


                #pygame.draw.rect(tela,(255,0,0),(creditos.x-2,creditos.y-2,creditos.width+4, creditos.height+4))
                #tela.blit(creditos.surface,((int(tel_width/8)*3),int(tel_hight/16)*9))
                creditos.draw(int(tel_width/8)*3,int(tel_hight/16)*9,selector.rect.midtop)

                
                m_print.draw(tela)
                pygame.display.flip()
                

# GAME OVER / WIN ----------------------------------------------------------------------------
#-------------------------------------------------------------

fonte_Titulo=pygame.font.Font('freesansbold.ttf',32)
acabou = fonte_Titulo.render("Game over bro... ;(",True,(50,255,100),(0,0,128))
area_acabou = acabou.get_rect()
area_acabou.center = (int(tel_width/2),int(tel_hight/4))

ganhou = fonte_Titulo.render("YOU WIN :D",True,(250,50,250),(0,0,128))
area_ganhou = ganhou.get_rect()
area_ganhou.center = (int(tel_width/2),int(tel_hight/4))


def win(ganhou_jogo):
    global level, jogador, pontos, go_to_menu
    if level<=2:
        trocar_level(True)
        level +=1
    else:
        pygame.mixer.music.fadeout(1500)
        go_to_menu = False
        in_win_page = True
        while in_win_page:
            sair()
            tela.fill((0,0,0))
            if ganhou_jogo:
                    tela.blit(ganhou,area_ganhou)
            else:
                    tela.blit(acabou,area_acabou)
            selector.rect.midtop = pygame.mouse.get_pos()
           # buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if starting.rect.collidepoint(selector.rect.midtop):
                               in_win_page = False
                               level = 0
                               pygame.mixer.music.play(-1)
                               if not ganhou_jogo: 
                                       jogador = player(100,(tel_hight-200),64,32,(255,0,0),3,True)
                                       jogadores.add(jogador)    
                               jogador.rect.x = 100
                               jogador.life = 3
                               pontos = 0
                               for i in inimigo_group_1:
                                       i.kill()
                               for i in inimigo_group_2:
                                       i.kill()
                               for i in projeteis_enemy:
                                       i.kill()
                               for i in projeteis:
                                       i.kill()    
                        #if (Scores_button.x<selector.rect.x+selector.point<Scores_button.x+Scores_button.width) and (Scores_button.y<selector.rect.y<Scores_button.y+Scores_button.height+25):
                        if Scores_button.rect.collidepoint(selector.rect.midtop):
                               Scores()
                        #if (retornar_menu.x<selector.rect.x+selector.point<retornar_menu.x+retornar_menu.width) and (retornar_menu.y<selector.rect.y<retornar_menu.y+retornar_menu.height+25):
                        if retornar_menu.rect.collidepoint(selector.rect.midtop):
                               in_win_page = False
                               level = 0
                               pygame.mixer.music.stop()
                               if not ganhou_jogo: 
                                       jogador = player(100,(tel_hight-200),64,32,(255,0,0),3,True)
                                       jogadores.add(jogador)    
                               jogador.rect.x = 100
                               jogador.life = 3
                               pontos = 0
                               for i in inimigo_group_1:
                                       i.kill()
                               for i in inimigo_group_2:
                                       i.kill()
                               for i in projeteis_enemy:
                                       i.kill()
                               for i in projeteis:
                                       i.kill()   
                               go_to_menu = True
                        

            #pygame.draw.rect(tela,(255,0,0),(starting.x-2,starting.y-2,starting.width+4, starting.height+4))
            #tela.blit(starting.surface,((int(tel_width/8)*3),(int(tel_hight/16)*6)))
            starting.draw(int(tel_width/8)*3,int(tel_hight/16)*6,selector.rect.midtop)


            #pygame.draw.rect(tela,(255,0,0),(Scores_button.x-2,Scores_button.y-2,Scores_button.width+4, Scores_button.height+4))
            #tela.blit(Scores_button.surface,(int(tel_width/8)*3,int(tel_hight/16)*8))
            Scores_button.draw(int(tel_width/8)*3,int(tel_hight/16)*8,selector.rect.midtop)


            #pygame.draw.rect(tela,(255,0,0),(retornar_menu.x-2,retornar_menu.y-2,retornar_menu.width+4, retornar_menu.height+4))
            #tela.blit(retornar_menu.surface,((int(tel_width/8)*3),(int(tel_hight/16)*13)))
            retornar_menu.draw(int(tel_width/8)*3,int(tel_hight/16)*13,selector.rect.midtop)

            
            m_print.draw(tela)
            pygame.display.flip()
        

# recive levels ------------------------------------------------------
def trocar_level(trocar_level):
    global level, think_1, think_2
    if trocar_level:
        if level == 0:
                think_1 = 0
                think_2 = 0

                for i in range(0,5,1):
                        inimigo_group_1.add(enemy((75+i*75),100,5,'enemy-1.png',50*(1.5+i),3))
                for i in range(0,5,1):
                        inimigo_group_2.add(enemy(75+i*75,250,8,'enemy-2.png',50*(1.5+i),1))

        
        if level == 1:
            
            think_1 = 1
            think_2 = 0

            for i in range(0,10,1):
                inimigo_group_1.add(enemy((75+i*75),50,3,'enemy-1.png',50*(1.5+i),3))
        
            for i in range(0,5,1):
                inimigo_group_2.add(enemy(75+i*75,200,10,'enemy-2.png',50*(1.5+i),2))
        
        elif level == 2:
            
            think_1 = 0
            think_2 = 1

            j = 1
            for i in range(0,15,1):
                inimigo_group_1.add(enemy((10+i*36),120-45*j,7,'enemy-1.png',50*(1.5+i),4))
                j *= -1
            j = k = 1
            for i in range(0,20,1):
                inimigo_group_2.add(enemy(75+k*38,200+j*75,7,'enemy-2.png',50*(1.5+i),2))
                k += 1
                j = k%2
                j *= -1 

hive_mind_turning = False
think_1 = think_2 = 0
choice = True

go_to_menu = True
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------- MAIN GAME ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

while True:
    if go_to_menu:
        menu()
        level = 1
        #pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)
        go_to_menu = False
    enemy_count = 0  
#    while choice:
#            menu(choice)
    sair()
    moviment()

    
    tela.fill((0,0,0))

    #display--------------------------------------------------------
    tela.blit(background_normal,(0,0))

    projeteis.update()
    
    projeteis.draw(tela)

    projeteis_enemy.update()

    projeteis_enemy.draw(tela)

    point_count()
    
    jogadores.draw(tela)
    jogador.show_life()
    
    hive_mind_turning = False
    thinking(inimigo_group_1,think_1)
    for i in inimigo_group_1:
        i.mov()
        i.shot()
        i.show_life()
        
    hive_mind_turning = False
    thinking(inimigo_group_2,think_2)
    for i in inimigo_group_2:
        i.mov()    
        i.shot()
        i.show_life()
            
    inimigo_group_1.draw(tela)
    inimigo_group_2.draw(tela)
    
    Death(inimigo_group_1,projeteis)

    Death(jogadores,projeteis_enemy)

    Death(inimigo_group_2,projeteis)
        
    
    pygame.display.flip()
    
    if enemy_count <= 0:
        win(True)

    if not jogador.alive:
        win(False)


    clock.tick(60)

