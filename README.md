photo-autosort
==============

Introduction
------------
Did you ever go on a trip with friends/family and each of you took
pictures in their own cameras? Did you found out after the fact that the
camera dates were wrong? How did you sort them by datetime? (if you ever
did?)

This is a very simpe script to help you sort pictures from different
cameras by timestamp, using the EXIF information from the pictures, and
taking into account that cameras can be out of sync. It has two parts.

To use:
-------
1. make a root folder, with no pictures
2. make one subfolder for each camera, with all its pictures
3. When you execute the first part of the script, it creates a list of
pictures with its timestamp (DateTimeOriginal) in the root folder and a
playlist to see the order in which the pictures will be sorted.
4. After verifying that the order is fine, execute the second part of the
script. It will *NOT* touch your original pictures, just make a copy of
them.
5. If the order is wrong, make a "delay.txt" file in each desired subfolder
with the timeshift of the camera (format is yyyy:MM:dd hh:mm:ss). This
time will be added to all pictures in that subfolder when you execute again
the first part of the script.

The playlist can be seen with, for example, the following command line:
$feh --full-screen --auto-zoom --quiet --hide-pointer --filelist playlist.txt
or any other program that allows a playlist of pictures.


Requirements
------------
For now, it requires
* python
* exiftool
* feh or any other picture viewer that has playlist support
* bash

I have all that installed, but if there's enough interest I can translate
the script to python with the minimum possible requirements.

License
-------
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
