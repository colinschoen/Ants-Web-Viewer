import ants
import state
import json #Need JSON to save game state
import threading
from time import sleep
from ucb import *

ASSETS_DIR = "assets/"
INSECT_DIR = "insects/"
STRATEGY_SECONDS = 3
INSECT_FILES = {
       'Worker': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Thrower': ASSETS_DIR + INSECT_DIR +  "ant_thrower.gif",
       'Long': ASSETS_DIR + INSECT_DIR +  "ant_longthrower.gif",
       'Short': ASSETS_DIR + INSECT_DIR +  "ant_shortthrower.gif",
       'Harvester': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Fire': ASSETS_DIR + INSECT_DIR +  "ant_fire.gif",
       'Bodyguard': ASSETS_DIR + INSECT_DIR +  "ant_bodyguard.gif",
       'Hungry': ASSETS_DIR + INSECT_DIR +  "ant_hungry.gif",
       'Slow': ASSETS_DIR + INSECT_DIR +  "ant_slow.gif",
       'Stun': ASSETS_DIR + INSECT_DIR +  "ant_stun.gif",
       'Ninja': ASSETS_DIR + INSECT_DIR +  "ant_ninja.gif",
       'Wall': ASSETS_DIR + INSECT_DIR +  "ant_wall.gif",
       'Scuba': ASSETS_DIR + INSECT_DIR +  "ant_scuba.gif",
       #TODO needs to be updated to laser ant art
       'Laser': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Queen': ASSETS_DIR + INSECT_DIR +  "ant_queen.gif",
       'Bee': ASSETS_DIR + INSECT_DIR +  "bee.gif",
       #TODO implement remover
}

class GUI:
    """Browser based GUI that communicates with Python game engine"""

    def __init__(self):
        self.active = True
        self.state = state.State()
        self.initialized = False
        self.gameOver = False
        self.colony = None
        self.currentBeeId = 0
        self.insects = []
        self.beeToId = {}
        self.beeLocations = {}


    def newGameThread(self):
        print("Trying to start new game")
        ants.start_with_strategy(gui.args, gui.strategy)
        self.gameOver = True
        #self.killGUI()

    def killGUI(self):
        self.active = False

    def startGame(self, data=None):
        threading.Thread(target=self.newGameThread).start()
        print("Game started")

    def exit(self, data=None):
        self.active = False

    def initialize_colony_graphics(self, colony):

        self.colony = colony
        self.ant_type_selected = -1
        self.saveState("strategyTime", STRATEGY_SECONDS)
        self.saveState("food", self.colony.food)
        self.ant_types = self.get_ant_types()
        self._init_places(colony)
        self.saveState("places", self.places)
        #Finally log that we are initialized
        self.initialized = True

    def get_ant_types(self, noSave=False):
        ant_types = {};
        i = 0
        for name, ant_type in self.colony.ant_types.items():
            ant_types[i] = {"name": name, "cost": ant_type.food_cost, "img": self.get_insect_img_file(name)}
            i+= 1

        if not noSave:
            self.saveState("ant_types", ant_types)
        return ant_types

    def get_insect_img_file(self, name):
        return INSECT_FILES[name]

    def getState(self, data=None):
        """Get our message from JSON"""
        return self.state.getState()

    def saveState(self, key, val):
        """Saves our game object to JSON file"""
        self.state.updateState(key, val)

    def strategy(self, colony):
        """The strategy function is called by ants.AntColony each turn"""
        #Have we initialized our graphics yet?
        if not self.initialized:
            #No, so do that now
            self.initialize_colony_graphics(colony)
        elapsed = 0 #Physical time elapsed this turn
        self.saveState("time", int(elapsed))
        while elapsed < STRATEGY_SECONDS:
            self.saveState("time", colony.time)
            self._update_control_panel(colony)
            sleep(0.25) 
            elapsed += 0.25

    def _update_places(self, colony):
        """Reflect the game state in the play area.

        This function handles several aspects of the game:
        - Adding Ant images for newly placed ants
        - Moving Bee images for beets that have advanced
        - Moving insects out of play when they have expired
        """
        return

    def get_place_row(self, name):
        return name.split("_")[1]

    def get_place_column(self, name):
        return name.split("_")[2]

    def _init_places(self, colony):
        """Calculate all of our place data"""
        self.places = {};
        self.images = { 'AntQueen': dict() }
        rows = 0
        cols = 0
        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.exit.name == 'AntQueen':
                rows += 1
            if not pRow in self.places:
                self.places[pRow] = {}
            self.places[pRow][pCol] = { "name": name, "type": "tunnel", "water": 0, "insects": {} } 
            if "water" in name:
                self.places[pRow][pCol]["water"] = 1
            self.images[name] = dict()
        #Add the Hive
        self.places[colony.hive.name] = { "name": name, "type": "hive", "water": 0, "insects": {} }
        self.places[colony.hive.name]["insects"] = []
        for bee in colony.hive.bees:
            self.insects.append(bee)
            self.places[colony.hive.name]["insects"].append({"id": self.currentBeeId, "type": "bee"})
            self.beeToId[bee] = self.currentBeeId
            self.currentBeeId += 1
        self.saveState("rows", rows)
    

    def update_food(self):
        self.saveState("food", self.colony.food)

    def _update_control_panel(self, colony):
        """Reflect the game state in the play area."""
        self.update_food()
        current_insects = []
        for name, place in colony.places.items():
            current_insects += place.bees + [place.ant] 
            if place.name == 'Hive':
                continue

            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.ant is not None:
                #Ok there is an ant that needs to be drawn here
                self.places[pRow][pCol] = { "name": name, "type": "tunnel", "water": 0, "insects": {"type": place.ant.name, "img": self.get_insect_img_file(place.ant.name)} }
                if not place.ant in self.insects:
                    #Add this ant to our internal list of insects
                    self.insects.append(place.ant)
            #Loop through our bees
            for bee in place.bees:

                self.beeLocations[self.beeToId[bee]] = name
                #Check to see if we are at an exit
                for other_place in colony.places.values():
                    if other_place.exit is place:
                        break
                """
                else:
                    other_place = colony.hive
                    self.places[pRow][pCol]["bee"] = 1
                self.images[name][bee] = image
                """
        #Save our new bee locations to our game state
        self.saveState("beeLocations", self.beeLocations)
        #Remove expired insects
        for insect in self.insects:
            if insect not in current_insects: 
                #TODO
                #Ok this insect needs to be removed
                x = "hi"

    def deployAnt(self, data):
        pname, ant = data["pname"], data["ant"]
        try:
            print("colony.deploy_ant('{0}', '{1}')".format(pname, ant))
            self.colony.deploy_ant(pname, ant);
        except Exception as e:
            print(e)
            return { "error": str(e) }
        self._update_control_panel(self.colony);
        return { "success": 1 }



import http.server
import cgi
class HttpHandler(http.server.SimpleHTTPRequestHandler):
    #Override the default do_POST method
    def log_message(self, format, *args):
        #I hate this console output so simply do nothing.
        return
    def cgiFieldStorageToDict(self, fieldStorage):
        """ Get a plain dictionary rather than the '.value' system used by the 
           cgi module's native fieldStorage class. """
        params = {}
        for key in fieldStorage.keys():
            params[key] = fieldStorage[key].value
        return params

    def do_POST(self):
        path = self.path
        action = {
                '/ajax/fetch/state': gui.getState,
                '/ajax/start/game': gui.startGame,
                '/ajax/exit': gui.exit,
                '/ajax/deploy/ant': gui.deployAnt,
                }.get(path) 
        if not action:
            #We could not find a valid route
            return
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
             'CONTENT_TYPE':self.headers['Content-Type'],
            })
        data = self.cgiFieldStorageToDict(form)
        response = action(data)
        self.send_response(200)
        if response:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps(response)
            self.wfile.write(response.encode('ascii'))

import socketserver, socket
class CustomThreadingTCPServer(socketserver.ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

@main
def run(*args):
    #Start webserver
    import socketserver
    import webbrowser
    PORT = 8000
    global gui
    gui = GUI()
    gui.args = args
    #Basic HTTP Handler
    #Handler = http.server.SimpleHTTPRequestHandler
    httpd = CustomThreadingTCPServer(("", PORT), HttpHandler)
    print("Web Server started @ localhost:" + str(PORT))
    def start_http():
        while gui.active:
            httpd.handle_request()
        print("Web server terminated")
    threading.Thread(target=start_http).start()
    webbrowser.open("localhost:" + str(PORT), 2)
