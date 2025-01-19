import sqlite3
import random
from collections import defaultdict

conn = sqlite3.connect('flag_football_league.db')
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS PlayerStats;
DROP TABLE IF EXISTS PlaysIn;
DROP TABLE IF EXISTS ParticipatesIn;
DROP TABLE IF EXISTS TeamStats;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS League;
""")

schema = """
CREATE TABLE IF NOT EXISTS League (
    LeagueID INTEGER PRIMARY KEY,
    LeagueName TEXT NOT NULL,
    Division TEXT
);

CREATE TABLE IF NOT EXISTS Team (
    TeamID INTEGER PRIMARY KEY,
    TeamName TEXT NOT NULL,
    Coach TEXT,
    HomeCity TEXT,
    LeagueID INTEGER,
    Wins INTEGER DEFAULT 0,
    Losses INTEGER DEFAULT 0,
    Draws INTEGER DEFAULT 0,
    FOREIGN KEY (LeagueID) REFERENCES League(LeagueID)
);

CREATE TABLE IF NOT EXISTS Game (
    GameID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Time TEXT NOT NULL,
    Location TEXT NOT NULL,
    Weather TEXT
);

CREATE TABLE IF NOT EXISTS Player (
    PlayerID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    DateOfBirth TEXT,
    Height REAL,
    Weight REAL,
    Position TEXT NOT NULL,
    TeamID INTEGER,
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
);

CREATE TABLE IF NOT EXISTS PlaysIn (
    PlayerID INTEGER,
    GameID INTEGER,
    Touchdowns INTEGER DEFAULT 0,
    Yards INTEGER DEFAULT 0,
    Tackles INTEGER DEFAULT 0,
    Interceptions INTEGER DEFAULT 0,
    PRIMARY KEY (PlayerID, GameID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);

CREATE TABLE IF NOT EXISTS ParticipatesIn (
    GameID INTEGER,
    TeamID INTEGER,
    TeamScore INTEGER,
    PRIMARY KEY (GameID, TeamID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID),
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
);
"""
cursor.executescript(schema)

# Insert Leagues
leagues = [
    (1, 'NFC East', 'D1'),
    (2, 'NFC West', 'D2')
]
cursor.executemany("""
    INSERT OR IGNORE INTO League (LeagueID, LeagueName, Division)
    VALUES (?, ?, ?)
""", leagues)

teams = [
    (1, 'Philadelphia Eagles', 'Nick Sirianni', 'Philadelphia', 1, 6, 0, 0),
    (2, 'Dallas Cowboys', 'Mike McCarthy', 'Dallas', 1, 4, 2, 0),
    (3, 'New York Giants', 'Brian Daboll', 'New York', 1, 2, 4, 0),
    (4, 'Washington Commanders', 'Ron Rivera', 'Washington', 1, 3, 3, 0),
    (5, 'San Francisco 49ers', 'Kyle Shanahan', 'San Francisco', 2, 10, 6, 0),
    (6, 'Seattle Seahawks', 'Pete Carroll', 'Seattle', 2, 9, 7, 0),
    (7, 'Los Angeles Rams', 'Sean McVay', 'Los Angeles', 2, 11, 5, 0),
    (8, 'Arizona Cardinals', 'Jonathan Gannon', 'Glendale', 2, 7, 9, 0)
]
cursor.executemany("""
    INSERT OR IGNORE INTO Team (TeamID, TeamName, Coach, HomeCity, LeagueID, Wins, Losses, Draws)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", teams)

players = [
    # Philadelphia Eagles (TeamID 1)
    (1, 'Jalen', 'Hurts', '1998-08-07', 185, 101, 'Quarterback', 1),
    (2, "D'Andre", 'Swift', '1999-01-14', 180, 95, 'Running Back', 1),
    (3, 'A.J.', 'Brown', '1997-06-30', 185, 102, 'Wide Receiver', 1),
    (4, 'DeVonta', 'Smith', '1998-11-14', 183, 77, 'Wide Receiver', 1),
    (5, 'Dallas', 'Goedert', '1995-01-03', 196, 116, 'Tight End', 1),
    (6, 'Jason', 'Kelce', '1987-11-05', 191, 134, 'Center', 1),
    (7, 'Lane', 'Johnson', '1990-05-08', 198, 147, 'Offensive Tackle', 1),
    (8, 'Fletcher', 'Cox', '1990-12-13', 193, 141, 'Defensive Tackle', 1),
    (9, 'Brandon', 'Graham', '1988-04-03', 188, 120, 'Defensive End', 1),
    (10, 'Haason', 'Reddick', '1994-09-22', 185, 108, 'Linebacker', 1),
    (11, 'Darius', 'Slay', '1991-01-01', 183, 86, 'Cornerback', 1),
    (12, 'James', 'Bradberry', '1993-08-04', 185, 95, 'Cornerback', 1),
    (13, 'Jake', 'Elliott', '1995-01-21', 175, 75, 'Kicker', 1),
    # Dallas Cowboys (TeamID 2)
    (14, 'Dak', 'Prescott', '1993-07-29', 188, 104, 'Quarterback', 2),
    (15, 'Tony', 'Pollard', '1997-04-30', 183, 95, 'Running Back', 2),
    (16, 'CeeDee', 'Lamb', '1999-04-08', 188, 88, 'Wide Receiver', 2),
    (17, 'Michael', 'Gallup', '1996-03-04', 185, 93, 'Wide Receiver', 2),
    (18, 'Jake', 'Ferguson', '1999-01-18', 196, 111, 'Tight End', 2),
    (19, 'Tyron', 'Smith', '1990-12-12', 196, 141, 'Offensive Tackle', 2),
    (20, 'Zack', 'Martin', '1990-11-20', 193, 143, 'Guard', 2),
    (21, 'DeMarcus', 'Lawrence', '1992-04-28', 191, 121, 'Defensive End', 2),
    (22, 'Micah', 'Parsons', '1999-05-26', 191, 111, 'Linebacker', 2),
    (23, 'Leighton', 'Vander Esch', '1996-02-08', 193, 116, 'Linebacker', 2),
    (24, 'Trevon', 'Diggs', '1997-09-20', 185, 93, 'Cornerback', 2),
    (25, 'Jayron', 'Kearse', '1994-02-11', 193, 98, 'Safety', 2),
    (26, 'Brandon', 'Aubrey', '1995-03-16', 183, 85, 'Kicker', 2),
    # New York Giants (TeamID 3)
    (27, 'Daniel', 'Jones', '1997-05-27', 196, 100, 'Quarterback', 3),
    (28, 'Saquon', 'Barkley', '1997-02-09', 180, 106, 'Running Back', 3),
    (29, 'Darius', 'Slayton', '1997-01-12', 185, 88, 'Wide Receiver', 3),
    (30, 'Sterling', 'Shepard', '1993-02-10', 178, 88, 'Wide Receiver', 3),
    (31, 'Darren', 'Waller', '1992-09-13', 198, 116, 'Tight End', 3),
    (32, 'Andrew', 'Thomas', '1999-01-22', 196, 142, 'Offensive Tackle', 3),
    (33, 'Leonard', 'Williams', '1994-06-20', 196, 137, 'Defensive End', 3),
    (34, 'Kayvon', 'Thibodeaux', '2000-12-15', 193, 113, 'Linebacker', 3),
    (35, 'Bobby', 'Okereke', '1996-07-29', 188, 109, 'Linebacker', 3),
    (36, 'Adoree\'', 'Jackson', '1995-09-18', 180, 85, 'Cornerback', 3),
    (37, 'Xavier', 'McKinney', '1999-08-09', 183, 90, 'Safety', 3),
    (38, 'Graham', 'Gano', '1987-04-09', 188, 93, 'Kicker', 3),
    # Washington Commanders (TeamID 4)
    (39, 'Sam', 'Howell', '2000-09-16', 185, 100, 'Quarterback', 4),
    (40, 'Brian', 'Robinson Jr.', '1999-03-22', 185, 103, 'Running Back', 4),
    (41, 'Terry', 'McLaurin', '1995-09-15', 183, 95, 'Wide Receiver', 4),
    (42, 'Jahan', 'Dotson', '2000-03-22', 180, 83, 'Wide Receiver', 4),
    (43, 'Logan', 'Thomas', '1991-07-01', 198, 118, 'Tight End', 4),
    (44, 'Charles', 'Leno Jr.', '1991-10-09', 193, 141, 'Offensive Tackle', 4),
    (45, 'Jonathan', 'Allen', '1995-01-16', 191, 136, 'Defensive Tackle', 4),
    (46, 'Daron', 'Payne', '1997-05-27', 191, 147, 'Defensive Tackle', 4),
    (47, 'Montez', 'Sweat', '1996-09-04', 198, 120, 'Defensive End', 4),
    (48, 'Jamin', 'Davis', '1998-12-12', 188, 104, 'Linebacker', 4),
    (49, 'Kendall', 'Fuller', '1995-02-13', 180, 90, 'Cornerback', 4),
    (50, 'Kamren', 'Curl', '1999-03-31', 185, 90, 'Safety', 4),
    (51, 'Joey', 'Slye', '1996-04-10', 183, 97, 'Kicker', 4),
    # San Francisco 49ers (TeamID 5)
    (52, 'Jimmy', 'Garoppolo', '1991-11-02', 180, 102, 'Quarterback', 5),
    (53, 'Raheem', 'Mostert', '1997-01-09', 175, 88, 'Running Back', 5),
    (54, 'George', 'Kittle', '1993-10-09', 196, 102, 'Tight End', 5),
    (55, 'Nick', 'Bosa', '1997-10-23', 201, 124, 'Defensive End', 5),
    (56, 'Deebo', 'Samuel', '1999-06-15', 190, 93, 'Wide Receiver', 5),
    (57, 'Fred', 'Warner', '1993-02-23', 190, 99, 'Linebacker', 5),
    (58, 'A.J.', 'Bouye', '1996-12-10', 175, 80, 'Cornerback', 5),
    (59, 'K.J.', 'Hutchison', '1998-04-16', 201, 105, 'Safety', 5),
    # Seattle Seahawks (TeamID 6)
    (60, 'Russell', 'Wilson', '1992-11-29', 188, 84, 'Quarterback', 6),
    (61, 'DK', 'Metcalf', '1997-07-14', 193, 101, 'Wide Receiver', 6),
    (62, 'Tyler', 'Lockett', '1992-04-08', 181, 89, 'Wide Receiver', 6),
    (63, 'Bobby', 'Davis', '1997-02-19', 184, 84, 'Cornerback', 6),
    (64, 'Rashaad', 'White', '1996-07-12', 185, 88, 'Running Back', 6),
    (65, 'Logan', 'Thomas', '1995-07-27', 196, 108, 'Linebacker', 6),
    (66, 'Vance', 'McDonald', '1998-07-17', 198, 111, 'Linebacker', 6),
    (67, 'Kenneth', 'Moses', '1997-12-07', 194, 98, 'Safety', 6),
    # Los Angeles Rams (TeamID 7)
    (68, 'Matthew', 'Stafford', '1990-02-07', 200, 110, 'Quarterback', 7),
    (69, 'Cooper', 'Kupp', '1993-06-15', 185, 102, 'Wide Receiver', 7),
    (70, 'Aaron', 'Donald', '1991-05-23', 190, 125, 'Defensive Tackle', 7),
    (71, 'Viktor', 'Ahnert', '1993-07-19', 190, 120, 'Linebacker', 7),
    (72, 'Tyler', 'Higbee', '1993-01-01', 198, 115, 'Tight End', 7),
    (73, 'Robert', 'Witten', '1992-10-18', 191, 125, 'Guard', 7),
    (74, 'Hunter', 'Henry', '1994-08-16', 198, 100, 'Offensive Tackle', 7),
    # Arizona Cardinals (TeamID 8)
    (75, 'Kyler', 'Murray', '1997-08-07', 188, 101, 'Quarterback', 8),
    (76, 'DeAndre', 'Hopkins', '1992-06-07', 193, 102, 'Wide Receiver', 8),
    (77, 'Budda', 'Baker', '1993-10-01', 183, 102, 'Safety', 8),
    (78, 'Andy', 'Igboananike', '1995-09-10', 185, 115, 'Defensive Tackle', 8),
    (79, 'James', 'Conner', '1996-03-18', 183, 110, 'Running Back', 8),
    (80, 'Chandler', 'Jones', '1989-07-15', 193, 122, 'Linebacker', 8)
]
cursor.executemany("""
    INSERT OR IGNORE INTO Player (PlayerID, FirstName, LastName, DateOfBirth, Height, Weight, Position, TeamID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", players)

games = [
    (1, '2023-09-10', '13:00', 'FedEx Field', 'Sunny'),
    (2, '2023-09-17', '16:25', 'MetLife Stadium', 'Cloudy'),
    (3, '2023-09-24', '20:20', 'AT&T Stadium', 'Rainy'),
    (4, '2023-10-01', '16:25', 'Lincoln Financial Field', 'Cloudy'),
    (5, '2023-10-08', '13:00', 'FedEx Field', 'Sunny'),
    (6, '2023-10-15', '16:25', 'AT&T Stadium', 'Sunny'),
    (7, '2023-10-22', '13:00', 'MetLife Stadium', 'Cloudy'),
    (8, '2023-10-29', '16:25', 'FedEx Field', 'Rainy'),
    (9, '2023-11-05', '13:00', 'Lincoln Financial Field', 'Windy'),
    (10, '2023-11-12', '16:25', 'AT&T Stadium', 'Sunny'),
    (11, '2023-11-19', '13:00', 'MetLife Stadium', 'Cloudy'),
    (12, '2023-11-26', '16:25', 'FedEx Field', 'Snowy'),
    (13, '2023-09-11', '13:30', 'CenturyLink Field', 'Sunny'),
    (14, '2023-09-18', '16:30', 'SoFi Stadium', 'Cloudy'),
    (15, '2023-09-25', '20:30', 'SoFi Stadium', 'Rainy'),
    (16, '2023-10-02', '13:30', 'State Farm Stadium', 'Cloudy'),
    (17, '2023-10-09', '16:30', 'SoFi Stadium', 'Sunny'),
    (18, '2023-10-16', '20:30', 'SoFi Stadium', 'Sunny'),
    (19, '2023-10-23', '13:30', 'CenturyLink Field', 'Windy'),
    (20, '2023-10-30', '16:30', 'State Farm Stadium', 'Rainy'),
    (21, '2023-11-06', '13:30', 'SoFi Stadium', 'Windy'),
    (22, '2023-11-13', '16:30', 'SoFi Stadium', 'Sunny'),
    (23, '2023-11-20', '13:30', 'CenturyLink Field', 'Cloudy'),
    (24, '2023-11-27', '16:30', 'State Farm Stadium', 'Snowy')
]
cursor.executemany("""
    INSERT OR IGNORE INTO Game (GameID, Date, Time, Location, Weather)
    VALUES (?, ?, ?, ?, ?)
""", games)

print("Game table populated.")

participates_in = [
    (1, 1, 28),
    (1, 4, 21),
    (2, 2, 31),
    (2, 3, 17),
    (3, 1, 27),
    (3, 2, 24),
    (4, 3, 14),
    (4, 1, 30),
    (5, 3, 21),
    (5, 4, 24),
    (6, 4, 20),
    (6, 2, 27),
    (7, 1, 35),
    (7, 3, 21),
    (8, 2, 28),
    (8, 4, 17),
    (9, 4, 14),
    (9, 1, 31),
    (10, 3, 24),
    (10, 2, 34),
    (11, 2, 21),
    (11, 1, 27),
    (12, 4, 17),
    (12, 3, 20),
    (13, 6, 24),
    (13, 5, 21),        
    (14, 5, 28),
    (14, 6, 24),
    (15, 7, 31),
    (15, 8, 21),
    (16, 8, 17),
    (16, 7, 24),
    (17, 5, 27),
    (17, 7, 24),
    (18, 7, 30),
    (18, 5, 24),
    (19, 6, 21),
    (19, 8, 17),
    (20, 8, 24),
    (20, 6, 20),  
    (21, 5, 35),
    (21, 7, 21),       
    (22, 7, 28),
    (22, 6, 24),
    (23, 6, 24),
    (23, 7, 21),
    (24, 8, 28),
    (24, 6, 21)
]
cursor.executemany("""
    INSERT OR IGNORE INTO ParticipatesIn (GameID, TeamID, TeamScore)
    VALUES (?, ?, ?)
""", participates_in)

print("ParticipatesIn table populated.")

plays_in = []

for player_id in range(1, 81):
    cursor.execute("""
        SELECT Position, TeamID FROM Player WHERE PlayerID = ?
    """, (player_id,))
    result = cursor.fetchone()

    if result:
        position, team_id = result

        cursor.execute("""
            SELECT GameID, TeamScore FROM ParticipatesIn WHERE TeamID = ?
        """, (team_id,))
        games_played = cursor.fetchall()

        for game in games_played:
            game_id, team_score = game
            touchdowns = 0
            yards = 0
            tackles = 0
            interceptions = 0

            if position in ['Running Back', 'Wide Receiver', 'Tight End']:
                touchdowns = random.randint(0, 3)
                yards = random.randint(0, 150)
                tackles = 0
                interceptions = 0

            elif position == 'Quarterback':    
                touchdowns = random.randint(0, 3)
                yards = random.randint(40, 350)
                tackles = 0
                interceptions = random.randint(0, 3)

            elif position in ['Defensive Tackle', 'Defensive End', 'Linebacker', 'Cornerback', 'Safety']:
                touchdowns = 0
                yards = 0
                tackles = random.randint(3, 12)
                interceptions = random.randint(0, 3)

            elif position == 'Kicker':
                touchdowns = 0
                yards = 0
                tackles = 0
                interceptions = 0

            elif position in ['Center', 'Offensive Tackle', 'Guard']:
                touchdowns = 0
                yards = 0
                tackles = 0
                interceptions = 0

            else:
                touchdowns = 0
                yards = 0
                tackles = 0
                interceptions = 0

            plays_in.append((player_id, game_id, touchdowns, yards, tackles, interceptions))

cursor.executemany("""
    INSERT OR IGNORE INTO PlaysIn (PlayerID, GameID, Touchdowns, Yards, Tackles, Interceptions)
    VALUES (?, ?, ?, ?, ?, ?)
""", plays_in)

print("PlaysIn table populated with player statistics.")

conn.commit()
conn.close()

print("Database successfully populated with updated schema and data for the 2023 season.")
