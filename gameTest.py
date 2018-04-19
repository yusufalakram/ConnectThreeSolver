import connect
env = connect.Connect(verbose=True)
env.reset(first_player='o')

# Player 'o' plays
print("Current player at turn:", env.player_at_turn)
env.act(action=2)

# Player 'x' plays
env.change_turn()
print("Current player at turn:", env.player_at_turn)
env.act(action=2)

# Player 'o' plays
env.change_turn()
print("Current player at turn:", env.player_at_turn)
env.act(action=2)

# Print grid
print("Printing grid")
current_grid = env.grid
print(current_grid)

# Print available actions
print("Available actions:")
print(env.available_actions)

# Was last game move a win?
print("Winning move?", env.was_winning_move())

# Make some moves
env.change_turn()
env.act(action=3)
env.change_turn()
env.act(action=1)
env.change_turn()
env.act(action=3)
env.change_turn()
env.act(action=0)

# Check again whether a player has won the game.
print("Winning move?", env.was_winning_move())

# Is grid full? Used to check for draw
print("Is grid full?", env.grid_is_full())
