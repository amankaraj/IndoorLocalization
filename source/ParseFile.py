__author__ = 'Aman'

from os import walk




listOfFiles = []
for (dirpath, dirnames, filenames) in walk("/Users/Aman/Desktop/Projects/IndoorLocalization/Data/"):
    listOfFiles.extend(filenames)

print listOfFiles