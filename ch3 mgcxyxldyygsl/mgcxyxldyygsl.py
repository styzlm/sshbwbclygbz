import numpy
import random
import time
import pygame
import sys
import threading
class Node:
    x = None
    y = None
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self,other):
        if other.x == self.x and other.y == self.y:
            return True
        else:
            return False

def dist(N1,N2):
    return numpy.sqrt((N1.x-N2.x)*(N1.x-N2.x)+(N1.y-N2.y)*(N1.y-N2.y))

class mgcxyxldyygsl:
    height = 10
    width = 10
    leinum = 5
    frame = numpy.zeros([width + 2, height + 2])
    framedisplay = numpy.zeros([width + 2, height + 2])
    leilist = []
    gamestatus = 'S'
    starttime = 0
    finishtime = 0

    def __init__(self):
        self.frame = numpy.zeros([self.width + 2, self.height + 2])
        self.framedisplay = numpy.zeros([self.width + 2, self.height + 2])
        self.leilist = []
        self.gamestatus = 'S'
        self.starttime = 0
        for i in range(0,self.width + 2):
            self.framedisplay[i][0] = 1
            self.framedisplay[i][self.height+1] = 1
        for i in range(0,self.height + 2):
            self.framedisplay[0][i] = 1
            self.framedisplay[self.width+1][i] = 1

    def lei(self):
        random.seed(time.time())
        for i in range(0,self.leinum):
            while True:
                leix = random.randint(1,self.width)
                leiy = random.randint(1,self.height)
                leipos = Node(leix,leiy)
                if leipos not in self.leilist:
                    self.frame[leipos.x][leipos.y] = -1
                    self.leilist.append(leipos)
                    break


    def hint(self):
        for lei in self.leilist:
            for i in range(-1,2):
                for j in range(-1,2):
                    if ((i != 0 or j != 0) and self.frame[lei.x+i][lei.y+j]!= -1):
                        self.frame[lei.x+i][lei.y+j] = self.frame[lei.x+i][lei.y+j] + 1

    def marklei(self,screen, pos):
        if self.framedisplay[pos.x][pos.y] == 0:
            self.framedisplay[pos.x][pos.y] = 2
        elif self.framedisplay[pos.x][pos.y] == 2:
            self.framedisplay[pos.x][pos.y] = 3
        elif self.framedisplay[pos.x][pos.y] == 3:
            self.framedisplay[pos.x][pos.y] = 0
        self.drawNode(screen,pos)


    def judge(self,screen):
        green = 0, 255, 0
        red = 255, 0, 0
        yellow = 255, 240, 200
        if self.gamestatus == 'Failure':
            pygame.draw.circle(screen, red, [self.width * 10, self.height * 20 + 20], 10)
            pygame.display.update()
            return
        for i in range(1,self.width):
            for j in range(1,self.height):
                if self.framedisplay[i][j] != 1 and self.frame[i][j] != -1:
                    self.gamestatus = 'N'
                    pygame.draw.circle(screen, yellow, [self.width * 10, self.height * 20 + 20], 10)
                    pygame.display.update()
                    return
        self.gamestatus = 'Win'
        for i in range(1, len(self.framedisplay) - 1):
            for j in range(1, len(self.framedisplay[0]) - 1):
                self.framedisplay[i][j] = 1
                self.drawNode(screen, Node(i, j))
        for lei in self.leilist:
            self.framedisplay[lei.x][lei.y] = 2
            self.drawNode(screen, lei)
        pygame.draw.circle(screen, green, [self.width * 10, self.height * 20 + 20], 10)
        pygame.display.update()
        return

    def start(self):
        self.lei()
        self.hint()


    def displayinfoupdate(self, pos, screen):
        openlist = []
        openlist.append(pos)
        closelist = []
        if self.framedisplay[pos.x][pos.y] == 0:
            if self.frame[pos.x][pos.y] == -1:
                self.gamestatus = 'Failure'
                for lei in self.leilist:
                    self.framedisplay[lei.x][lei.y] = 1
                    self.drawNode(screen,lei)
                closelist.append(pos)
                openlist.remove(pos)
            elif self.frame[pos.x][pos.y] != 0:
                self.framedisplay[pos.x][pos.y] = 1
                self.drawNode(screen, pos)
                closelist.append(pos)
                openlist.remove(pos)
            while openlist != []:
                cn = openlist.pop()
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nn = Node(cn.x + i, cn.y + j)
                        if self.framedisplay[nn.x][nn.y] == 0:
                            if self.frame[nn.x][nn.y] == 0:
                                self.framedisplay[nn.x][nn.y] = 1
                                self.drawNode(screen, nn)
                                openlist.append(nn)
                            else:
                                self.framedisplay[nn.x][nn.y] = 1
                                self.drawNode(screen, nn)
                                closelist.append(nn)
        elif self.framedisplay[pos.x][pos.y] == 1:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nn = Node(pos.x + i, pos.y + j)
                    if self.framedisplay[nn.x][nn.y] == 2:
                        self.drawNode(screen, nn)
                        count = count + 1
            if count == self.frame[pos.x][pos.y]:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nn = Node(pos.x + i, pos.y + j)
                        if self.framedisplay[nn.x][nn.y] == 0:
                            self.displayinfoupdate(nn,screen)
        pygame.display.update()

    def drawNode(self, screen, pos):
        i = pos.x
        j = pos.y
        white = 255, 255, 255
        black = 0, 0, 0
        blue = 0, 255, 255
        red = 255, 0, 0
        if self.framedisplay[i][j] == 0:
            pygame.draw.rect(screen, black, [(i - 1) * 20, (j - 1) * 20, 19, 19], 0)
        elif self.framedisplay[i][j] == 1:
            pygame.draw.rect(screen, white, [(i - 1) * 20, (j - 1) * 20, 19, 19], 0)
            fontObj = pygame.font.SysFont('arial', 16)
            textSurfaceObj = fontObj.render(str(int(self.frame[i][j])), True, black, white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (i * 20 - 10, j * 20 - 11)
            textRectObj.height = 18
            textRectObj.width = 18
            screen.blit(textSurfaceObj, textRectObj)
        elif self.framedisplay[i][j] == 2:
            pygame.draw.rect(screen, red, [(i - 1) * 20, (j - 1) * 20, 19, 19], 0)
        elif self.framedisplay[i][j] == 3:
            pygame.draw.rect(screen, blue, [(i - 1) * 20, (j - 1) * 20, 19, 19], 0)



    def display_time(self,screen):
        while True:
            if self.gamestatus == 'N':
                curtime = time.clock()
            elif self.gamestatus == 'S':
                curtime = self.starttime

            white = 255, 255, 255
            black = 0, 0, 0
            pygame.draw.rect(screen, white, [self.width * 20 - 60, self.height * 20 + 10, 40, 20], 0)
            fontObj = pygame.font.SysFont('arial', 16)
            textSurfaceObj = fontObj.render(format((curtime-self.starttime),'.2f'), True, black, white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.width * 20 - 40, self.height * 20 + 20)
            textRectObj.height = 20
            textRectObj.width = 40
            screen.blit(textSurfaceObj, textRectObj)
            time.sleep(0.1)
            pygame.display.update()

    def display_update_all(self,screen):
        for i in range(1, len(self.framedisplay)-1):
            for j in range(1, len(self.framedisplay[0])-1):
                self.drawNode(screen, Node(i,j))
        pygame.display.update()

    def startgame(self):
        self.start()
        WINSIZE = [self.width * 20, self.height * 20 + 40]
        pygame.init()
        screen = pygame.display.set_mode(WINSIZE)

        pygame.display.set_caption('saolei')
        yellow = 255, 240, 200
        black = 20, 20, 40

        screen.fill((100, 100, 100))

        pygame.display.flip()
        pygame.draw.circle(screen, yellow,[self.width * 10, self.height * 20 + 20],10)
        timethread = threading.Thread(target = self.display_time,args = (screen,))
        timethread.start()
        pygame.display.update()


        for i in range(1, len(self.framedisplay)-1):
            for j in range(1, len(self.framedisplay[0])-1):
                if self.framedisplay[i][j] == 0:
                    pygame.draw.rect(screen,black,[(i-1) * 20, (j-1) * 20,19,19],0)
        self.display_update_all(screen)
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    [x, y] = pygame.mouse.get_pos()
                    if self.gamestatus == 'S'and x <= self.width * 20 and y<= self.height * 20:
                        self.starttime = time.clock()
                        self.gamestatus ='N'
                    if self.gamestatus == 'N' and x <= self.width * 20 and y<= self.height * 20:
                        x = int(x / 20) + 1
                        y = int(y / 20) + 1
                        if event.button == 1:
                            self.displayinfoupdate(Node(x,y),screen)
                            self.judge(screen)
                        if event.button == 3:
                            self.marklei(screen,Node(x,y))


                    if dist(Node(x,y),Node(self.width * 10, self.height * 20 + 20)) <= 10:
                        self.__init__()
                        self.start()
                        self.judge(screen)
                        self.display_update_all(screen)






saoleiplay = mgcxyxldyygsl()
saoleiplay.startgame()