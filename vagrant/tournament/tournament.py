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
            self.insert - object of class string
            self.insert_score - object of class string
            self.insert_check - object of class string
            self.counter - object of class string
            self.remove_players - object of class string
            self.remove_matches - object of class string
            self.standings - object of class string
            self.get_wins - object of class string
            self.get_match - object of class string
            self.pairings - object of class string
            self.log - logger class instance
            self.tiner - object of type integer
        '''
        self.insert_name = 'INSERT INTO players (name) VALUES (%s);'
        self.init_wins = 'INSERT INTO wins (id, wins) VALUES (%s, %s);'
        self.init_matches = 'INSERT INTO wins (id, wins) VALUES (%s, %s);'
        self.insert_score = "UPDATE players SET wins = %s, matches = %s WHERE\
                          id = %s;"
        self.insert_check = 'SELECT id FROM players WHERE name=%s;'
        self.counter = 'SELECT * from players;'
        self.remove_players = 'TRUNCATE players;'
        self.remove_wins = 'TRUNCATE wins;'
        self.remove_matches = 'TRUNCATE matches;'
        self.zero_wins = 'UPDATE wins SET wins = 0 WHERE wins > 0 ;'
        self.zero_matches = "UPDATE matches SET maches = 0 WHERE matches > 0"
        self.standings = 'SELECT * FROM standings;'
        self.get_wins = "SELECT wins FROM players WHERE id = %s;"
        self.get_match = "SELECT matches FROM players WHERE id = %s;"
        self.pairings = "SELECT id, name FROM players ORDER BY wins DESC"
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
            cursor.execute(self.remove_wins)
            cursor.execute(self.remove_matches)
            connection.commit()
            cursor.execute(self.counter)
            if cursor.rowcount == 0:
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
            cursor.execute(self.insert_check, (name, ))
            pid = cursor.fetchall()
            if len(pid):
                cursor.execute(self.init_wins, (pid, 0))
                cursor.execute(self.init_matches, (pid, 0))
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
            cursor.execute(self.zero_matches)
            cursor.execute(self.zero_wins)
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

    def setMatchScore(self, uid_win, uid_lost):
        '''
        Set match score

        Args: self
              uid_win object of type integer
              uid_lost object of type integer
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
            cursor.execute(
                self.insert_score,
                (self.getWins(uid_win) + 1,
                 self.getMatch(uid_win) + 1,
                 uid_win))
            cursor.execute(
                self.insert_score,
                (self.getWins(uid_lost),
                 self.getMatch(uid_lost) + 1,
                 uid_lost))
            connection.commit()
            self.log.info(
                'Match between ' +
                uid_win +
                ' and ' +
                uid_lost +
                ' was succefully stored')
            return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def getWins(self, uid):
        '''
        Get win record for user by its id

        Args: self
              uid - object of type integer
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
            cursor.execute(self.get_wins, (uid,))
            wins = cursor.fetchone()
            return wins[0]
        except Exception as e:
            self.log.exception(e)
            return None

    def getMatch(self, uid):
        '''
        Get match record for user by its id

        Args: self
              uid - object of type integer
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
            cursor.execute(self.get_match, (uid,))
            match = cursor.fetchone()
            return match[0]
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
            self.setMatchScore(str(uid[0]), str(uid[1]))
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
