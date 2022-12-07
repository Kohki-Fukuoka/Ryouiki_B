import tkinter
import time

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
        return self.out_of_screen()# | self.hit()

    def out_of_screen(self):
        return (self.x < border_left) | (self.x > border_right) | (self.y < border_top) | (self.y > border_buttom)

    def hit(self):
        pass

    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)

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
        if(self.x < border_left + self.v):
            self.x -= self.v
    
    def move_up(self):
        if(self.y < border_top + self.v):
            self.y -= self.v
    
    def move_down(self):
        if(self.y < border_buttom - self.v):
            self.y += self.v
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.size/2, self.y, self.x + self.size/2, self.y + self.size/2, fill=self.color, outline=self.color)
        canvas.create_rectangle(self.x - self.size/5, self.y - self.size/2, self.x + self.size/5, self.y, fill=self.color, outline=self.color)

class Car:

    def __init__(self, x, y, vx, vy, size, color):
        self.isActive = True
        self.setPosition(x, y)
        self.setVector(vx, vy)
        self.setVisual(size, color)

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

    def reflecte(self):
        if((self.x - self.w/2 < border_left) | (self.x + self.w/2 > border_right)):
            self.vx *= -1
            self.x += self.vx * 2
        if((self.y - self.h/2 < border_top) | (self.y + self.h/2 > border_buttom)):
            self.vy *= -1
            self.y += self.vy * 2
    
    def hit(self, b_x, b_y, b_size):
        if((b_x > self.x - self.w/2) & (b_x < self.x + self.w/2)):
            if((b_y > self.y - (self.h/2 + b_size)) & (b_y < self.y + (self.h/2 + b_size))):
                return True
        return False

    def draw(self, canvas):

        canvas.create_rectangle(self.x+self.w/3-self.w/2, self.y-self.h/2, self.x+self.w/3*2-self.w/2, self.y+self.h/3-self.h/2, fill=self.color, outline=self.color)
        canvas.create_rectangle(self.x-self.w/2, self.y+self.h/3-self.h/2, self.x+self.w-self.w/2, self.y+self.h/3*2-self.h/2, fill=self.color, outline=self.color)
        canvas.create_oval(self.x+self.w/6-self.w/2, self.y+self.h/3*2-self.h/2, self.x+self.w/6*2-self.w/2, self.y+self.h-self.h/2, fill="black")
        canvas.create_oval(self.x+self.w/6*4-self.w/2, self.y+self.h/3*2-self.h/2, self.x+self.w/6*5-self.w/2, self.y+self.h-self.h/2, fill="black")

def exit_clicked():
    frame.active = False

def key_handler(event):
    if(event.keycode == 32):
        bullets.append(Bullet(player.x, player.y - player.size/2, 0, -5, 10, "black"))

def make_car():
    return Car(50, 100, 10, 0, 100, "red")

frame = tkinter.Tk()
frame.geometry('600x800')
frame.title("課題4-3")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)
frame.protocol("WM_DELETE_WINDOW", exit_clicked)
frame.bind("<KeyPress>", key_handler)
frame.active = True

player = Player(300, 700, 50, "blue")
bullets = []
car = make_car()

while(frame.active):
    try:
        canvas.delete("all")

        if(not(car.isActive)):
            car = make_car()
        
        car.move()
        car.draw(canvas)
        
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
            bullets[i].draw(canvas)
        for i in range(len(remove_list)):
            bullets.pop(remove_list[i])
        
        frame.update()
        time.sleep(1/30)
    except Exception as e:
        print(str(e))
        break