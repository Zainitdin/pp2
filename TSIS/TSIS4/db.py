import psycopg2
from config import DB_CONFIG


# 🔹 Create connection to PostgreSQL using config.py
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# 🔹 Get existing player OR create new one
def get_or_create_player(username):
    conn = get_connection()     # connect to DB
    cur = conn.cursor()         # cursor = allows SQL execution

    # Check if user already exists
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()

    if player:
        # If found → reuse existing ID
        player_id = player[0]
    else:
        # If not → create new player
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()  # save changes

    # Close DB resources
    cur.close()
    conn.close()

    return player_id


# 🔹 Save game session after game over
def save_game(username, score, level):
    # First ensure player exists
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()

    # Insert game result into table
    cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


# 🔹 Get Top 10 leaderboard
def get_top_10():
    conn = get_connection()
    cur = conn.cursor()

    # Join players + sessions and sort by score DESC
    cur.execute(
        """
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
        """
    )

    rows = cur.fetchall()  # get all rows

    cur.close()
    conn.close()

    return rows


# 🔹 Get best score of current user
def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username = %s
        """,
        (username,)
    )

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    # If no games yet → return 0
    return result if result is not None else 0