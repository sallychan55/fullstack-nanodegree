#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE from matches;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE from players;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = "SELECT count(*) FROM players;"
    cursor.execute(query)
    db.commit()
    total = cursor.fetchone();
    db.close()

    return total[0]  # TODO: check if query returns None


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM standings;"
    cursor.execute(query)
    standings = [row[0:4] for row in cursor.fetchall()]
    db.commit()
    db.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    cursor.execute(query, (winner, loser))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = [(row[0], row[1]) for row in playerStandings()]
    pairings = []

    num_of_games = len(standings) / 2
    # print "num_of_games: %d" % num_of_games

    for k in range(0, num_of_games):
        for i in range(0, len(standings) - 1):
            player1_id = standings[i][0]
            player1_name = standings[i][1]

            j = i + 1
            if j < len(standings):
                player2_id = standings[j][0]
                player2_name = standings[j][1]
                pairings.append((player1_id, player1_name, player2_id, player2_name))
                standings.remove((player1_id, player1_name))
                standings.remove((player2_id, player2_name))
                break

    # print "pairings: %s" % pairings
    return pairings


# Simple test
'''
deleteMatches()
deletePlayers()
registerPlayer("Twilight Sparkle")
registerPlayer("Fluttershy")
registerPlayer("Applejack")
registerPlayer("Pinkie Pie")
standings = playerStandings()
pairings = swissPairings()
[id1, id2, id3, id4, id5] = [row[0] for row in standings]
print "1st parings: %s" % pairings
reportMatch(id1, id2)
reportMatch(id3, id4)
standings = playerStandings()
pairings = swissPairings()
print "2nd parings: %s" % pairings
[id1, id2, id3, id4, id5] = [row[0] for row in standings]
reportMatch(id1, id2)
reportMatch(id3, id4)
#[id1, id2, id3, id4] = [row[0] for row in playerStandings()]
#print "standings: %s" % standings
'''
