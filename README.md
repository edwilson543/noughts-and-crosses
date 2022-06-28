<h1> 'Noughts and Crosses' Project</h1>
<hr>


<h4>
This repository is an m, n, k noughts and crosses (aka tic-tac-toe) application.
The game includes a tkinter GUI allowing users to play each other, as well as automatic play implemented using the
minimax algorithm.
</h4>
<hr>


<h3>Setup and gameplay:</h3>
<p>
    <b>1)</b> Clone the repository<br>
    <b>2)</b> Create a virtual environment<br>
    <b>3)</b> Install the application dependencies from the requirements.txt file<br>
    <b>4)</b> Run the play.py module in the root directory
</p>
<hr>


<h3>GUI screenshots</h3>

<img src="/noughts_and_crosses/tkinter_gui/readme_screenshots/setup_window.png" title="Screenshot of the game setup window">
<br>
<img src="/tkinter_gui/readme_screenshot/main_game_window_game_play.png" title="Screenshot of the main game playing window">
<br>
<img src="tkinter_gui/readme_screenshot/main_game_window_game_over.png" title="Main game window and pop up when a player has won">


<hr>


<h3>Authors and acknowledgement:</h3>
<p>
    <b>
        <a href="https://github.com/edwilson543">Ed Wilson</a>
    </b>
<br>
    <b>
        <a href="https://github.com/szepfalvibalint">Balint Szepfalvi</a>
    </b> 
</p>
<hr>


<h3>Notable or potentially interesting features of the application:</h3>

<h5> Backend (core game processing excluding minimax player): </h5>

<p>

<b>Board representation:</b> The board has been represented by a numpy array where X/Os are represented by 1/-1s and 
empty cells by the imaginary number i (or in python 1j). This allows for rapid, vectorised extraction of data from the 
board. 
<br>

<b>Win checking:</b> The core idea used for searching for wins was to convolute the arrays intersecting the previous
move, also within the winning length, with an array of ones of the winning length. For example, a row containing a win
in a 3,3,3 game might produce (1, 1, 1) . (1, 1, 1) = 3, telling us there is a win, where '.' is the 'dot product' in 
this description but is implemented as a discrete linear convolution in the code.
<br>

<b>Caching searched boards:</b> A custom least recently used (LRU) cache was defined for the win search method, to avoid
repeatedly searching the same board for a win (largely relevant to minimax algorithm). This was implemented as a 
decorator class caching function returns in an ordered dict, and is applied to the win check function. The main
motivations for defining this decorator rather than just using the functools.lru_cache were:<br>
1) The custom decorator allowed caching based only on a subset of the win checking function's arguments, and only this
subset affects the return value, minimising the number of primary calls to the function.
2) The custom cache allows the symmetry of the board to be leveraged - i.e. when the win checker is called on a given
board, we can also create the symmetric equivalence class for the active board and cache all these boards against the
same return value. This is only relevant for the minimax player - note also that extensive profiling of this feature 
using cProfile (see game_profiling.py) showed that it does save time in smaller games (<=5x5), but for bigger games 
where there is quickly less symmetry, just slowed it down, so by default a use_symmetry attribute of the decorator class 
is set to False.
3) Some arguments of the win check are not hashable (numpy arrays), so are converted to tuples for creating the hash
keys. A separate decorator that could be applied to all functions was also implemented, with only this feature, 
which did leverage the existing functools.lru_cache.
<br>
4) 
</p>


<h5> Backend (minimax player): </h5>

<p>

<b>Minimax implementation (general):</b> The methodology used to get automated moves is an implementation of the minimax
algorithm, an established artificial intelligence algorithm. Minimax is used in this context to decide which move to
make on the current board by searching ahead in the game for favourable board configurations (and ultimately wins), 
assuming that the opposition also plays optimally.
<br>

<b>Minimax implementation (alpha-beta pruning):</b> Alpha-beta pruning has been implemented, which significantly 
reduces the number of nodes (future boards) which the algorithm has to search, by keeping track of the maximising and 
minimising player's respective best moves at each search depth, and never pursuing boards which are guaranteed to have
a less favourable end-state.
<br>

<b>Minimax implementation (iterative deepening):</b> 'Iterative deepening' here refers to iterating the minimax algorithm
at increasing maximum search depths until a fixed amount of time has run-out. The best move at each search depth is 
maintained, and replaced if a better one is found. This also includes a minimum search depth, and overall ensures that 
the algorithm spends a consistent amount of time searching, and quickly finds a (naive) move which is subsequently
improved on.
<br>

<b>Non-terminal board evaluation:</b> A considered set of functions has been implemented for scoring non-terminal boards
(by default the minimax algorithm as implemented is looking for terminal boards - wins, losses and draws). A key idea
here was the use of the imaginary i (or 1j in python) to represent empty cells - convolving with an array of ones of the
winning length then tells us immediately whether a given streak can be completed. For example in a 3x3 game, 
(1, -1, 0).(1, 1, 1) = 1, which is not very helpful, 
whereas: (1, -1, i).(1, 1, 1) = i, such that: abs(Real(0)) + abs(Imag(i)) = 1 < 3, telling us that there cannot be a
winning streak within this array, and thus is scored as 0 - which is more helpful.
<br>

<b>Multiprocessing of the search space (Discarded)</b> The search space of the minimax algorithm can be very large for
bigger boards: simulating a 10,10,5 game of minimax vs minimax that resulted in a draw, as one might hope, led to
145407 calls to the 'get_minimax_move_at_max_search_depth' method, 277 primary calls, (and 100 calls of the method that
controls the iterative deepening, noting 10x10 = 100). This is hence a case of a CPU-Bound program. Therefore, 
multiprocessing of the search space was trialed (using the built-in multiprocessing package). 
This was implemented by creating a pool of the nodes at search depth 0, and concurrently finding the best move within 
each subset of nodes, where one cpu evaluates one subset. This worked, although profiling found that it actually added 
time to the processing this scenario - I expect because it was reducing the effectiveness of the alpha-beta pruning 
(due to each process having its own memory space), and also the overheads introduced with repeatedly having to re-pool 
the processes at each max search depth. Before finding a resolution for this, it was found that despite being able to
run simulations and profile the backend code, the GUI structure would not allow multiprocessing as tkinter apps are not
picklable.
<br>

</p>
<hr>


<h3>Ideas for future extension:</h3>

<h5> Backend application:</h5>

<p>
<b> - Make fully n-dimensional.</b> Several methods have already been implemented as n-dimensional methods for generality, 
(most notably the win_check_and_location_search method, and most minimax methods), however not all have been.
<br>

<b> - Make the minimax player available at variable difficulties.</b> The current minimax player is intended to be as
difficult to play against as possible, subject to processing constraints. A difficulty level could be introduced most
simply by adding a random integer in a defined range [-a, a] to the board scoring system that informs the algorithm, 
where a is increased to make the game easier.
<br>

<b> - Leverage a transposition table/database.</b> This would be used to look up the outcome of different move in historic
games, to evaluate their effectiveness in an active game. Creating such a database could build on the GameSimulator in
game_simulation_base_class, and get_symmetry_set_of_tuples_from_array to run simulations of games and then store
that simulation an it's entire equivalence class in the transposition database
</p>

<h5> Frontend application</h5>

<p>
<b> - Also expand the dimensionality of the game (probably just to 3 dimensions).</b> This could be achieved using 3D 
visualisation, or even more simply by displaying multiple two-dimensional playing grids.
<br>

<b> - Allowing players to create an account and save the outcome of previous games against different opposition.</b>
Fairly endless possibilities about what could be done with this and how it could be implemented, a leaderboard and or
player scores using the Glicko rating system (the system used by chess.com) could be fun.
<br>
<b> - General extensions to GUI.</b> Including allowing players to change the game parameters between games, adding 
different themes to the display (e.g. light/dark), and other features of popular games.
</p>
