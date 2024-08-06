# -*- coding: utf-8 -*-
import tkinter as tk


def init_Graph(self):
    self.line_height = 0
    self.tailleTitleReduc=30
    self.padding=2
    
    self.selected_button_extReduc = tk.IntVar(value=1)
    
    self.toolbar = tk.Frame(self)
    self.toolbar.grid(row=0, column=0, sticky="ew")
    
    self.extendButton = tk.Button(self.toolbar, text="Extend", command=self.on_extendButton_click)
    self.extendButton.pack(side=tk.LEFT, padx=5, pady=5)
    self.ReducButton = tk.Button(self.toolbar, text="Reduce", command=self.on_ReducButton_click)
    self.ReducButton.pack(side=tk.LEFT, padx=5, pady=5)
    self.extendButton.config(relief=tk.SUNKEN if self.selected_button_extReduc.get() == 1 else tk.RAISED)
    self.ReducButton.config(relief=tk.SUNKEN if self.selected_button_extReduc.get() == 2 else tk.RAISED)
    
    self.RecenteredButton = tk.Button(self.toolbar, text="Align", command=self.on_RecenteredButton_click)
    self.RecenteredButton.pack(side=tk.LEFT, padx=5, pady=5)
    
    self.expert_mode = 0
    self.ExpertButton = tk.Button(self.toolbar, text=self.getComplex, command=self.on_ExpertButton_click)
    self.ExpertButton.pack(side=tk.RIGHT, padx=5, pady=5)
    
    self.canvas_frame = tk.Frame(self)
    self.canvas_frame.grid(row=1, column=0, sticky="nsew")
    
    self.canvas = tk.Canvas(self.canvas_frame, bg='white')
    self.canvas.grid(row=0, column=0, sticky="nsew")
    
    self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
    self.scrollbar_x.grid(row=1, column=0, sticky="ew")
    self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
    self.scrollbar_y.grid(row=0, column=1, sticky="ns")
    
    self.canvas.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

    #Configure le poids des lignes et des colonnes pour rendre le canevas extensible
    self.grid_rowconfigure(0, weight=0)  #Ligne 0 pour la "toolbar" avec les bouton "Extend", "Reduce" et "Recenter"
    self.grid_rowconfigure(1, weight=1)  #Ligne 1 pour le "canvas_frame" avec le graphe
    self.grid_columnconfigure(0, weight=1)
    self.canvas_frame.grid_rowconfigure(0, weight=1)
    self.canvas_frame.grid_columnconfigure(0, weight=1)

    #Lier les "events" de la souris sur le canvas
    self.canvas.bind("<ButtonPress-1>", self.on_node_click)
    self.canvas.bind("<B1-Motion>", self.on_node_drag)
    
    self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
    self.canvas.bind("<Shift-MouseWheel>", self._on_shift_mouse_wheel)
        
def delete(self):
    self.canvas.delete("all")
    
#Permet de scroller avec la roulette de la souris quand la souris est relâchée.
def on_mouse_wheel(self, event):
    self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

#Permet de scroller avec la roulette de la souris quand la souris est enfoncée.
def on_shift_mouse_wheel(self, event):
    self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

#Retourne la taille du nœud (XRight, YDown) quand il est réduit ou étendu
#Retourne la position (X, Y) centrale du bouton de réduction/extantion
def getTailleBox(self, node):
    txt = None
    text_lines = self.G.nodes[node]['contenue'].split('\n')
    if self.G.nodes[node]['reduced']>0:
        if len(text_lines[0])>self.tailleTitleReduc:
            txt = text_lines[0][:self.tailleTitleReduc] + " ..."
        else:
            txt=text_lines[0]
    else:
        txt=self.G.nodes[node]['contenue']
    text_id = self.canvas.create_text(0, 0, text=txt, fill='black', anchor='nw')
    bbox = self.canvas.bbox(text_id)
    self.canvas.delete(text_id)
    
    text_id = self.canvas.create_text(0, 0, text=text_lines[0], fill='black', anchor='nw')
    bboxTitle = self.canvas.bbox(text_id)
    self.canvas.delete(text_id)
    
    if self.G.nodes[node]['reduced']>0:
        self.line_height = bbox[3] - bbox[1]
        if len(self.G.nodes[node]['pointeur'])==0:
            return (bbox[2]+self.line_height+3*self.padding, bbox[3]+2*self.padding), (bbox[2]+2*self.padding+self.line_height/2, self.padding+self.line_height/2), (bboxTitle[2]+self.padding, bboxTitle[3]+self.padding)
        else:
            return (bbox[2]+2*self.line_height+4*self.padding, bbox[3]+2*self.padding), (bbox[2]+2*self.padding+self.line_height/2, self.padding+self.line_height/2), (bboxTitle[2]+self.padding, bboxTitle[3]+self.padding)
    else:
        self.line_height = (bbox[3] - bbox[1]) / len(text_lines)
        return (bbox[2]+self.line_height+3*self.padding, bbox[3]+2*self.padding), (bbox[2]+2*self.padding+self.line_height/2, self.padding+self.line_height/2), (bboxTitle[2]+self.padding, bboxTitle[3]+self.padding)

#Configure le scroll pour pouvoir scroller et donc observer tous les nœuds
def scrollregion(self):
    if self.G.number_of_nodes() >0:
        max_x = max(self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0] for node in self.G.nodes() if self.G.nodes[node]['pos'] != None)
        max_x = max(max_x+25, self.canvas.winfo_width())
        max_y = max(self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1] for node in self.G.nodes() if self.G.nodes[node]['pos'] != None)
        max_y = max(max_y+25, self.canvas.winfo_height())
        
        min_x = min(self.G.nodes[node]['pos'][0] for node in self.G.nodes() if self.G.nodes[node]['pos'] != None)
        min_x = min(min_x-25, 0)
        min_y = min(self.G.nodes[node]['pos'][1] for node in self.G.nodes() if self.G.nodes[node]['pos'] != None)
        min_y = min(min_y-25, 0)

        self.canvas.config(scrollregion=(min_x, min_y, max_x, max_y))
    else:
        self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))
    
#Dessine la boite, le carré du noeud "node" qu'il soit réduit ou étandu, avec le texte en conséquence, le bouton réduction/extantion,
# si le nœud est étendu, dessine aussi les lignes entre les lignes de texte et dessine les boules des pointeurs
# si le nœud est réduit, dessine aussi la boule pointeur du nœud réduit
def boite(self, node):
    if self.G.nodes[node]['pos'] ==None:
        return
    txt = None
    if self.G.nodes[node]['reduced']>0:
        text_lines = self.G.nodes[node]['contenue'].split('\n')
        if len(text_lines[0])>self.tailleTitleReduc:
            txt = text_lines[0][:self.tailleTitleReduc] + " ..."
        else:
            txt=text_lines[0]
    else:
        txt=self.G.nodes[node]['contenue']
    self.canvas.create_rectangle(self.G.nodes[node]['pos'][0], self.G.nodes[node]['pos'][1], self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0], self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1], fill=self.G.nodes[node]['couleur'], tags=node)
    if self.G.nodes[node]['reduced']>0:
        self.canvas.create_rectangle(self.G.nodes[node]['pos'][0]+self.padding, self.G.nodes[node]['pos'][1]+self.padding, self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]-(self.line_height/2)-self.padding, self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1]-self.padding, fill="yellow", outline='', tags=node)
    else:
        self.canvas.create_rectangle(self.G.nodes[node]['pos'][0]+self.padding, self.G.nodes[node]['pos'][1]+self.padding, self.G.nodes[node]['pos'][0] + self.G.nodes[node]['tailleTitre'][0], self.G.nodes[node]['pos'][1] + self.line_height+self.padding, fill="yellow", outline='', tags=node)
        parts = self.G.nodes[node]['contenue'].rsplit('\n', 1)
        if len(parts)>1:
            if parts[1]==self.sentenceSeeMore100:
                self.canvas.create_rectangle(self.G.nodes[node]['pos'][0], self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1]-self.line_height-self.padding, self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0], self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1], fill="cyan", outline='', tags=node)
    self.canvas.create_text(self.G.nodes[node]['pos'][0]+self.padding, self.G.nodes[node]['pos'][1]+self.padding, text=txt, fill='black', anchor='nw', tags=node)
    creeReducBox(self, node)
    if self.G.nodes[node]['reduced']>0:
        CreePointerReduced(self, node)
    else:
        CreeLineAndPointer(self, node)

#Est une sous-fonction de "boite"
#Dessine le bouton reduce/extande: le carré blanc avec "-" ou "+"
def creeReducBox(self,node):
    xLTitle = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]-(self.line_height/2-2)
    xRTitle = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+(self.line_height/2-2)
    yTTitle = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-(self.line_height/2-2)
    yDTitle = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+(self.line_height/2-2)
    self.canvas.create_rectangle(xLTitle, yTTitle, xRTitle, yDTitle,fill='white', outline='black', tags=node)
    
    if self.G.nodes[node]['reduced']>0:
        self.canvas.create_text(self.G.nodes[node]['pos'][0]+self.G.nodes[node]['reduc'][0], self.G.nodes[node]['pos'][1]+self.G.nodes[node]['reduc'][1], text="+", fill='black', anchor='center', tags=node)
    else:
        self.canvas.create_text(self.G.nodes[node]['pos'][0]+self.G.nodes[node]['reduc'][0], self.G.nodes[node]['pos'][1]+self.G.nodes[node]['reduc'][1], text="-", fill='black', anchor='center', tags=node)

#Est une sous-fonction de "boite"
#Dessine le rond du pointeur "pB" du nœud "node" quand ce nœud est sous forme réduite et qu'il a des pointeurs
def CreePointerReduced(self,node):
    if len(self.G.nodes[node]['pointeur'])<1:
        return
    xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2+self.padding+2
    xRigh = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height+(self.line_height/2)+self.padding-2
    yTop = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-(self.line_height/2)+2
    yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+(self.line_height/2)-2
    if self.G.nodes[node]['reduced']==2:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='orange', outline='black', tags=node)
    elif self.G.nodes[node]['reduced']==3:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='green', outline='black', tags=node)
    else:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='red', outline='black', tags=node)

#Est une sous-fonction de "boite"
#Dessine dans la boite du nœud "node" les lignes entre chaque ligne de texte et lance "DrawPointeur" pour chaque pointeur du node
def CreeLineAndPointer(self,node):
    text_lines=self.G.nodes[node]['contenue'].split('\n')
    for i, line in enumerate(text_lines):
        y_line = self.padding + (i * self.line_height)
        if i==0:
            continue
        else:
            self.canvas.create_line(self.G.nodes[node]['pos'][0], self.G.nodes[node]['pos'][1] + y_line, self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0], self.G.nodes[node]['pos'][1] + y_line, fill='black', tags=node)

            for pointeurNode in range(len(self.G.nodes[node]['pointeur'])):
                if line == self.G.nodes[node]['pointeur'][pointeurNode]['name']:
                    self.G.nodes[node]['pointeur'][pointeurNode]['pSize'] = (self.G.nodes[node]['taille'][0]-self.line_height-self.padding, y_line, self.G.nodes[node]['taille'][0]-self.padding, y_line+self.line_height)
                    DrawPointeur(self, node, pointeurNode)
                    break

#Est une sous-fonction de "boite"
#Dessine le rond du pointeur "pB" du nœud "node" quand ce nœud est sous forme agrandie
def DrawPointeur(self, node, pB):
    xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][0]+2
    xRigh = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][2]-2
    yTop  = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][1]+2
    yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][3]-2
    if self.G.nodes[node]['pointeur'][pB]['visible']:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='green', outline='black', tags=node)
    else:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='red', outline='black', tags=node)
        
def changeReducPointOrange(self, node):
    xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2+self.padding+2
    xRigh = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height+(self.line_height/2)+self.padding-2
    yTop = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-(self.line_height/2)+2
    yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+(self.line_height/2)-2
    self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='orange', outline='black', tags=node)
    

#Dessine une arête
def line(self,node1,node2,pB):
    if self.G.nodes[node1]['pos'] ==None or self.G.nodes[node2]['pos'] ==None:
        return
    start_pos = None
    if self.G.nodes[node1]['reduced']==0:
        start_pos = (self.G.nodes[node1]['pos'][0] + (self.G.nodes[node1]['pointeur'][pB]['pSize'][0] + self.G.nodes[node1]['pointeur'][pB]['pSize'][2])/2, self.G.nodes[node1]['pos'][1] + (self.G.nodes[node1]['pointeur'][pB]['pSize'][1]+self.G.nodes[node1]['pointeur'][pB]['pSize'][3])/2) 
    else:
        start_pos = (self.G.nodes[node1]['pos'][0] + self.G.nodes[node1]['reduc'][0] + self.line_height + self.padding, self.G.nodes[node1]['pos'][1]+self.G.nodes[node1]['reduc'][1])                 
    end_pos = (self.G.nodes[node2]['pos'][0], self.G.nodes[node2]['pos'][1] + self.G.nodes[node2]['taille'][1]/2)
    self.canvas.create_line(start_pos, end_pos, arrow=tk.LAST, arrowshape=(10, 12, 5), width=2)
        
def getX(self, x):
    return self.canvas.canvasx(x)

def getY(self, y):
    return self.canvas.canvasy(y)