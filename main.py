# IMPORTS
import pygame as pg
from random import choice
import os
import numpy as np
from math import sqrt
try:
    pg.init()
except:
    print("Erro. pygame n foi inicializado")


class Enviroment:
    def __init__(self, width, height, num_mesas, num_estantes, num_robos):
        self.width = width
        self.height = height
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.brown = (140, 70, 20)
        self.gray = (170, 170, 170)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.num_mesas = num_mesas
        self.num_estantes = num_estantes
        self.num_robos = num_robos
        self.mesaDev_x = mesaDev_x
        self.mesaDev_y = mesaDev_y
        self.livrosDev = livros_dev
        os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'
        self.screen = pg.display.set_mode((width, height))
        self.screen_size = (self.width, self.height)
        self.estante_size = (150, 40)
        self.mesa_size = (40, 40)
        self.robo_size = (30, 30)
        self.mesaDev_size = (100, 40)
        # usuario coloca o numero do livro que ele deseja
        self.input_box = pg.Rect(0, self.height-32, 50, 32)
        self.font = pg.font.Font(None, 32)
        self.text_dev_w, self.text_dev_h = self.font.size('Devolver')
        self.rect_dev = pg.Rect(
            50, self.height-(self.text_dev_h+10), self.text_dev_w, self.text_dev_h)
        self.text_dev = self.font.render('Devolver', True, self.green)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.clock = pg.time.Clock()
        pg.display.set_caption('Robôs Carregadores de Livros')

    def createlista_Estantes(self):
        self.lista_possiveis = []
        for i in range(0, self.width-self.estante_size[0], self.estante_size[0]):
            for j in range(0, self.height-self.estante_size[1], self.estante_size[1]):
                self.lista_possiveis.append([i, j])
        for i in range(self.num_estantes):
            x, y = choice(self.lista_possiveis)
            self.lista_possiveis.remove([x, y])
            lista_estantes.append(
                [x, y, self.estante_size[0], self.estante_size[1]])

    def renderlista_Estantes(self):
        for estante in lista_estantes:
            pg.draw.rect(self.screen, self.brown, estante)
            self.estante_tag = self.font.render(
                str(lista_estantes.index(estante)+1), True, self.black)
            self.screen.blit(
                self.estante_tag, (estante[0]+(estante[2])/2, estante[1]+(estante[3]/2)))

    def createlista_Mesas(self):
        

        for i in range(self.num_mesas):
            x, y = choice(self.lista_possiveis)
            self.lista_possiveis.remove([x, y])
            lista_mesas.append(
                [x, y, self.mesa_size[0], self.mesa_size[1]])

    def renderlista_Mesas(self):
        for mesa in lista_mesas:
            pg.draw.rect(self.screen, self.white, mesa)
            self.mesa_tag = self.font.render(
                str(lista_mesas.index(mesa)+1), True, self.black)
            self.screen.blit(
                self.mesa_tag, (mesa[0]+(mesa[2])/2, mesa[1]+(mesa[3]/2)))

    def createlista_Robos(self):
        

        for i in range(self.num_robos):

            x, y = choice(self.lista_possiveis)
            self.lista_possiveis.remove([x, y])
            lista_robos.append(
                [x, y, self.robo_size[0], self.robo_size[1]])
            base_robos.append([x,y])

    def renderlista_Robos(self):

        for robo in lista_robos:

            pg.draw.rect(self.screen, self.gray, robo)
            self.robo_tag = self.font.render(
                str(lista_robos.index(robo)+1), True, self.black)
            self.screen.blit(
                self.robo_tag, (robo[0]+(robo[2])/2, robo[1]+(robo[3]/2)))

    def createMesaDev(self):
        x, y = choice(self.lista_possiveis)
        self.lista_possiveis.remove([x, y])
        return(x, y)

    def renderMesaDev(self):
        pg.draw.rect(self.screen, self.red, [
            mesaDev_x, mesaDev_y, self.mesaDev_size[0], self.mesaDev_size[1]])


class Robots:
    def __init__(self, width, height, num_robos, num_estantes, vel):
        self.width = width
        self.height = height
        self.num_robos = num_robos
        self.num_mesas = num_mesas
        self.num_estantes = num_estantes
        self.estados = []
        self.mesaDev_x = mesaDev_x
        self.mesaDev_y = mesaDev_y
        self.vel = vel

    def dist(self, x, y):

        d = sqrt(pow(x, 2)+pow(y, 2))
        return d

    def manageStates(self):  # set states of robots in real time
        if len(robos_tirar) < len(livros_tirar):
            num_tirar = len(livros_tirar)
            for estante in livros_tirar:  # get the nearest robot of each bookshelf
                dist_estante = []
                for i in range(num_robos):
                    dist_estante_x, dist_estante_y = self.distRobo(
                        lista_robos[i][:2], lista_estantes[estante])  # for estante
                    dist = self.dist(dist_estante_x, dist_estante_y)
                    dist_estante.append(dist)
                dist_estante = np.array(dist_estante)
                idx_estante = np.where(
                    dist_estante == np.amin(dist_estante))[0][0]
                robos_tirar.append(idx_estante)
                self.mudarEstado(idx_estante, 1)

        elif len(livros_dev) > self.estados.count(3) and len(livros_dev) > self.estados.count(4):
            distancias_dev = []
            for i in range(num_robos):  

                dist_dev_x, dist_dev_y = self.distRobo(
                    lista_robos[i][:2], (mesaDev_x, mesaDev_y))  # for dev table
                distancias_dev.append(self.dist(dist_dev_x, dist_dev_y))
            for livros in livros_dev:
                distancias_dev = np.array(distancias_dev)
                idx_dev = np.argpartition(distancias_dev, np.where(
                    distancias_dev == np.amax(distancias_dev))[0][0])
                # get the num_dev's nearest robots to the devolutions table
                
                for i in idx_dev[:len(livros_dev)]:
                    if self.estados[i] == 4:
                        pass
                    else:
                        robos_dev.append(i)
                        self.mudarEstado(i, 3)
        else:
            for i in range(num_robos):
                if self.estados[i] == 1:
                    idx = robos_tirar.index(i)
                    estante = livros_tirar[idx]
                    if self.distRobo(lista_robos[i][:2], lista_estantes[estante][:2]) == (0, 0):
                        self.removeLivrosTirar(estante)
                        self.mudarEstado(i, 2)
                if self.estados[i] == 2:
                    if self.distRobo(lista_robos[i][:2], lista_mesas[mesa][:2]) == (0, 0):
                        self.mudarEstado(i, 0)
                if self.estados[i] == 3:
                    if self.distRobo(lista_robos[i][:2], (mesaDev_x, mesaDev_y)) == (0, 0):
                        self.mudarEstado(i, 4)
                if self.estados[i] == 4:
                    idx = robos_dev.index(i)
                    estante = livros_dev[idx]
                    if self.distRobo(lista_robos[i][:2],lista_estantes[estante][:2]) == (0,0):
                        self.removeLivrosDev(estante)
                        self.mudarEstado(i, 0)

    def takeActions(self):
        for i in range(num_robos):
            if self.estados[i] == 1:
                idx = robos_tirar.index(i)
                estante = livros_tirar[idx]
                x, y = self.move(lista_robos[i][:2], lista_estantes[estante][:2])
                lista_robos[i][0], lista_robos[i][1] = x, y
            elif self.estados[i] == 2:
                x, y = self.move(lista_robos[i][:2], lista_mesas[mesa][:2])
                lista_robos[i][0], lista_robos[i][1] = x, y
            elif self.estados[i] == 3:
                idx = robos_dev.index(i)
                x, y = self.move(lista_robos[i][:2], (mesaDev_x, mesaDev_y))
                lista_robos[i][0], lista_robos[i][1] = x, y
            if self.estados[i] == 4:
                idx = robos_dev.index(i)
                estante = livros_dev[idx]
                x, y = self.move(lista_robos[i][:2], lista_estantes[estante][:2])
                lista_robos[i][0], lista_robos[i][1] = x, y
            if self.estados[i] == 5:
                pass
            else:  # self.state[i] == 0
                x, y = self.move(lista_robos[i][:2], base_robos[i])
                lista_robos[i][0], lista_robos[i][1] = x, y

    def setEstados(self):
        for i in range(num_robos):
            # Estado 0- inativo, 1- pegar livro em estante, 2- levar livro para mesa do usuario 3- pegar livro em mesa de devolução 4- entregar livro da mesa de devolução para a estante
            self.estados.append(0)

    def mudarEstado(self, robo, modo):

        self.estados[robo] = modo

    def move(self, robo, target):
        robo_x, robo_y = robo
        t_x, t_y = target
        if t_x > robo_x:
            robo_x += self.vel
        elif t_x < robo_x:
            robo_x -= self.vel
        elif t_y > robo_y:
            robo_y += self.vel
        elif t_y < robo_y:
            robo_y -= self.vel
             
        return(robo_x, robo_y)

    def avoidCollision(self):
        for i in range(num_robos):
            for j in range(num_robos):
                if not self.estados[i] == 0 and not self.estados[j] == 0 and (self.distRobo(lista_robos[i],lista_robos[j])[0] < 5 or self.distRobo(lista_robos[i],lista_robos[j])[1] < 5):
                    self.estados[i] = 5
                if self.estados[i] == 5 and (self.distRobo(lista_robos[i],lista_robos[j])[0] > 5 or self.distRobo(lista_robos[i],lista_robos[j])[1] > 5):
                    self.estados[i] = 0
                



    def distRobo(self, robo, target):
        dis_x = target[0] - robo[0]
        dis_y = target[1] - robo[1]
        return (dis_x, dis_y)

    def addLivrosDev(self, livro):
        livros_dev.append(livro)

    def removeLivrosDev(self, livro):
        idx = livros_dev.index(livro)
        robos_dev.pop(idx)
        livros_dev.remove(livro)

    def addLivrosTirar(self, livro):
        livros_tirar.append(livro)

    def removeLivrosTirar(self, livro):
        idx = livros_tirar.index(livro)
        robos_tirar.pop(idx)
        livros_tirar.remove(livro)


width = 900
height = 600
# Define Important Variables
lista_estantes = []
lista_mesas = []
lista_robos = []
base_robos = []
livros_tirar = []  # list of books to be taken from bookshelves
# list of robots in state-1(the ith robot in this list must take the ith robot in livros_tirar list)
robos_tirar = []
livros_dev = []
robos_dev = []
mesaDev_x = 0
mesaDev_y = 0
ultimo_livro = None
num_mesas = int(input('Numero de mesas: '))
num_estantes = int(input('Numero de estantes: '))
num_robos = int(input('Numero de robos: '))
mesa = -1
while mesa < 0 or mesa > num_mesas:
    mesa = int(input('Mesa em que você se encontra: ')) - 1

env = Enviroment(width, height, num_mesas, num_estantes, num_robos)
env.createlista_Estantes()
env.createlista_Mesas()
env.createlista_Robos()
mesaDev_x, mesaDev_y = env.createMesaDev()
robos = Robots(width, height, num_robos, num_estantes, 2)
robos.setEstados()
while not env.done:

    env.screen.fill(env.black)
    env.renderlista_Estantes()
    env.renderlista_Mesas()
    env.renderlista_Robos()
    env.renderMesaDev()
    robos.manageStates()
    robos.takeActions()
    robos.avoidCollision()
    print(robos.estados)
    print(livros_dev)
    print(robos_dev)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            env.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if env.input_box.collidepoint(event.pos):
                # Toggle the active variable.
                env.active = not env.active
            else:
                active = False
            if env.rect_dev.collidepoint(event.pos):
                robos.addLivrosDev(int(ultimo_livro))
                env.text = ''
            # Change the current color of the input box.
            env.color = env.color_active if env.active else env.color_inactive
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                env.done = True
            if env.active:
                if event.key == pg.K_RETURN:
                    ultimo_livro = int(env.text)-1
                    robos.addLivrosTirar(ultimo_livro)
                    tirar = True
                elif event.key == pg.K_BACKSPACE:
                    env.text = env.text[:-1]
                else:
                    env.text += event.unicode

    # Render the current text.
    txt_surface = env.font.render(env.text, True, env.color)
    # Resize the box if the text is too long.
    width = max(50, txt_surface.get_width()+10)
    env.input_box.w = width
    # Blit the text.
    env.screen.blit(txt_surface, (env.input_box.x+5, env.input_box.y+5))
    env.screen.blit(env.text_dev, (env.rect_dev.x+5, env.rect_dev.y+5))
    # Blit the input_box rect.
    pg.draw.rect(env.screen, env.color, env.input_box, 2)
    pg.display.flip()
