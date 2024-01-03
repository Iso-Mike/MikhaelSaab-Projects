
# Hollow Escape Simulation

## Author
Mikhael Saab

## Overview
The Hollow Escape Simulation is a dynamic and interactive program that simulates the challenging escape of two heroes through a hollow, amidst threats from flying monkeys and attack birds. This program showcases the use of multiple processes, threading, and network communication to display the game in one terminal window, while simultaneously allowing a spectator to view the identical escape output in a different window.

## Features
- **Multi-Process Architecture:** Utilizes multiple processes to separate the game logic from the spectator view, enhancing the scalability and robustness of the application.
- **Threading for Real-Time Updates:** Implements a separate communications manager thread for outputting the game state at predefined intervals, ensuring smooth and consistent updates.
- **TCP/IP Networking:** Features network connectivity for a client-server application, allowing real-time communication between different instances of the game.
- **Signal Handling:** Efficiently manages Unix signals for inter-process communication and control, ensuring responsive and stable operation.
- **Dynamic Interaction:** Offers a rich interactive experience with dynamically managed game entities like heroes, birds, and monkeys.
- **Visual Representation:** Manages the visual output of the game scenario effectively, providing an engaging user interface.

## Source Files
- `main.c`: Contains the main program flow and logic.
- `connect.c`: Handles network connectivity for a TCP/IP based client-server application.
- `escape.c`: Orchestrates the overall escape scenario game.
- `flyer.c`: Defines and manages the behaviors and interactions of the flyers within the escape scenario.
- `hero.c`: Defines and handles the functionalities related to the heroes in the escape scenario.
- `spectator.c`: Contains client code for the spectator view.
- `view.c`: Manages the visual representation and output of the escape scenario.

## Header Files
- `defs.h`: Defines structures, constants, and thread management used throughout the program.

## How to Compile and Run
- **Compilation:** Run the 'make' command in the project directory.
- **Execution:** Open two separate windows. In the first one run `./a5`. And in the second one run `./a5 127.0.0.1`.

## Usage Instructions
- **Starting the Game:** Open two separate terminal windows. In the first window, run `./a5` to start the game. In the second window, run `./a5 127.0.0.1` to start the spectator view.
