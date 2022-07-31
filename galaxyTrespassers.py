import pygame, random, pygame_textinput
pygame.init()

# Basic Game Information
screenWidth = 970
screenHeight = 825
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Galaxy Trespassers")
clock = pygame.time.Clock()
tick = 120
textinput = pygame_textinput.TextInput()


# Globals
mode = 0
oldScore = 0
signY = -380
score = 0
runOnce = 0
lives = 3
win = False


# Load Images
def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()


# Text
def text(msg, color, x, y, size):
    font = pygame.font.SysFont('freesansbold.ttf', size)
    text = font.render(msg, True, color)
    screen.blit(text, (x, y)) 


# Button Class
class button:
    def __init__(self, pos, width, height, color, mouseOverColor, originalColor, text, textSize):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.mouseOverColor = mouseOverColor
        self.originalColor = originalColor
        self.text = text
        self.textSize = textSize

    def draw(self):
        font = pygame.font.SysFont('freesansbold.ttf', self.textSize)
        pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.width, self.height]) 

        if self.color == (128,0,128):
            textColor = (0,0,255)
        else:
            textColor = (128,0,128)

        text(self.text, textColor, self.pos[0]+(self.width-font.size(self.text)[0])/2, self.pos[1]+15, self.textSize)

    def check(self, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + self.width and pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.height:                    
                return True

            else:
                return False

        if event.type == pygame.MOUSEMOTION: 
            if pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + self.width and pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.height:
                self.color = self.mouseOverColor
                
            else:
                self.color = self.originalColor

# Buttons
startGameButton = button((345, 310), 280, 78, (0,0,255), (128,0,128), (0,0,255), "Start Game", 70)
infoButton = button((385,420), 200, 60, (128,0,128), (0,0,255), (128,0,128), "Info", 50)
backButton = button((0,0), 130, 60, (0, 0, 255), (128,0,128), (0,0,255), "Back", 50)
endlessButton = button((280, 440), 200, 60, (128,0,128), (0,0,255), (128,0,128), "Endless", 50)
storyModeButton = button((500, 440), 200, 60, (0,0,255), (128,0,128), (0,0,255), "Story Mode", 50)
playAgainButton = button((88, 310), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Play Again", 50)
switchModeButton = button((320, 310), 350, 60, (128,0,128), (0,0,255), (128,0,128), "Switch Game Mode", 50)
quitButton = button((700, 310), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Quit", 50)


# Leaderboard Scores
leaderboard = []
highscoreFile = open('highscoreFile.txt', 'r')
nameFile = open('names.txt', 'r')

for i in range(3):
    leaderboard.append( [int(highscoreFile.readline().rstrip("\n")), nameFile.readline().rstrip("\n")] )

highscoreFile.close()
nameFile.close()

def printLeaderboard():
    text("Leaderboard", (255, 0, 25), 330, 535, 70)
    textY = 600
    for i in leaderboard:
        if i[1] != '':
            nameText = i[1]

        else:
            nameText = '___'

        text(nameText, (0,0,0), 305, textY, 50)
        text(str(i[0]), (0,0,0), 610, textY, 50)
        textY+=50


# Play Again
def playAgain(changeMode):
    global score, x, enemyVel, control, runOnce, win, signY, lives, mode, count, storyY
    
    if changeMode:
        if mode == 1:
            mode = 0
        else:
            mode = 1

    textinput = pygame_textinput.TextInput()
    signY = -380
    win = False
    lives = 3
    runOnce = 0
    enemyVel = 1.6
    control = 54
    projectiles.clear()
    enemies.clear()
    score = 0
    x = 390
    redraw()
    count = 0
    storyY = 900

    while mode == 0 and storyY > -400 and changeMode:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        screen.blit(background, (0,0))
        screen.blit(story, (30,storyY))

        count+=1
        if count % 5 == 0:
            storyY-=1
        
        pygame.display.update()


# Background
background = loadify('img/background.jpg')

# Lines
life2Line = loadify('img/crackedLine.png')
life3Line = loadify('img/crackedLiner.png')

# Story
story = loadify('img/story.png')

# Controls
info = loadify('img/info.png')

# Victory Message
winSign = loadify('img/victoryMessage.png')

# Fighter
fighter = loadify('img/galaxyFighter.png')
vel = 6
x = 390
y = 688


# Projectiles
shootLoop = 0
projectiles = []
class projectileObject:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)


# Enemies
enemyShips = [loadify('img/enemy1.png'), loadify('img/enemy2.png'), loadify('img/enemy3.png')]
enemyVel = 1.6
spawnCount = 0
control = 54
enemies = []

class enemyObject:
  def __init__(self, ship, y, x, vel):
    self.ship = ship
    self.y = y
    self.x = x
    self.vel = vel


# Add Enemy
def addEnemy():

    screen.blit(background, (0,0))
    x = random.randrange(10, 830)

    # Create New Enemy Object and Add to List
    newEnemy = enemyObject(enemyShips[random.randrange(0,3)], -100, x, enemyVel)
    enemies.append(newEnemy)              


# Redraw scene
def redraw():
    global clicked, event, control, enemyVel, runOnce, win, signY, mode, oldScore, scores, names, run, lives

    # Background
    screen.blit(background, (0,0)) 

    # Fighter
    screen.blit(fighter, (x, y))

    # Enemies
    for enemy in enemies:
        screen.blit(enemy.ship, (enemy.x, enemy.y))

    # Projectiles
    for projectile in projectiles:
        projectile.draw() 
    
    # Score
    text("Score: "+str(score), (255, 255, 255), 10, 800, 30)
    
    # Choose line based on how many lives left
    if lives == 3:
        pygame.draw.lines(screen, (255,0,0), False, [(0, 679), (970, 679)], 4)
    
    elif lives == 2:
        screen.blit(life2Line, (0, 679))

    elif lives == 1:
        screen.blit(life3Line, (0, 679))

    # Increase difficulty level in story mode
    if mode == 0:
        
        if score > 19 and runOnce == 0:
            control = 53
            enemyVel = 1.75
            
            text("Phase 2", (255, 80, 34), 380, 120, 100)
            pygame.display.update()
            pygame.time.wait(2500)
            runOnce = 1
            
        elif score > 39 and runOnce == 1:
            control = 49
            enemyVel = 1.85

            text("Phase 3", (255, 0, 0), 380, 120, 100)
            pygame.display.update()
            pygame.time.wait(2500)
            runOnce = 2
        
        if score > 59 and runOnce == 2:
            win = True

            if len(enemies) == 0 and runOnce != 3:
                screen.blit(winSign, (201, signY))
                signY+=1
                pygame.display.update()

            if signY >= 140:
                runOnce = 3
                text("Created by ", (255,255,255), 260, 20, 50)
                text("Vidster Studios", (255,0,0), 453, 20, 50)
                clicked = True
                pos = (0,0)
                while clicked:
                    
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()

                    quitButton.draw()
                    if event.type == pygame.QUIT or quitButton.check(pos):
                        quit()
                    
                    playAgainButton.draw()
                    if playAgainButton.check(pos):
                        clicked = False
                        playAgain(False)
                        return
                    
                    switchModeButton.draw()
                    if switchModeButton.check(pos):
                        clicked = False
                        playAgain(True)
                        return

                    pygame.display.update()
    
    # Increase speed every time score is a multiple of 5 in endless mode
    elif score % 5 == 0 and score != 0:
        if score != oldScore:
            control-=1
            enemyVel+=0.1
        oldScore = score    

    # Check If Game Over
    for enemy in enemies:
        if enemy.y >= 581:
            
            # Remove Life
            if mode == 1 and lives > 0:
                lives-=1
                enemies.remove(enemy)
                return
            

            # End Game
            if mode == 0 or lives < 1:
                # GAME OVER SCREEN

                # Game Over Text
                text("GAME OVER", (255, 0, 0), 277, 190, 100)
                text("Created by ", (255,255,255), 260, 20, 50)
                text("Vidster Studios", (255,0,0), 453, 20, 50)
                pygame.display.update() 

                # Check If New Highscore
                if score > leaderboard[2][0] and mode == 1:
                    
                    if score > leaderboard[0][0]:
                        text("NEW HIGHSCORE!", (0,230,0), 345, 130, 50)
                    else:
                        text("TOP 3 SCORE!", (0,230,0), 360, 130, 50)

                    text("What's your name?", (255,0,0), 320, 410, 50)

                    # Text Input
                    typing = True
                    while typing:
                        events = pygame.event.get()
                        for event in events:
                            pos = pygame.mouse.get_pos()
                            
                            if event.type == pygame.QUIT or quitButton.check(pos):
                                quit()
                            
                            keys = pygame.key.get_pressed()

                            if keys[pygame.K_RETURN]:
                                name = textinput.get_text().strip()
                                typing = False
                                    
                        quitButton.draw()

                        pygame.draw.rect(screen, (255,255,255), (130,460,700,40))
                        screen.blit(textinput.get_surface(), (140,466))
                        textinput.update(events)
                        
                        pygame.display.update()

                    textinput.clear_text()

                    # Update Leaderboard
                    leaderboard[2][1] = name
                    leaderboard[2][0] = score
                    leaderboard.sort(reverse=True)
                    
                    highscoreFile = open('highscoreFile.txt', 'w')
                    nameFile = open('names.txt', 'w')

                    for i in leaderboard:
                        highscoreFile.write(str(i[0])+'\n')
                        nameFile.write(i[1]+"\n")

                    highscoreFile.close()
                    nameFile.close() 
            
                # Leaderboard
                printLeaderboard()
                
                pos = (0,0)
                clicked = True
                while clicked:
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()

                    quitButton.draw()
                    if event.type == pygame.QUIT or quitButton.check(pos):
                        quit()
                    
                    playAgainButton.draw()
                    if playAgainButton.check(pos):
                        clicked = False
                        playAgain(False)
                        return
                    
                    switchModeButton.draw()
                    if switchModeButton.check(pos):
                        clicked = False
                        playAgain(True)
                        return

                    pygame.display.update()

        pygame.display.update()   
        return


# Start Game Screen
screen.blit(background, (0,0))
printLeaderboard()
text("GALAXY TRESPASSERS", (255, 255, 255), 100, 70, 100)
pos=(-10,0)


# Start Game Button
inInfo = True
clicked = False
while not clicked:

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

    if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        quit()

    startGameButton.draw()
    if startGameButton.check(pos):
        clicked = True

    infoButton.draw()
    if infoButton.check(pos):
        screen.blit(background, (0,0))
        text("GALAXY TRESPASSERS", (255, 255, 255), 100, 70, 100)
        screen.blit(info, (0,170)) 
        text("Created by ", (255,255,255), 260, 770, 50)
        text("Vidster Studios", (255,0,0), 453, 770, 50)

        inInfo = True
        while inInfo:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            backButton.draw()
            if backButton.check(pos):
                screen.blit(background, (0,0))
                printLeaderboard()
                text("GALAXY TRESPASSERS", (255, 255, 255), 100, 70, 100)
                inInfo = False
            pygame.display.update()
        continue

    pygame.display.update()


# Title
screen.blit(background, (0,0))
text("GALAXY TRESPASSERS", (255, 255, 255), 100, 70, 100)

# Choose Mode
while clicked:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        endlessButton.draw()
        if endlessButton.check(pos):
            mode = 1
            clicked = False
        
        storyModeButton.draw()
        if storyModeButton.check(pos):
            clicked = False

        pygame.display.update()


# Story
count = 0
storyY = 900
while mode == 0 and storyY > -400:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    screen.blit(background, (0,0))
    screen.blit(story, (30,storyY))

    count+=1
    if count % 5 == 0:
        storyY-=1
    
    pygame.display.update()


# Main Loop
run = True
while run:

    clock.tick(tick)

    # Prevent player from shooting too many bullets
    if shootLoop > 0:
        shootLoop +=1
        if shootLoop > 19:
            shootLoop = 0

    spawnCount += 1

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Move Enemies
    for enemy in enemies:
        enemy.y += enemy.vel

    # Hit Check
    for projectile in projectiles:
        for enemy in enemies:
            if projectile.y <= enemy.y + 100 and projectile.x >= enemy.x and projectile.x <= enemy.x + 100:
                projectiles.pop(projectiles.index(projectile))
                enemies.pop(enemies.index(enemy))
                score += 1

        # Check If Projectile Has Left The Screen
        if projectile.y > 0:
            projectile.y -= projectile.vel
        else:
            if projectile in projectiles:
                projectiles.pop(projectiles.index(projectile))


    # Controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0 and len(projectiles) < 2:
        projectiles.append(projectileObject(x + 62, y, 8))
        shootLoop = 1

    if keys[pygame.K_LEFT] and x >=10:
        x-=vel

    elif keys[pygame.K_RIGHT] and x <= 842:
        x+=vel
    
    # Stop spawning if won
    if not win:
        if spawnCount >= control:
            addEnemy()
            spawnCount = 0

    redraw()

pygame.quit()


