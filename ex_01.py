import tkinter

frame = tkinter.Tk()
frame.geometry('600x400')
frame.title("課題1-2")
canvas = tkinter.Canvas(frame, bg = "white")
canvas.pack(fill=tkinter.BOTH, expand=True)

canvas.create_arc(100+10, 100, 250+10, 250, extent=45, start=157.5, outline="yellow", fill="yellow")

canvas.create_rectangle(250, 100, 350, 150, fill="black")
canvas.create_rectangle(175, 150, 425, 200, fill="black")
canvas.create_oval(200, 200, 250, 250, fill="black")
canvas.create_oval(350, 200, 400, 250, fill="black")

canvas.create_text(300, 300, anchor=tkinter.CENTER, fill="black", text="Kohki Fukuoka", font=("",20))

print("open picture")

frame.mainloop()

print("picture was closed")