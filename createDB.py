# this file will create a sample database using sqlite3 to test the streamlit form

import pyodbc as odbc


def getID(cursor: odbc.Cursor, movies: dict):
    director_id = cursor.execute(
        f"""
        SELECT pk_director_Id FROM director 
        WHERE director_firstname = '{movies["directorF"]}' 
        AND director_lastname = '{movies["directorL"]}'
    """).fetchone()

    production_id = cursor.execute(
        f"""
        SELECT pk_production_Id FROM production 
        WHERE production_name = '{movies["studio"]}' 
    """).fetchone()

    genre_id = cursor.execute(
        f"""
        SELECT pk_genre_Id FROM genre
        WHERE genre_name = '{movies["genre"]}' 
    """).fetchone()

    lead_actor_id = cursor.execute(
        f"""
        SELECT pk_lead_actor_Id FROM lead_actor
        WHERE lead_actor_firstname = '{movies["leadF"]}' 
        AND lead_actor_lastname = '{movies["leadL"]}'
    """).fetchone()

    movie_id = cursor.execute(
        f"""
        SELECT pk_movie_Id FROM movie
        WHERE movie_title = '{movies["title"]}' 
        AND movie_release_year = {int(movies["year"])}
    """).fetchone()

    idDictionary = {
        "director_id": director_id,
        "production_id": production_id,
        "genre_id": genre_id,
        "lead_actor_id": lead_actor_id,
        "movie_id": movie_id
    }

    return idDictionary


def connectDB(driver: str, server: str, database: str):
    conn_string = f"""
        Driver={{{driver}}};
        SERVER={{{server}}};
        DATABASE={{{database}}};
        Trusted_Connection=yes;
    """

    conn = odbc.connect(conn_string)

    c = conn.cursor()

    return conn, c


def insertIntoDB(conn: odbc.Connection, cursor: odbc.Cursor, movies: dict, user: dict):
    ids = getID(cursor, movies)

    if (ids["genre_id"] == None):
        cursor.execute(
            """
            INSERT INTO genre
            VALUES (?)
            """, (movies["genre"])
        )
        conn.commit()
        ids = getID(cursor, movies)

    if (ids["production_id"] == None):
        cursor.execute(
            """
            INSERT INTO production
            VALUES (?, ?)
            """, (movies["studio"], movies["location"])
        )
        conn.commit()
        ids = getID(cursor, movies)

    if (ids["director_id"] == None):
        cursor.execute(
            """
            INSERT INTO director
            VALUES (?, ?)
            """, (movies["directorF"], movies["directorL"])
        )
        conn.commit()
        ids = getID(cursor, movies)

    if (ids["lead_actor_id"] == None):
        cursor.execute(
            """
            INSERT INTO lead_actor
            VALUES (?, ?)
            """, (movies["leadF"], movies["leadL"])
        )
        conn.commit()
        ids = getID(cursor, movies)

    if (ids["movie_id"] == None):
        cursor.execute(
            """
            INSERT INTO movie
            VALUES (?, ?, ?, ?, ?, ?)
            """, (movies["title"], movies["year"], ids["genre_id"][0], ids["director_id"][0], ids["production_id"][0], ids["lead_actor_id"][0])
        )
        conn.commit()
        ids = getID(cursor, movies)

    cursor.execute(
        """
            INSERT INTO viewer
            VALUES (?, ?, ?, ?, ?, ?)
            """, (user["fname"], user["lname"], user["age"], user["nationality"], user["gender"], ids["movie_id"][0])
    )

    conn.commit()
