# Swiss tournament
========

[![Build Status](https://travis-ci.org/rbagrov/fullstack-nanodegree-vm.svg?branch=master)](https://travis-ci.org/rbagrov/fullstack-nanodegree-vm)

Small library for calculating swiss tournament results

Table of contents
=================

- [Swiss tournament](#swiss-tournament)
- [Table of contents](#table-of-contents)
- [Intro](#intro)
- [Install](#install)
- [Contents](#contents)
- [Code base](#code-base)
- [Tests](#tests)
- [License](#License)


Intro
==========

This library can manipulate user creation and removal.
It can match outome of a match between two players, rank players and mark player standings.
It uses [PostreSQL](https://www.postgresql.org/docs/9.3/static/index.html) database engine.

Install
=========

```bash
git clone https://github.com/rbagrov/fullstack-nanodegree-vm.git
cd fullstack-nanodegree-vm
vagrant up
vagrant ssh
psql --file=/vagrant/tournament/tournament.sql
pip install -r /vagrant/tournament/requirements.txt
```


Contents
=======

* [tournament.py](https://github.com/rbagrov/fullstack-nanodegree-vm/blob/master/vagrant/tournament/tournament.py)
* [tournament.log](https://github.com/rbagrov/fullstack-nanodegree-vm/blob/master/vagrant/tournament/tournament.log)
* [tournament.sql](https://github.com/rbagrov/fullstack-nanodegree-vm/blob/master/vagrant/tournament/tournament.sql)
* [tournament_test.py](https://github.com/rbagrov/fullstack-nanodegree-vm/blob/master/vagrant/tournament/tournament_test.py)
* [requirements.txt`](https://github.com/rbagrov/fullstack-nanodegree-vm/blob/master/vagrant/tournament/requirements.txt)



Code base
=======
 
```python
NAME
    tournament

FILE
    /vagrant/tournament/tournament.py

DESCRIPTION
    # tournament.py -- implementation of a Swiss-system tournament
    #

CLASSES
    __builtin__.object
        Game
        Players
        db
        logger
    
    class Game(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Creates instant object
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |              class instance object
     |  
     |  playerStandings(self)
     |      Returns a list of the players and their win records,
     |          sorted by wins.
     |      
     |      The first entry in the list should be the player in first place,
     |      or a player tied for first place if there is currently a tie.
     |      
     |      Returns:
     |           A list of tuples,
     |              each of which contains (id, name, wins, matches):
     |          rid: the player's unique id (assigned by the database)
     |           name: the player's full name (as registered)
     |           wins: the number of matches the player has won
     |           matches: the number of matches the player has played
     |  
     |  reportMatch(self, player1, player2)
     |      Records the outcome of a single match between two players.
     |      
     |      Args:
     |          player1: the id number of the first player
     |          player2: the id number of the player second player
     |  
     |  swissPairings(self)
     |      Returns a list of pairs of players for the next round of a match.
     |      
     |      Assuming that there are an even number of players registered,
     |      each player appears exactly once in the pairings.
     |      Each player is paired with another player with an equal
     |      or nearly-equal win record, that is, a player adjacent to him or her
     |      in the standings.
     |      
     |      Returns:
     |      A list of tuples, each of which contains (id1, name1, id2, name2)
     |      id1: the first player's unique id
     |      name1: the first player's name
     |      id2: the second player's unique id
     |      name2: the second player's name
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Players(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Instantiates objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |              class instance object
     |              class instance object
     |  
     |  countPlayers(self)
     |      Returns the number of players currently registered.
     |  
     |  deleteMatches(self)
     |      Remove all the match records from the database.
     |  
     |  deletePlayers(self)
     |      Remove all the player records from the database.
     |  
     |  registerPlayer(self, name)
     |      Adds a player to the tournament database.
     |      The database assigns a unique serial id number for the player.  (This
     |      should be handled by your SQL database schema,
     |      not in your Python code.
     |      Args:
     |      name: the player's full name (need not be unique).
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class db(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Create references to statement objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |          self.insert - object of class string
     |          self.insert_score - object of class string
     |          self.insert_check - object of class string
     |          self.counter - object of class string
     |          self.remove_players - object of class string
     |          self.remove_matches - object of class string
     |          self.standings - object of class string
     |          self.get_wins - object of class string
:
     |      name2: the second player's name
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Players(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Instantiates objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |              class instance object
     |              class instance object
     |  
     |  countPlayers(self)
     |      Returns the number of players currently registered.
     |  
     |  deleteMatches(self)
     |      Remove all the match records from the database.
     |  
     |  deletePlayers(self)
     |      Remove all the player records from the database.
     |  
     |  registerPlayer(self, name)
     |      Adds a player to the tournament database.
     |      The database assigns a unique serial id number for the player.  (This
     |      should be handled by your SQL database schema,
     |      not in your Python code.
     |      Args:
     |      name: the player's full name (need not be unique).
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class db(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Create references to statement objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |          self.insert - object of class string
     |          self.insert_score - object of class string
     |          self.insert_check - object of class string
     |          self.counter - object of class string
     |          self.remove_players - object of class string
     |          self.remove_matches - object of class string
     |          self.standings - object of class string
     |          self.get_wins - object of class string
     |      name2: the second player's name
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Players(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Instantiates objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |              class instance object
     |              class instance object
     |  
     |  countPlayers(self)
     |      Returns the number of players currently registered.
     |  
     |  deleteMatches(self)
     |      Remove all the match records from the database.
     |  
     |  deletePlayers(self)
     |      Remove all the player records from the database.
     |  
     |  registerPlayer(self, name)
     |      Adds a player to the tournament database.
     |      The database assigns a unique serial id number for the player.  (This
     |      should be handled by your SQL database schema,
     |      not in your Python code.
     |      Args:
     |      name: the player's full name (need not be unique).
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class db(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Create references to statement objects
     |      
     |      Args: self
     |      Raises:
     |      Returns:
     |          self.insert - object of class string
     |          self.insert_score - object of class string
     |          self.insert_check - object of class string
     |          self.counter - object of class string
     |          self.remove_players - object of class string
     |          self.remove_matches - object of class string
     |          self.standings - object of class string
     |          self.get_wins - object of class string
    |          self.get_match - object of class string
     |          self.record - object of class string
     |          self.pairings - object of class string
     |          self.log - logger class instance
     |          self.tiner - object of type integer
     |  
     |  countPlayers(self)
     |      Counter entries in players table
     |      
     |      Args: self
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type integer
     |              object of type None
     |  
     |  deleteMatches(self)
     |      Removes all matches entires
     |      
     |      Args: self
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type string
     |              object of type None
     |  
     |  deletePlayers(self)
     |      Truncates players table
     |      
     |      Args: self
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type string
     |              object of type None
     |  
     |  getMatch(self, uid)
     |      Get match record for user by its id
     |      
     |      Args: self
     |            uid - object of type integer
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type integer
     |              object of type None
     |  
     |  getWins(self, uid)
     |      Get win record for user by its id
     |      
     |      Args: self
     |            uid - object of type integer
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type integer
     |              object of type None
     |  
     |  get_pairings(self)
     |      Returns formatted list with player pairings
     |      
     |      Args: self
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type list
     |  
     |  open_connection(self)
     |      Connect to the PostgreSQL database.
     |      Returns a database connection and a cursor.
     |      
     |      Args: self
     |      Raises: psycopg2.OperationalError
     |      Returns:
     |              object of type list(psycopg2 connection and cursor objects)
     |  
     |  pair_rawlist(self, player_list, step)
     |      Creates a list with user pairings
     |      
     |      Args: self
     |            player_list - object of type list
     |            step - object of type integer
     |      Raises:
     |            IndexError - catch it if list indexes are uneven
     |      Returns:
     |              object of type list
     |  
     |  playerStandings(self)
     |      Returns current standings from players table
     |      
     |      Args: self
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type list
     |              object of type None
     |  
     |  query(self, **kwargs)
     |      Executes different queries base on keyed arguments
     |      
     |      Args: self
     |            key arguments
     |      Raises:
     |      Returns: (in descending order)
     |              object of type String/None
     |              object of type Integer/None
     |              object of type String/None
     |              object of type String/None
     |              object of type List/None
     |              object of type List/None
     |  
     |  recordMatch(self, uid)
     |      Writes played match into games tables
     |      
     |      Args: self
     |            uid - object of type list
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |  
     |  registerPlayer(self, name)
     |      Insert player details into players table
     |      
     |      Args: self
     |            name - object of type string
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type string
     |              object of type None
     |  
     |  
     |  reportMatch(self, uid)
     |      Sets match score
     |      
     |      Args: self
     |            uid - object of type list
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |  
     |  setMatchScore(self, uid_win, uid_lost)
     |      Set match score
     |      
     |      Args: self
     |            uid_win object of type integer
     |            uid_lost object of type integer
     |      Raises:
     |              pokemon catching exceptions for log purposes
     |      Returns:
     |              object of type string
     |              object of type None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class logger(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      References to a log file.
     |      Sets log config
     |      
     |      Args: self
     |      Raises:
     |      Returns: None
     |  
     |  exception(self, message)
     |      Logs exception message
     |      
     |      Args: self, message
     |      Raises:
     |      Returns: None
     |  
     |  info(self, message)
     |      Logs info message
     |      
     |      Args: self, message
     |      Raises:
     |      Returns: None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

```


Tests
=======

``` bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py 
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!

```


License
=======

[GPL](https://www.gnu.org/licenses/gpl-3.0.html)
