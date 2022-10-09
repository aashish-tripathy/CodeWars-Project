import pygame
from robot import Robot
from pygame.sprite import Sprite

class Base(Sprite):
    def __init__(self, screen, x, y, type, __robot_list, __robot_map, game):
        super().__init__()
        self.screen = screen
        self.type = type
        self.__robot_map = __robot_map
        self.__robot_list = __robot_list
        self.__myGame = game
        self.__SelfElixir = 2000
        self.__TotalTeamElixir = 2000
        self.__TotalVirus = 0
        self.__MovingAverage = 2000
        self.__Signal = ''
        
        if type == "red":
            self.image = pygame.image.load("redbase.png")
        else:
            self.image = pygame.image.load("bluebase.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def actVirus(self, v, pos):
        g = self.__myGame
        if pos[0] < 0 or pos[0] >= g._Game__dim[0]:
            return
        if pos[1] < 0 or pos[1] >= g._Game__dim[1]:
            return
        if self.__robot_map[pos[1]][pos[0]]==0:
            g._Game__resources[pos[1]][pos[0]]-= v
            return
        if self.__robot_map[pos[1]][pos[0]]==1 and self ==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==1 and self==g._Game__bluebase:
            g._Game__redbase.VirusOnRobot(pos, v)
            return
        if self.__robot_map[pos[1]][pos[0]]==2 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==2 and self==g._Game__redbase:
            g._Game__bluebase.VirusOnRobot(pos, v)
            return
        if self.__robot_map[pos[1]][pos[0]]==3 and self==g._Game__bluebase:
            if v <= g._Game__redbase.__SelfElixir:
                g._Game__redbase.__SelfElixir -= v
                g._Game__redbase.__TotalTeamElixir -= v
            else:
                g._Game__redbase.__SelfElixir  = 0
                g._Game__redbase.__TotalTeamElixir = 0
            return
        if self.__robot_map[pos[1]][pos[0]]==3 and self==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==4 and self==g._Game__redbase:
            if v <= g._Game__bluebase.__SelfElixir:
                g._Game__bluebase.__SelfElixir -= v
                g._Game__bluebase.__TotalTeamElixir -= v
            else:
                g._Game__bluebase.__SelfElixir = 0
                g._Game__bluebase.__TotalTeamElixir = 0
            return
        if self.__robot_map[pos[1]][pos[0]]==4 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return

    def GetListOfSignals(self):
        res = []
        for x in self.__robot_list:
            res.append(x._Robot__Signal)
        return res

    def addResource(self, v):
        if v < 0:
            self.__TotalVirus -= v
        else:
            self.__SelfElixir += v
            self.__TotalTeamElixir += v
        
    def VirusOnRobot(self, pos,virus):
        robots = self.__myGame._Game__PositionToRobot[pos]
        if len(robots)==0:
            self.__myGame._Game__resources[pos[1]][pos[0]]-= virus
            return
        virus /= len(robots)
        delete = []
        for robot in robots:
            if robot._Robot__selfElixir <= virus:
                e = virus - robot._Robot__selfElixir
                self.__TotalTeamElixir -= robot._Robot__selfElixir
                delete.append(robot)
                robot.kill()
                self.__robot_map[pos[1]][pos[0]] = 0
                self.__myGame._Game__resources[pos[1]][pos[0]]-=e
            else:
                self.__TotalTeamElixir -= virus
                robot._Robot__selfElixir-=virus
        for d in delete:
            del self.__myGame._Game__PositionToRobot[pos][d]
    def create_robot(self, signal):
        if self.__SelfElixir >= 50:
            str = 'wncc'
            if type(signal)!=type(str) or len(signal) > 20:
                signal = ''
            self.__SelfElixir -= 50
            #self.GlobalRobotCount += 1
            robo = Robot(self.screen, self.rect.x, self.rect.y, self.type, signal, self)
            self.__robot_list.add(robo)
            if (self.rect.x//20, self.rect.y//20) in self.__myGame._Game__PositionToRobot:
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)][robo] = True
            else:
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)][robo] = True
            if self.type == 'red':
                self.__robot_map[self.rect.y//20][self.rect.x//20] = 3
            else:
                self.__robot_map[self.rect.y//20][self.rect.x//20] = 4

    def investigate_up(self):
        if self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    

    def investigate_down(self):
        if self.rect.y == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    
    def investigate_left(self):
        if self.rect.x == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_right(self):
        if self.rect.x == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_ne(self):
        if self.rect.x == 780 or self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_nw(self):
        if self.rect.x == 0 or self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_se(self):
        if self.rect.x == 780 or self.rect.y == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_sw(self):
        if self.rect.x == 0 or self.rect.y==780:
            return "wall"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    
    def GetYourSignal(self):
        return self.__Signal
    
    def SetYourSignal(self, s):
        str = 'wncc'
        if type(s)!=type(str) or len(s) > 20:
            return
        self.__Signal = s
    def GetTotalElixir(self):
        return self.__TotalTeamElixir
    def GetElixir(self):
        return self.__SelfElixir
    def GetVirus(self):
        return self.__TotalVirus
    
    def GetPosition(self):
        return (self.rect.x//20,self.rect.y//20)
    
    def GetDimensionX(self):
        return self.__myGame._Game__dim[0]

    def GetDimensionY(self):
        return self.__myGame._Game__dim[1]

    def DeployVirus(self, v):
        if v > self.__TotalVirus or v <= 0:
            return
        self.__TotalVirus -= v
        self.actVirus(v/8,(self.rect.x-1,self.rect.y))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x,self.rect.y-1))

    def blitme(self):
        self.screen.blit(self.image, self.rect)
import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            print( "Red Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            print( "Red Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            print( "Red Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            print( "Red Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Red Team Wins", True, (255,100,100), (230,230,230))
            print( "Red Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import warnings 
from base import Base
from collectible import Collectible
import scriptred
import scriptblue
#__resources library

class Game():

        
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        #self.score = pygame.display.set_mode((400, 800))
        #self.scoreboard = pygame.display.set_caption("Code Wars")
        self.fps_controller = pygame.time.Clock()
        self.__dim = (40,40)
        self.__resources = self.create_map()
        self.__resources[19][9] = 0
        self.__resources[19][29] = 0
        self.GlobalRobotCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 10

        self.__collectibles = []
        
        self.__PositionToRobot = {}
        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__robots = np.zeros(self.__dim)
        # 0 in self.robots means no robots
        # 1 means one robot of red team
        # 2 means one robot of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, 180, 380, 'red', self.__redbots, self.__robots,self)
        self.__bluebase = Base(self.screen, 580, 380, 'blue', self.__bluebots, self.__robots,self)
        self.__PositionToRobot[(9,19)] = {self.__redbase:True}
        self.__PositionToRobot[(29,19)] = {self.__bluebase:True}
        self.update_score()

    def run_game(self):
        iter = 0
        while True:
            iter+=1
            self.screen.fill((60,60,60))
            scriptblue.ActBase(self.__bluebase)
            scriptred.ActBase(self.__redbase)
            moves = {}
            for robo in self.__redbots:
                n = scriptred.ActRobot(robo)
                moves[robo] = n
            for robo in self.__bluebots:
                n = scriptblue.ActRobot(robo)
                moves[robo] = n
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            self.__bluebase.blitme()
            self.__redbase.blitme()
            self.__bluebots.draw(self.screen)
            self.__redbots.draw(self.screen)
            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            self.game_over()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            if iter > 1500:
                break
        self.game_over_iter()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            
        else:
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            print( "Blue Wins")
        self.screen.blit(game_over, (400,400))
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__robots[i][j] = 0
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__robots[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = (860, 655)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, (830, 650))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = (1058, 655)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, (1030, 650))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Robot__selfElixir > r._Robot__selfElixir:
                    b._Robot__selfElixir -= r._Robot__selfElixir
                    self.__robots[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    r._Robot__selfElixir = 0
                elif b._Robot__selfElixir < r._Robot__selfElixir:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 1
                    r._Robot__selfElixir -= b._Robot__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    b.__Robot_selfElixir = 0
                else:
                    self.__robots[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Robot__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                    r._Robot__selfElixir = 0
                    b._Robot__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Robot__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__redbase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0

        for b in bluebase_collisions:
            if b._Robot__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Robot__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Robot__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Robot__selfElixir
                b._Robot__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToRobot[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self):
        """Take info about __collectibles and create the map"""
        im = cv2.imread("test_img3.jpg", cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (40,40))
        im = np.array(im)
        im = im - np.full((40,40), 127)
        im = (im/127)*50
        return np.array(im)

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToRobot.keys():
            value = self.__PositionToRobot[key]
            if self.__robots[key[1]][key[0]] == 1 or self.__robots[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()


                


    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = 900
        titlerect.y = 50
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render("Blue Team", False, (130,130,255))
        self.screen.blit(blue_head, (830, 130))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_robots = norm_font.render("No. of Robots: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, (850, 170))
        self.screen.blit(blue_self, (850, 210))
        self.screen.blit(blue_robots, (850, 250))
        self.screen.blit(blue_virus, (850, 290))

        red_head = head_font.render("Red Team", False, (255,130,130))
        self.screen.blit(red_head, (830, 400))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_robots = norm_font.render("No. of Robots: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, (850, 440))
        self.screen.blit(red_self, (850, 480))
        self.screen.blit(red_robots, (850, 520))
        self.screen.blit(red_virus, (850, 560))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0:
            print( "Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
        elif self.__bluebase._Base__SelfElixir <= 0:
            print("Blue Wins")
            game_over = game_over_font.render("Blue Team Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, (400,400))
            pygame.display.flip()
            time.sleep(5)
            sys.exit(0)
            
    

game = Game()
game.run_game()

