#stab at connect four
from os.path import realpath, join, dirname
import logging
import random
import itertools

log_file = realpath(join(dirname(__file__),"connect4.log"))
logging.basicConfig(filename=log_file, filemode="w+", level=logging.DEBUG)
log = logging.getLogger(__name__)

class Board(object):

    def __init__(self, p0moves=[], p1moves=[], turn=1):
#       if p0moves is None:
#         p0moves = []
       self.size = (6, 7)
       self.p0_moves = p0moves[:]
       self.p1_moves = p1moves[:]
       self.turn = turn 
    
    @classmethod
    def for_testing(cls, board_string, turn=1):
        #convert string to p0 and p1 moves
        p0 = []
        p1 = []
        for index, ele, in enumerate(board_string.split(',')):
           for i, e in enumerate(ele):
              if e == 'x':
                  p0.append([index, i]) 
              elif e == 'o':
                  p1.append([index, i])
        b = cls (p0, p1, turn)
        return b

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
     
    def move (self, move, turn=None ):   
        #move is tuple/list. return a brand new board
        b = Board( self.p0_moves,self.p1_moves)
        if turn != None:
           b.turn = turn
        elif b.turn == 1:
           b.p0_moves.append(move)
        elif b.turn == -1:
           b.p1_moves.append(move)
       # if check_winning( a_board ):
       #    print  " you won !!! "
        return b
        
    def check_valid_move ( self, move):
        #move is tuple
        if self.gameboard[move[0]][move[1]] ==' ':
           if move[0]==5 or self.gameboard[move[0]+1][move[1]] != ' ':
              return True
           #TODO: add occasion where input is not int type
           else:
          #  print " invalid move. try again ^^ "
              return False
        else:
          return False

    def get_avail_moves ( self):
        cells = []
        for r in range( self.size[0] ):
            for c in range( self.size[1] ):
                if self.check_valid_move ( [r, c] ):
                   cells.append ( [r,c] )
        return cells

    def get_possible_boards ( self ):
        boards = []
        for cell in self.get_avail_moves ():
            print cell
            new_board = self.move ( cell )
            print new_board.gameboard
            new_board.turn = -1 * new_board.turn
            boards.append( new_board )
        
        log.info("===================================")
        for b in boards:
            log.info("possible board")
            #print " possi board \n"
            for element in b.gameboard:
            #   print str(element)[1:-1]
               log.info( "{element}\n".format(element=element))
            log.info( " ---------------")
        log.info("===================================")

        return boards

    def check_winning (self ):
        for element in self.connections:
            #print "connections  " + str(element)[1:-1] 
            if 3 in element:
               return True
        return False

    def check_ending ( self ):
        if self.check_winning():
           print " YOU WON!! " 
           return True
        else:
           for element in self.gameboard:
               for cell in element:
                  if cell == ' ':
                     return False
           return True

    def num_center ( self ):
        if self.turn == -1:
           #TODO: use list.count() to refactor this?
           return len( [ x for x in self.p0_moves if x[1] == 3 ] )
        elif self.turn == 1:
           return len( [ x for x in self.p1_moves if x[1] == 3 ] )

    def num_n_conxtn ( self, n ):
        #cal number of 2s or 1s in the connections grid
        ####  turn means it is someone's turn for next move
        ###   but we want to evaluate the move that is JUST MADE
        ###   switch turns back
        ##    if -1 then evalue  'x'  1 --> evaluate 'o'
        if self.turn == -1:
           v = 0
           for x in self.p0_moves:
             if self.cal_connections (x) == n:
                v += 1
           return v
        elif self.turn == 1:
           vl = 0
           for y in self.p1_moves:
             if self.cal_connections (y) == n:
                vl += 1
           return vl

    def evaluate_board ( self ):
        #evaluation result in tuples (9,5,3) 
        return ( self.check_winning(), self.num_n_conxtn(2), self.num_n_conxtn(1), self.num_center())
 
def play (board):
    if board.turn == 1:
       next_board = human_move(board)
    else:
       next_board = minimax ( board, 0 )
    next_board.turn = -1 * board.turn 
    return next_board

def human_move ( a_board ):
    #let human make the move
    print "place your move."
    print "enter row number 0 to 5. Bottom row is 0"
    row = int(raw_input())
    print"enter column number 0 to 6"
    col = int(raw_input())
    the_move = ((5-row),col)

    if a_board.check_valid_move( the_move ):
       new_board = a_board.move ( the_move )
    else:
       new_board =  human_move ( a_board )
    return new_board

def minimax ( a_board, depth ):
    b = Board ( a_board.p0_moves, a_board.p1_moves )
    if depth == 1:
#       print "evaluation   " , evaluate_board ( b)
       return a_board.evaluate_board ()
    if b.turn == -1:
       value = (0,0,0)   #TODO...modify accoridng to evalu func
    elif b.turn == 1:
       value = (1,9,9)   #TODO> modify

    for element in b.get_possible_boards ():
        #print "posi board turn " , element.turn
        #print "posi board" , element.gameboard
        v = minimax ( element, depth + 1 )
        if b.turn == -1 and v > value:  
          the_right_move = element
          value = v
          log.info("max value is {value}".format( value= value ))
       #   print  " max value is ",  value
        elif b.turn == 1 and v < value:
          the_right_move = element
          value = v
          log.info("min value is {value}".format( value=value ))
       #   print " min value is ", value

    if b.turn == -1:
       log.info("max value is {value}".format( value=value ))
    elif b.turn == 1:
       log.info("min value is {value}".format( value=value ))

    if depth == 0:
       return the_right_move
    
    return value     

def main():
    b = Board()
    s = ',,,nnnxnnn,nnoxxon,onoxoxn'
    board = b.for_testing ( s, -1)
#   board.p0_moves= [[3,4], [4,3], [4,5], [5,2], [5,4] ]
#   board.p1_moves= [ [4,2], [4,4], [5,3], [5,5] ]
    while True:
          board.show()
          if board.check_ending():
             break
          else:
             board = play(board)

if __name__=="__main__":
   main()
