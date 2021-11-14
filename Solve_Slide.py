import copy

BLANK = None
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'



class Node:

    def __init__(self, Value: [], ParentID: int, NodeID: int, NodeLevel: int, Relation: str, NoChilds: int):
        self.Value = Value
        self.ParentID = ParentID
        self.NodeID = NodeID
        self.NodeLevel = NodeLevel
        self.Relation = Relation
        self.NoChilds = NoChilds


class Slide_Solve_AI:

    def __init__(self, mainBoard: [], SOLVEDBOARD: [], BOARDWIDTH: int, BOARDHEIGHT: int):
        self.mainBoard = mainBoard
        self.SOLVEDBOARD = SOLVEDBOARD
        self.BOARDWIDTH = BOARDWIDTH
        self.BOARDHEIGHT = BOARDHEIGHT

    def solve(self):
        solved = True
        tree = []
        solve_move = []
        while solved:
            if self.mainBoard == self.SOLVEDBOARD:
                return solve_move
            else:
                node = Node(copy.deepcopy(self.SOLVEDBOARD), 0, 0, 0, UP, 0)
                tree.append(node)
                i = 0
                while solved:
                    board = copy.deepcopy(tree[i].Value)
                    blank = self.find_blank(board, self.BOARDWIDTH, self.BOARDHEIGHT)
                    valid_move = self.Check_Valid_Move(blank, self.BOARDWIDTH, self.BOARDHEIGHT)
                    valid_move = self.Remove_Grandpa(valid_move, tree[i].Relation)
                    new_boards = self.new_move_board(valid_move, copy.deepcopy(board), blank)
                    for xboard in range(len(new_boards)):
                        tree.append(Node(new_boards[xboard], tree[i].NodeID, len(tree), tree[i].NodeLevel + 1,
                                        valid_move[xboard], 0))
                        tree[i].NoChilds += 1
                        if new_boards[xboard] == self.mainBoard:
                            solved = False
                            print("solved! value: ", tree[len(tree)-1].Value, "\n ParentID: ", tree[len(tree)-1].ParentID,
                                  "  NodeID:", tree[len(tree)-1].NodeID, "   Relation: ", tree[len(tree)-1].Relation,
                                  "  NodeLevel:", tree[len(tree)-1].NodeLevel, "  NoChilds: ", tree[len(tree)-1].NoChilds)
                            solve_move = self.solve_moves(tree)
                    i += 1
        #for x in range(len(tree)):
            #print('\n', tree[x].Value, tree[x].ParentID, tree[x].NodeID, tree[x].Relation, tree[x].NodeLevel,
                #tree[x].NoChilds)
        print("solve_move: ", solve_move, "\n")
        return solve_move


    def solve_moves(self, tree):
        solve_move = []
        id = tree[len(tree)-1].NodeID
        while id > 0:
            relation = tree[id].Relation
            solve_move.append(relation)
            id = tree[id].ParentID
        solve_move.reverse()
        return solve_move


    def opssite_move(self, relation):
        if relation == UP:
            relation = DOWN
        elif relation == DOWN:
            relation = UP
        elif relation == RIGHT:
            relation = LEFT
        elif relation == LEFT:
            relation = RIGHT
        return relation


    def new_move_board(self, move, board, blank):
        new_board = []
        for x in range(len(move)):
            new_board.append(self.apply_move(move[x], copy.deepcopy(board), blank))
        return new_board


    def apply_move(self, x, apply_board, blank):
        blankx, blanky = blank
        if x == UP:
            apply_board[blankx][blanky] = apply_board[blankx][blanky + 1]
            apply_board[blankx][blanky + 1] = BLANK
        elif x == DOWN:
            apply_board[blankx][blanky] = apply_board[blankx][blanky - 1]
            apply_board[blankx][blanky - 1] = BLANK
        elif x == RIGHT:
            apply_board[blankx][blanky] = apply_board[blankx - 1][blanky]
            apply_board[blankx - 1][blanky] = BLANK
        elif x == LEFT:
            apply_board[blankx][blanky] = apply_board[blankx + 1][blanky]
            apply_board[blankx + 1][blanky] = BLANK
        return apply_board


    # check valid move &grand pa
    def Check_Valid_Move(self, blank, BOARDWIDTH, BOARDHEIGHT):
        valid_move = []
        blankx, blanky = blank
        if blanky + 1 < BOARDWIDTH:
            valid_move.append(UP)
        if blanky - 1 >= 0:
            valid_move.append(DOWN)
        if blankx + 1 < BOARDHEIGHT:
            valid_move.append(LEFT)
        if blankx - 1 >= 0:
            valid_move.append(RIGHT)
        return valid_move


    def find_blank(self, board, BOARDWIDTH, BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[x][y] == BLANK:
                    blank = [x, y]
                    return blank


    def Remove_Grandpa(self, valid_move, Relation):
        if Relation == UP:
            Relation = DOWN
        elif Relation == DOWN:
            Relation = UP
        elif Relation == RIGHT:
            Relation = LEFT
        elif Relation == LEFT:
            Relation = RIGHT
        for x in valid_move:
            if x == Relation:
                valid_move.remove(x)
        return valid_move

