#!/usr/bin/env python
"""Music XML to Microbit Javascript Transpiler
"""

import zipfile
import os
import argparse
import xml.etree.ElementTree as ET

def main(args):
    filename = args.filename

    # read the xml
    with zipfile.ZipFile(filename) as myzip:
        xml_filename = [fn for fn in myzip.namelist() if os.path.splitext(fn)[1] == ".xml" and "container.xml" not in fn][0]
        with myzip.open(xml_filename) as myfile:
            tree = ET.parse(myfile)
            
    # parse XML
    root = tree.getroot()

    # find the part
    parts = [p.get('id') for p in root.findall('part-list/score-part')]
    part_id = parts[0]
    part = root.find(f"part[@id='{part_id}']")

    # parse the part
    script = []
    for measure in part:
        for note in measure.findall("note"):
            duration = int(note.find("duration").text) * 100
            rest = note.find("rest")
            pitch = note.find("pitch")

            if rest is not None:
                script.append(f"music.rest({duration});")

            if pitch is not None:
                step = pitch.find("step").text
                octave = pitch.find("octave").text
                alter = pitch.find("alter")
                if alter is not None:
                    if alter.text == "1":
                        alter = "Sharp"
                    elif alter.text == "-1":
                        alter = "Sharp"
                else:
                    alter = ""
                script.append(f"music.playTone(music.noteFrequency(Note.{step}{alter}{octave}), {duration});")
                
    print(" ".join(script))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run with -h or --help for help.')
    parser.add_argument('-f',
                        '--filename',
                        dest = 'filename',
                        default = '',
                        help = 'Music XML file to parse')
    args = parser.parse_args()
    main(args)