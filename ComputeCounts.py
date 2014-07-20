import json
from sets import Set
import operator
from DBHelper import DBHelper

""" 
> STRING: dict of artists -> (lyric string, lyric array)
< STRING: dict of artists -> (lyric string, phrase count string)
"""

IGNORE_WORDS = ['a', "ain't", 'am', 'and', 'as', 'be', 'but', 'do', "don't", 'for', 'from', 'girl', 'got', 'had', 'i', "i'm", 'if', 'in', 'is', 'it', "it's", 'its', 'like', 'me', 'my', 'of', 'on', 'that', 'the', 'them', 'they', 'this', 'to', 'too', 'wanna', 'want', 'was', 'we', 'were', 'what', 'when', 'with', 'you', "you're", 'your']

class ComputeCounts:


	@staticmethod
	def lcs(s1,s2):
		m = len(s1)
		n = len(s2)
		array = [[0 for x in range(n)] for x in range(m)] 
	   	z = 0

	   	commons = Set()

	   	for i in range(0,m):
	   		for j in range(0,n):
	   			if s1[i] == s2[j]:
	   				if i==0 or j==0:
	   					array[i][j] = 1
	   				else:
	   					array[i][j] = array[i-1][j-1] + 1

	   				if array[i][j] > z:
	   					z = array[i][j]
	   					commons.add(s1[i-z+1:i+1])
	   				elif array[i][j] == z:
	   					commons = commons.union(Set([s1[i-z+1:i+1]]))
				else:
					array[i][j] = 0

	   	ret = {}
	   	for sub_seq in commons:
	   		if len(sub_seq) > 1:
	   			st = " ".join(sub_seq)
	   			ret[st] = 1
	   	return ret

	@staticmethod
	def aggregate(old, new):
		for k in new.keys():
			if k in old.keys():
				old[k] += new[k]
			else:
				old[k] = new[k]
		return old

	@staticmethod
	def all_ignore_words(words):
		all_ignore = True
		for word in words.split():
			if word not in IGNORE_WORDS:
				all_ignore = False
				break
		return all_ignore

	@staticmethod
	def is_subset(p, all_p):
		is_sub = False
		for a in all_p:
			if p in a and p != a:
				is_sub = True
				break
		return is_sub

	@staticmethod
	def get_phrase_counts(lyrics, phrases, option):

		counts = []

		for phrase in phrases:
			if len(phrase) >= 20:
				continue
			if phrase in lyrics:
				counts.append({"text": phrase, "size": lyrics.count(phrase)})

		max_count = max([c["size"] for c in counts]);

		for word in list(counts):
			if word["size"] < .05*max_count:
				counts.remove(word)

		if option == 'default':
			return ComputeCounts.default_count(counts)
		elif option == 'gayson':
			return ComputeCounts.gayson_count(counts)

	@staticmethod
	def default_count(counts):
		return json.dumps(counts, separators=(',', ':')).replace('"', '\"')

	@staticmethod
	def gayson_count(counts):
		max_count = max([c["size"] for c in counts]);
		total = sum([c["size"] for c in counts])
		d = len(counts)
		alpha = .5
		multiplier = 75 * (total + d*alpha) / (max_count + alpha)

		formated_counts = []

		for word in counts:
			s = multiplier*(word["size"] + alpha) / (total + d*alpha)
			if s < 10:
				continue
			word["size"] = s
			formated_counts.append(word)

		return json.dumps(formated_counts, separators=(',', ':')).replace('"', '\"')

	@staticmethod
	def all_lcs(artist_lines, stored=True):

		longest_common = {}

		if stored:
			for artist in artist_lines.keys():
				with open('phrases/' + artist, 'r') as inputfile:
					longest_common[artist] = json.load(inputfile)[artist]
		else:
			# xxx skip doing this for now
			# find most frequent longest-common-subseq for each artist
			for artist in artist_lines.keys():
				for lin1 in artist_lines[artist]:
					line1 = tuple(lin1[1].split())
					for lin2 in artist_lines[artist]:
						line2 = tuple(lin2[1].split())
						if line1 != line2:
							if artist in longest_common.keys():
								longest_common[artist] = aggregate(longest_common[artist],lcs(line1, line2))
							else:
								longest_common[artist] = lcs(line1, line2)

			for artist in longest_common.keys():
				with open(artist, 'w') as outfile:
					json.dump({artist: longest_common[artist]}, outfile)	


		return longest_common
	
	@staticmethod
	def filter_all_phrases(longest_common):
		# norm_phrases = {}
		for artist in longest_common.keys():
			sorted_lcss = sorted(longest_common[artist].iteritems(), key=operator.itemgetter(1), reverse=True)
			longest_common[artist] = ComputeCounts.filter_phrases(sorted_lcss)
			longest_common[artist] = longest_common[artist][:(min(len(longest_common[artist])/4, 15))]
		# return norm_phrases

	@staticmethod
	def filter_phrases(phrases):

		norm_phrases = []
		all_p = [p[0] for p in phrases]

		for phrase in phrases:
			p = phrase[0]
			if not ComputeCounts.all_ignore_words(p) and not ComputeCounts.is_subset(p, all_p):
				norm_phrases.append(phrase)
		return norm_phrases

	@staticmethod
	def get_all_phrase_counts(db_name, table_name, artist_lyrics, norm_phrases, option):
		for artist in norm_phrases.keys():
			phrase_counts = DBHelper.get_phrase_counts(db_name, table_name, artist)
			if phrase_counts:
				norm_phrases[artist] = phrase_counts
			else:
				norm_phrases[artist] = ComputeCounts.get_phrase_counts(artist_lyrics[artist], [p[0] for p in norm_phrases[artist]], option)
				DBHelper.update_phrase_counts(db_name, table_name, artist, norm_phrases[artist])
		

	@staticmethod
	def compute_counts(db_name, table_name, artists):

		# artist -> [(phrase,occurance)]
		sql_dict = ComputeCounts.all_lcs(artists)

		for artist in sql_dict.keys():
			# print sql_dict[artist]
			print len(sql_dict[artist])
			break

		print "=====Filtering phrases====="

		# artist -> [(phrase, occurance)] w/ subset and ignore phrases removed
		ComputeCounts.filter_all_phrases(sql_dict)
		for artist in sql_dict.keys():
			print artist , sql_dict[artist]
			print len(sql_dict[artist])
			# break

		print "=====Getting phrase counts ====="

		# artist -> [{text:,size:}]
		ComputeCounts.get_all_phrase_counts(db_name, table_name, dict((key, value) for (key, value) in artists.iteritems()), sql_dict, 'gayson')
		for artist in sql_dict.keys():
			print artist, sql_dict[artist]
			# break

