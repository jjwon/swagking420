import sqlite3
from os import listdir
from os.path import isfile, join
import sys
import re
import json

def make_table(db_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute('''CREATE TABLE music (artist_name text, lyrics text, counts text)''')
	conn.commit()
	conn.close()

def normalize_line(line):
	# print line
	while ('[' in line) and (']' in line):
		line = line.split('[', 1)[0] + line.split(']', 1)[1]
	while ('(' in line) and (')' in line):
		line = line.split('(', 1)[0] + line.split(')', 1)[1]

	for p in [("(", ")"), ("[", "]")]:
		if p[0] in line and p[1] in line:
			print 'we fucked up somehow'

	# print line
	punct = ["?", "!", ",", "."]

	for p in punct:
		line = line.replace(p, '')

	if "," in line:
		print line
	return line.lower().replace('"', "'").decode('utf-8').replace(u'\u2019', "'")

def normalize_data(filename):
	lines = [normalize_line(line) for line in open(filename)]
	return ' '.join(" ".join(lines).split())

def insert_rows(dict, db_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute('delete from music;');
	for k in dict.keys():
		row = dict[k]
		c.execute('''INSERT INTO music VALUES ((?), (?), (?))''', (k, row[0], row[1]))
	conn.commit()
	conn.close()	

def count_words(data):

	counts = {}
	SKIP_THESE_WORDS = ['i', 'we', 'a', 'to', 'me', 'you', 'if', "i'm", 'it']
	# SKIP_THESE_WORDS = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']

	for word in data.split():
		if word in SKIP_THESE_WORDS:
			continue
		if word in counts.keys():
			counts[word] += 1
		else:
			counts[word] = 1

	max_count = max(counts.values());
	for word in counts.keys():
		if counts[word] < .05*max_count:
			del counts[word]
	total = sum(counts.values())
	d = len(counts.values())

	alpha = 1

	formated_counts = []

	for word in counts.keys():
		s = total*(counts[word] + alpha) / (total + d*alpha)
		if s < 10:
			continue
		formated_counts.append({"text": word, "size": s})

	return json.dumps(formated_counts, separators=(',', ':')).replace('"', '\"')


if __name__ == "__main__":

	path = "/Users/jawon/swagking/artists/"
	artists = [ f.replace('.txt', '') for f in listdir(path) if isfile(join(path,f)) ]
	db_name = "swag.db"

	# print artists

	temp_dict = {}

	for artist in artists:
		data = normalize_data(path + artist + ".txt")
		counts = count_words(data)
		temp_dict[artist] = [data, counts]

	# print temp_dict.keys()

	# for artist in temp_dict.keys():
	if len(sys.argv) > 1:
		make_table(sys.argv[1])
	else:
		# pass
		insert_rows(temp_dict, db_name)

