# -*- coding: utf-8 -*-

import PIL.Image as pil
from tkinter import Tk, Label, Menu, Canvas, PhotoImage, OptionMenu, IntVar, Button
from tkinter.filedialog import askopenfilename
import os
# Importations : PIL, Tkinter, OS


class Application(object):

    def __init__(self):

        self.master = Tk()
        self.master.geometry(newGeometry = '300x300')
        # Fenêtre tkinter

        self.menu = Menu(self.master)

        self.filemenu = Menu(self.menu,
                             tearoff = 0)
        self.filemenu.add_command(label = "Open", command = self.open)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = self.master.destroy)
        self.menu.add_cascade(label = "File",
                              menu = self.filemenu)

        self.master.config(menu = self.menu)
        # On crée un menu

        self.canvas = Canvas(master=self.master,
                             width=200,
                             height=200,
                             bg='#cccccc')

        self.canvas.place(x=150,
                          y=100,
                          anchor='center')

        Label(master=self.master,
              text='Preview',
              font='YuMinchoDemibold',
              foreground='white',
              background='#535353').place(x=120,
                                          y=190)

    def open(self):

        self.image_path = askopenfilename(initialdir = os.path.dirname(os.path.join(os.getcwd(), __file__)),
                                          filetypes = (("png files",".png"),
                                                       ("jpg files",".jpg"),
                                                       ("all files (risk)", ".")),
                                          defaultextension = ".png",
                                          title = "Open picture file")
        # on demande le fichier à ouvrir

        if self.image_path == "":
            # Si l'utilisateur choisit annuler
            return None
        else:
            pass

        self.pyimage = PhotoImage(file = self.image_path)
        print(self.image_path)
        self.PILimage = pil.open(self.image_path)

        if self.PILimage.size[0] > 200 or\
           self.PILimage.size[1] > 200:

            if self.PILimage.size[0] >= self.PILimage.size[1]:
                x = 200
                pourcentage = int(((200*100)/self.PILimage.size[0]))
                y = self.PILimage.size[1] - (self.PILimage.size[1]* (100 - pourcentage) /100)
            else:
                y = 200
                pourcentage = int(((200 * 100) / self.PILimage.size[1]))
                x = self.PILimage.size[0] - (self.PILimage.size[0] * (100 - pourcentage) / 100)

            Label(master = self.master,
                  text = 'Image resized \nfor preview ({}%)'.format(pourcentage),
                  font = 'YuMinchoDemibold 6',
                  fg = 'black').place(x=190,y=200)
            print('cc3')
            self.PILimage.resize((int(x),int(y)), pil.BILINEAR).save("tmp.png")
            self.pyimage = PhotoImage(file="tmp.png")
            os.remove('tmp.png')
            # On redimensionne l'image pour la preview

        self.image_tag = self.canvas.create_image(100,
                                                  100,
                                                  anchor = 'center',
                                                  image = self.pyimage)
        # On affiche l'image

        Label(master = self.master,
              text = 'Image original size:',
              font = 'YuMinchoDemibold 7',
              relief = 'groove').place(x = 20, y = 230)
        Label(master=self.master,
              text='({},{})'.format(self.PILimage.size[0],self.PILimage.size[1]),
              font='YuMinchoDemibold 8').place(x=37, y=250)

        Label(master=self.master,
              text='Choisir taille thumbnail:',
              font='YuMinchoDemibold 7',
              relief='groove').place(x=140, y=230)

        liste_valeurs = (30,50,100)

        self.taille_var = IntVar()
        self.menu_taille = OptionMenu(self.master,
                                      self.taille_var,
                                      *liste_valeurs)
        self.menu_taille.place(x=140, y=250)

        Button(master = self.master,
               text = 'Créer Thumbnail',
               font = 'YuMinchoDemibold 8',
               command = self.create_thumbnail).place(x=300,y=300,anchor='se')

    def create_thumbnail(self):

        if self.PILimage.size[0] >= self.PILimage.size[1]:
            x = self.taille_var.get()
            pourcentage = int(((x*100)/self.PILimage.size[0]))
            y = int(self.PILimage.size[1] - (self.PILimage.size[1] * (100-pourcentage)/100))
        else:
            y = self.taille_var.get()
            pourcentage = int(((y * 100) / self.PILimage.size[1]))
            x = int(self.PILimage.size[0] - (self.PILimage.size[0] * (100-pourcentage)/100))
        # On récupère les valeurs

        name = self.image_path.split('/')[-1].split(".")
        name = name[0] + 'THUMBNAIL.' + name[1]
        self.PILimage.resize((x,y),pil.BILINEAR).save(name)


def main():

    instance = Application()

    instance.master.mainloop()

main()

