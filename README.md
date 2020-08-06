# MineSweeper

## Running the game

* Option 1: Play game in terminal
    * clone the repo and install requirements ``pip3 install -r requirements.txt``
    * run ``python3 game.py``
    * follow instructions - enter coordinates to play
    * Note: currently, the game shows the board solution in the beginning. Comment out line 112 in ``play()`` function of game.py to remove solution

* Option 2: Play the game in localhost
    * clone the repo and install requirements ``pip3 install -r requirements.txt``
    * run ``export FLASK_APP=app.py`` followed by ``flask run`` to run the app locally

* Option 3: Play the app live
    * Note: the game doesn't function properly on the Heroku app, this is likely do to an issue with serving static files. I included the app to show that it's "running" live, however it's currently incomplete due to this static images issue. The Heroku app is running the code found in this repo, however it doesn't function the same way the localhost version does. 
    * https://minesweeper-rachel-quiz.herokuapp.com/

## Testing the app
* After installing the necessary requirements, run ``python3 test.py`` to test the app
* This test script runs 2000 tests (which can be changed in line 92 of test.py), which mimic gameplay and assert that the final outcome is the expected outcome.
* The first 1000 tests test winning games by guessing random points that 1) are not mines and 2) haven't been guessed or "clicked" before. By "clicked," I mean that the piece hasn't been guessed directly, or revealed by being adjacent to a piece that isn't next to a mine.
* The second 1000 tests test losing games. First, the test computes a random ``max_turns`` value between 2 and the max possible pieces that can be clicked in a losing scenario. ``max_turns`` determines how many correct pieces will be clicked before a mine is clicked. After ``max_turns`` turns, a random mine is picked from the set of mines. 
    * It's important to note a design tradeoff in the "lose tests." By including randomness in this test to make the tests more robust, it is possible that the game is won before ``max_turns`` have passed. Thus, in these tests, it's possible that not all 1000 tests will be a lose scenario. However, we expect that most will be a lose scenario, and given the large number of tests, I believe that this approach thoroughly tests the lose scenario. 
    * Similarly, I don't exclude tiles that have been revealed by clicking a neighbor that has 0 adjacent mines because this reduces the number of moves to win, which would increase the number of win scenarios in the lose test.

## Design Write Up
* For the sake of code extendability and maintainability, I have chosen to take an object-oriented programming approach to this challenge. I initially built the terminal version of the app, and afterwards I found it quite easy to extend the app to a web version because of the design choices I made early on.
* game.py contains two classes: ``Tile`` and ``Mine``. 
* The ``Tile`` class represents the individual pieces on the board, which have attributes ``is_clicked``, which is a boolean representing whether the user has "clicked" the tile and ``value`` which is the number of mines adjacent to the tile. A mine has a value of -1 and a tile with no adjacent mines has a value of 0. 
* The ``Mine`` class is a blueprint for a game. It includes the ``size`` of the board, ``num_mines``, the number of mines in the game, ``x_guess`` and ``y_guess``, the x and y values of the current tile picked, and ``board``, which is a 2D array of ``Tile`` elements that represents the game board. In this version of the app, I've only included one level of the game, but with this approach, including different levels is as simple as modifying the ``num_mines`` and ``size`` values when initializing the game. ``Mine`` has the following functions which control the gameplay:
    * ``create_board()`` creates a 2D array of ``Tile`` elements to represent a board. Here, the ``Tile`` elements all have default values of ``False`` for ``is_clicked`` and ``None`` for ``value``. 
    * Given the game requirements that the first click will never result in a mine, only after a user selects an initial tile are the mine locations created. ``create_mines(x_guess, y_guess)`` is called after the first tile is selected, which creates ``num_mines`` mines in any location that is not the first tile selected and counts the number of adjacent mines of each tile. 
    * ``get_neighbors(coordinate)`` finds all the neighbors of a given ``Tile`` coordinate. The code I used is inspired by [this post](https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list), as it is the most concise and beautiful version python code I've seen to get the neighbors of a given element in a 2D list.
    * ``update(x, y)`` is a recursive function that clicks a square and  clicks all adjacent squares recurisvely if that square has no adjacent mines.
    * ``print_board()`` and ``print_solution()`` print the board in a readable manner for the terminal version of the game. ``play()`` is a handler for the terminal game, taking in coordinate inputs and updating until game ends.
    * ``has_lost()`` checks if the user has lost by checking if the guessed Tile is a mine (has a value of -1)
    * ``has_won()`` checks if the user has won by checking if the only unclicked pieces on the board are all tiles
    * ``to_json()`` is used to relay data to the frontend.
* app.py includes code to build a Flask app and launch a server to run the game as a web app. It includes a few routes and HTTP methods to allow communication between the frontend and game logic. 
    * ``/new_game`` creates a new game by initiallizing a new ``Mine`` instance.
    * ``/update_game`` sends the x,y coordinates of the chosen tile. It updates the board and checks if the user has won or lost. 
* The static files include minesweeper images for the board, HTML, CSS, and JavaScript. The frontend of this project is heavily inspired by [this repo](https://github.com/emanuelzaymus/MineSweeper/). I have used the same index.html and style.css files, and modified the script.js to match my ``Mine`` implementation and to make the front end a bit more similar to [this online version of the game](https://minesweeper.online/).
* The logic for the terminal game and web app are quite similar. The main differences are that the Flask app methods in app.py handle the input/update logic for the web app, whereas the ``play()`` function in game.py handles this logic for the terminal game.

## Game Twist
* I enjoy games that are involve strategy and luck. I would propose adding an tile type, a "superwin" piece to the game that automatically causes the user to win upon clicking it. 
* The twist is that there's no way to differentiate this "superwin" piece from the mines. The tiles surrounding it would show the number of adjacent mines AND winning pieces that are adjecent to those pieces. 
* This twist adds some risk and reward: a user might be avoiding a piece that is actually the "superwin" tile, or they might accidentally click the "superwin" tile! 


