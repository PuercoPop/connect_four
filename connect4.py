#stab at connect four
from os.path import realpath, join, dirname
import logging
import copy
import random
import itertools

log_file = realpath(join(dirname(__file__),"connect4.log"))
logging.basicConfig(filename=log_file, filemode="w+", level=logging.DEBUG)
log = logging.getLogger(__name__)

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
        #whether there is a same cell in a particular direction.e.g (-1,1)
        new_cell = [ cell[0]+dirtn[0], cell[1]+dirtn[1] ]
        if self.check_boundary(new_cell) and self.gameboard[new_cell[0]][new_cell[1]] == self.gameboard[cell[0]][cell[1]]:
            # another way to do it: final = self.conxtn_one_dir(new_cell, dirtn, total + 1 )
            # and then add else: final = total
            # to explicitly save the value at that point in that nested functionO...finally else: return final
            return self.conxtn_one_dir(new_cell, dirtn, total + 1 )
        else:
            return total 

    def cal_connections (self, cell):
        if self.gameboard[cell[0]][cell[1]] == ' ':
           return 0
        else:
           temp = []
           #loop through all the neighbouring directions
           for pos in self.rela_pos:
               temp.append (self.conxtn_one_dir ( cell, pos, 0)) 
           return max(temp)

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
    if board.turn == 1:
       next_board = human_move_result( board, human_move() )
    else:
       next_board = minimax ( board, 0 )
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
    
def check_valid_move ( a_board, row, col ):
    if a_board.gameboard[row][col] == ' ':
      if row == 5:
         return True
      elif a_board.gameboard[row+1][col] != ' ':
         return True
      #TODO: add occasion where input is not int type
      else:
  #       print " invalid move. try again ^^ "
         return False
    else:
      return False

def get_avail_moves ( a_board ):
    cells = []
    for r in range( a_board.size[0] ):
        for c in range( a_board.size[1] ):
            if check_valid_move ( a_board, r, c):
               cells.append ( [r,c] )
    return cells

def get_possible_boards ( a_board ):
    boards = []
    for cell in get_avail_moves ( a_board ):
        new_board = update_board ( a_board, cell[0], cell[1] )
        new_board.turn = -1 * new_board.turn
        boards.append( new_board )
    
    log.info("===================================")
    for b in boards:
        log.info( " possible board: \n" )
        for element in b.gameboard:
           log.info( " possible board: \n{element}\n".format(element=element))
        log.info( " ---------------")
    log.info("===================================")

    return boards

def check_winning ( a_board ):
    for element in a_board.connections:
        print "connections  " + str(element)[1:-1] 
        if 3 in element:
           return True
    return False

def num_center ( a_board ):
    if a_board.turn == -1:
       #TODO: use list.count() to refactor this?
       l = [ x for x in a_board.p0_moves if x[1] == 3 ]
    elif a_board.turn == 1:
       l = [ x for x in a_board.p1_moves if x[1] == 3 ]
    return len(l)

def num_n_conxtn ( a_board , n ):
    #cal number of 2s or 1s in the connections grid
    ####  turn means it is someone's turn for next move
    ###   but we want to evaluate the move that is JUST MADE
    ###   switch turns back
    ##    if -1 then evalue  'x'  1 --> evaluate 'o'
    if a_board.turn == -1:
       v = 0
       for x in a_board.p0_moves:
         if a_board.cal_connections (x) == n:
            v += 1
       return v
    elif a_board.turn == 1:
       vl = 0
       for y in a_board.p1_moves:
         if a_board.cal_connections (y) == n:
            vl += 1
       return vl

def evaluate_board ( a_board ):
    #evaluation result in tuples (9,5,3) 
    return ( check_winning(a_board), num_center(a_board), num_n_conxtn(a_board, 2), num_n_conxtn(a_board,1),)

def minimax ( a_board, depth ):
    b = Board ( a_board )
    if depth == 4:
       print "evaluation   " , evaluate_board ( b)
       return evaluate_board ( b )
    if b.turn == -1:
       value = (0,0,0)   #TODO...modify accoridng to evalu func
    elif b.turn == 1:
       value = (1,9,9)   #TODO> modify
    for element in get_possible_boards ( b ):
        print "posi board turn " , element.turn
        print "posi board" , element.gameboard
        v = minimax ( element, depth + 1 )
        if b.turn == -1 and v > value:  
          the_right_move = element
          value = v
          print  " max value is ",  value
        elif b.turn == 1 and v < value:
          the_right_move = element
          value = v
          print " min value is ", value

    if b.turn == -1:
       log.info("max value is {value}".format( value=value ))
    elif b.turn == 1:
       log.info("min value is {value}".format( value=value ))

    if depth == 0:
       return the_right_move
    
    return value     

def check_ending ( a_board ):
    if check_winning( a_board ):
       print " YOU WON!! " 
       return True
    else:
       for element in a_board.gameboard:
           for cell in element:
              if cell == ' ':
                 return False
       return True

def main():
    board = Board()

#    board.p0_moves= [[3,4], [4,3], [4,5], [5,2], [5,4] ]
#    board.p1_moves= [ [4,2], [4,4], [5,3], [5,5] ]
    while True:
          board.show()
          if check_ending( board ):
             break
          else:
             board = play(board)

if __name__=="__main__":
   main()
