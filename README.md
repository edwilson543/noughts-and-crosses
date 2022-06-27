<h1> 'Noughts and Crosses' Project</h1>
<hr>

<h4>
This repository is an m, n, k noughts and crosses (aka tic-tac-toe) application.
The game includes a tkinter GUI allowing users to play each other, as well as an automatic player which has been
implemented using the minimax algorithm.
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
<h3>Notable/interesting features of the application:</h3>



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
