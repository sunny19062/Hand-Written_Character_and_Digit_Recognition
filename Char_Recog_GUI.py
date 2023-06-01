from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np

model = load_model('model_hand.h5')
print("step1")

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    
    #predicting the class
    res = model.predict([img])[0]
    print(res)
    print(np.argmax(res))
    print(max(res))
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        
        # Creating elements
        
        
        self.label1 = tk.Label(self, text = "Welcome to our HCR",fg='red',font=("Helvetica", 20))
        
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Draw a capital letter..", font=("Helvetica", 40))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting)   
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        self.label2 = tk.Label(self, text = "this app is created by sunny kumar",fg='green',font=("Helvetica", 10))
        self.label3 = tk.Label(self, text = "                       Mohit Chauhan",fg='green',font=("Helvetica", 10))
        self.label4 = tk.Label(self, text = "                       Uday Pratap Singh",fg='green',font=("Helvetica", 10))
        self.label5 = tk.Label(self, text = "                       Jogit Singh",fg='green',font=("Helvetica", 10))
       
        # Grid structure
        self.label1.grid(row=0, column=0,pady=2, padx=2)
        self.canvas.grid(row=1, column=0, pady=2, sticky=W, )
        self.label.grid(row=1, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=2, column=1, pady=2, padx=2)
        self.button_clear.grid(row=2, column=0, pady=2)
        self.label2.grid(row=3, column=0,pady=2, padx=2)
        self.label3.grid(row=4, column=0,pady=2, padx=2)
        self.label4.grid(row=5, column=0,pady=2, padx=2)
        self.label5.grid(row=6, column=0,pady=2, padx=2)
        
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a,b,c,d = rect
        rect=(a+4,b+4,c-4,d-4)
        im = ImageGrab.grab(rect)
        word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
        digit, acc = predict_digit(im)
        img_pred = word_dict[digit]
        self.label.configure(text= str(img_pred)+', '+ str(int(acc*100))+'%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=10
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
print("step2")       
app = App()
mainloop()
