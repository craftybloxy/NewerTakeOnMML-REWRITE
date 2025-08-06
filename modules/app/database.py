import sqlite3
from rich.pretty import pprint


class Database:
    def __init__(self, services, db_name=":memory:"):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.create_tables()
        self.init_services(services)
        self.cur.execute("PRAGMA foreign_keys = ON;")
    def execute(self, query):
        self.cur.execute(query)
    def create_tables(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS services (
                id TEXT PRIMARY KEY
            )
        """
        )

        # Create tables for artists, albums, songs, playlists, and playlist-songs relationships
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY,
                name TEXT,
                source_id TEXT,
                FOREIGN KEY (source_id) REFERENCES services(id)
                
            )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS artists_source_info(
                service_id TEXT NOT NULL,
                artist_id INTEGER,
                service_artist_id TEXT NOT NULL,
                service_artist_name TEXT,
                UNIQUE (service_id, service_artist_id, service_artist_name),
                PRIMARY KEY(service_id, artist_id),
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
                )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist_id INTEGER,
                source_id TEXT,
                FOREIGN KEY (source_id) REFERENCES services(id)
                UNIQUE (artist_id, title),
                FOREIGN KEY (artist_id) REFERENCES artists(id)
            )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS songs_source_info(
                service_id TEXT NOT NULL,
                song_id INTEGER,
                service_song_id TEXT NOT NULL,
                service_song_title TEXT,
                PRIMARY KEY(service_id, song_id),
                FOREIGN KEY (song_id) REFERENCES songs (id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                source_id TEXT,
                FOREIGN KEY (source_id) REFERENCES services(id)
            )
        """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists_source_info(
                service_id TEXT NOT NULL,
                playlist_id INTEGER,
                service_playlist_id TEXT NOT NULL,
                service_playlist_name TEXT,
                PRIMARY KEY(service_id, playlist_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id INTEGER,
                song_id INTEGER,
                PRIMARY KEY (playlist_id, song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                FOREIGN KEY (song_id) REFERENCES songs (id)
            )
        """
        )
        self.con.commit()


    
    def init_services(self, services):
        """
        services (list): a list of service_id
        """
        # from list to list of tupples
        services_tuples = ((service_id,) for service_id in services)
        self.cur.executemany(
            """
            INSERT OR IGNORE INTO services(id) VALUES (?)
            """,
            services_tuples,
        )

    def insert_artist(self, data):
        # Tries first to find the artist_id directly using service_artist_id in artists_source_info
        self.cur.execute(
            """
            SELECT artist_id 
            FROM artists_source_info 
            WHERE service_id = (?) 
            AND service_artist_id = (?)
            """,
            (data["service_id"], data["artist_id"]),
        )
        artist_id_from_db = self.cur.fetchone()
        if artist_id_from_db:
            artist_id = artist_id_from_db[0]
            return artist_id

        # Tries to see if its an homonym using the service's id system
        self.cur.execute(
            """
            SELECT artist_id 
            FROM artists_source_info 
            WHERE service_id = (?) 
            AND service_artist_name = (?)
            AND NOT service_artist_id = (?)
            """,
            (data["service_id"], data["artist_name"], data["artist_id"]),
        )
        homonym_from_db = self.cur.fetchone()
        if homonym_from_db:
            self.cur.execute(
                """
                INSERT INTO artists(name, source_id) VALUES(?, ?)
                """,
                ((data["artist_name"],data["service_id"])),
            )

            artist_id = self.cur.lastrowid
        else:
            # Check if the artist is already in the db using its name
            self.cur.execute(
                "SELECT id FROM artists WHERE name = ?", (data["artist_name"],)
            )

            artist = self.cur.fetchone()

            if artist:
                artist_id = artist[0]  # Artist found, use the existing ID
            else:
                # Artist does not exist, insert a new one
                self.cur.execute(
                    "INSERT INTO artists(name, source_id) VALUES(?, ?)", (data["artist_name"],data["service_id"])
                )
                artist_id = self.cur.lastrowid

        # Fills out artists_source_info
        self.cur.execute(
            """
            INSERT OR IGNORE INTO artists_source_info(service_id, artist_id, service_artist_id, service_artist_name)
            VALUES (?, ?, ?, ?)
            """,
            (
                data["service_id"],
                artist_id,
                data["artist_id"],
                data["artist_name"],
            ),
        )
        return artist_id

    def insert_artists(self, artists):
        for artist in artists:
            self.insert_artist(artist)

    def insert_song(self, data):
        #
        # ÉTAPE 1: Identifier l'artiste avec un artist_id
        #
        artist_id = self.insert_artist(data)
        #
        # ÉTAPE 2: Identifier la musique
        #
        # TODO Identifier la musique avec l'auteur et la musique
        # TODO ajouter un moyen manuel de le faire
        db_song_id = data.get("db_song_id")
        if db_song_id:
            song_id = db_song_id
            # Fills out songs_source_info
            self.cur.execute(
                """
                INSERT OR IGNORE INTO songs_source_info(service_id, song_id, service_song_id, service_song_title)
                VALUES (?, ?, ?, ?)
                """,
                (
                    data["service_id"],
                    song_id,
                    data["song_id"],
                    data["song_title"],
                ),
            )
        else:
            # Tries to find the song_id using service_song_id in songs_source_info
            self.cur.execute(
                """
                SELECT song_id 
                FROM songs_source_info 
                WHERE service_id = (?) 
                AND service_song_id = (?)
                """,
                (data["service_id"], data["song_id"]),
            )
            song_id_from_db = self.cur.fetchone()
            if song_id_from_db:
                song_id = song_id_from_db[0]
            else:
                # Uses the unique name constraints to find or create an song_id
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO songs(title, artist_id, source_id) VALUES(?, ?, ?)
                    """,
                    ((data["song_title"], artist_id, data["service_id"])),
                )
                # fetch the songid
                self.cur.execute(
                    """
                    SELECT id FROM songs WHERE title=? and artist_id=?
                    """,
                    ((data["song_title"], artist_id)),
                )
                song_id = self.cur.fetchone()[0]

                # Fills out songs_source_info
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO songs_source_info(service_id, song_id, service_song_id, service_song_title)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        data["service_id"],
                        song_id,
                        data["song_id"],
                        data["song_title"],
                    ),
                )
        return song_id

    def insert_songs(self, songs):
        if songs:
            for data in songs:
                if data:
                    self.insert_song(data)
        self.con.commit()

    def insert_playlist(self, data):
        #
        # 1 - Get a playlist_id
        #
        db_playlist_id = data.get("db_playlist_id")
        if db_playlist_id:
            playlist_id = db_playlist_id
            # Fills out playlists_source_info
            self.cur.execute(
                """
                INSERT OR IGNORE INTO playlists_source_info(service_id, playlist_id, service_playlist_id, service_playlist_name)
                VALUES (?, ?, ?, ?)
                """,
                (
                    data["service_id"],
                    playlist_id,
                    data["playlist_id"],
                    data["playlist_name"],
                ),
            )
        else:
            self.cur.execute(
                """
                SELECT playlist_id 
                FROM playlists_source_info 
                WHERE service_id = (?) 
                AND service_playlist_id = (?)
                """,
                (data["service_id"], data["playlist_id"]),
            )
            playlist_id_from_db = self.cur.fetchone()
            if playlist_id_from_db:
                playlist_id = playlist_id_from_db[0]
            else:
                # Uses the unique name constraints to find or create an playlist_id
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO playlists(name) VALUES(?)
                    """,
                    ((data["playlist_name"],)),
                )
                # fetch the playlist_id
                self.cur.execute(
                    """
                    SELECT id FROM playlists WHERE name=?
                    """,
                    ((data["playlist_name"],)),
                )
                playlist_id = self.cur.fetchone()[0]

                # Fills out playlists_source_info
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO playlists_source_info(service_id, playlist_id, service_playlist_id, service_playlist_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        data["service_id"],
                        playlist_id,
                        data["playlist_id"],
                        data["playlist_name"],
                    ),
                )

        # 2 - Add the songs in playlist_songs by getting their id using insert_song
        for song in data["songs"]:
            # Use insert_song to insert the song if not already in the database
            # This will insert the song and return its ID
            song_id = self.insert_song(song)

            # Insert the relationship between the playlist and song into playlist_songs
            self.cur.execute(
                "INSERT OR IGNORE INTO playlist_songs(playlist_id, song_id) VALUES (?, ?)",
                (playlist_id, song_id),
            )


    def insert_playlists(self, playlists):
        if playlists:
            for playlist in playlists:
                self.insert_playlist(playlist)
        self.con.commit()

    def fetch_unidentified_songs(self, service_id):
        results = []
        self.cur.execute(
            """
            SELECT services.id, artists_source_info.service_artist_id , artists_source_info.service_artist_name, artists.name, songs_source_info.service_song_id, songs_source_info.service_song_title, songs.title, songs.id
            FROM songs, services
            JOIN artists ON songs.artist_id = artists.id

            LEFT JOIN artists_source_info
            ON artists.id = artists_source_info.artist_id 
            AND artists_source_info.service_id = services.id

            LEFT JOIN songs_source_info
            ON songs.id = songs_source_info.song_id 
            AND songs_source_info.service_id = services.id

            WHERE services.id = (?) AND songs_source_info.service_song_title IS NULL
            """,
            (service_id,),
        )
        raw_unidentified_songs = self.cur.fetchall()
        for song_data in raw_unidentified_songs:
            results.append(
                {
                    "service_id": song_data[0],
                    "artist_id": song_data[1],
                    "artist_name": song_data[2],
                    "input_artist_name": song_data[3],
                    "song_id": song_data[4],
                    "song_title": song_data[5],
                    "input_song_title": song_data[6],
                    "db_song_id": song_data[7]
                }
            )
        return results

    def fetch_unidentified_playlists(self, service_id):
        results = []
        self.cur.execute(
            """
            SELECT services.id, playlists.name,playlists_source_info.service_playlist_id, playlists.id
            FROM playlists, services
            LEFT JOIN playlists_source_info ON playlists.id = playlists_source_info.playlist_id AND playlists_source_info.service_id = services.id 
            WHERE services.id = (?) AND playlists_source_info.service_playlist_id IS NULL
            """,
            (service_id,),
        )
        raw_unidentified_playlists = self.cur.fetchall()
        for playlist_data in raw_unidentified_playlists:
            results.append(
                {"service_id": playlist_data[0], "playlist_name": playlist_data[1],"playlist_id":playlist_data[2], "db_playlist_id":playlist_data[3]}
            )
        return results

    def fetch_playlists(self, service_id):
        pass

    def print_table(self, table):

        print("=" * 80)
        print(f"{'Table: ' + table:^80}")
        print("=" * 80)

        # Fetch column names
        self.cur.execute(f"PRAGMA table_info({table});")
        column_info = self.cur.fetchall()
        column_names = [column[1] for column in column_info]

        # Print column names
        print("\t".join(f"{col:<20}" for col in column_names))
        print("-" * 80)

        # Fetch and print the first 100 rows from the table
        self.cur.execute(f"SELECT * FROM {table};")
        rows = self.cur.fetchall()

        if rows:
            # Print each row of data
            for row in rows:
                print("\t".join(f"{str(cell):<20}" for cell in row))
            print("-" * 4 + f"{len(rows)} entries" + "-" * 80)
        else:
            print(f"{'No data in this table':^80}")

        # Add some space between tables
        print("\n")

    def print_all_table(self):
        # Fetch all table names from sqlite_master
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        print(tables)
        # Print a header
        print("=" * 80)
        print(f"{'TABLES IN THE DATABASE':^80}")
        print("=" * 80)

        for table in tables:
            self.print_table(table[0])

    def find_duplicates(self, table, wanted_column, id_column):
        """
        Broken from now.. finds songs from spotify and youtube to be duplicated
        """
        # Construct the query with dynamic table and column names
        query = f"""
        SELECT {wanted_column}, COUNT(*) AS cnt, GROUP_CONCAT({id_column}) AS nos
        FROM {table}
        GROUP BY {wanted_column}
        HAVING COUNT(*) > 1
        """

        # Execute the query
        self.cur.execute(query)

        # Fetch and return all results
        return self.cur.fetchall()


if __name__ == "__main__":
    Spotify_songs = [
        {
            "service_id": "spotify",
            "artist_id": "1muzcpVFKmKSrT7rVNAwBB",
            "artist_name": "late night drive home",
            "song_id": "4RuSob7vIafKuRwFQ3y2QA",
            "song_title": "talk to me (before the night ends)",
        },
        {
            "service_id": "spotify",
            "artist_id": "35EN35AllxAEzEdDMl7YFT",
            "artist_name": "Loni",
            "song_id": "4RuSob7vIafKuRwFQ3y2QA",
            "song_title": "talk to me (before the night ends)",
        },
        {
            "service_id": "spotify",
            "artist_id": "4X76fYx1a6EmEvCqDudesG",
            "artist_name": "Netrum",
            "song_id": "3SuxtjdFxY3RIaWyPgtkfk",
            "song_title": "Phoenix",
        },
        {
            "service_id": "spotify",
            "artist_id": "4jbh1BeqqFVqqH7GACcWdH",
            "artist_name": "Halvorsen",
            "song_id": "3SuxtjdFxY3RIaWyPgtkfk",
            "song_title": "Phoenix",
        },
        {
            "service_id": "spotify",
            "artist_id": "5iMYu8Sj8dZEDsWJxSFwPP",
            "artist_name": "Jhariah",
            "song_id": "3ekN6ytJmlh5y93ChIqOtA",
            "song_title": "RISK, RISK, RISK!",
        },
        {
            "service_id": "spotify",
            "artist_id": "4MCBfE4596Uoi2O4DtmEMz",
            "artist_name": "Juice WRLD",
            "song_id": "1a7WZZZH7LzyvorhpOJFTe",
            "song_title": "Wasted (feat. Lil Uzi Vert)",
        },
        {
            "service_id": "spotify",
            "artist_id": "4O15NlyKLIASxsJ0PrXPfz",
            "artist_name": "Lil Uzi Vert",
            "song_id": "1a7WZZZH7LzyvorhpOJFTe",
            "song_title": "Wasted (feat. Lil Uzi Vert)",
        },
        {
            "service_id": "spotify",
            "artist_id": "5nWYvcpaqKtp08cYxjOfFr",
            "artist_name": "Gibran Alcocer",
            "song_id": "0yfMign5fsLtw5I4pK73ge",
            "song_title": "Solas",
        },
        {
            "service_id": "spotify",
            "artist_id": "0NIPkIjTV8mB795yEIiPYL",
            "artist_name": "Wallows",
            "song_id": "57RA3JGafJm5zRtKJiKPIm",
            "song_title": "Are You Bored Yet? (feat. Clairo)",
        },
        {
            "service_id": "spotify",
            "artist_id": "3l0CmX0FuQjFxr8SK7Vqag",
            "artist_name": "Clairo",
            "song_id": "57RA3JGafJm5zRtKJiKPIm",
            "song_title": "Are You Bored Yet? (feat. Clairo)",
        },
    ]
    songs = [
        {
            "service_id": "spotify",
            "artist_id": "artist100_spotify_id",
            "artist_name": "John Doe",
            "song_id": "song100_spotify_id",
            "song_title": "Amazing Journey",
        },
        {
            "service_id": "youtube",
            "artist_id": "artist100_youtube_id",
            "artist_name": "John Doe",
            "song_id": "song100_youtube_id",
            "song_title": "Amazing Journey",
        },
        {
            "service_id": "spotify",
            "artist_id": "artist200_spotify_id",
            "artist_name": "Jane Smith",
            "song_id": "song200_spotify_id",
            "song_title": "Sunset Dreams",
        },
        {
            "service_id": "spotify",
            "artist_id": "artist101_spotify_id",
            "artist_name": "John Doe FAN",
            "song_id": "song101_spotify_id",
            "song_title": "Amazing Journey Remix",
        },
        {
            "service_id": "spotify",
            "artist_id": "artist201_spotify_id",
            "artist_name": "Jane Smith FAN",
            "song_id": "song201_spotify_id",
            "song_title": "Sunset Dreams COVER",
        },
    ]

    playlists = [
        {
            "service_id": "spotify",
            "playlist_id": "playlist101_spotify_id",
            "playlist_name": "Morning Vibes",
            "songs": [
                {
                    "service_id": "spotify",
                    "artist_id": "artist100_spotify_id",
                    "artist_name": "John Doe",
                    "song_id": "song100_spotify_id",
                    "song_title": "Amazing Journey",
                },
                {
                    "service_id": "youtube",
                    "artist_id": "artist100_youtube_id",
                    "artist_name": "John Doe",
                    "song_id": "song100_youtube_id",
                    "song_title": "Amazing Journey",
                },
                {
                    "service_id": "spotify",
                    "artist_id": "artist200_spotify_id",
                    "artist_name": "Jane Smith",
                    "song_id": "song200_spotify_id",
                    "song_title": "Sunset Dreams",
                },
            ],
        }
    ]
    data_quack = {
    "service_id": "youtube",
    "artist_id": "quack",
    "artist_name": "quack",
    "song_id": "quack",
    "song_title": "quack",
    }
    db = Database(["spotify", "youtube"], "library.db")
    
    db.insert_songs(songs)
    db.insert_playlists(playlists)

    # [('artists',), ('artists_source_info',), ('songs',), ('songs_source_info',), ('playlists',), ('playlists_source_info',), ('playlist_songs',)]
    # db.print_table("artists_source_info")
    db.print_all_table()

    pprint(db.fetch_unidentified_songs("youtube"))
    pprint(db.fetch_unidentified_playlists("youtube"))
