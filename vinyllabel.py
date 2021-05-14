# import main modules
import json
from mutagen.aiff import AIFF
from mutagen import MutagenError

# importing sub modules from package

# global static definitions
config_file = "conf/config.json"
data_dir = "data/"

"""
TODO:
"""

class VinylLabel:
    config = {}
    data = {}

    def __init__(self):
        """Constructor for core class.

        Keyword arguments:

        """
        # load global configuration
        self.loadConfig()

    def loadConfig(self):
        """Read global config file."""
        with open(config_file) as f:
            self.config = json.load(f)

    def writeConfig(self):
        """Write global config file."""
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=4, sort_keys=True)

    def loadFile(self, filepath):
        """Loads a audio file"""
        try:
            self.data = AIFF(filepath)
        except (FileNotFoundError,IOError):
            print("Wrong file or file path")
        except MutagenError:
            print("Loading file", filepath, "failed")

    def run(self):
        """Runs main routine."""

        self.loadFile("test/1000/Side A1.aiff")
        #print(type(self.data))
        print(self.data.pprint())
        #print(self.data.tags['TPE1'].text[0]) #Artist
        #print(self.data.tags["TIT2"].text[0]) #Track
        #print(self.data.tags["TDRC"].text[0]) #Release

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop
if __name__ == "__main__":
    vinlbl = VinylLabel()
    vinlbl.run()

