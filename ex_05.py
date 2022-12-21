import math
import random as rand
import time
import tkinter

border_top = 0
border_buttom = 800
border_left = 0
border_right = 600

class Bullet:

    def __init__(self, x, y, vx, vy, r, color):
        self.setPosition(x, y)
        self.setVector(vx, vy)
        self.setVisual(r, color)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def setVector(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def setVisual(self, r, color):
        self.r = float(r)
        self.color = color
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def remove_flag(self):
        return self.out_of_screen()

    def out_of_screen(self):
        return (self.x < border_left) | (self.x > border_right) | (self.y < border_top) | (self.y > border_buttom)

    def hit(self):
        pass

    def draw(self, canvas):
        canvas.create_oval(int(self.x - self.r), int(self.y - self.r), int(self.x + self.r), int(self.y + self.r), fill=self.color)

class ReflectableBullet(Bullet):
    def __init__(self, x, y, vx, vy, r, color, reflectableH, reflectableV):
        Bullet.__init__(self, x, y, vx, vy, r, color)
        self.refH = reflectableH
        self.refV = reflectableV

    def move(self):
        Bullet.move(self)
        self.reflecte()

    def reflecte(self):
        if(self.refH & ((self.x < border_left) | (self.x > border_right))):
            self.vx *= -1
            self.x += self.vx * 2
        if(self.refV & ((self.y < border_top) | (self.y > border_buttom))):
            self.vy *= -1
            self.y += self.vy * 2

class Player:

    def __init__(self, x, y, size, color):
        self.v = 10
        self.setPosition(x, y)
        self.setVisual(size, color)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setVisual(self, size, color):
        self.size = float(size)
        self.color = color
    
    def move_right(self):
        if(self.x < border_right - self.v):
            self.x += self.v
    
    def move_left(self):
        if(self.x > border_left + self.v):
            self.x -= self.v
    
    def move_up(self):
        if(self.y > border_top + self.v):
            self.y -= self.v
    
    def move_down(self):
        if(self.y < border_buttom - self.v):
            self.y += self.v
    
    def draw(self, canvas):
        canvas.create_rectangle(int(self.x - self.size/2), int(self.y), int(self.x + self.size/2), int(self.y + self.size/2), fill=self.color, outline=self.color)
        canvas.create_rectangle(int(self.x - self.size/5), int(self.y - self.size/2), int(self.x + self.size/5), int(self.y), fill=self.color, outline=self.color)

    def hit(self, blt):
        if(abs(blt.y - self.y) > self.size/2.0 + blt.r):
            return False
        elif(blt.y < self.y - self.size/2.0):
            if(abs(blt.x - self.x) <= self.size/5.0):
                return True
            cornerX = self.x
            cornerY = self.y - self.size/2
            if(blt.x < self.x):
                cornerX -= self.size/5.0
            else:
                cornerX += self.size/5.0
            dis = math.sqrt((blt.x - cornerX)**2 + (blt.y - cornerY)**2)
            return (dis <= blt.r)
        elif(blt.y < self.y - blt.r):
            return (abs(blt.x - self.x) <= self.size/5 + blt.r)
        elif(blt.y < self.y):
            if(abs(blt.x - self.x) <= self.size/2.0):
                return True
            cornerX = self.x
            cornerY = self.y
            if(blt.x < self.x):
                cornerX -= self.size/2.0
            else:
                cornerX += self.size/2.0
            dis = math.sqrt((blt.x - cornerX)**2 + (blt.y - cornerY)**2)
            return (dis <= blt.r)
        elif(blt.y < self.y + self.size/2.0):
            return (abs(blt.x - self.x) <= self.size/2.0 + blt.r)
        else:
            if(abs(blt.x - self.x) <= self.size/2.0):
                return True
            cornerX = self.x
            cornerY = self.y + self.size/2
            if(blt.x < self.x):
                cornerX -= self.size/2.0
            else:
                cornerX += self.size/2.0
            dis = math.sqrt((blt.x - cornerX)**2 + (blt.y - cornerY)**2)
            return (dis <= blt.r)

class Car:

    def __init__(self, x, y, vx, vy, size, color):
        self.isActive = True
        self.setPosition(x, y)
        self.setVector(vx, vy)
        self.setVisual(size, color)

        self.invincible = 30    #invincible flame num

        self.w=self.size
        self.h=self.size/2

    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def setVector(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def setVisual(self, size, color):
        self.size = float(size)
        self.color = color
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.reflecte()
        if(self.invincible > 0):
            self.invincible -= 1

    def reflecte(self):
        if((self.x - self.w/2 < border_left) | (self.x + self.w/2 > border_right)):
            self.vx *= -1
            self.x += self.vx * 2
        if((self.y - self.h/2 < border_top) | (self.y + self.h/2 > border_buttom)):
            self.vy *= -1
            self.y += self.vy * 2
    
    def hit(self, b_x, b_y, b_size):
        if(self.invincible > 0):
            return False
        if((b_y < self.y - self.h/2 - b_size/2) | (b_y > self.y + self.h/2 + b_size/2)):    # out area
            return False
        elif(b_y < self.y - self.h/2):    # area 1
            if(abs(b_x - self.x) <= self.w/6):
                return True
            cornerX = self.x
            cornerY = self.y - self.h/2
            if(b_x < self.x):
                cornerX -= self.w/6
            else:
                cornerX += self.w/6
            dis = math.sqrt((b_x - cornerX)**2 + (b_y - cornerY)**2)
            return (dis <= float(b_size)/2.0)
        elif(b_y < self.y - self.h/6 - b_size): # area 2
            return abs(b_x - self.x) <= (b_size/2 + self.w/6)
        elif(b_y < self.y - self.h/6):  # area 3
            if(abs(b_x - self.x) <= self.w/2):
                return True
            cornerX = self.x
            cornerY = self.y - self.h/6
            if(b_x < self.x):
                cornerX -= self.w/2
            else:
                cornerX += self.w/2
            dis = math.sqrt((b_x - cornerX)**2 + (b_y - cornerY)**2)
            return (dis <= float(b_size)/2.0)
        elif(b_y < self.y + self.h/6):  # area 4
            return abs(b_x - self.x) <= (b_size/2 + self.w/2)
        elif(b_y < self.y + self.h/6 + b_size/2):   # area 5
            if(abs(b_x - self.x) <= self.w/2):
                return True
            cornerX = self.x
            cornerY = self.y + self.h/6
            if(b_x < self.x):
                cornerX -= self.w/2
            else:
                cornerX += self.w/2
            dis = math.sqrt((b_x - cornerX)**2 + (b_y - cornerY)**2)
            return (dis <= float(b_size)/2.0)
        else:   # area 6
            cornerX = self.x
            cornerY = self.y + self.h/3
            if(b_x < self.x):
                cornerX -= self.w/4
            else:
                cornerX += self.w/4
            dis = math.sqrt((b_x - cornerX)**2 + (b_y - cornerY)**2)
            return (dis <= float(b_size)/2.0)
    
    def shot(self):
        if(rand.random() > 0.95):
            ref = [False, False]
            color = ["black", "black"]
            if(rand.random() > 0.97):
                ref[0] = True
                color[0] = "red"
            if(rand.random() > 0.97):
                ref[1] = True
                color[1] = "red"
            car_bullets.append(ReflectableBullet(self.x - self.w/8, self.y + self.h/6, rand.uniform(-5, 5), rand.uniform(3, 10), self.w/12, color[0], True, ref[0]))
            car_bullets.append(ReflectableBullet(self.x + self.w/8, self.y + self.h/6, rand.uniform(-5, 5), rand.uniform(3, 10), self.w/12, color[1], True, ref[1]))
        

    def draw(self, canvas):

        canvas.create_rectangle(int(self.x+self.w/3-self.w/2), int(self.y-self.h/2), int(self.x+self.w/3*2-self.w/2), int(self.y+self.h/3-self.h/2), fill=self.color, outline=self.color)
        canvas.create_rectangle(int(self.x-self.w/2), int(self.y+self.h/3-self.h/2), int(self.x+self.w-self.w/2), int(self.y+self.h/3*2-self.h/2), fill=self.color, outline=self.color)
        canvas.create_oval(int(self.x+self.w/6-self.w/2), int(self.y+self.h/3*2-self.h/2), int(self.x+self.w/6*2-self.w/2), int(self.y+self.h-self.h/2), fill="black")
        canvas.create_oval(int(self.x+self.w/6*4-self.w/2), int(self.y+self.h/3*2-self.h/2), int(self.x+self.w/6*5-self.w/2), int(self.y+self.h-self.h/2), fill="black")

class Score:
    
    def __init__(self):
        self.shotCount = 0
        self.hitCount = 0
        self.damagedCount = 0
        self.score = 0
    
    def shot(self):
        self.shotCount += 1
    
    def hit(self):
        self.hitCount += 1
        self.score += self.getHitRate()
    
    def damaged(self):
        self.damagedCount += 1
    
    def getHitRate(self):
        rate = 0.0
        if(self.shotCount != 0):
            rate = float(self.hitCount) / float(self.shotCount)
        return rate

def exit_clicked():
    frame.active = False

def key_handler(event):
    if(event.keycode == 32):    # space
        bullets.append(Bullet(player.x, player.y - player.size/2, 0, -20, 10, "blue"))
        score.shot()
    elif((event.keycode == 87) | (event.keycode == 38)):  # w || up
        player.move_up()
    elif((event.keycode == 65) | (event.keycode == 37)):  # a || left
        player.move_left()
    elif((event.keycode == 83) | (event.keycode == 40)):  # s || down
        player.move_down()
    elif((event.keycode == 68) | (event.keycode == 39)):  # d || right
        player.move_right()

def make_car():
    return Car(50, 100, rand.randint(5, 20), 0, 100, "red")

def draw_score(canvas):
    msg = ("Score : %.3f | Hit Rate : %.3f" % (score.score, score.getHitRate()))
    canvas.create_text(10, 10, anchor="nw", fill="black", text=msg, font=("",15))

def result_methods():
    best = 0.0
    try:
        file = open("bestscore.txt", "r")
        file.seek(0)
        str = file.read()
        print(str)
        if(str != ""):
            best = float(str)
        file.close()
    except IOError:
        pass
    if(score.score > best):
        file = open("bestscore.txt", "w")
        file.truncate()
        str = "%.5f" % score.score
        file.write(str)
        file.close()
    return best

def draw_result(canvas, best):
    msg = ("Shot : %d\nHit : %d\nHitRate : %.3f\n--------------------\nScore : %.3f\n(BestScore : %.3f)" % (score.shotCount, score.hitCount, score.getHitRate(), score.score, best))
    canvas.create_text(300, 400, anchor="center", fill="black", text=msg, font=("", 24))

frame = tkinter.Tk()
frame.geometry('600x800')
frame.title("課題4-3")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)
frame.protocol("WM_DELETE_WINDOW", exit_clicked)
frame.bind("<KeyPress>", key_handler)
frame.active = True
game_active = True

player = Player(300, 700, 50, "blue")
bullets = []
car = make_car()
car_bullets = []

score = Score()

while(frame.active & game_active):
    try:
        canvas.delete("all")

        if(not(car.isActive)):
            car = make_car()
        
        car.move()
        car.draw(canvas)

        car.shot()
        
        player.draw(canvas)

        remove_list = []
        for i in range(len(bullets)):
            bullets[i].move()
            if(bullets[i].remove_flag()):
                remove_list.append(i)
                continue
            if(car.isActive):
                if(car.hit(bullets[i].x, bullets[i].y, bullets[i].r)):
                    car.isActive = False
                    remove_list.append(i)
                    score.hit()
            bullets[i].draw(canvas)
        for i in range(len(remove_list)):
            bullets.pop(remove_list[i])
        remove_list.clear()

        for i in range(len(car_bullets)):
            car_bullets[i].move()
            if(player.hit(car_bullets[i])):
                game_active = False
            if(car_bullets[i].remove_flag()):
                remove_list.append(i)
                continue
            car_bullets[i].draw(canvas)
        for i in range(len(remove_list)):
            car_bullets.pop(remove_list[i])

        draw_score(canvas)

        frame.update()
        time.sleep(1/30)
    except Exception as e:
        print(str(e))
        break

if(frame.active):
    canvas.create_text(300, 400, anchor="center", text="Crash!", fill="black", font=("", 32))
    canvas.update()
    time.sleep(1)
    canvas.create_rectangle(0, 0, 600, 800, fill="white", outline="white")
    best = result_methods()
    draw_result(canvas, best)
    while(frame.active):
        canvas.update()
        time.sleep(0.1)
    
