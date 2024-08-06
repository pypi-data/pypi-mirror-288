# -*- coding: utf-8 -*-
import tkinter as tk
from logging import getLogger
from thonny import get_workbench, ui_utils
from thonny.common import ValueInfo
from thonny.languages import tr
from thonnycontrib.data_visualization.representation_format import repr_format
import thonnycontrib.data_visualization.sender as sender
import builtins

'''Enregistrement en mémoire des arrays décrivant les builtin types pour pouvoir les détecter et les traiter séparément'''
builtin_types = [str(getattr(builtins, d)) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
builtin_types.append("<class 'function'>")
builtin_types.append("<class 'method'>")
builtin_types.append("<class 'NoneType'>")
builtin_types.append("<class 'module'>")
builtin_types.append("<class 'builtin_function_or_method'>")
builtin_types.remove("<class 'type'>")
builtin_data_struct = ["<class 'dict'>", "<class 'list'>", "<class 'set'>", "<class 'tuple'>"]

logger = getLogger(__name__)

class HierarchicalView(ui_utils.TreeFrame):

    '''Création d'une structure ui_utils_TreeFrame permettant facilement une mise en forme de vue hiéréchique'''
    def __init__(self, master):

        ui_utils.TreeFrame.__init__(
            self,
            master,
            columns=("value","id")
        )

        self.lazy_on = True # Permet de définir si le développement de la vue hiérarchique se fait de façon lazy
        self.iter = 0
        self.clean = True
        self.extend_max = 9

        self.name = "HV"

        self.parent_id = None # Enregistre à chaque itération le noeuds parents à la suite duquel il faut développer la vue
        self.categorie_id = (None,None) # Enregistre si la variable à rechercher fait partie de la catégorie des varibles globales ou locales
        self.object_id = None # Enregistre à chaque opération l'ID de l'objet qui est recherché dans la DB
        self.object_name = None # Enregistre à chaque opération le nom de l'objet qui est recherché dans la DB
        self.var_to_request = {} # Stocke les différents objets qui va falloir aller rechercher dans la DB

        self.lazy_id = None # Fonctionne si le programme est en lazy et stocke l'ID su noeud à développer
        self.extended = {} # Enregistre tous les noeuds déjà étendus dans le cas lazy pour ne pas devoir les redévelopper
        self.obj_len = {}

        self.tree_db = {} # Stockage de chaque objet rencontré à partir de sa véritable ID et attribution d'un tuple composé de sa représentation en string et de son nom
        self.type_db = {} # Stockage du nombre d'objet d'un certain type que le programme rencontre (pour simplifier les ID)
        self.repr_db = {} # Stockage de la représentation complète simplifiée d'un objet à partir de sa représentation par défaut

        self._last_progress_message = None

        '''Ce sont ici toutes les réactions de notre programme aux intéractions de l'utilisateur et aux réponses de la mémoire'''
        if (self.lazy_on):
            self.tree.bind("<<TreeviewSelect>>", self.lazy_adding) # Permet le fonctionnement de l'affichage en mode lazy

        #get_workbench().bind("ObjectSelect", self.show_object, True)
        get_workbench().bind("ToplevelResponse", self._handle_toplevel_response, True) # Permet le fonctionnement du bouton 'run'
        get_workbench().bind("DebuggerResponse", self._debugger_response, True) # Permet l'interaction avec le debugger
        get_workbench().bind("get_object_info_response", self._handle_object_info_event, True) # Permet de recevoir les réponses de la mémoire
        get_workbench().bind("BackendRestart", self.restart, True) # Permet un redémarrage propre du programme

        '''Attribution des paramètres de l'arbre et de sa réprésentation graphique en vue hiérarchique'''
        self.tree.column("#0", width=350, anchor=tk.W)
        self.tree.column("value", width=300, anchor=tk.W)
        self.tree.column("id", width=30, anchor=tk.W)

        self.tree.heading("#0", text="Name", anchor=tk.W)
        self.tree.heading("value", text="Value", anchor=tk.W)

        self.tree.configure(displaycolumns=("value"))

        self.tree["show"] = ("headings", "tree")
        
    '''Permet un redémarrage propre du programme'''
    def restart(self, event=None):

        self.lazy_on = True
        self.obj_len = {}

        self.parent_id = None
        self.categorie_id = (None,None)
        self.object_id = None
        self.object_name = None
        self.var_to_request = {}
        self.lazy_id = None
        self.extended = {}

        self.tree_db = {}
        self.type_db = {}
        self.repr_db = {}

        self._last_progress_message = None
        self._clear_tree()
    
    '''Réagis à l'utilisation du bouton "run"'''
    def _handle_toplevel_response(self, event):
        if "globals" in event and event["globals"]:
            self.update(event["globals"])
        
    '''Permet l'interaction avec le debugger'''
    def _debugger_response(self, event):
        self._last_progress_message = event
        frame_info = self.get_frame_by_id(event.stack[-1].id)
        self.update(frame_info.globals, frame_info.locals)
    
    '''extrait les infos de la frame concernée'''
    def get_frame_by_id(self, frame_id):
        for frame_info in self._last_progress_message.stack:
            if frame_info.id == frame_id:
                return frame_info

        raise ValueError("Could not find frame %d" % frame_id)

    '''Le corps du programme, permet d'updater la vue hiérarchique en fonction des intéractions avec l'utilisateur
    Pour chaque "run", chaque étape dans le parcours du débugger, la vue va repartir de zéro pour se reconstruire
    Arguments :
    - globals_ : liste des variables globales présentes dans le programme de l'utilisateur
    - locals_ : liste des variables locales présentes dans le programme de l'utilisateur à la frame concernée'''
    def update(self, globals_, locals_ = None):

        self.restart()

        globalst = None
        localst = None

        if (globals_):
            globalst = globals_.copy()
        if (locals_ and locals_ != globals_):
            localst = locals_.copy()

        self.var_to_request["globals"] = globalst # Ajoute les variables globales dans la liste des variables à demander à la DB
        self.var_to_request["locals"] = localst # Ajoute les variables locales dans la liste des variables à demander à la DB
        self.var_to_request["children"] = {} # Initialise le stockage des objets dépends de ceux rencontrés précédemment
        self.var_to_request["lazy"] = {} # Initialise le stockages des variables à développer de façon lazy

        #if (self.winfo_ismapped()):
        self.send_request() # Entre dans la phase de requête des varibles ci-dessus à la mémoire
    
    '''Envoie en requête à la mémoire les informations nécessaires sur les différentes variables à afficher dans la vue hiérarchique'''
    def send_request(self):
        # S'il n'y a plus aucune variable à aller chercher, on s'assure que tout est bien réinitialisé
        if not self.var_to_request["globals"] and not self.var_to_request["locals"] and not self.var_to_request["children"] and not self.var_to_request["lazy"]:
            self.var_to_request["globals"] = {}
            self.var_to_request["locals"] = {}
            self.var_to_request["children"] = {}
            self.var_to_request["lazy"] = {}
            self.object_id = None
            self.parent_id = None
            self.categorie_id = (None,None)
            self.lazy_id = None

        else:
            sender.send(self)
    
    '''Réceptionne les réponses envoyées par la mémoire aux différentes requêtes'''
    def _handle_object_info_event(self, msg):
        
        if msg.info["id"] == self.object_id: # Si la réponse contient bien des infos sur la variable demandée
            if "error" in msg.info.keys() or (hasattr(msg, "not_found") and msg.not_found):
                self.object_id = None
                self.object_name = None
                
            else:
                object_infos = msg.info # Récupération des informations
                object_infos["name"] = self.object_name # Ajout du nom (qui a été attribué à la variable par l'utilisateur)

                if (self.lazy_id is not None): # Si le but était de développer un objet existant alors nous passons directement à la fonction "extend"
                    if (self.object_name == "next"):
                        self.extend(object_infos, self.lazy_id, self.obj_len[self.lazy_id])
                    else :    
                        self.extend(object_infos, self.lazy_id)
                    self.lazy_id = None

                elif (object_infos["type"] != "<class 'method'>"): # Choix que nous avons fait de ne pas afficher les méthodes des différentes classes
                    self.format(object_infos)

                self.send_request() # Retour au sender pour demander les informations sur les variables suivantes
        
        elif self.object_id != None and msg.get("command_id") != 'HV ' + str(self.iter):
            '''Si nous n'avons pas reçu de message correspondant à la variable que nous voulons, nous renvoyons une demande
            Cela est nécessaire car Thonny supprime automatiquement les demandes mémoires si une demande du même type (demande d'information sur un objet) est déjà en cours.
            Or, l'inpecteur d'objet fait également ce type de demande ce qui peut provoquer la perte de certaines de nos demandes'''
            sender.fast_send(self)
    
    '''Permet d'afficher proprement les différentes informations nécessaires à la vue hiérarchique et de connecter le noeud contenant ces informations à l'arbre de la vue'''
    def format(self, object_infos):

        if (self.parent_id == "Globals" or self.parent_id == "Locals"): # Si le noeud est le premier de la partie des variables globales ou de celle des locales
            if self.categorie_id[0] == self.parent_id:
                self.parent_id = self.categorie_id[1]
            else :
                parent_id = self.tree.insert("", 0, text=self.parent_id, open=True)
                self.tree.set(parent_id, "id", self.parent_id) # On ajoute la racine de départ de la partie concernée (globale ou locale)
                self.categorie_id = (self.parent_id, parent_id)
                self.parent_id = parent_id
        
        txt = ""
        txt = object_infos["name"]
        if (self.parent_id in self.obj_len and self.obj_len[self.parent_id] > 101):
            node_id = self.tree.insert(self.parent_id, index=len(self.tree.get_children(self.parent_id))-1, text=txt, open=False) # On ajoute le noeud avec l'affichage de son nom (donné à la variable par l'utilisateur)
        else : node_id = self.tree.insert(self.parent_id, "end", text=txt, open=False) # On ajoute le noeud avec l'affichage de son nom (donné à la variable par l'utilisateur)
        self.tree.set(node_id, "id", object_infos["id"])

        tp = object_infos["type"]
        
        if (object_infos["id"] not in self.tree_db.keys()): # Si l'objet que l'on rencontre est un objet que l'on ne connait pas encore

            s, at_bool, homemade = repr_format(self, object_infos['repr']) # On va formater sa représentation pour qu'elle soit la plus claire et facilement interprétable possible
            
            if (tp not in builtin_types): # Si la variable recherchée est bel et bien un objet considéré comme intéressant

                if at_bool: # Si la représentation de l'objet a une référence à son emplacement mémoire, alors on la remplace par une attribution plus simple
                    if (tp not in self.type_db.keys()):
                        self.type_db[tp] = 0
                    self.type_db[tp] += 1
                    s += " n°" + str(self.type_db[tp]) # Cette attribution simplifiée attribue un numéro correspondant au nombre d'objet de ce type déjà rencontré

                name = object_infos["name"] # Le nom de l'objet désigné par l'utilisateur
                if (self.tree.set(self.parent_id, "id") != "Globals" and self.tree.set(self.parent_id, "id") != "Locals"): # Si som'est un enfant, on l'utilise en référence à son objet parent
                    name = self.tree_db[self.tree.set(self.parent_id, "id")][1] + "." + str(name)
                
                self.tree_db[object_infos["id"]] = (s, name, homemade)
                self.repr_db[object_infos["repr"]] = s + " (" + name + ")"

            if (len(s) > 200):
                s = s[:75] + " ... " + s[-75:]
            
            self.tree.set(node_id, "value", s)

        else : # Si la représentation simplifiée de l'objet existe déjà, on va simplement la récupérer 
            self.tree.set(node_id, "value", self.repr_db[object_infos["repr"]])
        
        if (tp not in builtin_types or tp in builtin_data_struct): # Si l'objet est un objet intéressant à pouvoir développer dans la vue hiérarchique
            if (self.lazy_on): # Si on est en mode lazy, on lui attribue un noeud enfant vide pour offrir à l'utilisateur la possibilité de voir que cet objet est développable
                self.tree.insert(node_id, "end", open=False) 
            else: # Sinon, on étend directement l'objet
                self.extend(object_infos, node_id)

    '''Etend le noeud choisi (node_id) avec les informations le concernant'''
    def extend(self, object_infos, node_id, iter = 0):
        tp = object_infos['type']
        obj_id = object_infos['id']

        if (tp not in builtin_types): # Si l'objet est intéressant à développer
            if (self.clean and not self.tree_db[obj_id][2]):
                self.tree.insert(node_id, "end", text="See more details in the Object inspector", open=True)
                return
            attributes = object_infos['attributes']
            keys = list(attributes.keys())
            if (len(attributes) > iter): # S'il possède des attributs 
                self.var_to_request["children"][node_id] = {}
                i = iter
                for attr in keys[iter:]:
                    if(i > self.extend_max + iter):
                        if not iter : self.var_to_request["children"][node_id]["..."] = None
                        self.obj_len[node_id] = i
                        break
                    self.var_to_request["children"][node_id][attr] = ValueInfo(attributes[attr].id, attributes[attr].repr)
                    i+=1
        
        elif (tp in builtin_data_struct): # Si l'objet est une structure de donnée builtin intéressante
            if (tp == "<class 'dict'>"):
                entries = object_infos['entries']
                if (len(entries) > iter):
                    for i in range(iter, len(entries)):
                        if(i > self.extend_max + iter):
                            if not iter : self.var_to_request["children"][node_id]["..."] = None
                            self.obj_len[node_id] = i
                            break
                        entr_id = self.tree.insert(node_id, "end", text=i, open=True)
                        entr = entries[i]
                        self.var_to_request["children"][entr_id] = {}
                        self.var_to_request["children"][entr_id]["key"] = ValueInfo(entr[0].id, entr[0].repr)
                        self.var_to_request["children"][entr_id]["value"] = ValueInfo(entr[1].id, entr[1].repr)
                        
            else: # Pour les listes, tuples, ...
                elements = object_infos['elements']
                if (len(elements) > iter):
                    self.var_to_request["children"][node_id] = {}
                    for i in range(iter, len(elements)):
                        if(i > self.extend_max + iter):
                            if not iter : self.var_to_request["children"][node_id]["..."] = None
                            self.obj_len[node_id] = i
                            break
                        elem = elements[i]
                        self.var_to_request["children"][node_id][i] = ValueInfo(elem.id, elem.repr)
                        
    
    '''Permet d'étendre de façon lazy les noeuds de l'arbre correspondant à la vue hiérarchhique'''
    def lazy_adding(self, event):
        node_id = self.tree.focus() # On récupère l'ID du noeud
        if (self.tree.item(node_id, "text") == "Click here to see more"):
            parent_id = self.tree.parent(node_id)
            self.lazy_id = parent_id
            self.var_to_request["lazy"] = {}
            self.var_to_request["lazy"]["next"] = ValueInfo(self.tree.set(parent_id, "id"), "next") # On va récupérer dans l'arbre l'ID de l'objet correspondant au noeud à développer
            self.send_request()
        else :
            children = self.tree.get_children(node_id)

            if (node_id not in self.extended.keys() and len(children) == 1): # On vérifie que le noeud n'a pas déjà été étendu et qu'il correspond bien à un objet développable
                self.tree.delete(children[0]) # On supprime le noeud enfant indicateur
                self.extended[node_id] = True
                self.lazy_id = node_id
                self.var_to_request["lazy"] = {}
                self.var_to_request["lazy"][node_id] = ValueInfo(self.tree.set(node_id, "id"), 0) # On va récupérer dans l'arbre l'ID de l'objet correspondant au noeud à développer
                self.send_request()
    
    def add_next(self, parent, var):
        self.tree.insert(parent, "end", text=var, open=False)

    '''Permet de nettoyer complètement l'arbre'''
    def _clear_tree(self):
        for child_id in self.tree.get_children():
            self.tree.delete(child_id)
