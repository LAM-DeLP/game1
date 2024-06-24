import sys,pygame,math
from pygame.locals import *

#すべてのボール位置、大きさ取得→(位置+大きさ)マスを衝突判定に追加
#衝突→反射→適用

class charaObj:
    def __init__(self,posx,posy,radius,vx,vy):
        self.pos = [posx,posy]
        self.ver = [vx,vy]
        self.rad = radius
        self.numset = []#衝突判定を保留するのを判定する配列
    
    def reflect(self,wall:list):
        for i in range(2):
            if abs(self.pos[i]-wall[i]/2) > wall[i]/2-self.rad:
                if self.ver[i]>0:
                    self.pos[i]=wall[i]-self.rad
                else:
                    self.pos[i]=0+self.rad
                self.ver[i] = -self.ver[i]
            else:
                pass

    def collide(self,indexnum,xylist:list,verlist:list,radlist:list):#運動量保存
        for now in range(len(radlist)):
            sumrad = radlist[indexnum]+radlist[now] #直径(質量と同等として扱う)の合計
            relativepos = [xylist[now][0]-xylist[indexnum][0],xylist[indexnum][1]-xylist[now][1]] #二物体の相対位置
            if now == indexnum:
                self.numset.append([-1,-1])
            elif relativepos[0]**2+relativepos[1]**2 >=(sumrad**2):
                self.numset.append([-1,-1])
            elif self.numset[now] != [indexnum,now]:

                if relativepos[0]==0:
                    thetapos = math.pi/2
                else:
                    thetapos = math.atan(relativepos[1]/relativepos[0])
                    if thetapos < 0:#衝突角度をなす角に修正(cos,sinに影響するため)
                        thetapos += math.pi
                    else:
                        pass
                i_tempver = [verlist[indexnum][0]*math.cos(thetapos)+verlist[indexnum][1]*-math.sin(thetapos),verlist[indexnum][0]*math.sin(thetapos)+verlist[indexnum][1]*math.cos(thetapos)]
                n_tempver = [verlist[now][0]*math.cos(thetapos)+verlist[now][1]*-math.sin(thetapos),verlist[now][0]*math.sin(thetapos)+verlist[now][1]*math.cos(thetapos)]
                i_tempver[0] = ((radlist[indexnum]-radlist[now])*i_tempver[0]+2*radlist[now]*n_tempver[0])/sumrad                
                self.ver[0] = i_tempver[0]*math.cos(thetapos)+i_tempver[1]*math.sin(thetapos)
                self.ver[1] = i_tempver[0]*-math.sin(thetapos)+i_tempver[1]*math.cos(thetapos) 
                self.pos[0] += self.ver[0]
                self.pos[1] += self.ver[1]#衝突した物体同士が埋まらないように引き離す
            else:
                pass

    def move(self):
        for i in range(2):    
            self.pos[i] += self.ver[i]
            self.ver[i] -= 0*self.rad*self.ver[i]


class originGames:
    def __init__(self,w,h):
        pygame.init()
        pygame.display.set_caption("monsterStrike")
        self.wall = [w,h]
        self.screen = pygame.display.set_mode((w,h)) 

    def main(self):
        balli = [charaObj(30,100,30,10,0),charaObj(100,30,20,0,0)]

        while True:
            self.screen.fill((255,255,255))
            xys=[]
            vers = []
            rads=[]

            for ball in balli:
                xy_c = list(ball.pos)
                ver_c = list(ball.ver)
                xys.append(xy_c)
                vers.append(ver_c)
                rads.append(ball.rad)
                pygame.draw.circle(self.screen,(0,0,0),(ball.pos[0],ball.pos[1]),ball.rad)

            for i in range(len(balli)):
                balli[i].collide(i,xys,vers,rads)
                balli[i].reflect(self.wall)
                balli[i].move()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        balli.append(charaObj(x,y,20,0,0))
            
            pygame.display.update()
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game1 = originGames(375,667)
    game1.main()
