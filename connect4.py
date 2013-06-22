#stab at connect four
import copy
import random
import itertools

class Board(object):

    def __init__(self,board=None):
       self.size = (6, 7)
       if board == None:
          self.p0_moves = []
          self.p1_moves = []
          self.turn = 1 
       else:
          self.p0_moves = copy.deepcopy(board.p0_moves)
          self.p1_moves = copy.deepcopy(board.p1_moves)
          self.turn = board.turn

    @property
    def gameboard (self):
        gameboard = [[' ']*self.size[1] for x in range(self.size[0])]
        for r,c in self.p0_moves:
            gameboard[r][c] = 'x'
        for r,c in self.p1_moves:
            gameboard[r][c] = 'o'
        return gameboard

    @property
    #relative positions of neighbours of any cell relative to its own coordinate
    def rela_pos (self):
        rela_postns = list( itertools.permutations(range(-1,2),2) )
        rela_postns.extend([(1,1),(-1,-1)])
        return rela_postns

    def check_boundary ( self, a_cell):
        return a_cell[0]>0 and a_cell[0]<self.size[0] and a_cell[1]>0 and a_cell[1]<self.size[1]

    def conxtn_one_dir (self, cell, dirtn, total):
#        out = total
        #whether there is a same cell in a particular direction.e.g (-1,1)
        new_cell = [ cell[0]+dirtn[0], cell[1]+dirtn[1] ]
        if self.check_boundary(new_cell) and self.gameboard[new_cell[0]][new_cell[1]] == self.gameboard[cell[0]][cell[1]]:
            print dirtn
            final = self.conxtn_one_dir(new_cell, dirtn, total+1)
        else:
            final = total
        return final

    def cal_connections (self, cell):
        if self.gameboard[cell[0]][cell[1]] == ' ':
           value = 0
        else:
           value = 0
            #loop through all the neighbouring directions
           for pos in self.rela_pos:
              num = self.conxtn_one_dir ( cell, pos, value)
              if num > value:
                   # num_conxtn should be the max of all directions
                 value = num 
        return value

    @property
    def connections (self):
        connections = [[0]*self.size[1] for x in range(self.size[0])]
        for r in range(self.size[0]):
            for c in range(self.size[1]):
               connections[r][c] = self.cal_connections( [r,c] )
        return connections

    def show (self):
        for element in self.gameboard:
            print '|'+'|'.join(element)+'|'
      
def play (board):
    next_board = human_move_result( board, human_move() )
    next_board.turn = -1 * board.turn 
    return next_board

def human_move ():
    print "place your move."
    print "enter row number 0 to 5. Bottom row is 0"
    row = int(raw_input())
    print"enter column number 0 to 6"
    col = int(raw_input())
    return ((5-row),col)

def human_move_result ( a_board, the_move ):
    if check_valid_move(a_board, the_move[0], the_move[1]) :
       new_board = update_board(a_board, the_move[0], the_move[1])
    else:
       new_board =  human_move_result( a_board, human_move())
    return new_board

def update_board ( a_board, row, col ):   
    a_board = Board(a_board)
    if a_board.turn == 1:
       a_board.p0_moves.append([row, col])
    elif a_board.turn == -1:
        a_board.p1_moves.append([row, col])
    if check_winning( a_board ):
       print  " you won !!! "
    return a_board   
    
def check_winning ( a_board ):
    for element in a_board.connections:
        if 4 in element:
           print "connections  " + str(element)[1:-1] 
           return True
        else:
           print "connections  " + str(element)[1:-1] 
    return False

def check_ending ( a_board ):
    if check_winning( a_board ):
       return True
    else:
       for element in a_board.gameboard:
           for cell in element:
              if cell == ' ':
                 return False
       return True

def check_valid_move ( a_board, row, col ):
    if a_board.gameboard[row][col] == ' ':
      if row == 5:
         return True
      elif a_board.gameboard[row+1][col] != ' ':
         return True
      #TODO: add occasion where input is not int type
      else:
         print " invalid move. try again ^^ "
         return False
      
def main():
    board = Board()
    while True:
          board.show()
          if check_ending( board ):
             break
          else:
             board = play(board)

if __name__=="__main__":
   main()
