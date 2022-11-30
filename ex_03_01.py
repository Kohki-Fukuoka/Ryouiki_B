import tkinter
import time

class Car:

    def __init__(self, size, color):
        self.size = size
        self.color = color

    def setBorder(self, bleft, bright, btop, bbottom):
        self.bl = bleft
        self.br = bright
        self.bt = btop
        self.bb = bbottom

    def setPos(self, x, y):
        self.x = x
        self.y = y
    
    def setMovement(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if((self.x < self.bl) | (self.x + self.size > self.br)):
            self.vx *= -1
            self.x += self.vx * 2
        if((self.y < self.bt) | (self.y + self.size > self.bb)):
            self.vy *= -1
            self.y += self.vy * 2

    def draw(self, canvas):
        #canvas.create_arc(100+10, 100, 250+10, 250, extent=45, start=157.5, outline="yellow", fill="yellow")

        w=self.size
        h=self.size/2

        canvas.create_rectangle(self.x+w/3, self.y, self.x+w/3*2, self.y+h/3, fill=self.color, outline=self.color)
        canvas.create_rectangle(self.x, self.y+h/3, self.x+w, self.y+h/3*2, fill=self.color, outline=self.color)
        canvas.create_oval(self.x+w/6, self.y+h/3*2, self.x+w/6*2, self.y+h, fill="black")
        canvas.create_oval(self.x+w/6*4, self.y+h/3*2, self.x+w/6*5, self.y+h, fill="black")

        #canvas.create_text(300, 300, anchor=tkinter.CENTER, fill="black", text="Kohki Fukuoka", font=("",20))


frame = tkinter.Tk()
frame.geometry('600x400')
frame.title("課題2-1")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)

car = Car(100, "#FF0000")
car.setBorder(0, 600, 0, 400)
car.setPos(250, 150)
car.setMovement(10, 0)

while(canvas != None):
    try:
        canvas.delete("all")
        car.move()
        car.draw(canvas)
        frame.update()
        time.sleep(1/60)
    except:
        print("error")
        break