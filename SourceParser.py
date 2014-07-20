import os
from os import listdir
from os.path import isfile, join
import unicodedata
from DBHelper import DBHelper

""" 
> STRING: abs file dir specifying list of artists 
< STRING: normalized lyrics of all the arists
"""


class SourceParser:

	@staticmethod
	def normalize_line(line):
		while ('[' in line) and (']' in line):
			line = line.split('[', 1)[0] + line.split(']', 1)[1]
		while ('(' in line) and (')' in line):
			line = line.split('(', 1)[0] + line.split(')', 1)[1]

		for p in [("(", ")"), ("[", "]")]:
			if p[0] in line and p[1] in line:
				print 'we fucked up somehow'

		punct = ["?", "!", ",", "."]
		for p in punct:
			line = line.replace(p, '')

		line = line.decode('utf-8').lower().replace('"', "'").replace(u'\u2019', "'").replace(u'\n', "")

		return line

	@staticmethod
	def normalize_data(filename):
		lines = [SourceParser.normalize_line(line) for line in open(filename) if line != '\n']
		# return ' '.join(" ".join(lines).split()), lines
		return str(lines)


	@staticmethod
	def normalize_artists(path, db_name, table_name):

		DBHelper.make_table(db_name,table_name)

		artists = SourceParser.retrieve_artists(path)
		norm_artists = {}

		for artist in artists:
			lyrics = DBHelper.get_lyrics(db_name, table_name, artist)
			if lyrics:
				norm_artists[artist] = lyrics
			else:
				norm_artists[artist] = SourceParser.normalize_data(path + artist + ".txt")
				DBHelper.update_lyrics(db_name,table_name, artist, norm_artists[artist])
		return norm_artists

	@staticmethod
	def retrieve_artists(path):
		artists = [ f.replace('.txt', '') for f in listdir(path) if isfile(join(path,f)) ]
		return artists

