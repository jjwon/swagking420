#!/usr/bin/python
import os
from SourceParser import SourceParser
from ComputeCounts import ComputeCounts
import time
import sys

if __name__ == "__main__":


	start_time = time.time()

	db_name = sys.argv[1]
	table_name = sys.argv[2]

	base_dir = os.getcwd()
	artists_path = base_dir + "/artists/"

	artists_lyrics = SourceParser.normalize_artists(artists_path, db_name, table_name)

	ComputeCounts.compute_counts(db_name, table_name,artists_lyrics)

	print "--- %s seconds ---" % str(time.time() - start_time)