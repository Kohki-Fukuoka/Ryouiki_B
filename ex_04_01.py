import tkinter
import time

class Bullet:

    border_top = 0
    border_buttom = 400
    border_left = 0
    border_right = 600

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
        return (self.x < self.border_left) | (self.x > self.border_right) | (self.y < self.border_top) | (self.y > self.border_buttom)

    def hit(self):
        pass

    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)

class Player:

    border_left = 0
    border_right = 600

    def __init__(self, x, y, size, color):
        self.setPosition(x, y)
        self.setVisual(size, color)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setVisual(self, size, color):
        self.size = float(size)
        self.color = color
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.size/2, self.y, self.x + self.size/2, self.y + self.size/2, fill=self.color)
        canvas.create_rectangle(self.x - self.size/4, self.y - self.size/2, self.x + self.size/4, self.y, fill=self.color)

def exit_clicked():
    frame.active = False

frame = tkinter.Tk()
frame.geometry('600x400')
frame.title("課題2-1")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)
frame.protocol("WM_DELETE_WINDOW", exit_clicked)
frame.active = True

player = Player(300, 300, 50, "blue")
bullets = []

counter = 0

while(frame.active):
    counter += 1
    counter %= 30
    try:
        canvas.delete("all")
        player.draw(canvas)
        if(counter == 0):
            bullets.append(Bullet(player.x, player.y - player.size/2, 0, -5, 10, "black"))
        remove_list = []
        for i in range(len(bullets)):
            bullets[i].move()
            if(bullets[i].remove_flag()):
                remove_list.append(i)
                continue
            bullets[i].draw(canvas)
        for i in range(len(remove_list)):
            bullets.pop(remove_list[i])
        frame.update()
        time.sleep(1/30)
    except Exception as e:
        print(str(e))
        break