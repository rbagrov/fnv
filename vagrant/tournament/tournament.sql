-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament
CREATE TABLE players(
   ID SERIAL PRIMARY KEY,
   NAME    VARCHAR(20)    NOT NULL
);

CREATE TABLE matches(
   ID SERIAL PRIMARY KEY,
   winner INTEGER REFERENCES players(ID),
   loser INTEGER REFERENCES players(ID)
);


CREATE VIEW standings AS
   SELECT players.id, 
          players.name, 
          (SELECT COUNT(matches.winner) FROM matches WHERE players.id = matches.winner) as wins, 
          (SELECT COUNT(matches.id) FROM matches WHERE players.id = matches.winner OR players.id = matches.loser) as matches
   FROM players
   ORDER BY wins DESC;

CREATE VIEW selection AS
   SELECT standings.id,
          standings.name
   FROM standings;
