#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of photo-autosort.

photo-autosort is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

photo-autosort is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with photo-autosort.  If not, see <http://www.gnu.org/licenses/>.

------------------------------------------------------------------------------

Script to sort pictures from different cameras by timestamp, using the EXIF
information from the pictures. This is the first half of the script.

To use:
 - make a root folder, with no pictures
 - make one subfolder for each camera, with all its pictures
When you execute this script, it creates a list of pictures with its
timestamp (DateTimeOriginal) in the root folder and a playlist to see the
order in which the pictures will be sorted.

The playlist can be seen with, for example, the following command line:
$feh --full-screen --auto-zoom --quiet --hide-pointer --filelist playlist.txt
or any other program that allows a playlist of pictures.

After verifying that the order is fine, execute the second part of the script.
If the order is wrong, make a "delay.txt" file in each desired subfolder with
the timeshift of the camera (format is yyyy:MM:dd hh:mm:ss). This time will be
added to all pictures in that subfolder.

Known bugs: I _think_ that negative delays can't be used
"""

from datetime import datetime, timedelta
import re
import subprocess
import os


def texttodate(text):
    '''Returns a datetime object and the corresponding filename from a text'''
    tokens = re.split('[:\t \n]', text, maxsplit=6)
    if (len(tokens) < 6):
        raise ValueError("The date is incomplete (" + text + ")\n")
    #              year,           month,          day,
    dto = datetime(int(tokens[0]), int(tokens[1]), int(tokens[2]),
    #              hour,           min,            sec
                   int(tokens[3]), int(tokens[4]), int(tokens[5]))
    file_name = tokens[6]
    return (dto, file_name)


def texttodelta(text):
    '''Returns a timedelta object from a text'''
    tokens = re.split('[:\t \n]', text)
    if (len(tokens) < 6):
        raise ValueError("The delay is not correct (" + text + ")\n")
    #               day,            sec,            µsec,
    tdo = timedelta(int(tokens[2]), int(tokens[5]), 0,
    #               ms, min,           hour,           week
                    0, int(tokens[4]), int(tokens[3]), 0)
    return tdo


def exec_cmd(cmd):
    '''Executes the command cmd and returns the output'''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    #Reads the output
    with process.stdout as fobj:
        lines = fobj.readlines()
    #If there's any error, it prints it
    with process.stderr as fobj:
        errors = fobj.readlines()
    if len(errors) > 0:
        print errors
    return lines


def get_date_list(dir_name):
    '''Returns the list of dates and filenames for a directory'''
    fullpath = os.path.join(os.getcwd(), dir_name)
    getexifcmd = ("/usr/bin/exiftool", "-s3", "-printFormat",
                  "'$DateTimeOriginal $FileName'", fullpath)
    data = exec_cmd(getexifcmd)
    data = [l.strip("'\n") for l in data]
    return data


def main():
    '''The main function of the script'''
    #Subdirectory list
    listdirs = os.listdir(os.path.curdir)
    subdirs = [subdir for subdir in listdirs if os.path.isdir(subdir)]
    #TODO: remove hidden directories
    print subdirs

    dataout = list()
    for directory in subdirs:
        date_list = get_date_list(directory)

        #Reads the delay for the directory
        filename = os.path.join(directory, "delay.txt")
        try:
            with open(filename, 'r') as fobj:
                delay = texttodelta(fobj.readline())
                print delay
        except (IOError):
            print "I can't open " + filename + "\tNo delay added"
            delay = timedelta(0)

        #Adds the delay to the timestamps
        for line in date_list:
            (date, filename) = texttodate(line)
            date += delay
            dataout.append(date.strftime("%Y:%m:%d %H:%M:%S\t" +
                            os.path.join(directory, filename)) + '\n')

    #Sorts the list by timestamp, and extracts the sorted filenames
    dataout.sort()
    names_list = list()
    for line in dataout:
        names_list.append(re.split('\t', line, maxsplit=1)[1])

    #Prints the list of all files and their corrected timestamps
    with open("list_all.txt", 'w') as fout:
        fout.writelines(dataout)
    #Prints the playlist
    with open("playlist.txt", 'w') as fout:
        fout.writelines(names_list)

    print("The sorted pictures can be seen, for example, " +
          "with the following command:")
    print("feh --full-screen --auto-zoom --quiet --hide-pointer " +
          "--filelist playlist.txt")


main()
