import tkinter

def draw_car(x, y, size, rgb):
    #canvas.create_arc(100+10, 100, 250+10, 250, extent=45, start=157.5, outline="yellow", fill="yellow")

    w=size
    h=size/2

    canvas.create_rectangle(x+w/3, y, x+w/3*2, y+h/3, fill=rgb, outline=rgb)
    canvas.create_rectangle(x, y+h/3, x+w, y+h/3*2, fill=rgb, outline=rgb)
    canvas.create_oval(x+w/6, y+h/3*2, x+w/6*2, y+h, fill="black")
    canvas.create_oval(x+w/6*4, y+h/3*2, x+w/6*5, y+h, fill="black")

    #canvas.create_text(300, 300, anchor=tkinter.CENTER, fill="black", text="Kohki Fukuoka", font=("",20))


frame = tkinter.Tk()
frame.geometry('620x620')
frame.title("課題2-2")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)

for i in range(0, 10):
    for j in range(0, 10):
        if((i+j)%2==0):
            draw_car(10+60*j, 10+60*i, 50, "#FF0000")
        else:
            draw_car(10+60*j, 10+60*i, 50, "#00FF00")

print("open picture")
frame.mainloop()
print("picture was closed")