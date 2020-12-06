from bangtal import *

import time
import threading
import random

mainScene = Scene("메인", "res/wallpaper/main.png")
mapScene = Scene("지도", "res/wallpaper/ingame2.png")
startScene = Scene("공격개시","res/wallpaper/ingame.png")
stage1 = Scene("한국","res/wallpaper/stage1.png")
stage2 = Scene("일본","res/wallpaper/stage2.png")
stage3 = Scene("중국","res/wallpaper/stage3.png")

stageNum = 1  # 현재 스테이지 번호 저장
prevScene = mainScene # 이전 Scene 저장
nowScene = mainScene # 현재 Scene 저장
stageObject = None # 현재 Stage 객체 저장

FRIEND = 0
ENEMY = 1

STAGE1 = 1
STAGE2 = 2
STAGE3 = 3

class Stage():
  def __init__(self,stage):
    #TODO Enemy 객체 생성하는 부분
    if(stage == STAGE1):
      self.friend = Friend(100,1000,stage)
      self.enemy = Enemy(1000,stage)
      catBtns[0].show()
    elif(stage == STAGE2):
      self.friend = Friend(500,2000,stage)
      self.enemy = Enemy(2000,stage)
      for i in range(0,3):
        catBtns[i].show()
    elif(stage == STAGE3):
      self.friend = Friend(1000,3000,stage)
      self.enemy = Enemy(3000,stage)
      for i in range(0,5):
        catBtns[i].show()

class Enemy():
  def createFriend(self):
    self.timer = threading.Timer(7,self.createFriend)
    isEmpty = False
    index = 0
    for i in range(0,5):
      if self.friends[i] == None:
        isEmpty = True
        index = i
        break

    if isEmpty:
      if self.enemyOrder[self.i] == 0:
        self.friends[index] = DogSoldier(index)
      elif self.enemyOrder[self.i] == 1:
        self.friends[index] = SnakeSoldier(index)
      elif self.enemyOrder[self.i] == 2:
        self.friends[index] = SheepSoldier(index)
      elif self.enemyOrder[self.i] == 3:
        self.friends[index] = BearSoldier(index)
      elif self.enemyOrder[self.i] == 4:
        self.friends[index] = CySoldier(index)
      self.i = self.i + 1

    self.timer.start()


  def __init__(self,castleStat,stage):
    self.castle = Castle(ENEMY,castleStat)
    self.friends = [None for i in range(5)]
    self.i = 0
    
    if stage == STAGE1:
      self.enemyOrder = [0 for i in range(20)]
    elif stage == STAGE2:
      self.enemyOrder = [0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1]
    elif stage == STAGE3:
      self.enemyOrder = [0,0,0,2,0,1,1,0,2,3,0,0,4,0,1,2,0,3]
    
    self.createFriend()


class Friend():
  def createFriend(self,type):
    isEmpty = False
    index = 0
    for i in range(0,5):
      if self.friends[i] == None:  # 아군이 5명이 넘지 않을 때
        isEmpty = True
        index = i
        break

    if isEmpty:
      if self.moneyNow >= catBtns[type].price: # 돈이 병사 가격보다 많을 때
        if type == 0 :
          self.friends[index] = CatSoldier(index)
        elif type == 1:
          self.friends[index] = TankCatSoldier(index)
        elif type == 2:
          self.friends[index] = AxeCatSoldier(index)
        elif type == 3:
          self.friends[index] = BirdCatSoldier(index)
        elif type == 4:
          self.friends[index] = TitanCatSoldier(index)

        self.moneyNow = self.moneyNow - catBtns[type].price
        catBtnsDisable[type].show()

        # 캐릭터 위에 작대기 2초동안 표시
        def onTimeout():
          catBtnsDisable[type].hide()
        timer = Timer(2)
        timer.start()
        timer.onTimeout = onTimeout



  def startTimer(self):  # 돈 계산해서 화면에 표시하는 함수
    self.timer = threading.Timer(1, self.startTimer)

    if self.moneyNow + 10 <= self.moneyMax:
      self.moneyNow = self.moneyNow + 10
    
    rest = self.moneyNow

    self.moneyThou.setImage(f"res/etc/{int(self.moneyNow / 1000)}.png")
    rest = self.moneyNow - int(self.moneyNow / 1000)*1000
    self.moneyThou.show()

    self.moneyHun.setImage(f"res/etc/{int(rest / 100)}.png")
    rest = self.moneyNow - int(self.moneyNow / 100)*100
    self.moneyHun.show()

    self.moneyTens.setImage(f"res/etc/{int(rest/10)}.png")
    rest = self.moneyNow - int(self.moneyNow / 10)*10
    self.moneyTens.show()

    self.moneyUnits.setImage(f"res/etc/{rest}.png")
    self.moneyUnits.show()

    self.timer.start()

  def endTimer(self):
    self.timer.cancel()

  def onMoneyTimeout(self):
    if self.moneyNow + 5 <= self.moneyMax:
      self.moneyNow = self.moneyNow + 5

  def __init__(self,moneyMax,castleStat,stage):
    self.moneyMax = moneyMax
    self.moneyNow = 0
    self.castle = Castle(FRIEND,castleStat)
    self.friends = [None for i in range(5)]
    self.moneyTotImg = Object(f"res/etc/{stage}_money.png")
    self.moneyTotImg.locate(nowScene,1000,650)
    self.moneyTotImg.setScale(0.5)
    self.moneyTotImg.show()
    self.sliceImg = Object(f"res/etc/slice.png")
    self.sliceImg.locate(nowScene,960,650)
    self.sliceImg.setScale(0.5)
    self.sliceImg.show()
    self.moneyThou = Object(f"res/etc/0.png")
    self.moneyThou.locate(nowScene,840,650)
    self.moneyThou.setScale(0.5)
    self.moneyHun = Object(f"res/etc/0.png")
    self.moneyHun.locate(nowScene,870,650)
    self.moneyHun.setScale(0.5)
    self.moneyTens = Object(f"res/etc/0.png")
    self.moneyTens.locate(nowScene,900,650)
    self.moneyTens.setScale(0.5)
    self.moneyUnits = Object(f"res/etc/0.png")
    self.moneyUnits.locate(nowScene,930,650)
    self.moneyUnits.setScale(0.5)

    self.startTimer()

class Soldier(Object):
  def __init__(self,file,move):
    super().__init__(file)
    self.move = move

class EnemySoldier(Soldier):
  def receiveAttack(self,damage,index):
    self.power = self.power - damage
    print('enemy')
    print(self.power)
    if self.power < 0:
      stageObject.enemy.friends[index] = None
      self.hide()
      self.attack = 0
      self.attackTimer.cancel()

  def attackOp(self):
    self.attackTimer = threading.Timer(self.interval,self.attackOp)
    while(True):
      attackIndex = random.randrange(0,5)
      if stageObject.friend.friends[attackIndex] != None:
        break
    
    stageObject.friend.friends[attackIndex].receiveAttack(self.attack,attackIndex)
    self.attackTimer.start()

  def movePos(self):
    self.moveTimer = threading.Timer(1, self.movePos)
    if (self.index == 0 and self.xPos + self.move <= 590) or (self.index == 1 and self.xPos + self.move <= 575) or (self.index == 2 and self.xPos + self.move <= 550) or (self.index == 3 and self.xPos + self.move <= 525) or (self.index == 4 and self.xPos + self.move <= 500):
      self.xPos = self.xPos + self.move
      self.locate(nowScene, self.xPos,self.yPos)
    else:
      self.moveTimer.cancel()
      self.attackOp()

    self.moveTimer.start()

  def __init__(self,file,index,move,attack,power,interval,xPos = 100,yPos = 180):
    super().__init__(file,move)
    self.attack = attack
    self.power = power
    self.interval = interval
    self.index = index
    self.xPos = xPos
    self.yPos = yPos
    self.locate(nowScene,xPos,yPos)
    self.show()
    self.movePos()
    self.attackTimer = threading.Timer(self.interval,self.attackOp)

class DogSoldier(EnemySoldier):
  def __init__(self,index):
    super().__init__(file="res/character/dog_move1.png",index = index,move = 25,attack = 25,power = 90,interval = 1)

class SnakeSoldier(EnemySoldier):
  def __init__(self,index):
    super().__init__(file="res/character/snake_move1.png",index = index,move = 40,attack = 30,power = 1000,interval = 1)

class SheepSoldier(EnemySoldier):
  def __init__(self,index):
    super().__init__(file="res/character/baabaa_move1.png",index = index,move = 20,attack = 100,power = 350,interval = 2)

class BearSoldier(EnemySoldier):
  def __init__(self,index):
    super().__init__(file="res/character/bear_move1.png",index = index,move = 50,attack = 200,power = 500,interval = 3)

class CySoldier(EnemySoldier):
  def __init__(self,index):
    super().__init__(file="res/character/cy_move1.png",index = index,move = 50,attack = 300,power = 2000,interval = 8)

class FriendSoldier(Soldier):
  def receiveAttack(self,damage,index):
    self.power = self.power - damage
    print('friend')
    print(self.power)
    if self.power < 0:
      print('dead')
      stageObject.friend.friends[index] = None
      self.hide()
      self.attack = 0
      self.attackTimer.cancel()

  def attackOp(self):
    self.attackTimer = threading.Timer(self.interval,self.attackOp)
    while(True):
      attackIndex = random.randrange(0,5)
      if stageObject.enemy.friends[attackIndex] != None:
        break
    
    stageObject.enemy.friends[attackIndex].receiveAttack(self.attack,attackIndex)
    self.attackTimer.start()
  def movePos(self):
    self.moveTimer = threading.Timer(1, self.movePos)
    if (self.index == 0 and self.xPos - self.move >= 610) or (self.index == 1 and self.xPos - self.move >= 625) or (self.index == 2 and self.xPos - self.move >= 650) or (self.index == 3 and self.xPos - self.move >= 675) or (self.index == 4 and self.xPos - self.move >= 700):
      self.xPos = self.xPos - self.move
      self.locate(nowScene, self.xPos,self.yPos)
    else:
      self.moveTimer.cancel()
      self.attackOp()

    self.moveTimer.start()

  def __init__(self,file,index,price,move,attack,power,interval,xPos = 1000,yPos = 180):
    super().__init__(file,move)
    self.attack = attack
    self.power = power
    self.interval = interval
    self.index = index
    self.price = price
    self.xPos = xPos
    self.yPos = yPos
    self.locate(nowScene,xPos,yPos)
    self.show()
    self.movePos()
    self.attackTimer = threading.Timer(self.interval,self.attackOp)
    

class CatSoldier(FriendSoldier):
  def __init__(self,index):
    super().__init__(file="res/character/cat1_move1.png",index = index,price = 50,move = 50,attack = 20,power = 130,interval = 1)

class TankCatSoldier(FriendSoldier):
  def __init__(self,index):
    super().__init__(file="res/character/tankcat_move1.png",index = index,price = 100,move = 40,attack = 5,power = 500,interval = 2)

class AxeCatSoldier(FriendSoldier):
  def __init__(self,index):
    super().__init__(file="res/character/axecat_move1.png",index = index,price = 200,move = 60,attack = 60,power = 150,interval = 1)

class BirdCatSoldier(FriendSoldier):
  def __init__(self,index):
    super().__init__(file="res/character/cat_bird_move1.png",index = index,price = 400,move = 50,attack = 250,power = 700,interval = 2)

class TitanCatSoldier(FriendSoldier):
  def __init__(self,index):
    super().__init__(file="res/character/titan_move1.png",index = index,price = 1000,move = 50,attack = 200,power = 800,interval = 4)

class Castle():
  def __init__(self,type,status):
    self.status = status
    self.type = type

class Point(Object):  # 지도에서 각 지역별 표시
  def __init__(self,file,type):
    super().__init__(file)
    self.type = type
    self.onMouseAction = self.point_onClick

  def point_onClick(self,x,y,action):
    global stageNum
    if self.type == STAGE1:
      koreaImg.show()
      japanImg.hide()
      chinaImg.hide()
      stageNum = STAGE1
    elif self.type == STAGE2:
      koreaImg.hide()
      japanImg.show()
      chinaImg.hide()
      stageNum = STAGE2
    elif self.type == STAGE3:
      koreaImg.hide()
      japanImg.hide()
      chinaImg.show()
      stageNum = STAGE3

gameBtn = Object("res/etc/game.png")
gameBtn.locate(mainScene, 400,200)
gameBtn.setScale(0.7)
gameBtn.show()

startBtn = Object("res/etc/start.png")
startBtn.locate(mapScene, 1000,200)
startBtn.setScale(0.5)
startBtn.show()

startImg = Object("res/wallpaper/start.png")
startImg.locate(mapScene,0,0)

backBtn = Object("res/etc/back.png")

pauseBtn = Object("res/etc/pause.png")
pauseBtn.locate(stage1, 0,600)
pauseBtn.setScale(0.6)
pauseBtn.show()

pauseImg = Object("res/etc/pauseimg.png")
pauseImg.locate(stage1, 400,200)
continueBtn = Object("res/etc/continue.png")
continueBtn.locate(stage1, 530,330)
exitBtn = Object("res/etc/exit.png")
exitBtn.locate(stage1, 530,230)

class CatBtn(Object):
  def onBtnClick(self,x,y,action):
    stageObject.friend.createFriend(self.type)
  def __init__(self,file,type,price):
    super().__init__(file)
    self.type = type
    self.price = price
    self.onMouseAction = self.onBtnClick


catCastle = Object("res/castle/cat_castle.png")
enCastle = Object("res/castle/en_castle.png")
catBtns = [CatBtn("res/etc/cat.png",0,50),CatBtn("res/etc/tankcat.png",1,100),CatBtn("res/etc/axecat.png",2,200),CatBtn("res/etc/birdcat.png",3,400), CatBtn("res/etc/titan.png",4,1000)]
catBtnsDisable = [Object("res/etc/none.png") for i in range(5)]

point1 = Point("res/etc/point.png",STAGE1)  #한국
point1.locate(mapScene, 580,335)
point1.show()
koreaImg = Object("res/etc/korea.png")
koreaImg.locate(mapScene, 660,585)
koreaImg.show()

point2 = Point("res/etc/point.png",STAGE2)  #일본
point2.locate(mapScene, 750,300)
point2.show()
japanImg = Object("res/etc/japan.png")
japanImg.locate(mapScene, 660,585)

point3 = Point("res/etc/point.png",STAGE3)  #중국
point3.locate(mapScene, 360,200)
point3.show()
chinaImg = Object("res/etc/china.png")
chinaImg.locate(mapScene, 660,585)

def gameBtn_onClick(x,y,action):
  global prevScene
  prevScene = mainScene
  backBtn.locate(mapScene,3,40)
  backBtn.show()
  mapScene.enter()
gameBtn.onMouseAction = gameBtn_onClick

def startBtn_onClick(x,y,action):
  global prevScene
  startImg.show()
  timer = Timer(1)
  timer.start()

  def onTimeout():
    global stageObject
    global nowScene
    startImg.hide()
    prevScene = mapScene
    if stageNum == STAGE1:
      nowScene = stage1
      stageObject = Stage(STAGE1)
    elif stageNum == STAGE2:
      nowScene = stage2
      stageObject = Stage(STAGE2)
    elif stageNum == STAGE3:
      nowScene = stage3
      stageObject = Stage(STAGE3)

    catCastle.locate(nowScene,1000,200)
    catCastle.show()
    enCastle.locate(nowScene,0,150)
    enCastle.setScale(0.8)
    enCastle.show()

    xPos = 230
    for i in range(0,5):
      catBtns[i].locate(nowScene,xPos,10)
      catBtnsDisable[i].locate(nowScene,xPos,10)
      xPos = xPos + 150

    nowScene.enter()
    pauseBtn.locate(nowScene, 0,600)
    locatePauseBox(nowScene)
  timer.onTimeout = onTimeout

startBtn.onMouseAction = startBtn_onClick

def locatePauseBox(stage):
    pauseBtn.locate(stage, 0,600)
    pauseImg.locate(stage, 400,200)
    continueBtn.locate(stage, 530,330)
    exitBtn.locate(stage, 530,230)

def backBtn_onClick(x,y,action):
  prevScene.enter()
backBtn.onMouseAction = backBtn_onClick

def pauseBtn_onClick(x,y,action):
  pauseImg.show()
  continueBtn.show()
  exitBtn.show()
pauseBtn.onMouseAction = pauseBtn_onClick

def exitBtn_onClick(x,y,action):
  stageObject.friend.endTimer()
  prevScene.enter()
  hidePauseBox()
exitBtn.onMouseAction = exitBtn_onClick

def continueBtn_onClick(x,y,action):
  hidePauseBox()
continueBtn.onMouseAction = continueBtn_onClick

def hidePauseBox():
  pauseImg.hide()
  continueBtn.hide()
  exitBtn.hide()

startGame(mainScene)

#구현해야하는 부분
#- 적군 캐릭터 생성
#- 각 캐릭터별 속성 정의
#- 공격 구현

#한국-일본-중국 순서