from bangtal import *

mainScene = Scene("메인", "res/wallpaper/main.png")
mapScene = Scene("지도", "res/wallpaper/ingame2.png")
startScene = Scene("공격개시","res/wallpaper/ingame.png")
stage1 = Scene("한국","res/wallpaper/stage1.png")
stage2 = Scene("일본","res/wallpaper/stage2.png")
stage3 = Scene("중국","res/wallpaper/stage3.png")

stageNum = 1
prevScene = mainScene

class Point(Object):
  def __init__(self,file,type):
    super().__init__(file)
    self.type = type
    self.onMouseAction = self.point_onClick

  def point_onClick(self,x,y,action):
    global stageNum
    if self.type == 1:
      koreaImg.show()
      japanImg.hide()
      chinaImg.hide()
      stageNum = 1
    elif self.type == 2:
      koreaImg.hide()
      japanImg.show()
      chinaImg.hide()
      stageNum = 2
    elif self.type == 3:
      koreaImg.hide()
      japanImg.hide()
      chinaImg.show()
      stageNum = 3

gameBtn = Object("res/etc/game.png")
gameBtn.locate(mainScene, 200,200)
gameBtn.show()

startBtn = Object("res/etc/start.png")
startBtn.locate(mapScene, 1000,200)
startBtn.setScale(0.5)
startBtn.show()

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


catCastle = Object("res/castle/cat_castle.png")
catCastle.locate(stage1,1000,200)
catCastle.show()
stage1Castle = Object("res/castle/stage1_castle.png")
stage1Castle.locate(stage1,0,150)
stage1Castle.setScale(0.8)
stage1Castle.show()

point1 = Point("res/etc/point.png",1)  #한국
point1.locate(mapScene, 580,335)
point1.show()
koreaImg = Object("res/etc/korea.png")
koreaImg.locate(mapScene, 660,585)
koreaImg.show()

point2 = Point("res/etc/point.png",2)  #일본
point2.locate(mapScene, 750,300)
point2.show()
japanImg = Object("res/etc/japan.png")
japanImg.locate(mapScene, 660,585)

point3 = Point("res/etc/point.png",3)  #중국
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
  if stageNum == 1:
    prevScene = mapScene
    stage1.enter()
  elif stageNum == 2:
    prevScene = mapScene
    stage2.enter()
  elif stageNum == 3:
    prevScene = mapScene
    stage3.enter()
startBtn.onMouseAction = startBtn_onClick

def backBtn_onClick(x,y,action):
  prevScene.enter()
backBtn.onMouseAction = backBtn_onClick

def pauseBtn_onClick(x,y,action):
  pauseImg.show()
  continueBtn.show()
  exitBtn.show()
pauseBtn.onMouseAction = pauseBtn_onClick

def exitBtn_onClick(x,y,action):
  prevScene.enter()
exitBtn.onMouseAction = exitBtn_onClick

def continueBtn_onClick(x,y,action):
  pauseImg.hide()
  continueBtn.hide()
  exitBtn.hide()
continueBtn.onMouseAction = continueBtn_onClick

startGame(mainScene)