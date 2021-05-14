# import main modules
import os, sys
from os.path import isfile, join
import json
import argparse
from jinja2 import Environment, FileSystemLoader
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
    args = {}
    tpl = 0
    id3 = {}

    def __init__(self):
        """Constructor for core class.

        Keyword arguments:

        """
        # configure commandline arguments
        parser = argparse.ArgumentParser(description='Create a printable label for vinyls using meta datafrom audio files.')
        parser.add_argument('path',
                metavar='PATH',
                help='directory to get files from')
        parser.add_argument('--template',
                metavar='T',
                default='default.html',
                help='template to use')
        parser.add_argument('--debug',
                metavar='D',
                type=bool,
                help='print additional information')

        self.args = parser.parse_args()

        # load global configuration
        self.loadConfig()

        # load template
        self.loadTemplate(self.args.template)

    def loadConfig(self):
        """Read global config file."""
        with open(config_file) as f:
            self.config = json.load(f)

    def writeConfig(self):
        """Write global config file."""
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=4, sort_keys=True)

    def loadTemplate(self, template):
        """Load jinja2 template."""
        file_loader = FileSystemLoader(self.config['application']['template_dir'])
        env = Environment(loader=file_loader)

        self.tpl = env.get_template(template)

    def processData(self):
        """Process data from ID3 into jinja2 template."""

        dirs = os.listdir(self.args.path)

        album = {}
        tracks = []

        for file in dirs:
            fname, fext = os.path.splitext(file)

            if fext == ".aiff":
                if not self.loadAIFF(join(self.args.path,file)):
                    exit
            else:
                continue
            
            track = {}

            for key, value in self.config['keymapping']['album'].items():
                if not album.get(key):
                    album[key] = self.data.tags[value].text[0]

            for key, value in self.config['keymapping']['track'].items():
                if self.data.tags.get(value):
                    track[key] = self.data.tags[value].text[0]

            track['length'] = self.data.info.length
 
            tracks.append(track)

        output = self.tpl.render(album=album, tracks=tracks)
        print(output)

    def loadAIFF(self, filepath):
        """Loads a audio file"""
        #TODO: raise exeption
        try:
            self.data = AIFF(filepath)
            if self.args.debug:
                self.prettyPrint(self.data.tags)
        except (FileNotFoundError,IOError):
            print("Wrong file or file path")
            return 0
        except MutagenError:
            print("Loading file", filepath, "failed")
            return 0
        
        return 1

    def prettyPrint(self, d, indent=0):
        for key, value in d.items():
            if key == 'APIC:':
                continue
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

    def run(self):
        """Runs main routine."""
        self.processData()

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop
if __name__ == "__main__":
    vinlbl = VinylLabel()
    vinlbl.run()

