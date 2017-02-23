-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- delete database if it exists
DROP DATABASE IF EXISTS tournament;

-- create database 
CREATE DATABASE tournament;

-- connect to db
\c tournament;

-- delete table if it exists
-- DROP TABLE IF EXISTS players;

-- players table
CREATE TABLE players (
	id SERIAL UNIQUE,
	name TEXT NOT NULL
);

-- delete table if it exists
--DROP TABLE IF EXISTS matches;

-- matches table
CREATE TABLE matches (
	game_id SERIAL UNIQUE,
	winner INT REFERENCES players(id) ON DELETE CASCADE,
	loser INT REFERENCES players(id) ON DELETE CASCADE
);


-- insert players
-- INSERT INTO players (name) VALUES ('Sally');
-- INSERT INTO players (name) VALUES ('Yuki');


-- insert result for a single match
-- INSERT INTO matches (WINNER, LOSER) VALUES (1, 2);

-- create a view to see wins
CREATE VIEW wins
AS
	SELECT players.id, players.name, count(matches.winner) AS wins 
	FROM players LEFT JOIN matches ON players.id = matches.winner
	GROUP BY players.id, players.name
	ORDER BY wins DESC;

-- create a view to see losses
CREATE VIEW losses
AS
	SELECT players.id, players.name, count(matches.loser) AS losses 
	FROM players LEFT JOIN matches ON players.id = matches.loser
	GROUP BY players.id, players.name
	ORDER BY losses DESC;

-- create view to see standings
CREATE VIEW standings
AS
	SELECT wins.id,
		   wins.name,
		   wins.wins,
		   wins.wins + losses.losses AS matches
	FROM wins,
		 losses
	WHERE wins.id = losses.id
	ORDER BY wins DESC;	 	   	