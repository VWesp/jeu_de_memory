if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from tkinter.font import Font
    from functools import partial
    import numpy as np
    import os
    import random
    import traceback
    import uuid
    import time

    class Application(tk.Frame):

        def __init__(self, master=None):
            tk.Frame.__init__(self, master)
            self.master = master
            self.initWindow()

        def initWindow(self):
            self.tiles = {}
            self.loadTiles("tiles")
            self.tiles_ids = list(self.tiles.keys())
            random.shuffle(self.tiles_ids)
            self.button_frame = tk.Frame(self.master)
            self.button_frame.pack(pady=10)
            self.buttons = []
            self.buttons_clicked = np.zeros(len(self.tiles_ids), dtype=bool)
            self.clicked_id = None
            self.clicked_pos = None
            for i in range(len(self.tiles_ids)):
                id = self.tiles_ids[i]
                if(self.tiles[id]["type"] == "image"):
                    button = tk.Button(self.button_frame, image=self.tiles[id]["default"], width=95, height=95, command=partial(self.clickButton, i, id))
                    button.grid(row=int(i/4), column=int(i%4))
                    self.buttons.append(button)
                elif(self.tiles[id]["type"] == "text"):
                    button = tk.Button(self.button_frame, text=self.tiles[id]["default"], width=13, height=6, command=partial(self.clickButton, i, id))
                    button.grid(row=int(i/4), column=int(i%4))
                    self.buttons.append(button)

        def clickButton(self, pos, id):
            if(self.tiles[id]["type"] == "image"):
                self.buttons[pos].configure(image=self.tiles[id]["value"])
            elif(self.tiles[id]["type"] == "text"):
                self.buttons[pos].configure(text=self.tiles[id]["value"])

            if(self.clicked_id == None):
                self.clicked_id = id
                self.clicked_pos = pos
            elif(id != self.clicked_id):
                if(self.tiles[id]["partner"] == self.clicked_id):
                    self.buttons[pos].config(command=0)
                    self.buttons[pos].config(bg="green")
                    self.buttons[self.clicked_pos].config(command=0)
                    self.buttons[self.clicked_pos].config(bg="green")
                else:
                    default_color = self.buttons[pos].cget("background")
                    self.buttons[pos].config(bg="red")
                    self.buttons[self.clicked_pos].config(bg="red")
                    tk.messagebox.showerror(title="No match", message="No match!")
                    self.buttons[pos].config(bg=default_color)
                    self.buttons[self.clicked_pos].config(bg=default_color)
                    if(self.tiles[id]["type"] == "image"):
                        self.buttons[pos].configure(image=self.tiles[id]["default"])
                    elif(self.tiles[id]["type"] == "text"):
                        self.buttons[pos].configure(text=self.tiles[id]["default"])

                    if(self.tiles[self.clicked_id]["type"] == "image"):
                        self.buttons[self.clicked_pos].configure(image=self.tiles[self.clicked_id]["default"])
                    elif(self.tiles[self.clicked_id]["type"] == "text"):
                        self.buttons[self.clicked_pos].configure(text=self.tiles[self.clicked_id]["default"])

                self.clicked_id = None
                self.clicked_pos = None


        def loadTiles(self, path):
            for file in os.listdir(path):
                filename = ".".join(file.split(".")[:-1])
                extension = file.split(".")[-1]
                current_id = uuid.uuid4().hex
                self.tiles[current_id] = {}
                for id in self.tiles:
                    if(id != current_id and self.tiles[id]["name"] == filename):
                        self.tiles[id]["partner"] = current_id
                        self.tiles[current_id]["partner"] = id
                        break

                self.tiles[current_id]["name"] = filename
                if(extension == "png"):
                    self.tiles[current_id]["type"] = "image"
                    blank_image = tk.PhotoImage(file="blank.png")
                    self.tiles[current_id]["default"] = blank_image.subsample(5)
                    image = tk.PhotoImage(file=path+"/"+file)
                    self.tiles[current_id]["value"] = image.subsample(5)
                elif(extension == "txt"):
                    self.tiles[current_id]["type"] = "text"
                    self.tiles[current_id]["default"] = " "
                    with open(path+"/"+file, encoding="utf-8") as text:
                        self.tiles[current_id]["value"] = text.readline().strip()


    try:
        root = tk.Tk()
        root.style = ttk.Style()
        root.style.theme_use("clam")
        root.title("Jeu de Memory")
        root.geometry("500x500")

        Application(root)
        root.mainloop()
    except Exception as ex:
        tk.messagebox.showwarning("Critical error", "A critical error occurred while executing the program. See the message below for more details:\n\n"
                             + traceback.format_exc())
