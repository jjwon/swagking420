import sqlite3

class DBHelper:

	@staticmethod
	def make_table(db_name, table_name):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		print "CREATE TABLE if not exists {} (artist_name text, lyrics text, phrase_counts text)".format(table_name)	
		c.execute("CREATE TABLE if not exists {} (artist_name text, lyrics text, phrase_counts text)".format(table_name))
		conn.commit()
		conn.close()

	@staticmethod
	def update_lyrics(db_name, table_name, artist, lyrics):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		# print'''INSERT INTO {} (artist_name, lyrics) VALUES (?,?)'''.format(table_name), (artist, lyrics)
		c.execute('''INSERT INTO {} (artist_name, lyrics) VALUES (?,?)'''.format(table_name), (artist, lyrics))
		conn.commit()
		conn.close()

	@staticmethod
	def get_lyrics(db_name, table_name, key):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute("SELECT lyrics from {} where artist_name='?'".format(table_name).replace("?", key) + ";")
		row = c.fetchone()
		conn.commit()
		conn.close()
		if row != None:
			return str(tuple(row)[0])

	@staticmethod
	def update_phrase_counts(db_name, table_name, artist, counts):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute('''UPDATE {} set phrase_counts=? where artist_name=?'''.format(table_name), (counts, artist))
		conn.commit()
		conn.close()

	@staticmethod
	def get_phrase_counts(db_name, table_name, key):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute("SELECT lyrics from {} where phrase_counts='?'".format(table_name).replace("?", key))
		row = c.fetchone()
		conn.commit()
		conn.close()
		if row != None:
			return str(tuple(row)[0])