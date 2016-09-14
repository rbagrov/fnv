-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;
CREATE DATABASE tournament;
\connect tournament
CREATE TABLE players(
   ID SERIAL PRIMARY KEY  NOT NULL,
   NAME           TEXT    NOT NULL,
   WINS           INT     NOT NULL,
   MATCHES        INT     NOT NULL
);
CREATE TABLE games(
   ID SERIAL PRIMARY KEY  NOT NULL,
   AID            INT	  NOT NULL,
   BID            INT     NOT NULL
);


