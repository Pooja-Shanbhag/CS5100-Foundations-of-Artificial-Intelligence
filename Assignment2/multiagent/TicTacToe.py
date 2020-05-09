class TicTacToe:
    def __init__(self, player):
        initialValue = ''
        self.data = [[initialValue for y in range(3)] for x in range(3)]

    def setGrid(self, data):
        self.data = data

    def utility(self, state):
        # terminal state test
        hasEmptyCells = False
        for i in range(0, 3):
            for j in range(0, 3):
                if state[i][0] == 'X' and state[i][1] == 'X' and state[i][2] == 'X':
                    return 1
                elif state[i][0] == 'O' and state[i][1] == 'O' and state[i][2] == 'O':
                    return -1
                elif state[0][j] == 'X' and state[1][j] == 'X' and state[2][j] == 'X':
                    return 1
                elif state[0][j] == 'O' and state[1][j] == 'O' and state[2][j] == 'O':
                    return -1
                elif state[i][j] == '':
                    hasEmptyCells = True

        if state[0][0] == 'X' and state[1][1] == 'X' and state[2][2] == 'X':
            return 1
        elif state[0][0] == 'O' and state[1][1] == 'O' and state[2][2] == 'O':
            return -1
        elif state[0][2] == 'X' and state[1][1] == 'X' and state[2][0] == 'X':
            return 1
        elif state[0][2] == 'O' and state[1][1] == 'O' and state[2][0] == 'O':
            return -1

        if hasEmptyCells:
            return None
        else:
            return 0

    def minimax(self, state, player):
        if self.utility(state) == 1 or self.utility(state) == -1 or self.utility(state) == 0:
            return self.utility(state)
        if player == 'X':
            value = -5
            for successorState in self.getSuccessor(state, player):
                currentEval = self.minimax(successorState, 'O')
                value = max(value, currentEval)
            return value
        else:
            value = 5
            for successorState in self.getSuccessor(state, player):
                currentEval = self.minimax(successorState, 'X')
                value = min(value, currentEval)
            return value

    def getSuccessor(self, state, player):
        listOfStates = []
        import copy
        duplicate = copy.deepcopy(state)
        for i in range(0, 3):
            for j in range(0, 3):
                if duplicate[i][j] == '':
                    duplicate[i][j] = player
                    listOfStates.append(duplicate)
                    duplicate = copy.deepcopy(state)
        return listOfStates


def main():
    # testing
    tic = TicTacToe(1)
    s0 = [['', '', ''], ['', '', ''], ['', '', '']]
    tic.setGrid(s0)
    assert tic.utility(tic.data) is None
    assert tic.minimax(s0, 'X') == 0
    print "Minmax at s0 ", tic.minimax(s0, 'X')
    s1 = [['', '', ''], ['', '', ''], ['', '', 'X']]
    tic.setGrid(s1)
    assert tic.utility(tic.data) is None
    assert tic.minimax(s1, 'O') == 0
    print "Minmax at s1 ", tic.minimax(s1, 'O')
    s2 = [['O', '', ''], ['', '', ''], ['', '', 'X']]
    tic.setGrid(s2)
    assert tic.utility(tic.data) is None
    # s2 doesn't give optimal result.
    print "Minmax at s2 ", tic.minimax(s2, 'X')
    s3 = [['O', '', ''], ['X', '', ''], ['', '', 'X']]
    tic.setGrid(s3)
    assert tic.utility(tic.data) is None
    print "Minmax at s3 ", tic.minimax(s3, 'O')
    s4 = [['O', 'O', ''], ['X', '', ''], ['', '', 'X']]
    tic.setGrid(s4)
    assert tic.utility(tic.data) is None
    print "Minmax at s4 ", tic.minimax(s4, 'X')
    s5 = [['O', 'O', 'X'], ['X', '', ''], ['', '', 'X']]
    tic.setGrid(s5)
    assert tic.utility(tic.data) is None
    print "Minmax at s5 ", tic.minimax(s5, 'O')
    s6 = [['O', 'O', 'X'], ['X', '', 'O'], ['', '', 'X']]
    tic.setGrid(s6)
    assert tic.utility(tic.data) is None
    assert tic.minimax(s6, 'X') == 1
    print "Minmax at s6 ", tic.minimax(s6, 'X')

    # terminal test
    s_final1 = [['O', 'O', 'X'], ['X', 'O', 'X'], ['O', 'X', 'X']]
    tic.setGrid(s_final1)
    assert tic.utility(tic.data) == 1

    s_final2 = [['O', 'O', 'X'], ['X', 'O', 'X'], ['', '', 'O']]
    tic.setGrid(s_final2)
    assert tic.utility(tic.data) == -1

    s_final3 = [['O', 'O', 'X'], ['X', 'O', 'X'], ['', '', 'X']]
    tic.setGrid(s_final3)
    assert tic.utility(tic.data) == 1

    s_final4 = [['O', 'O', 'O'], ['X', 'O', 'X'], ['', '', 'X']]
    tic.setGrid(s_final4)
    assert tic.utility(tic.data) == -1

    s_final5 = [['X', 'X', 'X'], ['X', 'O', 'X'], ['', '', 'X']]
    tic.setGrid(s_final5)
    assert tic.utility(tic.data) == 1

    s_final6 = [['O', 'O', 'X'], ['', 'X', ''], ['X', '', 'O']]
    tic.setGrid(s_final6)
    assert tic.utility(tic.data) == 1

    s_final7 = [['X', 'O', 'X'], ['0', 'X', '0'], ['O', 'X', 'O']]
    tic.setGrid(s_final7)
    assert tic.utility(tic.data) == 0


if __name__ == "__main__":
    main()


#Q3. Minmax for state s6 is 1. Verified at line 101
#Minmax for state s0 is 0. Verified at line 74.

#Q4. state s2 is suboptimal. As the action is max, minmax(s3) < minmax(s2)
#Optimal moves is: [['', '', ''], ['', 'O', ''], ['', '', 'X']]

# state s3 is suboptimal. As the action is min minmax(s4) > minmax{s3)
# Optimal moves are : [['O', '', ''], ['', '', ''], ['X', '', 'X']] or [['O', '', 'X'], ['', '', ''], ['', '', 'X']]