import sqlite3

class DatabaseEntity:
    def __init__(self, table_name, primary_key, connection, cursor):
        """
        Base class for handling common database operations.

        :param table_name: The name of the table.
        :param primary_key: The primary key column of the table.
        :param connection: The SQLite connection object.
        :param cursor: The SQLite cursor object.
        """
        self.table_name = table_name
        self.primary_key = primary_key
        self.con = connection
        self.cur = cursor


    def add_or_merge(self, data_dict, unique_columns=None):
        """
        Adds a new record to the database or merges it with an existing one.
        Uses helper methods to resolve names to IDs if needed and only inserts data if the column exists.

        :param data_dict: A dictionary containing the columns and values for the record.
        :param unique_columns: A list of column names that are used to identify unique records.
        """
        # Resolve names to IDs if necessary
        data_dict = self.resolve_names_to_ids(data_dict)

        # Get the valid columns from the table schema
        valid_columns = self.get_table_columns()
        
        # Filter data_dict to include only valid columns
        filtered_data = {key: value for key, value in data_dict.items() if key in valid_columns}
        
        if not filtered_data:
            print("No valid columns found to insert data.")
            return
        

        if unique_columns is None:
            # Default unique columns if not provided
            unique_columns = list(filtered_data.keys())[:2]  # Customize as needed

        # Check if all unique columns are in the filtered_data
        if not all(col in filtered_data for col in unique_columns):
            print("Not all unique columns are present in the data.")
            return
        
        unique_values = tuple(filtered_data[col] for col in unique_columns)
        unique_conditions = ' AND '.join([f"{col} = ?" for col in unique_columns])

        try:
            # Check if the record already exists based on unique columns
            self.cur.execute(f"""
                SELECT {self.primary_key} FROM {self.table_name} WHERE {unique_conditions}
            """, unique_values)
            result = self.cur.fetchone()

            if result:
                # Record exists, update the existing entry
                record_id = result[0]
                placeholders = ', '.join([f"{key} = ?" for key in filtered_data.keys()])
                values = list(filtered_data.values()) + [record_id]

                self.cur.execute(f"""
                    UPDATE {self.table_name}
                    SET {placeholders}
                    WHERE {self.primary_key} = ?
                """, values)
                print(f"Record in '{self.table_name}' updated.")
            else:
                # Record does not exist, insert a new entry
                columns = ', '.join(filtered_data.keys())
                placeholders = ', '.join(['?'] * len(filtered_data))
                values = list(filtered_data.values())

                self.cur.execute(f"""
                    INSERT INTO {self.table_name} ({columns})
                    VALUES ({placeholders})
                """, values)
                print(f"Record added to '{self.table_name}'.")

            # Commit the changes to the database
            self.con.commit()

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}")
        except sqlite3.Error as e:
            print(f"An SQLite error occurred: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")


    
    def get_table_columns(self):
        """
        Retrieve the column names from the table schema.
        """
        self.cur.execute(f"PRAGMA table_info({self.table_name})")
        columns_info = self.cur.fetchall()
        columns = [col[1] for col in columns_info]
        return columns
    
    def resolve_names_to_ids(self, data_dict):
        """
        Resolves names in data_dict to their corresponding IDs if applicable.

        :param data_dict: A dictionary containing the columns and values for    the record.
        :return: The updated dictionary with names replaced by IDs.
        """
        try:
            if 'artist' in data_dict:
                artist_name = data_dict['artist']
                self.cur.execute("""
                    SELECT artistid 
                    FROM artist 
                    WHERE name = ? 
                    UNION 
                    SELECT artistid 
                    FROM artist_alt 
                    WHERE artist = ?
                """, (artist_name, artist_name))
                artist_result = self.cur.fetchone()
                if artist_result:
                    data_dict['artistid'] = artist_result[0]
                else:
                    print(f"Artist '{artist_name}' not found in the database.")

            if 'album' in data_dict and 'artistid' in data_dict:
                album_title = data_dict['album']
                artist_id = data_dict['artistid']
                self.cur.execute("""
                    SELECT albumid 
                    FROM album 
                    WHERE title = ? AND artistid = ?
                """, (album_title, artist_id))
                album_result = self.cur.fetchone()
                if album_result:
                    data_dict['albumid'] = album_result[0]
                else:
                    print(f"Album '{album_title}' by artist ID '{artist_id}'    not found in the database.")

            if 'song' in data_dict and 'artistid' in data_dict:
                song_title = data_dict['song']
                artist_id = data_dict['artistid']
                self.cur.execute("""
                    SELECT songid 
                    FROM song 
                    WHERE title = ? AND artistid = ?
                """, (song_title, artist_id))
                song_result = self.cur.fetchone()
                if song_result:
                    data_dict['songid'] = song_result[0]
                else:
                    print(f"Song '{song_title}' by artist ID '{artist_id}' not  found in the database.")

            if 'playlist' in data_dict:
                playlist_title = data_dict['playlist']
                self.cur.execute("""
                    SELECT playlistid 
                    FROM playlist 
                    WHERE title = ?
                """, (playlist_title,))
                playlist_result = self.cur.fetchone()
                if playlist_result:
                    data_dict['playlistid'] = playlist_result[0]
                else:
                    print(f"Playlist '{playlist_title}' not found in the    database.")

        except Exception as e:
            print(f"An error occurred: {e}")

        return data_dict

    
class Song(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('song', 'songid', connection, cursor)

class Album(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('album', 'albumid', connection, cursor)

class Artist(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('artist', 'artistid', connection, cursor)

class Song_alt(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('song_alt', 'id', connection, cursor)

class Album_alt(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('album_alt', 'id', connection, cursor)

class Artist_alt(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('artist_alt', 'id', connection, cursor)

class Playlist(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('playlist', 'playlistid', connection, cursor)

class Playlist_index(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('playlist_index', 'playlistid', connection, cursor)

class Playlist_alt(DatabaseEntity):
    def __init__(self, connection, cursor):
        super().__init__('playlist_alt', 'id', connection, cursor)

class Database:
    def __init__(self, db_name=":memory:"):
        """
        Initializes the Database class.

        :param db_name: The name of the SQLite database file. If ":memory:", creates a database in RAM.
        """
        self.db_name = db_name
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        # Enable foreign key constraints
        self.cur.execute("PRAGMA foreign_keys = ON")

        self.setup_schema()

        # Initialize entities
        self.song = Song(self.con, self.cur)
        self.album = Album(self.con, self.cur)
        self.artist = Artist(self.con, self.cur)
        self.playlist = Playlist(self.con, self.cur)
        self.song_alt = Song_alt(self.con, self.cur)
        self.album_alt = Album_alt(self.con, self.cur)
        self.artist_alt = Artist_alt(self.con, self.cur)
        self.playlist_alt = Playlist_alt(self.con, self.cur)
        self.playlist_index = Playlist_index(self.con, self.cur)

    def setup_schema(self):
        """
        Sets up the database schema by creating necessary tables.
        """

        # Creating the artist table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS artist(
                artistid INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                genre TEXT
            )
        """)

        # Creating the album table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS album(
                albumid INTEGER PRIMARY KEY,
                artistid INTEGER,
                title TEXT,
                year TEXT,
                genre TEXT,
                FOREIGN KEY(artistid) REFERENCES artist(artistid)
            )
        """)

        # Creating the song table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS song(
                songid INTEGER PRIMARY KEY,
                albumid INTEGER,
                artistid INTEGER,
                title TEXT,
                genre TEXT,
                year TEXT,
                FOREIGN KEY(artistid) REFERENCES artist(artistid),
                FOREIGN KEY(albumid) REFERENCES album(albumid)
            )
        """)

        # Creating the playlist table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS playlist(
                playlistid INTEGER PRIMARY KEY,
                title TEXT
            )
        """)


        # Creating the playlist_index table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS playlist_index(
                songid INTEGER NOT NULL,
                playlistid INTEGER NOT NULL,
                PRIMARY KEY (songid, playlistid)
                FOREIGN KEY(songid) REFERENCES song(songid),
                FOREIGN KEY(playlistid) REFERENCES playlist(playlistid)
            )
        """)

        # Creating the artist_alt table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS artist_alt(
                id INTEGER PRIMARY KEY,
                in_service_id INTEGER,
                artistid INTEGER,
                url TEXT,
                artist TEXT,
                plugin TEXT,
                FOREIGN KEY(artistid) REFERENCES artist(artistid)
            )
        """)

        # Creating the album_alt table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS album_alt(
                id INTEGER PRIMARY KEY,
                in_service_id INTEGER,
                albumid INTEGER,
                url TEXT,
                album TEXT,
                plugin TEXT,
                FOREIGN KEY(albumid) REFERENCES album(albumid)
            )
        """)

        # Creating the song_alt table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS song_alt(
                id INTEGER PRIMARY KEY,
                in_service_id INTEGER,
                songid INTEGER,
                url TEXT,
                song TEXT,
                plugin TEXT,
                FOREIGN KEY(songid) REFERENCES song(songid)
            )
        """)

        # Creating the playlist_alt table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS playlist_alt(
                id INTEGER PRIMARY KEY,
                in_service_id INTEGER,
                playlistid INTEGER,
                title TEXT,
                artist TEXT,
                url TEXT,
                playlist TEXT,
                plugin TEXT,
                FOREIGN KEY(playlistid) REFERENCES playlist(playlistid)
            )
        """)

        self.con.commit()

    def print_all_tables(self):
        """
        Prints all data from all tables in the database.
        Dynamically retrieves the column names and data for each table.
        """
        try:
            # Retrieve all table names from the SQLite master table
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cur.fetchall()

            # Iterate over each table and print its data
            for table_name in tables:
                table_name = table_name[0]  # Extract the table name from the tuple
                print(f"\nTable: {table_name}")

                # Select all data from the table
                self.cur.execute(f"SELECT * FROM {table_name}")

                # Fetch the column names dynamically using cursor description
                column_names = [description[0] for description in self.cur.description]

                # Fetch all rows from the executed query
                rows = self.cur.fetchall()

                # Print column headers
                print(" | ".join(column_names))
                print("-" * (len(column_names) * 10))

                # Print each row in the table
                for row in rows:
                    print(" | ".join(map(str, row)))

        except sqlite3.Error as e:
            print(f"An SQLite error occurred: {e}")

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.con.close()
        except sqlite3.Error as e:
            print(f"An SQLite error occurred while closing the connection: {e}")

    def __del__(self):
        """
        Destructor method to ensure the database connection is closed.
        """
        self.close()

if __name__ == '__main__':
    # Create an instance of the Database class
    app = Database()

    # Adding or merging artist data first (to ensure there are no foreign key issues)
    app.artist.add_or_merge({"name": "Mother Mother", "genre": "Indie Rock"})
    app.artist.add_or_merge({"name": "Car Seat Headrest", "genre": "Rock"})

    # Adding or merging album data
    app.album.add_or_merge({"title": "O My Heart", "artist": "Mother Mother", "year": "2008", "genre": "Indie Rock"})
    app.album.add_or_merge({"title": "Twin Fantasy", "artist": "Car Seat Headrest", "year": "2018", "genre": "Rock"})

    # Adding or merging song data
    app.song.add_or_merge({"title": "Hayloft", "artist": "Mother Mother", "album": "O My Heart", "genre": "Indie Rock", "year": "2008"})
    app.song.add_or_merge({"title": "Sober to Death", "artist": "Car Seat Headrest", "album": "Twin Fantasy", "genre": "Rock", "year": "2018"})
    app.artist_alt.add_or_merge({"in_service_id": 999999,"url": "https://spotify.com/artist/1","artist": "Mother Mother", "plugin": "Spotify"
    })

    app.playlist.add_or_merge({"title":"<3"})
    app.playlist_index.add_or_merge({"song":"Sober to Death","artist":"Car Seat Headrest", "playlist":"<3"})

    app.print_all_tables()
    # Closing the database connection
    app.close()
