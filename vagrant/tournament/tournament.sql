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
   ID SERIAL references players(ID),
   MATCHES           INT  NOT NULL
);

CREATE TABLE wins(
   ID SERIAL references players(ID),
   WINS              INT  NOT NULL
);

CREATE VIEW standings
AS 
  SELECT players.id, 
         players.name, 
         wins.wins, 
         matches.matches 
  FROM players 
       LEFT JOIN wins 
              ON players.id = wins.id 
       LEFT JOIN matches 
              ON players.id = matches.id 
  GROUP BY players.id, wins.wins, matches.matches;

CREATE VIEW pairings
AS
   SELECT players.id,
          players.name
   FROM players
        LEFT JOIN wins
               ON players.id = wins.id
   ORDER BY wins.wins DESC; 
