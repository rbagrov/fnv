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
        self.log_file = 'tournament.log'
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s')

    def info(self, message):
        logging.info(message)

    def exception(self, message):
        logging.exception(message)


class db(object):

    def __init__(self):
        self.insert = 'INSERT INTO players (name, wins, matches) VALUES  (%s, 0, 0);'
        self.insert_score = "UPDATE players SET wins = %s, matches = %s WHERE id = %s;"
        self.insert_check = 'SELECT id FROM players WHERE name=%s;'
        self.counter = 'SELECT * from players;'
        self.remove_players = 'TRUNCATE players;'
        self.remove_matches = 'UPDATE players SET wins = 0, matches = 0  WHERE wins > 0 or matches > 0;'
        self.standings = 'SELECT id, name, wins, matches FROM players;'
        self.get_wins = "SELECT wins FROM players WHERE id = %s;"
        self.get_match = "SELECT matches FROM players WHERE id = %s;"
        self.record = "INSERT INTO games (aid, bid) VALUES (%s, %s);"
        self.pairings = "SELECT id, name FROM players ORDER BY wins DESC"
        self.log = logger()
        self.timer = 1

    def open_connection(self):
        '''
        Connect to the PostgreSQL database.
        Returns a database connection and a cursor.
        '''
        connection_up = False
        while connection_up is False:
            try:
                connection = psycopg2.connect(
                    'dbname=tournament')
                cursor = connection.cursor()
                connection_up = True
                return [connection, cursor]
            except psycopg2.OperationalError:
                self.log.info('Cannot connect. Retrying...')
                time.sleep(self.timer)

    def deletePlayers(self):
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.remove_players)
            connection.commit()
            cursor.execute(self.counter)
            if cursor.rowcount == 0:
                return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def countPlayers(self):
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
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.insert, (name, ))
            connection.commit()
            cursor.execute(self.insert_check, (name, ))
            if len(cursor.fetchall()):
                return 'OK'
        except Exception as e:
            self.log.exception(e)
            return None

    def deleteMatches(self):
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
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.standings)
            return cursor.fetchall()
        except Exception as e:
            self.log.exception(e)
            return None

    def recordMatch(self, uid):
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.record, (uid[0], uid[1]))
            connection.commit()
        except Exception as e:
            self.log.exception(e)

    def setMatchScore(self, uid_win, uid_lost):
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
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            cursor.execute(self.pairings)
            backlist = cursor.fetchall()
            return self.pair_rawlist(backlist, 2)
        except Exception as e:
            self.log.exception(e)
            return e

    def pair_rawlist(self, player_list, step):
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
        new = self.open_connection()
        connection = new[0]
        cursor = new[1]
        try:
            self.setMatchScore(str(uid[0]), str(uid[1]))
        except Exception as e:
            self.log.exception(e)

    def query(self, **kwargs):
        '''Executes different queries base on keyed arguments'''
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
        return int(self.dbapi.query(count='yes'))

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
        self.dbapi = db()

    def playerStandings(self):
        '''Returns a list of the players and their win records,
            sorted by wins.

        The first entry in the list should be the player in first place,
        or a player tied for first place if there is currently a tie.

        Returns:
             A list of tuples,
                each of which contains (id, name, wins, matches):
             id: the player's unique id (assigned by the database)
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
        return self.dbapi.query(report_match=[player1, player2])

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
