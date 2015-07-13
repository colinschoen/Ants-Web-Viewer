import ants
import state
import json #Need JSON to save game state
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
        self.colony = None

    def _init_control_panel(self, colony):
        return

    def exit(self):
        self.active = False

    def initialize_colony_graphics(self, colony):

        self.colony = colony
        self.ant_type_selected = -1
        self.saveState("food", self.colony.food)
        self.ant_types = self.get_ant_types()
        self.places = self._init_places(colony)
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

    def getState(self, key=None):
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
        #while elapsed < STRATEGY_SECONDS:
        #    self._update_control_panel(colony)

    def _update_places(self, colony):
        """Reflect the game state in the play area.

        This function handles several aspects of the game:
        - Adding Ant images for newly placed ants
        - Moving Bee images for beets that have advanced
        - Moving insects out of play when they hve expired
        """
        return

    def _init_places(self, colony):
        """Calculate all of our place data"""
        self.places = {};
        rows = 0
        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            if place.exit.name == 'AntQueen':
                rows += 1
            self.places[name] = { "type": "tunnel", "water": 0, "insects": [] } 
            if name.find("water"):
                self.places[name]["water"] = 1
        #Add the Hive
        self.places[colony.hive.name] = { "type": "hive", "water": 0, "insects": [] }
        for bee in colony.hive.bees:
            self.places[colony.hive.name]["insects"] = bee


    def _update_control_panel(self, colony):
        #TODO actually do something
        return


import http.server
class HttpHandler(http.server.SimpleHTTPRequestHandler):
    #Override the default do_POST method
    def log_message(self, format, *args):
        #I hate this console output so simply do nothing.
        return
    def do_POST(self):
        path = self.path
        action = {
                '/ajax/fetch/state': gui.getState,
                '/ajax/exit': gui.exit,
                }.get(path) 
        if not action:
            #We could not find a valid route
            return
        response = action()
        self.send_response(200)
        if response:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps(action())
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
    import threading
    import webbrowser
    PORT = 8000
    global gui
    gui = GUI()
    #Basic HTTP Handler
    #Handler = http.server.SimpleHTTPRequestHandler
    httpd = CustomThreadingTCPServer(("", PORT), HttpHandler)
    print("Web Server Started on port ", PORT)
    def start_http():
        while gui.active:
            httpd.handle_request()
        print("Web Server terminated")
    threading.Thread(target=start_http).start()
    webbrowser.open("localhost:" + str(PORT), 2)
    ants.start_with_strategy(args, gui.strategy)
