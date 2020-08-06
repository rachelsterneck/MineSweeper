from random import randint
from flask import jsonify
import itertools
import copy

class Tile:
    def __init__(self):
        self.is_clicked = False
        self.value = None
        
class Mine:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.board = self.create_board()
        self.x_guess = None
        self.y_guess = None

    # creates a 2D array of Tile elements to build a new board
    # returns new mine_board
    def create_board(self):   
        mine_board = [[None for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                mine_board[i][j] = Tile()
        return mine_board
    
    # adds num_mines mines to the board
    # parameters x_guess and y_guess ensure first tile is not a mine
    # returns board_copy which contains mines and counts of adjacent mines to each tile
    # and mines_set which is used only in  test.py 
    def create_mines(self, x_guess, y_guess):
        mines_set = set()
        while len(mines_set) < self.num_mines:
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
            if x != int(x_guess) and y != int(y_guess):
                mines_set.add((x, y))
        
        for m in mines_set:
            self.board[m[0]][m[1]].value = -1

        # get counts of adjacent pieces
        board_copy = copy.deepcopy(self.board)
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                if self.board[i][j].value != -1:
                    for n in self.get_neighbors((i, j)):
                        if self.board[n[0]][n[1]].value == -1:
                            count+=1
                    board_copy[i][j].value = count

        return board_copy, mines_set
    
    # print readable board for terminal game 
    def print_board(self):
        r = "  " + ' '.join(str(x) for x in range(self.size))
        print(r) 
        x = 0
        for i in range(self.size):
            board_string = "{} ".format(x)
            for j in range(self.size):
                if self.board[i][j].is_clicked:
                    if self.board[i][j].value == -1:
                        board_string += "* "
                    else:
                        board_string += "{} ".format(self.board[i][j].value)
                else:
                    board_string += ". "
            print(board_string)
            x+=1

    # print readable board solution for terminal game
    def print_solution(self):
        print("--------------------")
        r = "  " + ' '.join(str(x) for x in range(self.size))
        print(r) 
        x = 0
        for i in range(self.size):
            board_string = "{} ".format(x)
            for j in range(self.size):
                if self.board[i][j].value == -1: # is mine
                    board_string += "* "
                else:
                    board_string += "{} ".format(self.board[i][j].value)
            print(board_string)
            x+=1 
        print("--------------------\n")
          
    # check if user has selected a tile with mine
    def has_lost(self):
        return self.board[self.x_guess][self.y_guess].value == -1

    # check if the only unclicked pieces on the board are all tiles
    def has_won(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.board[i][j].is_clicked and not self.board[i][j].value == -1: ## not clicked and not mine
                    return False
        return True
            
    # click a square and click all adjacent squares 
    # recurisvely if that square has no adjacent mines
    def update(self, x, y):  
        if self.board[x][y].value == 0 and not self.board[x][y].is_clicked: 
            self.board[x][y].is_clicked = True

            for n in self.get_neighbors((x, y)):
                self.update(n[0], n[1])
        else:
            self.board[x][y].is_clicked = True
    
    # find coordinates of neighboring tiles
    # inspired by: https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
    def get_neighbors(self, coordinate):
        for x,y in itertools.product(*(range(i-1, i+2) for i in coordinate)):
            if (x,y) != coordinate and all(0 <= j < self.size for j in (x,y)):
                yield x, y

    # handler for terminal game input/output
    def play(self):
        while 1==1:
            xy = input('Enter the coordinates of your choice "x,y"\n')
            if self.x_guess is None and self.y_guess is None:
                self.board, _ = self.create_mines(xy[0], xy[2])
                self.print_solution()
            self.x_guess = int(xy[0])
            self.y_guess = int(xy[2])

            self.update(self.x_guess, self.y_guess)
            self.print_board()
            if self.board[self.x_guess][self.y_guess].value == -1:
                print("you lose!")
                break
            if self.has_won():
                print("congrats, you win!")
                break
    
    # convert Mine to json to be returned to client
    def to_json(self):
        json_board  = [[None for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                json_board[i][j] = {"is_clicked":self.board[i][j].is_clicked, "value":self.board[i][j].value}
        return {'size':self.size, 'num_mines':self.num_mines, 'board':json_board, 'x_guess':self.x_guess, 'y_guess':self.y_guess, "message":""}


if __name__=="__main__":
    print('\nWelcome to Minesweeper!\n')
    mine = Mine(size=9, num_mines=10)
    mine.print_board()
    mine.play()