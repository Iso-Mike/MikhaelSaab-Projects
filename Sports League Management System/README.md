# Sports League Management System

## Author
Mikhael Saab

## Overview
The Sports League Management System is a relational database solution designed to efficiently manage data for a flag football league. This system tracks players, teams, games, and leagues, along with their associated performance metrics. It facilitates game scheduling, player analytics, and decision-making for league administrators and coaches.

## Features
- **Relational Database Design:** Implements a normalized schema with key relationships such as `PlaysFor`, `PlaysIn`, `ParticipatesIn`, and `Contains` for efficient data organization.
- **Player and Team Performance Metrics:** Tracks comprehensive statistics including touchdowns, tackles, interceptions, and scores for in-depth analysis.
- **Game Management:** Stores detailed game information like date, time, location, and weather conditions for effective scheduling and logistics.
- **League Structure:** Supports hierarchical organization by linking teams to leagues with win-loss records.
- **Automated Data Population:** Uses Python scripts to generate realistic data, simulating player performance and game scenarios.

## Source Files
- `create_database.py`: Script for creating the database schema and populating it with initial data.
- `app.py`: Application script to interact with the database for querying and analysis.
- `ER.pdf`: Entity-relationship diagram illustrating the database design.

## How to Compile and Run
1. **Prerequisites:** Ensure Python 3.x and SQLite are installed on your system.
2. **Setup:** Run the following command to create and populate the database:
   ```bash
   python create_database.py

## Usage Instructions
1. **Database Creation**: Run python create_database.py to set up the database schema and populate it with data.
2. **Query Execution**: Use app.py or direct SQL queries to extract insights and manage league operations.
3. **Analysis**: Leverage the data to evaluate player performance, optimize schedules, and support team management.