#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import logging
import time


class logger(object):

    def __init__(self):
        '''
        References to a log file.
        Sets log config

        Args: self
        Raises:
        Returns: None
        '''
        log_file = 'tournament.log'
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s')

    def info(self, message):
        '''
        Logs info message

        Args: self, message
        Raises:
        Returns: None
        '''
        logging.info(message)

    def exception(self, message):
        '''
        Logs exception message

        Args: self, message
        Raises:
        Returns: None
        '''
        logging.exception(message)


class db(object):

    def __init__(self):
        '''
        Create references to statement objects

        Args: self
        Raises:
        Returns:
            self.insert_name - object of type string
            self.addmatch - object of type string
            self.counter - object of type string
            self.remove_players - object of type string
            self.remove_matches - object of type string
            self.standings - object of type string
            self.pairings - object of type string
            self.log - logger class instance
            self.tiner - object of type integer
        '''
        self.insert_name = 'INSERT INTO players (name) VALUES (%s);'
        self.addmatch = 'INSERT INTO matches (winner, loser) VALUES (%s, %s);'
        self.counter = 'SELECT * from players;'
        self.remove_players = 'TRUNCATE players CASCADE;'
        self.remove_matches = 'TRUNCATE matches;'
        self.standings = 'SELECT * FROM standings;'
        self.pairings = 'SELECT * FROM selection;'
        self.log = logger()
        self.timer = 1

    def open_connection(self):
        '''
        Connect to the PostgreSQL database.
        Returns a database connection and a cursor.

        Args: self
        Raises: psycopg2.OperationalError
        Returns:
                object of type list(psycopg2 connection and cursor objects)
        '''
        while True:
            try:
                connection = psycopg2.connect(
                    'dbname=tournament')
                return [connection, connection.cursor()]
            except psycopg2.OperationalError:
                self.log.info('Cannot connect. Retrying...')
                time.sleep(self.timer)

    def deletePlayers(self):
        '''
        Truncates players table

        Args: self
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type string
                object of type None
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.remove_players)
            connection.commit()
            cursor.execute(self.counter)
            if cursor.fetchone() == 0:
                return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def countPlayers(self):
        '''
        Counter entries in players table

        Args: self
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type integer
                object of type None
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.counter)
            return cursor.rowcount
        except Exception as e:
            self.log.exception(e)
            return None

    def registerPlayer(self, name):
        '''
        Insert player details into players table

        Args: self
              name - object of type string
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type string
                object of type None
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.insert_name, (name, ))
            connection.commit()
            return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def deleteMatches(self):
        '''
        Removes all matches entires

        Args: self
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type string
                object of type None
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.remove_matches)
            connection.commit()
            return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def playerStandings(self):
        '''
        Returns current standings from players table

        Args: self
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type list
                object of type None
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.standings)
            return cursor.fetchall()
        except Exception as e:
            self.log.exception(e)
            return None

    def get_pairings(self):
        '''
        Returns formatted list with player pairings

        Args: self
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
                object of type list
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.pairings)
            backlist = cursor.fetchall()
            return self.pair_rawlist(backlist, 2)
        except Exception as e:
            self.log.exception(e)
            return None

    def pair_rawlist(self, player_list, step):
        '''
        Creates a list with user pairings

        Args: self
              player_list - object of type list
              step - object of type integer
        Raises:
              IndexError - catch it if list indexes are uneven
        Returns:
                object of type list
        '''
        output = []
        try:
            for i in range(0, len(player_list), step):
                pairs = player_list[i][0], player_list[i][
                    1], player_list[i + 1][0], player_list[i + 1][1]
                output.append(pairs)
            return output
        except IndexError:
            return self.log.info('Players number is uneven')

    def reportMatch(self, uid):
        '''
        Sets match score

        Args: self
              uid - object of type list
        Raises:
                pokemon catching exceptions for log purposes
        Returns:
        '''
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.addmatch, (str(uid[0]), str(uid[1])))
            connection.commit()
            self.log.info(
                'Match between ' +
                str(uid[0]) +
                ' and ' +
                str(uid[1]) +
                ' was succefully stored')
            return 'OK'
        except Exception as e:
            self.log.exception(e)

    def query(self, **kwargs):
        '''
        Executes different queries base on keyed arguments

        Args: self
              key arguments
        Raises:
        Returns: (in descending order)
                object of type String/None
                object of type Integer/None
                object of type String/None
                object of type String/None
                object of type List/None
                object of type List/None
        '''
        for key, value in kwargs.iteritems():
            if key is 'player':
                return self.registerPlayer(value)
            if key is 'count' and value is 'yes':
                return self.countPlayers()
            if key is 'deletePlayers' and value is 'yes':
                return self.deletePlayers()
            if key is 'deleteMatches' and value is 'yes':
                return self.deleteMatches()
            if key is 'standings' and value is 'yes':
                return self.playerStandings()
            if key is 'report_match':
                self.reportMatch(value)
            if key is 'pairings' and value is 'yes':
                return self.get_pairings()


class Players(object):

    def __init__(self):
        '''
        Instantiates objects

        Args: self
        Raises:
        Returns:
                class instance object
                class instance object
        '''
        self.dbapi = db()
        self.log = logger()

    def deleteMatches(self):
        '''Remove all the match records from the database.'''
        if self.dbapi.query(deleteMatches='yes'):
            self.log.info('All matches information is nulated')

    def deletePlayers(self):
        '''Remove all the player records from the database.'''
        if self.dbapi.query(deletePlayers='yes'):
            self.log.info('All players have been deleted')

    def countPlayers(self):
        '''Returns the number of players currently registered.'''
        return self.dbapi.query(count='yes')

    def registerPlayer(self, name):
        '''Adds a player to the tournament database.
        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema,
        not in your Python code.
        Args:
        name: the player's full name (need not be unique).
        '''
        if self.dbapi.query(player=str(name)):
            self.log.info(
                '%s is registered succesfully' % (str(name)))


class Game(object):

    def __init__(self):
        '''
        Creates instant object

        Args: self
        Raises:
        Returns:
                class instance object
        '''
        self.dbapi = db()

    def playerStandings(self):
        '''Returns a list of the players and their win records,
            sorted by wins.

        The first entry in the list should be the player in first place,
        or a player tied for first place if there is currently a tie.

        Returns:
             A list of tuples,
                each of which contains (id, name, wins, matches):
            rid: the player's unique id (assigned by the database)
             name: the player's full name (as registered)
             wins: the number of matches the player has won
             matches: the number of matches the player has played
        '''
        return self.dbapi.query(standings='yes')

    def reportMatch(self, player1, player2):
        '''Records the outcome of a single match between two players.

        Args:
            player1: the id number of the first player
            player2: the id number of the player second player
        '''
        self.dbapi.query(report_match=[player1, player2])

    def swissPairings(self):
        '''Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered,
        each player appears exactly once in the pairings.
        Each player is paired with another player with an equal
        or nearly-equal win record, that is, a player adjacent to him or her
        in the standings.

        Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        '''
        return self.dbapi.query(pairings='yes')
