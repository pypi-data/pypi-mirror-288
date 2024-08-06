# -*- coding: utf-8 -*-
from thonnycontrib.data_visualization.Graphical import graphic
import networkx as nx

def init_DB(self):
    self.setReduc=0
    self.spaceBorderRecent=15
    self.G = nx.DiGraph()
    graphic.init_Graph(self)
    
def clearAll(self):
    self.G.clear()
    graphic.delete(self)
    graphic.scrollregion(self)

#Permet de scroller avec la roulette de la souris quand la souris est relâchée.
def on_mouse_wheel(self, event):
    graphic.on_mouse_wheel(self, event)

#Permet de scroller avec la roulette de la souris quand la souris est enfoncée.
def on_shift_mouse_wheel(self, event):
    graphic.on_shift_mouse_wheel(self, event)

def addEdge(self, startNode, endNode, startPointer):
    if isThereNode(self, startNode) and isThereNode(self, endNode):
        if self.G.has_edge(startNode, endNode):
            if startPointer in self.G.edges[(startNode, endNode)]['start']:
                return
            else:
                self.G.edges[(startNode, endNode)]['start'].add(startPointer)
        else:
            self.G.add_edges_from([(startNode, endNode,{'start':{startPointer}})], arrowstyle='->', arrowsize=10)

def removeEdge(self, edgeCreated):
    edges = list(self.G.edges())
    for i in edges:
        ed = self.G.edges[(i[0], i[1])]['start']
        for startPointer in ed:
            if (i[0],i[1],startPointer) not in edgeCreated:
                if len(self.G.edges[(i[0], i[1])]['start'])<=1:
                    self.G.remove_edge(i[0], i[1])
                else:
                    self.G.edges[(i[0], i[1])]['start'].remove(startPointer)

def addNode(self, idNode, text = ""):
    if idNode == "Globals":
        self.G.add_nodes_from([('Globals', {'contenue': f'Globals', 'type': 'TypeA', 'couleur': 'deep sky blue', 'pos': (self.spaceBorderRecent, self.spaceBorderRecent), 'taille':(0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'tailleTitre':(0,0), 'pointeur': []})])
    elif idNode == "Locals":
        #Positionne le nœud "local" en dessous du graphe déjà existant
        newY=self.spaceBorderRecent
        for n in self.G.nodes:
            if self.G.nodes[n]['pos'][1] + self.G.nodes[n]['taille'][1]+15>newY:
                newY=self.G.nodes[n]['pos'][1] + self.G.nodes[n]['taille'][1]+15
        self.G.add_nodes_from([('Locals', {'contenue': f'Locals', 'type': 'TypeB', 'couleur': 'lime green', 'pos': (self.spaceBorderRecent, newY), 'taille':(0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'tailleTitre':(0,0), 'pointeur': []})])
    else:
        self.G.add_nodes_from([(idNode,{'contenue': text, 'type': 'TypeC', 'couleur': 'turquoise', 'pos': None, 'taille':(0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'tailleTitre':(0,0), 'pointeur': []})])

#Rajoute du texte à "node"
def addNodeText(self, node, text, newLigne=True):
    if newLigne:
        self.G.nodes[node]['contenue']+="\n"+text
    else:
        self.G.nodes[node]['contenue']+=text

#Retire à "G" tous les nœuds qui ne se trouvent pas dans "self.nodeCreated"
def removeNode(self, nodeCreated):
    nodes = dict(self.G.nodes())
    for i in nodes:
        if i not in nodeCreated:
            self.G.remove_node(i)

#Remets le nœud "node" à zéro, en gardant sa position et juste en lui retirant ses pointeurs et son texte
def nodeReset(self, node):
        self.G.nodes[node]['contenue'] = self.G.nodes[node]['contenue'].split("\n")[0]
        self.G.nodes[node]['pointeur'] = []

#Rajoute un pointeur dans le graphe
def addPointeur(self,nodeParent, namePointeur, idPointeur, createdFromParent):
    if namePointeur in createdFromParent:
        self.G.nodes[nodeParent]['pointeur'].append({'name':namePointeur,'id':idPointeur,'visible':createdFromParent[namePointeur],'pSize':(0,0,0,0)})
    else:
        self.G.nodes[nodeParent]['pointeur'].append({'name':namePointeur,'id':idPointeur,'visible':False,'pSize':(0,0,0,0)})

#Change le pointeur "pB" de node à l’état ouvert ou fermé
def changePointeur(self, node, pB):
    self.G.nodes[node]['pointeur'][pB]['visible'] = not self.G.nodes[node]['pointeur'][pB]['visible']

#Est utilisé quand le nœud "node" est réduit
#Fixe la valeur de "self.G.nodes[node]['reduced']" en fonction des pointeurs de node et de leur état
#Change la taille de la boîte node et la taille de "reduc" (le carré blanc avec + et -)
def changeReduc(self, node):
    if self.G.nodes[node]['reduced'] == 0:
        if len(self.G.nodes[node]['pointeur'])<1:
            self.G.nodes[node]['reduced'] = 1 #Le nœud est réduit et n'a pas de pointeur
        else:
            change = False
            etat = self.G.nodes[node]['pointeur'][0]['visible']
            for i in self.G.nodes[node]['pointeur']:
                if i['visible'] != etat:
                    change=True
                    break
            if change:
                self.G.nodes[node]['reduced'] = 2 #Le nœud est réduit avec des pointeurs à l’état ouvert et fermé
            elif etat==True:
                self.G.nodes[node]['reduced'] = 3 #Le nœud est réduit avec seulement des pointeurs à l’état ouvert
            else:
                self.G.nodes[node]['reduced'] = 4 #Le nœud est réduit avec seulement des pointeurs fermés
    else:
        self.G.nodes[node]['reduced'] = 0 #Le nœud n'est pas réduit
    self.G.nodes[node]['taille'], self.G.nodes[node]['reduc'], self.G.nodes[node]['tailleTitre'] = graphic.getTailleBox(self, node)

#Est utilisé quand l'utilisateur clique sur la boule pointeur verte, orange ou rouge quand le nœud est sous forme réduite et qu'il a des pointeurs
#Change "self.G.nodes[node]['reduced']" (aller voir "changeReduc" pour savoir à quoi correspondent les valeurs possibles)
#Ferme ou ouvre en même temps tous les pointeurs de "node"
def changeReducPointeur(self, node):
    if self.G.nodes[node]['reduced']==2 or self.G.nodes[node]['reduced']==4 :
        self.G.nodes[node]['reduced'] = 3
        for pB in range(len(self.G.nodes[node]['pointeur'])):
            self.G.nodes[node]['pointeur'][pB]['visible']=True
    else:
        self.G.nodes[node]['reduced'] = 4
        for pB in range(len(self.G.nodes[node]['pointeur'])):
            self.G.nodes[node]['pointeur'][pB]['visible']=False
            
def changeReducPointOrange(self, node):
    self.G.nodes[node]['reduced']=2
    graphic.changeReducPointOrange(self, node)

#Affiche tout le graphe avec toute modification qui aurait été faite avant
def draw_graph(self):
    graphic.delete(self)
    for node in self.G.nodes():
        self.G.nodes[node]['visible']=False
    if self.G.has_node('Globals'):
        drawGraphIter(self, 'Globals')
    if self.G.has_node('Locals'):
        drawGraphIter(self, 'Locals')
    
    graphic.scrollregion(self)

#Suite/iteration de "draw_graph"
def drawGraphIter(self, node):
    self.G.nodes[node]['visible']=True

    #Trouve/vérifie la taille et la position de "reduc" de la boîte du nœud "node"
    self.G.nodes[node]['taille'], self.G.nodes[node]['reduc'], self.G.nodes[node]['tailleTitre'] = graphic.getTailleBox(self, node)
    #dessine "node"
    graphic.boite(self, node)
    for i in range(len(self.G.nodes[node]['pointeur'])):#Parcours tous les pointeurs pour trouver des nœuds enfant à afficher
        if self.G.nodes[node]['pointeur'][i]['visible']:
            for edge in self.G.out_edges(node):
                if self.G.nodes[node]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                    if self.G.nodes[edge[1]]['visible'] == False:#Itère si le nœud enfant n'est pas encore affiché
                        drawGraphIter(self, edge[1])
                    graphic.line(self, node, edge[1], i)#Affiche l'arête du nœud parent vers le nœud enfant
                    break

#Est appelé pour tout recentrer
def reCentrer(self):
    #Retire tout ce qui est affiché et mets tout à visible = False
    graphic.delete(self)
    for node in self.G.nodes():
        self.G.nodes[node]['visible']=False
    
    lowestY=None #lowestY = la coordonnée la plus basse du graphe sans le nœud "Locals" et ses enfants
    if self.G.has_node('Globals'):
        lowestY=self.spaceBorderRecent
        lowestY=reCentrerIter(self, 'Globals', self.spaceBorderRecent, self.spaceBorderRecent, lowestY)
    
    if self.G.has_node('Locals'):
        Y=self.spaceBorderRecent
        if lowestY:
            Y=lowestY+15
        reCentrerIter(self, 'Locals', self.spaceBorderRecent, Y, lowestY)
    
    graphic.scrollregion(self)

#Suite/iteration de "reCentrer"
def reCentrerIter(self, node, X, Y, lowestY):
    self.G.nodes[node]['visible']=True
    self.G.nodes[node]['pos'] = (X, Y)
    find_non_overlapping_position(self, node)
    graphic.boite(self, node)
    
    if self.G.nodes[node]['pos'][1]+self.G.nodes[node]['taille'][1]>lowestY:
        lowestY=self.G.nodes[node]['pos'][1]+self.G.nodes[node]['taille'][1]
    
    for i in range(len(self.G.nodes[node]['pointeur'])):#Trouve tous les nœuds enfant qui doivent être affichés
        if self.G.nodes[node]['pointeur'][i]['visible']:
            for edge in self.G.out_edges(node):
                if self.G.nodes[node]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                    if self.G.nodes[edge[1]]['visible'] == False:
                        #Calcule la nouvelle position du nœud enfant trouvé à afficher et itère dessus
                        newX = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0]+15
                        newY = self.G.nodes[node]['pos'][1]
                        lowestY = reCentrerIter(self, edge[1], newX, newY, lowestY)
                    #Afficher l’arête du nœud parent vers le nœud enfant
                    graphic.line(self, node, edge[1], i)
                    break
    
    return lowestY

#Change la position d’un nœud quand il est bougé et dessine tout le graphe en conséquence
def moveNode(self, event, node, offset):
    if node is not None:
        new_x = graphic.getX(self, event.x) - offset[0]
        new_y = graphic.getY(self, event.y) - offset[1]

        self.G.nodes[node]['pos'] = (new_x, new_y)
        draw_graph(self)

#Est appelé quand un nouveau nœud est créé et doit être affiché, il vient du pointeur "pB" du nœud "node"
#Affiche l’arête du nœud parent "node" vers le nouveau nœud, le nouveau nœud et tous les nœuds/arêtes suivants qui devraient être visibles
def showNodeEdge(self, node, pB, FromExtend = True):
    self.G.nodes[node]['pointeur'][pB]['visible'] = not self.G.nodes[node]['pointeur'][pB]['visible']
    if FromExtend:
        graphic.DrawPointeur(self, node, pB)#Change la couleur du pointeur "pB" si cette fonction est appelée de l'ouverture d'un pointeur d'un nœud qui est étandu
    for edge in self.G.out_edges(node):
        if self.G.nodes[node]['pointeur'][pB]['name'] in self.G.edges[edge]['start']:
            showIter(self, node, edge[1], pB)

    graphic.scrollregion(self)

#Suite/iteration de "showNodeEdge"
def showIter(self, node1, node2, pB):
    if self.G.nodes[node2]['visible']: #Affiche l’arête si le nœud est déjà affiché et s’arrête là
        graphic.line(self, node1, node2, pB)
        return
    else:
        if self.G.nodes[node2]['pos']==None: #Trouve une position au nœud s'il n'en a pas encore
            newX = self.G.nodes[node1]['pos'][0] + self.G.nodes[node1]['taille'][0]+15
            newY = self.G.nodes[node1]['pos'][1]
            self.G.nodes[node2]['pos'] = (newX, newY)
            self.G.nodes[node2]['taille'], self.G.nodes[node2]['reduc'], self.G.nodes[node2]['tailleTitre'] = graphic.getTailleBox(self, node2)
            find_non_overlapping_position(self, node2)
        else:
            self.G.nodes[node2]['taille'], self.G.nodes[node2]['reduc'], self.G.nodes[node2]['tailleTitre'] = graphic.getTailleBox(self, node2)
        self.G.nodes[node2]['visible']=True
        
        #Enregistre la taille et la position du bouton "extend/reduc" du nouveau nœud
        
        # Dessine le nouveau nœud et l’arête du nœud parent vers le nouveau nœud
        graphic.boite(self, node2)
        graphic.line(self, node1, node2, pB)
        
        for i in range(len(self.G.nodes[node2]['pointeur'])):#Cherche le nœud suivant parmi tous les pointeurs ouverts du nouveau nœud et lance le depth first search
            if self.G.nodes[node2]['pointeur'][i]['visible']:
                for edge in self.G.out_edges(node2):
                    if self.G.nodes[node2]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                        showIter(self, node2, edge[1], i)
                        break

#Est utilisé quand il faut recentrer ou qu'un nœud n'a pas encore de position, permet de trouver le "YDown+15" le plus bas parmi tous les nœuds enfant visibles de "node"
#Retourne un Y = YUp du nœud node si node n'a pas de nœud enfant affiché
def findNewY(self,node):
    maxY= self.G.nodes[node]['pos'][1]
    for i in range(len(self.G.nodes[node]['pointeur'])):
        if self.G.nodes[node]['pointeur'][i]['visible']:
            for edge in self.G.out_edges(node):
                if self.G.nodes[node]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                    if self.G.nodes[edge[1]]['visible']:
                        if self.G.nodes[edge[1]]['pos'][1] + self.G.nodes[edge[1]]['taille'][1]+15>maxY:
                            maxY=self.G.nodes[edge[1]]['pos'][1] + self.G.nodes[edge[1]]['taille'][1]+15
                    break
    return maxY

def rectangles_overlap(self, rect, newNode):
    """
    Vérifie si deux rectangles se chevauchent.
    Chaque rectangle est défini par (XGauche, YTop, XRight, YDown).
    """
    if self.G.nodes[rect]['pos'][0]+self.G.nodes[rect]['taille'][0]+self.padding <= self.G.nodes[newNode]['pos'][0] or self.G.nodes[newNode]['pos'][0]+self.G.nodes[newNode]['taille'][0]+self.padding <= self.G.nodes[rect]['pos'][0] or self.G.nodes[rect]['pos'][1]+self.G.nodes[rect]['taille'][1]+self.padding <= self.G.nodes[newNode]['pos'][1]:
        return 0
    if self.G.nodes[newNode]['pos'][1]+self.G.nodes[newNode]['taille'][1]+self.padding <= self.G.nodes[rect]['pos'][1]:
        return 1
    return 2

def find_non_overlapping_position(self, new_rect):
    """
    Trouve la première position libre en dessous de la position initiale où le nouveau rectangle
    ne chevauche aucun rectangle existant.
    """
    li = list(self.G.nodes())
    li.remove(new_rect)
    li2=[]
    isOverlap=False
    while(True):
        isOverlap=False
        for node in li:
            if self.G.nodes[node]['visible']==False:
                continue
            if self.G.nodes[node]['pos']==None:
                continue
            overLap = rectangles_overlap(self, node, new_rect)
            if overLap==1:
                li2.append(node)
            elif overLap==2:
                self.G.nodes[new_rect]['pos']= (self.G.nodes[new_rect]['pos'][0], self.G.nodes[node]['pos'][1]+self.G.nodes[node]['taille'][1]+self.padding)
                li2=li2+li[li.index(node) + 1:]
                isOverlap=True
                break
        if isOverlap==False:
            return self.G.nodes[new_rect]['pos'][1]+self.G.nodes[new_rect]['taille'][1]
        li=li2
        li2=[]
    
    




# True si le neoud "node" est sous forme reduite
def isReduced(self, node):
    return self.G.nodes[node]['reduced']>0

# True si le neoud "node" est sous forme reduite et que tout les pointeur de se noeud sont ouvert
def isNodeOpen(self, node):
    return self.G.nodes[node]['reduced']==3

# True si le clique "x, y" se situe sur le pointeur "pB" rond et rouge ou vert du noeud "node" sous forme agrandis
def isCliqueOnPointeur(self, x, y, node, pB):
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][0] <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][2] and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][1] <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][3]

# True si le clique "x, y" se situe sur le carre blanc de reduction/agrandissement du noeud "node"
def isCliqueOnReduc(self, x, y, node):
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]-self.line_height/2 <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2 and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-self.line_height/2 <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+self.line_height/2

# True si le clique "x, y" se situe sur le pointeur rond et rouge, orange ou vert du noeud "node" sous forme reduite
def isCliqueOnReducPointeur(self, x, y, node):
    if self.G.nodes[node]['reduced']<2:
        return False
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2+self.padding <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2+self.padding+self.line_height and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-self.line_height/2 <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+self.line_height/2

def isCliqueOnSeeMore(self, event, node):
    # Exemple de chaîne de caractères
    parts = self.G.nodes[node]['contenue'].rsplit('\n', 1)
    if len(parts)>1:
        if parts[1]==self.sentenceSeeMore100:
            if graphic.getY(self, event.y)>self.G.nodes[node]['pos'][1]+self.G.nodes[node]['taille'][1]-(self.line_height+self.padding):
                return True
    return False

# True si le pointeur "pB" du noeud "node" est cliqué/ouvert, en vert
def isPointeurOpen(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['visible']

def isThereNode(self, name):
    return self.G.has_node(name)

def isThereEdge(self, startNode, endNode, startPointer):
    return self.G.has_edge(startNode, endNode) and startPointer in self.G.edges[(startNode, endNode)]['start']










def getOffset(self, event, node):
    return (graphic.getX(self, event.x) - self.G.nodes[node]['pos'][0], graphic.getY(self, event.y) - self.G.nodes[node]['pos'][1])


# retourn le noeud qui se trouve à la position de event.x, event.y : l'endroits où l'utilisateur à cliqué
def getClickedNode(self, event):
        # Check if clicked inside a node and return its id
        for node in reversed(list(self.G.nodes())):
            if self.G.nodes[node]['pos'] != None :
                xLeft = self.G.nodes[node]['pos'][0]
                xRight= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0]
                yTop  = self.G.nodes[node]['pos'][1]
                yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1]
                if xLeft <= graphic.getX(self, event.x) <= xRight and yTop <= graphic.getY(self, event.y) <= yDown:
                    return node
        return None

def getPointeurId(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['id']

def getPoiteurName(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['name']

# retourne le nombre de poiteur qu'il y a dans le noeud "node"
def getLenPointeur(self, node):
    return len(self.G.nodes[node]['pointeur'])