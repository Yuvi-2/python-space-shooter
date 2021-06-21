import pygame
import random
from pygame import mixer
pygame.init()
mixer.init()

pygame.font.init()
win=pygame.display.set_mode((1250,700))
pygame.display.set_caption("GetTheVaccine")
vacimage=pygame.transform.scale(pygame.image.load("vac.png"),(80,80))
pygame.display.set_icon(vacimage)
mainsimage=pygame.image.load('main.png')
ealienimage=pygame.image.load('ealien.png')
velocity=10
keys=pygame.key.get_pressed()
enemy2shipimage=pygame.transform.rotate(pygame.image.load('enemy.png'),180)

vac2image=pygame.transform.scale(pygame.image.load("vac2.png") ,(80,80))
bossalienimage=pygame.transform.scale(pygame.image.load("boss.png"),(200,200))
bg=pygame.transform.scale(pygame.image.load("bg.jpg"),(1250,700))
earthimage=pygame.transform.scale(pygame.image.load("earth.png"),(400,400))
class Vac:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def draw(self,rot):
		img=pygame.transform.rotate(vacimage,rot)
		win.blit(img,(self.x,self.y))
		
	def move(self):
		self.y+=10
	def draw2(self,rot):
		img2=pygame.transform.rotate(vac2image,rot)
		win.blit(img2,(self.x,self.y))

class EnemyBullets:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def draw(self,window):
		pygame.draw.rect(window,(0,0,0),(self.x,self.y,20,20))
	def move(self):
		self.y+=5

	

class EnemyShip:
	def __init__(self,image):
		self.x=random.randint(10,1150)
		self.y=random.randint(720,1000)
		self.shoottime=random.randint(100,200)
		self.image=image
		self.pausetime=0
	def draw(self):

		if self.shoottime>0:
			pygame.draw.rect(win,(0,255,0),(self.x,self.y-10,self.shoottime/2,10))
		elif self.shoottime<=0:
			texttype=pygame.font.SysFont("comicsansms",40)
			Text=texttype.render("Shooting Time over",False,(0,0,0))
			win.blit(Text,(self.x,self.y-10))
		win.blit(enemy2shipimage,(self.x,self.y))
	def move(self):
		if self.pausetime<=0:
			self.y-=3
		if self.pausetime>0:
			self.y-=0
	def decreaseshoottime(self):
		if self.pausetime<=0:
			self.shoottime-=0.5
	def decreasefreezetime(self):
		self.pausetime-=0.2

class EnemyAlien:
	def __init__(self):
		self.x=random.randint(10,1200)
		self.y=random.randint(720,1000)
		self.shoottime=random.randint(100,180)
		self.pausetime=0
	def draw(self):
		if self.shoottime>0:
			pygame.draw.rect(win,(0,255,0),(self.x,self.y-10,self.shoottime/2,10))
		elif self.shoottime<=0:
			texttype=pygame.font.SysFont("comicsansms",30)
			Text=texttype.render("Shooting Time over",False,(0,0,0))
			win.blit(Text,(self.x,self.y-10))
		win.blit(ealienimage,(self.x,self.y))
	def move(self):
		if self.pausetime<=0:
			self.y-=3
		if self.pausetime>0:
			self.y-=0
	def decreaseshoottime(self):
		if self.pausetime<=0:
			self.shoottime-=0.5
	def decreasefreezetime(self):
		self.pausetime-=0.1


class Bullet:
	def __init__(self,x,y,btype):
		self.x=x
		self.y=y
		self.type=btype
	def draw(self,window):
		pygame.draw.rect(window,(0,0,0),(self.x,self.y,20,20))
	def move(self):
		self.y-=15
	def drawcircle(self,window):
		pygame.draw.circle(window,(0,0,100),(self.x,self.y),15,15)
		

class MShip:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.score=0
		self.vaccollected=0
		self.health=600
	def draw(self,window):
		window.blit(mainsimage,(self.x,self.y))
	def movement(self):
		keys=pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			self.y-=velocity
		if keys[pygame.K_DOWN]:
			self.y+=velocity
		if keys[pygame.K_RIGHT]:
			self.x+=velocity
		if keys[pygame.K_LEFT]:
			self.x-=velocity

def main():
	running=True
	clock=pygame.time.Clock()
	bullets=[]
	ealiens=[]
	enemyships2=[]
	enemybullets=[]
	vaccines=[]
	vaccines2=[]
	fuelheight=600
	textstyle=pygame.font.SysFont('comicsansms',50)
	
	mainship=MShip(300,300)
	play=0
	
	def draw():
		win.fill((50,100,200))
		
		mainship.draw(win)
		text=textstyle.render('health:',False,(0,0,0))
		mainship.movement()
		pygame.draw.rect(win,(100,200,90),(100,10,mainship.health/3,10))
		count=0
		win.blit(text,(0,0))

		for i in range(1):
			
				if len(ealiens)<2:
					alienship=EnemyAlien()
					ealiens.append(alienship)
					
				elif len(enemyships2)<1 and mainship.vaccollected>10:
					enemys=EnemyShip(enemy2shipimage)
					enemyships2.append(enemys)
					
		for bullet in bullets:
			if bullet.type=="freeze":
				bullet.drawcircle(win)
			else:
				bullet.draw(win)
			bullet.move()
			if bullet.y<0:
				bullets.remove(bullet)
		for alienship in ealiens:
			alienship.draw()
			alienship.decreaseshoottime()
			alienship.move()
			if alienship.y<-128:
				ealiens.remove(alienship)
			for bullet in bullets:
				if bullet.x>alienship.x and bullet.x<alienship.x+128 and bullet.y<alienship.y+128 and alienship in ealiens:
					if alienship.shoottime>0 and bullet.type=="normal":
						mainship.vaccollected+=1
						ealiens.remove(alienship)
						vaccine2=Vac(alienship.x,alienship.y)
						vaccines2.append(vaccine2)
					if bullet.type=="freeze":
						alienship.pausetime=10
		
					bullets.remove(bullet)
			alienship.decreasefreezetime()
		for enemys in enemyships2:
			enemys.draw()
			enemys.decreaseshoottime()
			enemys.move()
			a=random.randint(0,100)
			if a<2:
				enemybullet=EnemyBullets(enemys.x,enemys.y)
				enemybullets.append(enemybullet)
				
			if enemys.y<-128:
				enemyships2.remove(enemys)
			for bullet in bullets:
				if bullet.x>enemys.x and bullet.x<enemys.x+128 and bullet.y<enemys.y+128 and enemys in enemyships2:
					if enemys.shoottime>0 and bullet.type=="normal":
						mainship.vaccollected+=1
						enemyships2.remove(enemys)
						vaccine=Vac(enemys.x,enemys.y)
						vaccines.append(vaccine)
						
					if bullet.type=="freeze":
						enemys.pausetime=10
			enemys.decreasefreezetime()
			for enemybullet in enemybullets:
				enemybullet.draw(win)
				enemybullet.move()
		for vaccine in vaccines:
			vaccine.draw(random.randint(80,270))
			vaccine.move()
			if vaccine.y<0:
				vaccines.remove(vaccine)
		for vaccine2 in vaccines2:
			vaccine2.draw2(random.randint(70,360))
			vaccine2.move()

			if vaccine2.y<0:
				vaccines2.remove(vaccine2)
		for enemybullet in enemybullets:
			if enemybullet.x>mainship.x and enemybullet.x<enemys.x+128 and enemybullet.y<mainship.y+128 and enemybullet.y>mainship.y:
				mainship.health-=0.9
					
		VacText=textstyle.render(f'Vaccines Collected:{mainship.vaccollected}',False,(255,255,255))
		win.blit(VacText,(10,100))	
		pygame.display.update()
	while running:
		draw()
		clock.tick(60)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				 running=False
				 pygame.quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and len(bullets)<6:
			bullet=Bullet(mainship.x+50,mainship.y-20,"normal")
			bullets.append(bullet)
			mixer.music.load("sf_laser_13.mp3")
			mixer.music.set_volume(0.7)
			mixer.music.play()
		if keys[pygame.K_RSHIFT]:
			bullet=Bullet(mainship.x+50,mainship.y-20,"freeze")
			bullets.append(bullet)
			mixer.music.load("sf_laser_13.mp3")
			mixer.music.set_volume(0.7)
			mixer.music.play()
		if mainship.health<1:
			gameover(mainship.vaccollected)

		
			

def starting():
	r=True
	x=500
	y=0
	textstyle=pygame.font.SysFont('comicsansms',30)
	text=textstyle.render("Once upon a time, an alien visited earth",False,(255,255,255))
	text2=textstyle.render("And started the spread of a deadly virus",False,(255,255,255))
	text3=textstyle.render("Your target is to shoot his army and get as many vaccines as possible",False,(255,255,255))
	text4=textstyle.render("Press Space to start the war",False,(255,255,255))
	clock=pygame.time.Clock()
	sig=0
	sig2=0
	sig3=0
	def startdraw():
		win.blit(bg,(0,0))
		win.blit(earthimage,(400,400))
		win.blit(bossalienimage,(x,y))
		if sig==0:
			win.blit(text,(0,0))
		elif sig>0 and sig2<30:
			win.blit(text2,(0,0))

		if sig2>30:
			win.blit(text3,(0,0))
			win.blit(text4,(10,100))
			
		

		pygame.display.update()
	while r:
		startdraw()
		clock.tick(60)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				r=False
		y+=2
		if y==400:
			y-=12
			sig=1
		sig2+=0.1
		keys=pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			main()

def contolles():
	l=True
	bg=pygame.transform.scale(pygame.image.load("bgcontrolles.jpg"),(1250,700))
	textstyle=pygame.font.SysFont('comicsansms',30)
	def draw():
		win.blit(bg,(0,0))
		text=textstyle.render("Use Arrow Keys for movement",False,(255,255,255))
		text2=textstyle.render("Press Space to shoot laser",False,(255,255,255))
		text3=textstyle.render("Press Right Shift to shoot freezing lazer",False,(255,255,255))
		text6=textstyle.render("Once the shooting time of the spaceship is over,you can't shoot it",False,(255,255,255))
		text7=textstyle.render("The shooting time of the spaceship is indicated by the green bar on its top",False,(255,255,255))
		text4=textstyle.render("Press M for menu",False,(255,255,255))
		text5=textstyle.render("Press P to play",False,(255,255,255))
		
		win.blit(text,(100,100))
		win.blit(text2,(100,200))
		win.blit(text3,(100,300))
		win.blit(text6,(100,400))
		win.blit(text7,(0,450))
		win.blit(text4,(100,500))
		win.blit(text5,(100,550))
		pygame.display.update()
	while l:
		draw()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_q]:
			pygame.quit()
		if keys[pygame.K_p]:
			starting()
		if keys[pygame.K_m]:
			menu()

def gameover(vcollected):
	l=True
	bg=pygame.transform.scale(pygame.image.load("bgcontrolles.jpg"),(1250,700))
	textstyle=pygame.font.SysFont('comicsansms',50)
	mixer.music.load("music.mp3")
	mixer.music.set_volume(10)
	mixer.music.play()
	def draw():
		win.blit(bg,(0,0))
		text=textstyle.render(f"Game Over!,Vaccines collected:{vcollected}",False,(255,255,255))
		
		text4=textstyle.render("Press M for menu",False,(255,255,255))
		text5=textstyle.render("Press P to play",False,(255,255,255))
		
		win.blit(text,(100,100))
		
		win.blit(text4,(100,400))
		win.blit(text5,(100,500))
		pygame.display.update()
	while l:
		draw()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_q]:
			pygame.quit()
		if keys[pygame.K_p]:
			starting()
		if keys[pygame.K_m]:
			menu()

def menu():
	a=True
	textstyle=pygame.font.SysFont('comicsansms',50)

	def draw():
		win.fill((0,0,0))
		Head=textstyle.render("GetTheVaccine!",False,(255,255,255))
		text=textstyle.render("Press S to Play",False,(255,255,255))
		text2=textstyle.render("Press C for Controles",False,(255,255,255))
		text3=textstyle.render("Press Q to Quit",False,(255,255,255))
		win.blit(text,(300,300))
		win.blit(text2,(400,400))
		win.blit(text3,(500,500))
		win.blit(Head,(400,0))
		win.blit(vacimage,(440,30))
		
		pygame.display.update()
	while a:
		draw()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_s]:
			starting()

		if keys[pygame.K_q]:
			pygame.quit()
		if keys[pygame.K_c]:
			contolles()
menu()
