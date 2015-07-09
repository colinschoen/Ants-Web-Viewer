import ants
import json #Need JSON to save game state
from ucb import *

ASSETS_DIR = "assets/"
INSECT_DIR = "insects/"
GAME_STATE = "gameState.json"
JSON_LOCATION = "gameState.json"
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
       'Scuba': ASSETS_DIR + INSECT_DIR +  "scuba.gif",
       #TODO needs to be updated to laser ant art
       'Laser': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Queen': ASSETS_DIR + INSECT_DIR +  "ant_queen.gif",
       'Bee': ASSETS_DIR + INSECT_DIR +  "bee.gif",
       #TODO implement remover
} 

class GUI:
    """Browser based GUI that communicates with Python game engine"""

    def __init__(self):
        #Create our JSON state file
        self.createState()
        self.initialized = False
        self.colony = None

    def _init_control_panel(self, colony):
        return

    def initialize_colony_graphics(self, colony):

        self.colony = colony
        self.ant_type_selected = -1
        self.ant_types = self.get_ant_types();
        #Finally log that we are initialized
        self.initialized = True

    def get_ant_types(self, noSave=False):
        ant_types = {};
        i = 0
        for name, ant_type in self.colony.ant_types.items():
            ant_types[i] = {"name": name, "img": self.get_insect_img_file(name)}
            i+= 1

        if not noSave:
            self.saveState("ant_types", ant_types)
        return ant_types

    def get_insect_img_file(self, name):
        return INSECT_FILES[name]


    
    def getState(self, key=None):
        """Get our message from JSON"""
        with open(JSON_LOCATION) as f:
            data = json.load(f)
            if key:
                return data["key"]
            return data

    def saveState(self, key, obj):
        """Saves our game object to JSON file"""
        data = self.getState()
        data[key] = obj
        with open(JSON_LOCATION, 'w') as f:
            json.dump(data, f)


    def createState(self):
        """Creates our start json state file"""
        data = {}
        with open(JSON_LOCATION, 'w') as f:
            json.dump(data, f)

    def strategy(self, colony):
        """The strategy function is called by ants.AntColony each turn"""
        #Have we initialized our graphics yet?
        if not self.initialized:
            #No, so do that now
            self.initialize_colony_graphics(colony)

@main
def run(*args):
    ants.start_with_strategy(args, GUI().strategy)
