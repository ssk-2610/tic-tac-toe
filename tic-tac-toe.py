import numpy as np

def minimax_decision(state, game):

    player = game.to_move(state)
    print(player)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))





def depth_limit_search(state, game,depthLimit=6):

    player = game.to_move(state)

    def max_value(state,depth):
        if cutoff_test(state, depth):
            return eval_fn(state)

        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a), depth+1))
        return value

    def min_value(state,depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a), depth+1))
        return value


    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))


    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), 1))



def alpha_beta_search(state, game):

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a), alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        value = min_value(game.result(state, a), best_score, beta)
        if value > best_score:
            best_score = value
            best_action = a
    return best_action



class State:
    def __init__(self,to_move, utility, board, moves):
        self.to_move=to_move
        self.utility=utility
        self.board=board
        self.moves=moves




class Game:

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state):
        return not self.actions(state)

    def to_move(self, state):
        return state.to_move


    def display(self, state):
        board = state.board
        for x in range(0, self.h):
            for y in range(0, self.v):
                print(board[x][y], end=' ')
            print()

        print()



    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)



class TicTacToe(Game):

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(0, h)
                 for y in range(0, v)]
        self.initial = State(to_move='X', utility=0, board=np.full((h,v),'-'), moves=moves)


    def actions(self, state):
        return state.moves


    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move[0]][move[1]] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return State(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)



    def to_move(self, state):
        return state.to_move


    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility


    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0



    def k_in_row(self, board, move, player, delta_x_y):
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while x>=0 and x<self.h and y>=0 and y<self.v and board[x][y] == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while x>=0 and x<self.h and y>=0 and y<self.v and board[x][y] == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n


    def compute_utility(self, board, move, player):
        if (self.k_in_row(board, move, player, (0, 1))>=self.k) or (self.k_in_row(board, move, player, (1, 0))>=self.k) or (self.k_in_row(board, move, player, (1, -1))>=self.k) or (self.k_in_row(board, move, player, (1, 1))>=self.k):
            return +1 if player == 'X' else -1
        else:
            return 0





qwerty=1
while(qwerty>0):
    choice1=int(input('\nEnter your Choice of Game:\n1.Tic Tac Toe\n2.Open Field Tic Tac Toe.\n'))
    choice2=int(input('\nEnter your Choice of Search:\n1.Minimax Algorithm\n2.Alpha Beta Pruning\n3.Depth Limit\n'))

    if choice1==2:
        h=int(input("Enter the size of the board.\n"))
        k=int(input("Enter the number of pieces to be aligned to win the game.\n"))
        TT=TicTacToe(h,h,k)
    else:
        TT=TicTacToe()


    search=[minimax_decision,alpha_beta_search,depth_limit_search]
    search_type=search[choice2-1]



    while True:

        TT.initial.to_move='O'

        print(TT.display(TT.initial))

        x,y = list(map(int,input("\nEnter(x,y):\n").split(',')))
        player_turn=(x,y)
        TT.initial.board[x][y]='O'
        TT.initial.moves.remove(player_turn)

        if (TT.k_in_row(TT.initial.board, player_turn, 'O', (0, 1))>=TT.k) or (TT.k_in_row(TT.initial.board, player_turn, 'O', (1, 0))>=TT.k) or (TT.k_in_row(TT.initial.board, player_turn, 'O', (1, -1))>=TT.k) or (TT.k_in_row(TT.initial.board, player_turn, 'O', (1, 1))>=TT.k):
            print(TT.initial.moves)
            print('YOU WIN')
            break

        elif len(TT.initial.moves)==0:
            print('It\'s a Draw')
            break

        else:

            TT.initial.to_move='X'

            computer_turn=minimax_decision(TT.initial,TT)
            TT.initial.board[computer_turn[0]][computer_turn[1]]='X'
            TT.initial.moves.remove(computer_turn)

            if (TT.k_in_row(TT.initial.board, computer_turn, 'X', (0, 1))>=TT.k) or (TT.k_in_row(TT.initial.board, computer_turn, 'X', (1, 0))>=TT.k) or (TT.k_in_row(TT.initial.board, computer_turn, 'X', (1, -1))>=TT.k) or (TT.k_in_row(TT.initial.board, computer_turn, 'X', (1, 1))>=TT.k):
                print('AI Wins\n')
                break

            elif len(TT.initial.moves)==0:
                print('It\'s a Draw\n')
                break
    print('Do you want to play again?[y/n]\n')
    asd=str(input())
    if(asd=='y'):
        continue
    else:
        exit()