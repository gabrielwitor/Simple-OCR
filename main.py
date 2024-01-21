from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import PIL
import re
import os

from ocr import ocr_detect

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255, 255, 255)

class paintGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Witor's Optical Character Recognition")
        
        self.brush_width = 15
        self.current_color = "#000000"
        
        self.cnv = Canvas(self.root, width = WIDTH - 10, height = HEIGHT - 10, bg = "white")
        self.cnv.pack()
        
        #binds mouse to function
        
        self.cnv.bind("<B1-Motion>",self.paint)
        
        self.image = PIL.Image.new("RGB",(WIDTH,HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)
        
        self.btn_frame = Frame(self.root)
        self.btn_frame.pack(fill=X)
        
        self.btn_frame.columnconfigure(0,weight=1)
        self.btn_frame.columnconfigure(1,weight=1)
        self.btn_frame.columnconfigure(2,weight=1)
        
        self.clear_btn = Button(self.btn_frame, text = "Clear", command = self.clear)
        self.clear_btn.grid(row = 0, column = 1, sticky = W+E)

        self.save_btn = Button(self.btn_frame, text = "Save", command = self.save)
        self.save_btn.grid(row = 0, column = 2, sticky = W+E)

        self.bplus_btn = Button(self.btn_frame, text = "Brush size +", command = self.brush_plus)
        self.bplus_btn.grid(row = 0, column = 0, sticky = W+E)
        
        self.bminus_btn = Button(self.btn_frame, text = "Brush size -", command = self.brush_minus)
        self.bminus_btn.grid(row = 1, column = 0, sticky = W+E)
        
        self.color_btn = Button(self.btn_frame, text = "Color", command = self.change_color)
        self.color_btn.grid(row = 1, column = 2, sticky = W+E)
        
        self.ocr_btn = Button(self.btn_frame, text = "OCR", bg="RED", fg="WHITE", command = self.ocr)
        self.ocr_btn.grid(row = 1, column = 1, sticky = W+E)
        
        self.pen_btn = Button(self.btn_frame, text = "Pen", command = self.set_pen)
        self.pen_btn.grid(row = 2, column = 2, sticky = W+E)
        
        self.eraser_btn = Button(self.btn_frame, text = "Eraser", command = self.set_eraser)
        self.eraser_btn.grid(row = 2, column = 0, sticky = W+E)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.attributes("-topmost",True)
        self.root.mainloop()
        
    def paint(self, event):
        x1,y1 = (event.x - 1), (event.y - 1)
        x2,y2 = (event.x + 1), (event.y + 1)
        self.cnv.create_rectangle(x1,y1,x2,y2,outline = self.current_color, fill = self.current_color, width=self.brush_width)
        self.draw.rectangle([x1,y1,x2 + self.brush_width, y2 + self.brush_width], outline = self.current_color, fill = self.current_color, width=self.brush_width)
        
    
    def clear(self):
        self.cnv.delete("all")
        # self.draw.rectange([0,0,1000,1000],fill="white")
        self.draw.rectangle([0,0,1000,1000],fill="#FFFFFF")
    
    def save(self):
        filename = filedialog.asksaveasfilename(initialfile="untitled.png", defaultextension="png", filetypes=[("PNG", ".png"),("JPG", ".jpg")])
    
        if filename != "":
            self.image.save(filename)
            
    def brush_plus(self):
        self.brush_width += 1
    
    def brush_minus(self):
        if self.brush_width > 1:
            self.brush_width -= 1
    
    def change_color(self):
        _, self.current_color = colorchooser.askcolor(title="Choose a color")
        
    def ocr(self):
        self.image.save('ocr.png')
        ocr_detected = ocr_detect()
        ocr_detected = re.sub(r'[^a-zA-Z0-9]', '', ocr_detected)

        os.remove("ocr.png")
        
        messagebox.showinfo(title="OCR", message=f"Detected by OCR: {ocr_detected}", parent=self.root)
        
    def set_pen(self):
        self.current_color = "black"
    
    def set_eraser(self):
        self.current_color = "white"
    
    def on_closing(self):
        answer = messagebox.askyesnocancel("Quit", "Do you want to save the image?", parent=self.root)
        if answer is not None:
            if answer:
                self.save()
            self.root.destroy()
            exit(0)
            
    
        
paintGUI()