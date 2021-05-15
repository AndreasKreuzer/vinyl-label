# import main modules
import os, sys
from os.path import isfile, join
import math
import re
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
            
            # calculation of length in h:m:s out of float
            length = self.data.info.length
            lstr = ""
            if length >= 600:
                floor = math.floor(length / 600)
                length = length - (floor * 600)
                lstr = str(floor) + "h "
            if length >= 60:
                floor = math.floor(length / 60)
                length = length - (floor * 60)
                lstr = lstr + str(floor) + "m "
            lstr = lstr + str(math.floor(length)) + "s"
            track['length'] = lstr

            # using vinyl track pos if letters are in pos tag
            m = re.search('^([A-Za-z]*)([0-9]*)[/]?([0-9]*)$', track['pos'])

            postotal = ''
            posvinyl = ''
            posnumber = ''
            if len(m.group(3)):
                postotal = m.group(3)
                track['pos'] = '/' + postotal
            if len(m.group(1)):
                posvinyl = m.group(1)
                if len(m.group(2)):
                    posvinyl = posvinyl + m.group(2)
                else:
                    posvinyl = posvinyl + '1'
                track['pos'] = posvinyl + track['pos']
            else:
                posnumber = m.group(2)
                track['pos'] = posnumber + track['pos']

            track['postotal'] = postotal
            track['posvinyl'] = posvinyl
            track['posnumber'] = posnumber

            tracks.append(track)

        if len(tracks):
            sortedtracks = sorted(tracks, key=lambda k: k['pos'])
            output = self.tpl.render(album=album, tracks=sortedtracks)
        else:
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

    def prettyPrint(self, d, indent=4):
        print(json.dumps(d, indent=indent))

    def run(self):
        """Runs main routine."""
        self.processData()

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop
if __name__ == "__main__":
    vinlbl = VinylLabel()
    vinlbl.run()

