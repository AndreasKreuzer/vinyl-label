# Requires pydub (with ffmpeg) and Pillow
#
# Usage: python waveform.py <audio_file>
# https://gist.github.com/mixxorz/abb8a2f22adbdb6d387f
#

import sys

from pydub import AudioSegment
from PIL import Image, ImageDraw


class Waveform(object):

    bar_count = 300
    db_ceiling = 60

    def __init__(self, bar_count, db_ceiling):
        self.bar_count = bar_count
        self.db_ceiling = db_ceiling

    def open(self, filename):
        self.filename = filename

        audio_file = AudioSegment.from_file(
            self.filename, self.filename.split('.')[-1])

        self.peaks = self._calculate_peaks(audio_file)


    def _calculate_peaks(self, audio_file):
        """ Returns a list of audio level peaks """
        chunk_length = len(audio_file) / self.bar_count

        loudness_of_chunks = [
            audio_file[i * chunk_length: (i + 1) * chunk_length].rms
            for i in range(self.bar_count)]

        max_rms = max(loudness_of_chunks) * 1.00

        return [int((loudness / max_rms) * self.db_ceiling)
                for loudness in loudness_of_chunks]

    def _get_bar_image(self, size, fill):
        """ Returns an image of a bar. """
        width, height = size
        bar = Image.new('RGBA', size, fill)

        end = Image.new('RGBA', (width, 2), fill)
        draw = ImageDraw.Draw(end)
        draw.point([(0, 0), (3, 0)], fill='#c1c1c1')
        draw.point([(0, 1), (3, 1), (1, 0), (2, 0)], fill='#e7e7e7')

        bar.paste(end, (0, 0))
        bar.paste(end.rotate(180), (0, height - 2))
        return bar

    def _generate_waveform_image(self):
        """ Returns the full waveform image """
        im = Image.new('RGB', (802, 128), '#ffffff')
        for index, value in enumerate(self.peaks, start=0):
            column = index * 4 + 2
            upper_endpoint = 64 - value

            im.paste(self._get_bar_image((2, value * 2), '#c1c1c1'),
                     (column, upper_endpoint))

        return im

    def save(self, path):
        """ Save the waveform as an image """
        with open(path, 'wb') as imfile:
            self._generate_waveform_image().save(imfile, 'PNG')


if __name__ == '__main__':
    filename = sys.argv[1]

    waveform = Waveform(200, 60)
    waveform.save()
