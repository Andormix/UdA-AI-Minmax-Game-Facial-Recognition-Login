# Splatoon — AI Strategy Board Game

[![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Pygame](https://img.shields.io/badge/Game-Pygame-00A86B?style=for-the-badge)](#)
[![Artificial Intelligence](https://img.shields.io/badge/AI-Minimax%20%2B%20Alpha--Beta-8A2BE2?style=for-the-badge)](#)
[![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-FF6F00?style=for-the-badge&logo=opencv&logoColor=white)](#)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](#)
[![Academic Project](https://img.shields.io/badge/Project-M4%20REPTE-003366?style=for-the-badge)](#)

<p align="center">
  <img
    src="docs/ai-board-game-banner.svg"
    alt="Splatoon AI strategy board game"
    width="100%"
  />
</p>

**Splatoon** is a Python board game where a human player competes against an artificial intelligence opponent.

The game was developed as part of the **M4 REPTE** project and combines several different areas of programming:

- Game development with Pygame.
- Artificial intelligence using Minimax and alpha-beta pruning.
- Facial recognition with OpenCV.
- User registration and authentication.
- MySQL database persistence.
- Match history and replay functionality.
- Scoreboards and administrator tools.

The facial-recognition system is used during login. The main gameplay is based on the AI board game, where the player competes against the computer at different difficulty levels.

---

## Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Game](#game)
- [Artificial Intelligence](#artificial-intelligence)
- [Facial Recognition Login](#facial-recognition-login)
- [User and Administrator System](#user-and-administrator-system)
- [Database](#database)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [Main Menu](#main-menu)
- [Match History and Scoreboards](#match-history-and-scoreboards)
- [Development Notes](#development-notes)
- [Privacy and Security](#privacy-and-security)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Academic Context](#academic-context)
- [License](#license)

---

## Project Overview

The application starts with a login and registration system. Users can register an account and create a facial profile using a webcam. During future logins, the application checks the user's nickname and verifies their face before allowing access to the game.

After logging in, the user can choose a game mode, view previous matches, check scoreboards, or access administrator options if the account has administrator privileges.

The game itself is a turn-based board game. The player places pieces on the board while the AI calculates its own moves using a search algorithm.

---

## Main Features

### Game Features

- Human versus AI gameplay.
- Pygame board interface.
- Several difficulty levels.
- Player and AI turns.
- Score calculation.
- Win, loss, and draw detection.
- Board-state visualization.
- Background music and game sounds.
- Programmer mode for inspecting game states.
- Replay system for completed matches.

### AI Features

- Minimax algorithm.
- Alpha-beta pruning.
- Recursive board-state exploration.
- Valid-move generation.
- Search-depth-based difficulty.
- Board evaluation.
- AI movement selection.

### Authentication Features

- User registration.
- Nickname validation.
- Facial-recognition login.
- Webcam-based face capture.
- OpenCV Haar Cascade detection.
- LBPH facial-recognition model.
- Administrator account detection.
- User rejection when the detected face does not match the requested nickname.

### Database Features

- User storage.
- Administrator records.
- Player information.
- Match results.
- Individual movement history.
- Board-state storage.
- Top-ten match scoreboard.
- Top-five player scoreboard.
- Match replay by match ID.

---

## Game

The game is played on a board represented by a NumPy array.

The prototype uses a board with:

```python
ROW_COUNT = 6
COLUMN_COUNT = 8
```

The game contains two opponents:

```python
PLAYER = 0
AI = 1
```

The board is updated after every movement. Each movement can also be stored inside the match history so that the complete game can be reviewed later.

A normal match follows this structure:

```text
1. Create the board.
2. Place the initial pieces.
3. Give the first turn to the player.
4. Wait for the player's movement.
5. Calculate the AI movement.
6. Update the board.
7. Save the movement.
8. Check the result.
9. Continue until the match ends.
10. Save the final match and score.
```

The game can finish when:

- The player wins.
- The AI wins.
- The match ends in a draw.
- There are no valid movements remaining.
- A blocking or “ofegament” condition is reached.

---

## Artificial Intelligence

The AI is implemented using the Minimax algorithm.

The main function is located in the game logic and prototype files:

```text
Full project Source Files/LògicaJoc.py
Full project Source Files/pepomain.py
```

The function used by the prototype has the following structure:

```python
def minimax(board, depth, alpha, beta, maximizingPlayer):
    ...
```

### How the AI Selects a Move

For every AI turn:

1. The program finds all valid positions.
2. It creates a copy of the current board.
3. It simulates each possible AI movement.
4. It recursively simulates the player's response.
5. It evaluates the resulting states.
6. It selects the movement with the best result.

The AI tries to maximize its own score while assuming that the human player will choose movements that make the AI's result worse.

### Alpha-Beta Pruning

Alpha-beta pruning is used to avoid exploring branches that cannot improve the current decision.

The two values used by the algorithm are:

```text
Alpha — the best value currently available to the maximizing player.
Beta  — the best value currently available to the minimizing player.
```

When a branch can no longer produce a better result, the algorithm stops evaluating that branch.

This is important because Minimax can become expensive when the search depth increases.

### Board Evaluation

The board is evaluated by:

```python
def avalua_estat(board, piece):
    ...
```

This function is responsible for assigning a value to a board state. The value is then used by Minimax when it reaches the configured search depth or a terminal state.

The evaluation function is also one of the main areas that can be improved in future versions.

---

## Facial Recognition Login

Facial recognition is used as an authentication method before entering the game.

The implementation is located in:

```text
Full project Source Files/ReconeixementFacial.py
```

The system uses:

- OpenCV.
- Haar Cascade face detection.
- Grayscale images.
- LBPH face recognition.
- A webcam.
- MySQL-stored facial images.
- A generated recognition model.

### Registration Process

When a user registers:

1. The user enters their personal information.
2. A nickname is created.
3. The user record is inserted into MySQL.
4. A player record is created.
5. The webcam starts.
6. The application captures approximately fifty photographs.
7. The photographs are stored in the `Dataset` table.
8. The images are later used to train the recognition model.

The registration logic is implemented in:

```text
Full project Source Files/Login.py
```

The image capture function is:

```python
Crear_perfil(mycursor, mydb, Usuari)
```

### Training the Recognition Model

Before recognizing a user, the application loads the facial images from MySQL and writes them to local folders.

The dataset is organized by nickname:

```text
Dataset/
├── user_one/
│   ├── 1.png
│   ├── 2.png
│   └── ...
└── user_two/
    ├── 1.png
    ├── 2.png
    └── ...
```

The training process:

1. Opens each image.
2. Converts it to grayscale.
3. Detects the face.
4. Extracts the face region.
5. Assigns a numeric ID to the user.
6. Trains the LBPH recognizer.
7. Saves the model in `trainner.yml`.
8. Saves the label dictionary in `Etiquetes.pickle`.

The training method is implemented in:

```python
Crear_YML()
```

### Login Process

The login process checks the nickname first:

```python
SELECT NICK FROM Usuaris WHERE NICK = %s
```

If the user exists:

1. The dataset is loaded.
2. The LBPH model is created or loaded.
3. The webcam is opened.
4. Faces are detected in the camera frames.
5. The detected face is compared with the trained faces.
6. The recognized nickname is compared with the nickname entered by the user.
7. Several successful detections are required before the login is accepted.

The recognition function is:

```python
reconeixement_facial(Nick)
```

The application currently uses repeated detections as a basic verification mechanism:

```text
Five correct detections → Login accepted
Five incorrect detections → Login rejected
```

### Recognition Files

The facial-recognition system requires:

```text
Cascadas/haarcascade_frontalface_alt2.xml
trainner.yml
Etiquetes.pickle
```

The Haar Cascade is used to find faces in the image, while `trainner.yml` contains the trained LBPH model.

---

## User and Administrator System

The project supports two types of accounts:

- Normal players.
- Administrators.

The administrator status is checked using the `Administrador` table.

After facial recognition succeeds, the application chooses the correct menu:

```python
MenusJoc.menuPrincipal(Nick, mycursor, mydb, Admin)
```

Normal users can:

- Play matches.
- View their game history.
- View scoreboards.
- Replay stored matches.

Administrators also have access to the administrator menu implemented in:

```text
Full project Source Files/MenusJoc.py
```

---

## Database

The application uses MySQL through:

```python
import mysql.connector
```

The database is used to store users, player data, facial images, matches, and movement history.

The connection is created by the main application before the login loop starts.

For example:

```python
mydb = mysql.connector.connect(
    host="YOUR_DATABASE_HOST",
    user="YOUR_DATABASE_USER",
    password="YOUR_DATABASE_PASSWORD",
    database="YOUR_DATABASE_NAME"
)
```

The real database credentials should be configured locally and should not be committed to the repository.

### Tables Used by the Application

| Table | Purpose |
| :--- | :--- |
| `Usuaris` | Stores registered users |
| `Administrador` | Stores users with administrator privileges |
| `Players` | Stores player information |
| `Dataset` | Stores the facial images captured during registration |
| `Partides` | Stores completed matches and final scores |
| `Moviments` | Stores every movement and board state |

### `Usuaris`

The user table stores information such as:

- Nickname.
- First name.
- Surnames.

Example fields used during registration:

```text
NICK
Nom_Usuari
Cognom1
Cognom2
```

### `Players`

A player record is created when a user registers:

```text
NICK
Info
```

### `Dataset`

The facial dataset stores:

- User nickname.
- Image number.
- Image data.

The registration function inserts the captured images into the database:

```python
INSERT INTO Dataset(NICK, Num, Foto)
VALUES (%s, %s, %s)
```

### `Partides`

The match table stores:

- Player nickname.
- Level.
- Final score.
- Match ID.

### `Moviments`

The movement table stores detailed information about each movement, including:

- Movement number.
- Turn.
- AI points.
- Player points.
- AI positions.
- Player positions.
- Winner flags.
- Draw flags.
- Blocking flags.
- Match ID.
- Board state.

The board is converted into text before being inserted into the database:

```python
mapa = str(Part.LlistaMoviments.MEMO[x].Estat.tolist())
```

It is converted back into a NumPy array when replaying a match.

---

## Project Structure

```text
.
├── Full project Source Files/
│   ├── Constants.py
│   ├── LògicaJoc.py
│   ├── Login.py
│   ├── MenusJoc.py
│   ├── ReconeixementFacial.py
│   ├── TADS.py
│   ├── entrenament_cares.py
│   ├── main(Tkinter).py
│   ├── main(Terminal GUI).py
│   ├── pepomain.py
│   │
│   ├── Cascadas/
│   │   └── haarcascade_frontalface_alt2.xml
│   │
│   ├── Dataset/
│   ├── img/
│   └── audio/
│
├── trainner.yml
├── Etiquetes.pickle
├── docs/
│   └── ai-board-game-banner.svg
├── README.md
└── .gitignore
```

### Main Files

| File | Description |
| :--- | :--- |
| `main(Terminal GUI).py` | Terminal-based application entry point |
| `main(Tkinter).py` | Tkinter login and graphical entry point |
| `Login.py` | Registration and login logic |
| `MenusJoc.py` | Main menu, scoreboards, replay system, and database persistence |
| `LògicaJoc.py` | Main game loop and game rules |
| `ReconeixementFacial.py` | Facial image capture, training, and recognition |
| `entrenament_cares.py` | Facial dataset training script |
| `TADS.py` | Custom data structures for matches and movements |
| `Constants.py` | Game constants and configuration |
| `pepomain.py` | Standalone Pygame and Minimax prototype |
| `Cascadas/` | Haar Cascade model |
| `Dataset/` | Extracted facial images |
| `img/` | Temporary images used during recognition |
| `audio/` | Background music and game sounds |
| `trainner.yml` | Trained LBPH recognition model |
| `Etiquetes.pickle` | Mapping between numeric IDs and nicknames |

---

## Technologies Used

| Technology | Use in the Project |
| :--- | :--- |
| Python | Main programming language |
| Pygame | Game window, board rendering, input, and audio |
| NumPy | Board arrays and numerical operations |
| OpenCV | Face detection and recognition |
| OpenCV Contrib | LBPH face recognizer |
| Pillow | Image loading and grayscale conversion |
| Tkinter | Graphical login interface |
| MySQL Connector/Python | Communication with MySQL |
| MySQL | User, match, and movement storage |
| Pickle | Facial-recognition label storage |

---

## Requirements

To run the project, install:

- Python 3.
- MySQL Server.
- A webcam.
- Git.
- The Python dependencies required by the project.

The main Python packages are:

```text
numpy
pygame
opencv-python
opencv-contrib-python
Pillow
mysql-connector-python
```

`opencv-contrib-python` is required because the LBPH recognizer is included in OpenCV's contributed modules.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Andormix/TorronteraRuiz_M4_REPTE.git
cd TorronteraRuiz_M4_REPTE
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Python Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install numpy pygame opencv-python opencv-contrib-python Pillow mysql-connector-python
```

If the project contains a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Before starting the application, create the MySQL database and the tables required by the project.

The database connection should be configured locally in the Python entry point files.

Use your own values for:

```text
Host
User
Password
Database
```

Do not commit real credentials to GitHub.

A safer approach is to store the values in environment variables:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="your_user"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DATABASE="your_database"
```

or on macOS/Linux:

```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="your_user"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="your_database"
```

The database should contain the following tables:

```text
Usuaris
Administrador
Players
Dataset
Partides
Moviments
```

---

## Running the Application

The repository contains two main entry points.

### Terminal Version

Run the terminal-based application with:

```bash
python "Full project Source Files/main(Terminal GUI).py"
```

This version:

1. Connects to MySQL.
2. Opens the login menu.
3. Allows the user to register or log in.
4. Performs facial recognition.
5. Opens the main game menu.
6. Starts the selected game mode.

### Tkinter Version

Run the graphical version with:

```bash
python "Full project Source Files/main(Tkinter).py"
```

This version uses Tkinter for the login interface and then opens the game menu after successful authentication.

### Standalone AI Prototype

The standalone prototype can be run with:

```bash
python "Full project Source Files/pepomain.py"
```

This file is useful for testing the board and AI logic separately from the full login and database system.

---

## Main Menu

After logging in, the main menu provides the following options:

```text
1. Easy mode
2. Normal mode
3. Difficult mode
4. Programmer mode
5. God mode
6. View previous match movement history
7. View top-ten matches
8. View top-five players
9. View a match by ID
10. Exit
11. Administrator menu
```

The administrator option is shown only when the logged-in user exists in the `Administrador` table.

### Difficulty Modes

The first game modes call the game logic with different level values:

```python
LògicaJoc.joc(1, Part)
LògicaJoc.joc(2, Part)
LògicaJoc.joc(3, Part)
LògicaJoc.joc(4, Part)
```

These values are stored with the match and can be used to control the difficulty or score calculation.

### Programmer Mode

Programmer mode is useful for checking the internal state of a match.

It can display:

- The movement list.
- The pointer position inside the movement structure.
- The board at each stage.
- Player and AI scores.
- Winner and draw states.

### God Mode

God mode is intended for testing long or expensive AI calculations. The menu warns that it can take several minutes.

---

## Match History and Scoreboards

### Top-Ten Matches

The application queries stored matches and displays the best results.

The displayed data includes:

- Match ID.
- Player nickname.
- Score.
- Level.

### Top-Five Players

The player scoreboard groups results by nickname and shows the best score for the player's highest completed level.

### Match Replay

A stored match can be replayed by entering its ID.

The replay process is:

```text
1. Enter a match ID.
2. Load the movement records from MySQL.
3. Read the saved board states.
4. Convert the states back into arrays.
5. Draw each state using Pygame.
6. Display the match one movement at a time.
```

This functionality is implemented in `MenusJoc.py`.

---

## Development Notes

The project contains both a standalone AI prototype and the full integrated game.

### Standalone Prototype

```text
Full project Source Files/pepomain.py
```

The prototype focuses on:

- Board creation.
- Mouse input.
- Piece movement.
- Pygame rendering.
- AI turns.
- Minimax.
- Alpha-beta pruning.

### Integrated Game

```text
Full project Source Files/LògicaJoc.py
```

The integrated version adds:

- User authentication.
- Facial recognition.
- Game menus.
- Difficulty levels.
- Match persistence.
- Movement history.
- Scoreboards.
- Replay functionality.
- Administrator access.

### Movement Data Structure

The project uses custom structures from:

```text
Full project Source Files/TADS.py
```

These structures store the movements of a match, including:

- The board state.
- Turn information.
- Scores.
- Player positions.
- AI positions.
- Winner flags.
- Draw flags.
- Blocking conditions.

When a match finishes, the movement list is traversed and every state is inserted into the `Moviments` table.

---

## Privacy and Security

The facial-recognition system processes biometric data, so it should only be used with the consent of the people involved.

This project was created for academic purposes. It should not be used as a production authentication system without additional security measures.

Before using the project with real users:

- Ask for permission before capturing face images.
- Keep the facial dataset private.
- Do not upload personal face images to a public repository.
- Remove database passwords from the source code.
- Use environment variables for credentials.
- Limit access to administrator accounts.
- Provide a way to delete user data.
- Do not use the system for surveillance.
- Treat recognition results as potentially incorrect.

The current implementation is a learning project and does not include advanced protections such as liveness detection or anti-spoofing.

---

## Troubleshooting

### The Camera Does Not Open

The current code uses a camera index that may need to be changed depending on the computer.

For example:

```python
cap = cv2.VideoCapture(0)
```

If the first camera does not work, try:

```python
cap = cv2.VideoCapture(1)
```

Check that:

- The webcam is connected.
- No other application is using it.
- Camera permissions are enabled.
- The selected camera index is correct.

### `cv2.face` Does Not Exist

Install the OpenCV contributed package:

```bash
pip uninstall opencv-python
pip install opencv-contrib-python
```

Test the installation:

```bash
python -c "import cv2; print(hasattr(cv2, 'face'))"
```

The result should be:

```text
True
```

### The Recognition Model Cannot Be Loaded

Check that the following files are available:

```text
trainner.yml
Etiquetes.pickle
Cascadas/haarcascade_frontalface_alt2.xml
```

If the model has not been generated yet, run the training process after registering at least one user.

### The Face Is Not Detected

Try:

- Improving the lighting.
- Moving closer to the camera.
- Facing the camera directly.
- Removing objects that cover the face.
- Checking the Haar Cascade file path.
- Adjusting `scaleFactor`.
- Adjusting `minNeighbors`.

### The AI Takes Too Long

This can happen when the search depth is high or when God mode is selected.

Possible solutions:

- Use an easier difficulty mode.
- Reduce the Minimax depth.
- Improve the board evaluation function.
- Add move ordering.
- Cache repeated board states.
- Improve alpha-beta pruning.
- Limit the number of candidate movements.

### MySQL Connection Error

Check:

- The MySQL server is running.
- The database exists.
- The username and password are correct.
- The server address is reachable.
- The required tables have been created.
- The user has permission to access the database.

### Pygame Does Not Start

Check:

- Pygame is installed.
- The computer has a graphical desktop session.
- The audio files are available.
- The Python path is correct.
- The game is not being executed in a headless environment.

---

## Future Improvements

### AI

- Improve the board evaluation function.
- Add configurable search depth.
- Add better move ordering.
- Add transposition tables.
- Add iterative deepening.
- Compare Minimax with Monte Carlo Tree Search.
- Add AI performance statistics.
- Create more balanced difficulty levels.

### Game

- Add more game modes.
- Improve the graphical interface.
- Add animations.
- Add a proper settings menu.
- Add local multiplayer.
- Add online multiplayer.
- Add a tutorial.
- Add more visual effects.
- Add improved sound design.

### Facial Recognition

- Add liveness detection.
- Improve camera compatibility.
- Allow multiple reference images per user.
- Make the recognition threshold configurable.
- Add a password-based alternative login.
- Add secure biometric data storage.
- Improve recognition feedback.
- Add an option to remove a user's facial data.

### Database

- Move all credentials to environment variables.
- Add a database setup script.
- Add migrations.
- Add stronger error handling.
- Add transactions around match storage.
- Add database backups.
- Add unit and integration tests.

---

## Academic Context

This project was developed as part of the **M4 REPTE** activity.

It combines:

- Artificial intelligence.
- Game development.
- Minimax search.
- Alpha-beta pruning.
- Board-state evaluation.
- Python programming.
- Pygame.
- Computer vision.
- Facial recognition.
- MySQL databases.
- User authentication.
- Graphical user interfaces.

The project was created to apply algorithmic and software-development concepts in a complete application instead of using the AI algorithm in isolation.

---

## Author

Developed by **Eric Torrontera Ruiz**.

Repository:

```text
https://github.com/Andormix/TorronteraRuiz_M4_REPTE
```

---

## License

This project was created for educational and academic purposes.

The source code is provided for learning, experimentation, and demonstration of artificial intelligence, game development, computer vision, and database integration.

The facial-recognition system should not be used as a production identity-verification or surveillance system without implementing the necessary privacy, legal, security, and ethical safeguards.
