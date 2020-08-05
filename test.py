from game import Mine
import random
from random import randint

def update_clicked(board, clicked_set):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].is_clicked:
                clicked_set.add((i, j))

def test_win():
    count = 1
    mine = Mine(size=9, num_mines=10)
    has_won, x, y = None, None, None
    mines_set = set()
    clicked_set = set()
    x_init, y_init = randint(0, mine.size - 1), randint(0, mine.size - 1)
    while 1==1:
        if mine.x_guess is None and mine.y_guess is None:
            mine.board, mines_set = mine.create_mines(x_init, y_init)
            mine.print_solution()
        
        while 1==1:
            x, y = randint(0, mine.size - 1), randint(0, mine.size - 1)
            if (x, y) not in mines_set and (x, y) not in clicked_set:
                break
        
        mine.x_guess = x
        mine.y_guess = y
        print("Turn # {} Guess: ({},{})".format(count, mine.x_guess, mine.y_guess))

        mine.update(mine.x_guess, mine.y_guess)
        update_clicked(mine.board, clicked_set)
        mine.print_board()
        print("")
        count+=1
        if mine.board[mine.x_guess][mine.y_guess].value == -1:
            print("you lose!")
            has_won = False
            break
        if mine.has_won():
            print("congrats, you win!")
            has_won = True
            break
            
    assert(has_won)
            

def test_lose():
    count = 1
    mine = Mine(size=9, num_mines=10)
    has_won, x, y = None, None, None
    mines_set = set()
    clicked_set = set()
    x_init, y_init = randint(0, mine.size - 1), randint(0, mine.size - 1)
    max_turns = randint(2, mine.size*mine.size - mine.num_mines - 1)
    print("Max Turns: {}".format(max_turns))
    while count<max_turns:
        if mine.x_guess is None and mine.y_guess is None:
            mine.board, mines_set = mine.create_mines(x_init, y_init)
            mine.print_solution()
        
        while 1==1:
            x, y = randint(0, mine.size - 1), randint(0, mine.size - 1)
            if (x, y) not in mines_set and (x, y) not in clicked_set:
                clicked_set.add((x, y))
                break
        
        mine.x_guess = x
        mine.y_guess = y
        print("Turn # {} Guess: ({},{})".format(count, mine.x_guess, mine.y_guess))

        mine.update(mine.x_guess, mine.y_guess)
        mine.print_board()
        print("")
        count+=1
        if mine.board[mine.x_guess][mine.y_guess].value == -1:
            assert(False)
        if mine.has_won():
            print("congrats, you win!") ## if num turns is high, you might win
            assert(True)
    
    mine_xy = random.sample(mines_set, 1)
    mine.x_guess = mine_xy[0][0]
    mine.y_guess = mine_xy[0][1]
    print("Turn # {} Guess: ({},{})".format(count, mine.x_guess, mine.y_guess))
    mine.update(mine.x_guess, mine.y_guess)
            
    assert(mine.has_lost())

if __name__=="__main__":
    num_tests = 1000
    for i in range(num_tests):
        print("\nTEST # {}".format(i))
        test_lose()
    for i in range(num_tests):
        print("\nTEST # {}".format(i))
        test_win()

