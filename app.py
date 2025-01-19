import os
import re
import sys
import sqlite3
from typing import List, Tuple, Optional
from colorama import Fore, Style, init

init(autoreset=True)

DATABASE_PATH = 'flag_football_league.db'

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = self.connect_db()

    def connect_db(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error connecting to database: {e}{Style.RESET_ALL}")
            sys.exit(1)

    def execute_query(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Cursor]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor
        except sqlite3.Error as e:
            print(f"{Fore.RED}Database error: {e}{Style.RESET_ALL}")
            return None

    def commit(self) -> None:
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"{Fore.RED}Commit failed: {e}{Style.RESET_ALL}")

    def close(self) -> None:
        self.conn.close()

class TablePrinter:
    ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

    def __init__(self):
        pass

    @staticmethod
    def strip_ansi(text: str) -> str:
        return TablePrinter.ANSI_ESCAPE_PATTERN.sub('', text)

    @staticmethod
    def visible_length(text: str) -> int:
        return len(TablePrinter.strip_ansi(text))

    @staticmethod
    def pad_string(text: str, width: int, align: str = 'left') -> str:
        text_visible_length = TablePrinter.visible_length(text)
        padding = width - text_visible_length
        padding = max(padding, 0)

        if align == 'left':
            return text + ' ' * padding
        elif align == 'right':
            return ' ' * padding + text
        else:
            return text + ' ' * padding

    def print_table(self, headers: List[str], rows: List[Tuple], alignments: Optional[List[str]] = None) -> None:
        if not rows:
            print(f"{Fore.RED}No data available to display.{Style.RESET_ALL}")
            return

        for idx, row in enumerate(rows):
            if len(row) != len(headers):
                raise ValueError(f"Row {idx + 1} has {len(row)} cells but expected {len(headers)}.")

        all_rows = [headers] + [list(map(str, row)) for row in rows]

        column_widths = [max(self.visible_length(cell) for cell in col) for col in zip(*all_rows)]

        num_columns = len(headers)
        if alignments is None:
            alignments = ['left'] * num_columns
        else:
            if len(alignments) != num_columns:
                raise ValueError(f"Number of alignments ({len(alignments)}) does not match number of columns ({num_columns}).")
            for align in alignments:
                if align not in ('left', 'right'):
                    raise ValueError("Alignments must be 'left' or 'right'.")

        separator = '-+-'.join('-' * width for width in column_widths)

        colored_headers = [f"{Fore.GREEN}{header}{Style.RESET_ALL}" for header in headers]
        padded_headers = [self.pad_string(col, width, align=alignments[idx]) for idx, (col, width) in enumerate(zip(colored_headers, column_widths))]

        print(
            f"{Fore.CYAN}{Style.BRIGHT}"
            + " | ".join(padded_headers)
            + Style.RESET_ALL
        )

        print(f"{Fore.YELLOW}" + separator + Style.RESET_ALL)

        for row in rows:
            padded_row = [self.pad_string(str(cell), width, align=alignments[idx]) for idx, (cell, width) in enumerate(zip(row, column_widths))]
            print(" | ".join(padded_row))

class FlagFootballLeagueManager:
    def __init__(self, db_manager: DatabaseManager, table_printer: TablePrinter):
        self.db = db_manager
        self.printer = table_printer

    def view_players(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 VIEW ALL PLAYERS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query = """
        SELECT PlayerID, FirstName, LastName, DateOfBirth, Height, Weight, Position
        FROM Player
        ORDER BY LastName, FirstName
        """
        cursor = self.db.execute_query(query)
        players = cursor.fetchall() if cursor else []

        if players:
            headers = ["PlayerID", "First Name", "Last Name", "DOB", "Height (cm)", "Weight (kg)", "Position"]
            self.printer.print_table(headers, players)
        else:
            print(f"{Fore.RED}No players found.{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_player_details(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 VIEW PLAYER DETAILS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        player_id = input(f"{Fore.CYAN}Enter PlayerID: {Style.RESET_ALL}").strip()
        if not player_id.isdigit():
            print(f"{Fore.RED}\nInvalid PlayerID. Please enter a valid number.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}\nPress Enter to return to the main menu...{Style.RESET_ALL}")
            return

        query_player = """
        SELECT FirstName, LastName, DateOfBirth, Height, Weight, Position, TeamID
        FROM Player
        WHERE PlayerID = ?
        """
        cursor = self.db.execute_query(query_player, (player_id,))
        player = cursor.fetchone() if cursor else None

        if not player:
            print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}\nPress Enter to return to the main menu...{Style.RESET_ALL}")
            return

        first_name, last_name, dob, height, weight, position, team_id = player

        print(f"{Fore.GREEN}\n--- Player Details ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Name: {first_name} {last_name}")
        print(f"DOB: {dob}")
        print(f"Height: {height} cm")
        print(f"Weight: {weight} kg")
        print(f"Position: {position}")

        query_team = """
        SELECT TeamName, League.LeagueName, League.Division, Wins, Losses, Draws
        FROM Team
        INNER JOIN League ON Team.LeagueID = League.LeagueID
        WHERE Team.TeamID = ?
        """
        cursor = self.db.execute_query(query_team, (team_id,))
        team_info = cursor.fetchone() if cursor else None

        if not team_info:
            print(f"{Fore.YELLOW}\nNo team information available for this player.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}\nPress Enter to return to the main menu...{Style.RESET_ALL}")
            return

        team_name, league_name, division, wins, losses, draws = team_info
        print(f"\n{Fore.GREEN}Team: {team_name} ({league_name}, {division}){Style.RESET_ALL}")
        print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")

        query_stats = """
        SELECT 
            COALESCE(SUM(PlaysIn.Touchdowns), 0) AS TotalTouchdowns,
            COALESCE(SUM(PlaysIn.Yards), 0) AS TotalYards,
            COALESCE(SUM(PlaysIn.Tackles), 0) AS TotalTackles,
            COALESCE(SUM(PlaysIn.Interceptions), 0) AS TotalInterceptions
        FROM PlaysIn
        WHERE PlaysIn.PlayerID = ?
        """
        cursor = self.db.execute_query(query_stats, (player_id,))
        stats = cursor.fetchone() if cursor else (0, 0, 0, 0)

        print(f"\n{Fore.GREEN}--- Season Stats ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total Touchdowns: {stats[0]}")
        print(f"Total Yards: {stats[1]}")
        print(f"Total Tackles: {stats[2]}")
        print(f"Total Interceptions: {stats[3]}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def add_new_player(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 ADD A NEW PLAYER 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            first_name = input(f"{Fore.CYAN}First Name: {Style.RESET_ALL}").strip()
            last_name = input(f"{Fore.CYAN}Last Name: {Style.RESET_ALL}").strip()
            dob = input(f"{Fore.CYAN}Date of Birth (YYYY-MM-DD): {Style.RESET_ALL}").strip()
            height_input = input(f"{Fore.CYAN}Height (cm): {Style.RESET_ALL}").strip()
            weight_input = input(f"{Fore.CYAN}Weight (kg): {Style.RESET_ALL}").strip()

            if not height_input or not weight_input:
                raise ValueError("Height and Weight are required.")

            height = float(height_input)
            weight = float(weight_input)

            position = input(f"{Fore.CYAN}Position: {Style.RESET_ALL}").strip()
            team_id_input = input(f"{Fore.CYAN}Team ID: {Style.RESET_ALL}").strip()

            if not team_id_input.isdigit():
                raise ValueError("TeamID must be a numeric value.")

            team_id = int(team_id_input)

            cursor = self.db.execute_query("SELECT TeamName FROM Team WHERE TeamID = ?", (team_id,))
            team = cursor.fetchone()
            if not team:
                print(f"{Fore.RED}\nTeam with ID {team_id} does not exist.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            cursor = self.db.execute_query("SELECT MAX(PlayerID) FROM Player")
            new_player_id = (cursor.fetchone()[0] if cursor else 0) + 1

            insert_player = """
            INSERT INTO Player (PlayerID, FirstName, LastName, DateOfBirth, Height, Weight, Position, TeamID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.db.execute_query(insert_player, (new_player_id, first_name, last_name, dob, height, weight, position, team_id))

            self.db.commit()
            print(f"\n{Fore.GREEN}Player {first_name} {last_name} added successfully with ID {new_player_id}!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Player is assigned to Team ID {team_id} with Position '{position}'.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}\nAn unexpected error occurred: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def update_player_info(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 UPDATE PLAYER INFORMATION 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            player_id_input = input(f"{Fore.CYAN}Enter PlayerID of the player to update: {Style.RESET_ALL}").strip()
            if not player_id_input.isdigit():
                raise ValueError("PlayerID must be numeric.")
            player_id = int(player_id_input)
            cursor = self.db.execute_query("SELECT * FROM Player WHERE PlayerID = ?", (player_id,))
            player = cursor.fetchone()

            if not player:
                print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            print(f"\n{Fore.GREEN}Leave field blank to keep the current value.{Style.RESET_ALL}")
            first_name = input(f"{Fore.CYAN}Enter First Name [{player[1]}]: {Style.RESET_ALL}").strip() or player[1]
            last_name = input(f"{Fore.CYAN}Enter Last Name [{player[2]}]: {Style.RESET_ALL}").strip() or player[2]
            dob = input(f"{Fore.CYAN}Enter Date of Birth [{player[3]}]: {Style.RESET_ALL}").strip() or player[3]

            height_input = input(f"{Fore.CYAN}Enter Height in cm [{player[4]}]: {Style.RESET_ALL}").strip()
            weight_input = input(f"{Fore.CYAN}Enter Weight in kg [{player[5]}]: {Style.RESET_ALL}").strip()
            position = input(f"{Fore.CYAN}Enter Position [{player[6]}]: {Style.RESET_ALL}").strip() or player[6]
            team_id_input = input(f"{Fore.CYAN}Enter Team ID [{player[7]}]: {Style.RESET_ALL}").strip()
            team_id = int(team_id_input) if team_id_input.isdigit() else player[7]

            cursor = self.db.execute_query("SELECT TeamName FROM Team WHERE TeamID = ?", (team_id,))
            team = cursor.fetchone()
            if not team:
                print(f"{Fore.RED}\nTeam with ID {team_id} does not exist.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            height = float(height_input) if height_input else player[4]
            weight = float(weight_input) if weight_input else player[5]

            update_query = """
            UPDATE Player
            SET FirstName = ?, LastName = ?, DateOfBirth = ?, Height = ?, Weight = ?, Position = ?, TeamID = ?
            WHERE PlayerID = ?
            """
            self.db.execute_query(update_query, (first_name, last_name, dob, height, weight, position, team_id, player_id))
            self.db.commit()
            print(f"\n{Fore.GREEN}Player {first_name} {last_name} updated successfully!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Player is now assigned to Team ID {team_id} with Position '{position}'.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}\nAn unexpected error occurred: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def delete_player(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 DELETE PLAYER 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            player_id_input = input(f"{Fore.CYAN}Enter PlayerID of the player to delete: {Style.RESET_ALL}").strip()
            if not player_id_input.isdigit():
                raise ValueError("PlayerID must be numeric.")
            player_id = int(player_id_input)
            cursor = self.db.execute_query("SELECT FirstName, LastName FROM Player WHERE PlayerID = ?", (player_id,))
            player = cursor.fetchone()

            if not player:
                print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            confirmation = input(
                f"{Fore.YELLOW}Are you sure you want to delete {player[0]} {player[1]}? (y/n): {Style.RESET_ALL}"
            ).strip().lower()
            if confirmation == 'y':
                self.db.execute_query("DELETE FROM Player WHERE PlayerID = ?", (player_id,))
                self.db.commit()
                print(f"\n{Fore.GREEN}Player deleted successfully.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Deletion cancelled.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_team_stats(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 TEAM STATS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query = """
        SELECT 
            Team.TeamName, 
            Team.Wins, 
            Team.Losses, 
            Team.Draws,
            COALESCE(SUM(ParticipatesIn.TeamScore), 0) AS PointsScored
        FROM Team
        LEFT JOIN ParticipatesIn ON Team.TeamID = ParticipatesIn.TeamID
        GROUP BY Team.TeamID
        ORDER BY Team.Wins DESC, Team.Losses ASC
        """
        cursor = self.db.execute_query(query)
        stats = cursor.fetchall() if cursor else []

        if stats:
            headers = ['Team Name', 'Wins', 'Losses', 'Draws', 'Points Scored']
            self.printer.print_table(headers, stats)
        else:
            print(f"{Fore.RED}\nNo team stats available.{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_league_standings(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 LEAGUE STANDINGS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query_leagues = "SELECT LeagueName FROM League ORDER BY LeagueName"
        cursor = self.db.execute_query(query_leagues)
        leagues = cursor.fetchall() if cursor else []

        if not leagues:
            print(f"{Fore.RED}No leagues available.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Available Leagues:{Style.RESET_ALL}")
        for idx, league in enumerate(leagues, start=1):
            print(f"{Fore.CYAN}{idx}{Style.RESET_ALL}. {league[0]}")

        while True:
            choice = input(f"\n{Fore.CYAN}Enter the number of the league to view standings: {Style.RESET_ALL}").strip()
            if not choice.isdigit():
                print(f"{Fore.RED}Invalid input. Please enter a number corresponding to the league.{Style.RESET_ALL}")
                continue
            choice_num = int(choice)
            if 1 <= choice_num <= len(leagues):
                selected_league = leagues[choice_num - 1][0]
                break
            else:
                print(f"{Fore.RED}Number out of range. Please try again.{Style.RESET_ALL}")

        query_standings = """
        SELECT 
            Team.TeamName, 
            Team.Wins, 
            Team.Losses, 
            Team.Draws,
            COALESCE(SUM(ParticipatesIn.TeamScore), 0) AS PointsScored
        FROM Team
        INNER JOIN League ON Team.LeagueID = League.LeagueID
        LEFT JOIN ParticipatesIn ON Team.TeamID = ParticipatesIn.TeamID
        WHERE League.LeagueName = ?
        GROUP BY Team.TeamID
        ORDER BY Team.Wins DESC, Team.Losses ASC
        """
        cursor = self.db.execute_query(query_standings, (selected_league,))
        standings = cursor.fetchall() if cursor else []

        if standings:
            headers = ['Team', 'Wins', 'Losses', 'Draws', 'Points Scored']
            self.printer.print_table(headers, standings)
        else:
            print(f"{Fore.RED}\nNo league standings available for '{selected_league}'.{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_game_results(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 GAME RESULTS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query = """
        SELECT G.GameID, G.Date, G.Time, T1.TeamName AS Team1, PI1.TeamScore AS Score1,
               T2.TeamName AS Team2, PI2.TeamScore AS Score2
        FROM Game G
        INNER JOIN ParticipatesIn PI1 ON G.GameID = PI1.GameID
        INNER JOIN ParticipatesIn PI2 ON G.GameID = PI2.GameID AND PI1.TeamID != PI2.TeamID
        INNER JOIN Team T1 ON PI1.TeamID = T1.TeamID
        INNER JOIN Team T2 ON PI2.TeamID = T2.TeamID
        WHERE PI1.TeamID < PI2.TeamID
        ORDER BY G.GameID
        """
        cursor = self.db.execute_query(query)
        games = cursor.fetchall() if cursor else []

        if games:
            headers = ['GameID', 'Date', 'Time', 'Team 1', 'Score 1', 'Team 2', 'Score 2']
            self.printer.print_table(headers, games)
        else:
            print(f"{Fore.RED}\nNo game results available.{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_players_by_team(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 VIEW PLAYERS BY TEAM 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            query_teams = """
            SELECT Team.TeamID, Team.TeamName, League.LeagueName, League.Division
            FROM Team
            INNER JOIN League ON Team.LeagueID = League.LeagueID
            ORDER BY TeamName
            """
            cursor = self.db.execute_query(query_teams)
            teams = cursor.fetchall() if cursor else []

            if teams:
                print(f"{Fore.GREEN}Available Teams:{Style.RESET_ALL}")
                team_ids = []
                for team in teams:
                    print(f"{Fore.CYAN}{team[0]}{Style.RESET_ALL}: {team[1]} ({team[2]} - {team[3]})")
                    team_ids.append(team[0])
            else:
                print(f"{Fore.RED}No teams found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            team_id_input = input(f"\n{Fore.CYAN}Enter TeamID to view its players: {Style.RESET_ALL}").strip()
            if not team_id_input.isdigit():
                raise ValueError("TeamID must be numeric.")
            team_id = int(team_id_input)
            if team_id not in team_ids:
                print(f"{Fore.RED}\nInvalid TeamID selected.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            query_players = """
            SELECT PlayerID, FirstName, LastName, Position, DateOfBirth, Height, Weight
            FROM Player
            WHERE TeamID = ?
            ORDER BY LastName, FirstName
            """
            cursor = self.db.execute_query(query_players, (team_id,))
            players = cursor.fetchall() if cursor else []

            if players:
                headers = ['PlayerID', 'First Name', 'Last Name', 'Position', 'DOB', 'Height (cm)', 'Weight (kg)']
                self.printer.print_table(headers, players)
            else:
                print(f"{Fore.RED}\nNo players found for this team.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_games_by_player(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 VIEW GAMES BY PLAYER 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            player_id_input = input(f"{Fore.CYAN}Enter PlayerID: {Style.RESET_ALL}").strip()
            if not player_id_input:
                print(f"{Fore.RED}\nNo PlayerID entered.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            if not player_id_input.isdigit():
                raise ValueError("PlayerID must be numeric.")

            player_id = int(player_id_input)
            cursor = self.db.execute_query("SELECT FirstName, LastName FROM Player WHERE PlayerID = ?", (player_id,))
            player = cursor.fetchone()

            if not player:
                print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            query_games = """
            SELECT Game.GameID, Game.Date, Game.Time, Game.Location
            FROM PlaysIn
            INNER JOIN Game ON PlaysIn.GameID = Game.GameID
            WHERE PlaysIn.PlayerID = ?
            ORDER BY Game.Date DESC
            """
            cursor = self.db.execute_query(query_games, (player_id,))
            games = cursor.fetchall() if cursor else []

            if games:
                print(f"\n{Fore.GREEN}Game History for {player[0]} {player[1]} (PlayerID {player_id}):{Style.RESET_ALL}\n")
                headers = ['GameID', 'Date', 'Time', 'Location']
                self.printer.print_table(headers, games)
            else:
                print(f"{Fore.RED}\nNo games found for this player.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def search_players_by_name(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 SEARCH PLAYERS BY NAME 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        name = input(f"{Fore.CYAN}Enter player's first or last name to search: {Style.RESET_ALL}").strip()
        if not name:
            print(f"{Fore.RED}\nNo name entered.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
            return

        query = """
        SELECT PlayerID, FirstName, LastName, DateOfBirth, Height, Weight, Position
        FROM Player
        WHERE FirstName LIKE ? OR LastName LIKE ?
        ORDER BY LastName, FirstName
        """
        cursor = self.db.execute_query(query, (f"%{name}%", f"%{name}%"))
        players = cursor.fetchall() if cursor else []

        if players:
            print(f"\n{Fore.GREEN}Search Results for '{name}':{Style.RESET_ALL}\n")
            headers = ["PlayerID", "First Name", "Last Name", "DOB", "Height (cm)", "Weight (kg)", "Position"]
            self.printer.print_table(headers, players)

            while True:
                selected_player_id = input(
                    f"\n{Fore.CYAN}Enter the PlayerID of the player to view detailed stats or press Enter to skip: {Style.RESET_ALL}"
                ).strip()

                if not selected_player_id:
                    break
                if not selected_player_id.isdigit():
                    print(f"{Fore.RED}Invalid input. Please enter a valid numeric PlayerID.{Style.RESET_ALL}")
                    continue

                selected_player_id = int(selected_player_id)
                if any(player[0] == selected_player_id for player in players):
                    self.view_player_details_by_id(selected_player_id)
                    break 
                else:
                    print(f"{Fore.RED}PlayerID not found in the search results. Please try again.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}\nNo players found matching that name.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_player_details_by_id(self, player_id: int) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 PLAYER DETAILS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query_basic = """
        SELECT FirstName, LastName, DateOfBirth, Height, Weight, Position, TeamID
        FROM Player
        WHERE PlayerID = ?
        """
        cursor = self.db.execute_query(query_basic, (player_id,))
        player = cursor.fetchone() if cursor else None

        if not player:
            print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
            return

        first_name, last_name, dob, height, weight, position, team_id = player

        print(f"{Fore.GREEN}\n--- Details for {first_name} {last_name} ---{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Date of Birth: {Style.RESET_ALL}{dob}")
        print(f"{Fore.CYAN}Height: {Style.RESET_ALL}{height} cm")
        print(f"{Fore.CYAN}Weight: {Style.RESET_ALL}{weight} kg")
        print(f"{Fore.CYAN}Position: {Style.RESET_ALL}{position}")

        query_team = """
        SELECT TeamName, League.LeagueName, League.Division, Wins, Losses, Draws
        FROM Team
        INNER JOIN League ON Team.LeagueID = League.LeagueID
        WHERE Team.TeamID = ?
        """
        cursor = self.db.execute_query(query_team, (team_id,))
        team_info = cursor.fetchone() if cursor else None

        if not team_info:
            print(f"{Fore.YELLOW}\nNo team information available for this player.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}\nPress Enter to return to the main menu...{Style.RESET_ALL}")
            return

        team_name, league_name, division, wins, losses, draws = team_info
        print(f"\n{Fore.GREEN}Team: {team_name} ({league_name}, {division}){Style.RESET_ALL}")
        print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")

        query_stats = """
        SELECT 
            COALESCE(SUM(PlaysIn.Touchdowns), 0) AS TotalTouchdowns,
            COALESCE(SUM(PlaysIn.Yards), 0) AS TotalYards,
            COALESCE(SUM(PlaysIn.Tackles), 0) AS TotalTackles,
            COALESCE(SUM(PlaysIn.Interceptions), 0) AS TotalInterceptions
        FROM PlaysIn
        WHERE PlaysIn.PlayerID = ?
        """
        cursor = self.db.execute_query(query_stats, (player_id,))
        stats = cursor.fetchone() if cursor else (0, 0, 0, 0)

        print(f"\n{Fore.GREEN}--- Season Stats ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total Touchdowns: {stats[0]}")
        print(f"Total Yards: {stats[1]}")
        print(f"Total Tackles: {stats[2]}")
        print(f"Total Interceptions: {stats[3]}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_player_stats_by_game(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 PLAYER STATS BY GAME 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            game_id_input = input(f"{Fore.CYAN}Enter GameID: {Style.RESET_ALL}").strip()
            if not game_id_input.isdigit():
                raise ValueError("GameID must be numeric.")

            game_id = int(game_id_input)
            cursor = self.db.execute_query("SELECT Date, Time, Location FROM Game WHERE GameID = ?", (game_id,))
            game = cursor.fetchone()

            if not game:
                print(f"{Fore.RED}\nGame not found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            game_date, game_time, game_location = game
            print(f"{Fore.GREEN}\n--- Game Details ---{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}GameID: {game_id}")
            print(f"Date: {game_date}")
            print(f"Time: {game_time}")
            print(f"Location: {game_location}")

            query_stats = """
            SELECT Player.FirstName || ' ' || Player.LastName AS PlayerName, 
                   PlaysIn.Touchdowns, PlaysIn.Yards, PlaysIn.Tackles, PlaysIn.Interceptions
            FROM PlaysIn
            INNER JOIN Player ON Player.PlayerID = PlaysIn.PlayerID
            WHERE PlaysIn.GameID = ?
            ORDER BY PlayerName
            """
            cursor = self.db.execute_query(query_stats, (game_id,))
            stats = cursor.fetchall() if cursor else []

            if stats:
                print(f"\n{Fore.GREEN}Player Stats for GameID {game_id}:{Style.RESET_ALL}\n")
                headers = ['Player Name', 'Touchdowns', 'Yards', 'Tackles', 'Interceptions']
                self.printer.print_table(headers, stats)
            else:
                print(f"{Fore.RED}\nNo stats found for this game.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def search_players_by_name(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 SEARCH PLAYERS BY NAME 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        name = input(f"{Fore.CYAN}Enter player's first or last name to search: {Style.RESET_ALL}").strip()
        if not name:
            print(f"{Fore.RED}\nNo name entered.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
            return

        query = """
        SELECT PlayerID, FirstName, LastName, DateOfBirth, Height, Weight, Position
        FROM Player
        WHERE FirstName LIKE ? OR LastName LIKE ?
        ORDER BY LastName, FirstName
        """
        cursor = self.db.execute_query(query, (f"%{name}%", f"%{name}%"))
        players = cursor.fetchall() if cursor else []

        if players:
            print(f"\n{Fore.GREEN}Search Results for '{name}':{Style.RESET_ALL}\n")
            headers = ["PlayerID", "First Name", "Last Name", "DOB", "Height (cm)", "Weight (kg)", "Position"]
            self.printer.print_table(headers, players)

            while True:
                selected_player_id = input(
                    f"\n{Fore.CYAN}Enter the PlayerID of the player to view detailed stats or press Enter to skip: {Style.RESET_ALL}"
                ).strip()

                if not selected_player_id:
                    break
                if not selected_player_id.isdigit():
                    print(f"{Fore.RED}Invalid input. Please enter a valid numeric PlayerID.{Style.RESET_ALL}")
                    continue

                selected_player_id = int(selected_player_id)
                if any(player[0] == selected_player_id for player in players):
                    self.view_player_details_by_id(selected_player_id)
                    break 
                else:
                    print(f"{Fore.RED}PlayerID not found in the search results. Please try again.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}\nNo players found matching that name.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_player_details_by_id(self, player_id: int) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 PLAYER DETAILS 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        query_basic = """
        SELECT FirstName, LastName, DateOfBirth, Height, Weight, Position, TeamID
        FROM Player
        WHERE PlayerID = ?
        """
        cursor = self.db.execute_query(query_basic, (player_id,))
        player = cursor.fetchone() if cursor else None

        if not player:
            print(f"{Fore.RED}\nPlayer not found.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
            return

        first_name, last_name, dob, height, weight, position, team_id = player

        print(f"{Fore.GREEN}\n--- Details for {first_name} {last_name} ---{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Date of Birth: {Style.RESET_ALL}{dob}")
        print(f"{Fore.CYAN}Height: {Style.RESET_ALL}{height} cm")
        print(f"{Fore.CYAN}Weight: {Style.RESET_ALL}{weight} kg")
        print(f"{Fore.CYAN}Position: {Style.RESET_ALL}{position}")

        query_team = """
        SELECT TeamName, League.LeagueName, League.Division, Wins, Losses, Draws
        FROM Team
        INNER JOIN League ON Team.LeagueID = League.LeagueID
        WHERE Team.TeamID = ?
        """
        cursor = self.db.execute_query(query_team, (team_id,))
        team_info = cursor.fetchone() if cursor else None

        if not team_info:
            print(f"{Fore.YELLOW}\nNo team information available for this player.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}\nPress Enter to return to the main menu...{Style.RESET_ALL}")
            return

        team_name, league_name, division, wins, losses, draws = team_info
        print(f"\n{Fore.GREEN}Team: {team_name} ({league_name}, {division}){Style.RESET_ALL}")
        print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")

        query_stats = """
        SELECT 
            COALESCE(SUM(PlaysIn.Touchdowns), 0) AS TotalTouchdowns,
            COALESCE(SUM(PlaysIn.Yards), 0) AS TotalYards,
            COALESCE(SUM(PlaysIn.Tackles), 0) AS TotalTackles,
            COALESCE(SUM(PlaysIn.Interceptions), 0) AS TotalInterceptions
        FROM PlaysIn
        WHERE PlaysIn.PlayerID = ?
        """
        cursor = self.db.execute_query(query_stats, (player_id,))
        stats = cursor.fetchone() if cursor else (0, 0, 0, 0)

        print(f"\n{Fore.GREEN}--- Season Stats ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total Touchdowns: {stats[0]}")
        print(f"Total Yards: {stats[1]}")
        print(f"Total Tackles: {stats[2]}")
        print(f"Total Interceptions: {stats[3]}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    def view_player_stats_by_game(self) -> None:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 PLAYER STATS BY GAME 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        try:
            game_id_input = input(f"{Fore.CYAN}Enter GameID: {Style.RESET_ALL}").strip()
            if not game_id_input.isdigit():
                raise ValueError("GameID must be numeric.")

            game_id = int(game_id_input)
            cursor = self.db.execute_query("SELECT Date, Time, Location FROM Game WHERE GameID = ?", (game_id,))
            game = cursor.fetchone()

            if not game:
                print(f"{Fore.RED}\nGame not found.{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")
                return

            game_date, game_time, game_location = game
            print(f"{Fore.GREEN}\n--- Game Details ---{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}GameID: {game_id}")
            print(f"Date: {game_date}")
            print(f"Time: {game_time}")
            print(f"Location: {game_location}")

            query_stats = """
            SELECT Player.FirstName || ' ' || Player.LastName AS PlayerName, 
                   PlaysIn.Touchdowns, PlaysIn.Yards, PlaysIn.Tackles, PlaysIn.Interceptions
            FROM PlaysIn
            INNER JOIN Player ON Player.PlayerID = PlaysIn.PlayerID
            WHERE PlaysIn.GameID = ?
            ORDER BY PlayerName
            """
            cursor = self.db.execute_query(query_stats, (game_id,))
            stats = cursor.fetchall() if cursor else []

            if stats:
                print(f"\n{Fore.GREEN}Player Stats for GameID {game_id}:{Style.RESET_ALL}\n")
                headers = ['Player Name', 'Touchdowns', 'Yards', 'Tackles', 'Interceptions']
                self.printer.print_table(headers, stats)
            else:
                print(f"{Fore.RED}\nNo stats found for this game.{Style.RESET_ALL}")

        except ValueError as ve:
            print(f"{Fore.RED}\nInvalid input: {ve}{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}\nDatabase error: {e}{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}")

def main_menu():
    db_manager = DatabaseManager(DATABASE_PATH)
    table_printer = TablePrinter()
    manager = FlagFootballLeagueManager(db_manager, table_printer)

    menu_options = {
        "1": ("View All Players", manager.view_players),
        "2": ("View Player Details", manager.view_player_details),
        "3": ("Add New Player", manager.add_new_player),
        "4": ("Update Player Information", manager.update_player_info),
        "5": ("Delete Player", manager.delete_player),
        "6": ("View Team Stats", manager.view_team_stats),
        "7": ("View Players by Team", manager.view_players_by_team),
        "8": ("View Games by Player", manager.view_games_by_player),
        "9": ("View Player Stats by Game", manager.view_player_stats_by_game),
        "10": ("View League Standings", manager.view_league_standings),
        "11": ("Search Players by Name", manager.search_players_by_name),
        "12": ("View Game Results", manager.view_game_results),
        "13": ("Exit", None)  
    }

    while True:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50)
        print(f"{Fore.YELLOW}{Style.BRIGHT}" + "🏈 FLAG FOOTBALL LEAGUE MANAGEMENT SYSTEM 🏈".center(50))
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "=" * 50 + "\n")

        for key, (description, _) in menu_options.items():
            color = Fore.GREEN if key != "13" else Fore.RED 
            print(f"{color}{Style.BRIGHT}{key}{Style.RESET_ALL}. {description}")

        print(f"{Fore.MAGENTA}{Style.BRIGHT}" + "=" * 50)

        choice = input(f"{Fore.CYAN}{Style.BRIGHT}Enter your choice (1-13): {Style.RESET_ALL}").strip()

        if choice in menu_options:
            if choice == "13":
                print(f"\n{Fore.RED}{Style.BRIGHT}Exiting... Goodbye! 🏈\n")
                db_manager.close()
                break
            else:
                action = menu_options[choice][1]
                action()
        else:
            print(f"\n{Fore.RED}{Style.BRIGHT}Invalid choice. Please try again.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}{Style.BRIGHT}\nPress Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    main_menu()
