#------------IMPORTS--------------                                                                                            
import pygame
import random 
import mysql.connector
import time
#---------------------------------

#------------VARIABLES------------
s = 0 
x, y = 150, 150  
tx, ty = random.randrange(20, 281, 10), random.randrange(20, 281, 10)
velocity = 10 
radius = 10
run = True
swidth = 300 
sheight = 300
scoreSum = 0 
count = 0 
r, g, b = 255, 255, 0
tr, tg, tb = 0, 0, 0
can = 0 
#---------------------------------

#--------ASKING_PASSWORD----------
password=input("Please enter the password for the root user: ") 
passgame=password
#---------------------------------

#------------SQL_CONNECTION-------

# trying to connect to an existing database named "game" for an existing user 
try: 
    db = mysql.connector.connect(host="localhost",
            user="root",
            passwd='{}'.format(passgame,),
            database="game"
            )
    cursor = db.cursor()
    try: # tries to create a table score if not already present 
        cursor.execute("CREATE TABLE scores (id INT PRIMARY KEY AUTO_INCREMENT, score INT)")
    except: 
        except_temp = 0 

# if no database named "game" is present then it makes one for a new user 
except: 
    db = mysql.connector.connect(host="localhost",
            user="root",
            passwd="{}".format(passgame,)
            )
    cursor = db.cursor() 
    cursor.execute("CREATE DATABASE game")
    cursor.execute("USE game") 
    cursor.execute("CREATE TABLE scores (id INT PRIMARY KEY AUTO_INCREMENT, score INT)")
#---------------------------------

#------------TAKING_THE_AVG_SCORE----------------

su, c = 0, 0
try : 
	cursor.execute("SELECT SUM(score) FROM scores")
	for i in cursor:
		scoreSum = i 
	cursor.execute("SELECT COUNT(score) from scores")
	for i in cursor:
		count = i 
	for i in scoreSum:
		su = i 
	for i in count:
		c = i 
	avg = su // c 
except :  # <--- If the table is empty 
    avg = 0 
#------------------------------------------------

#------------PYGAME_INITIALISATION---------------
pygame.init()
window = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption("EAT EM' ALL")
#------------------------------------------------

#------------PYGAME_LOOP---------------------------------------------
while run: 
	pygame.time.delay(55)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			run = False 

	tr,tg,tb = 0, 0, 0
	avgDisp = 'Average expected score: ' + str(avg)
	scoreDisp = 'Score: ' + str(s)
	myfont = pygame.font.SysFont('Comic Sans MS', 15)
	Cscore = myfont.render(scoreDisp, False, (255, 255, 255))
	Cavg = myfont.render(avgDisp, False, (255,255,255))

	keys = pygame.key.get_pressed()

	'''
	Movement/Detection keys
	'''
	if keys[pygame.K_RIGHT] and x < swidth - radius:
		x += velocity 
	if keys[pygame.K_LEFT] and x >= velocity:
		x -= velocity
	if keys[pygame.K_DOWN] and y < sheight - radius:
		y += velocity
	if keys[pygame.K_UP] and y >= velocity:
		y -= velocity
	if keys[pygame.K_SPACE]: 
		if can < 2: 
			tr, tg, tb = 255, 0, 0
			can += 1 
			time.sleep(1)
			pygame.draw.circle(window, (tr, tg, tb), (tx, ty), 5)


	window.fill((0,0,0))
	pygame.draw.circle(window, (tr, tg, tb), (tx, ty), 5) # <--- Drawing the small random blob
	pygame.draw.circle(window, (r, g, b), (x, y), radius) # <--- Drawing the main blob
	window.blit(Cscore,(0,0)) # Displaying the current score at the top left 
	window.blit(Cavg,(100, 0)) # Displaying the average expected score at the top right
	pygame.display.update()
	
	# Checking if the main blob is in the vicinity and changing colours. 
	if ((ty == y) or (ty > y and ty < y + radius + 20) or (ty < y and ty > y - (radius + 20))) and ((tx == x) or (tx > x and tx < x + radius + 20) or (tx < x and tx > x - (radius +20))):
		r, g, b = random.randrange(0, 256),random.randrange(0, 256),random.randrange(0, 256)

	# Checking if the small blob has been consumed or not 
	if ((ty == y) or (ty > y and ty < y + radius) or (ty < y and ty > y - radius)) and ((tx == x) or (tx > x and tx < x + radius) or (tx < x and tx > x - radius)): 
		s += 10
		tx, ty = random.randrange(20, 181, 10), random.randrange(20, 181, 10) # Generating random coordinates for the small blob 
		pygame.display.update()

	# Checking if the player has touched the boundary 
	if (y <= radius or y  >= sheight - radius) or (x <= radius or x >= swidth- radius):
		run = False
		myfont = pygame.font.SysFont('Comic Sans MS', 30)
		Cscore = myfont.render(scoreDisp, False, (255, 255, 255))
		window.blit(Cscore,(100,130)) # <--- Displaying the current score at the middle of the screen 
		pygame.display.update()
		time.sleep(2) # <--- Waiting for 2 seconds before closing the window


pygame.quit()
#--------------------------------------------------------------------		

#------------SAVING_IN_DATABASE------------------
cursor.execute("INSERT INTO scores(score) VALUES(%s)", (s,))
db.commit()
#------------------------------------------------


