import random


class Player:
    def __init__(self, letter):
        self.letter = letter


class User(Player):
    def move(self, cells):
        while True:
            user_input = input('Enter the coordinates: ').split()
            redo = False
            for i in range(2):
                try:
                    if not user_input[i].isdigit():
                        print('You should enter numbers!')
                        redo = True
                    elif not (1 <= int(user_input[i]) <= 3):
                        print('Coordinates should be from 1 to 3!')
                        redo = True
                except IndexError:
                    pass
            if redo == True:
                continue
            user_col = int(user_input[0]) - 1
            user_row = (-int(user_input[1]) + 3)
            break
        return user_row, user_col

    def is_ai(self):
        return False


class Easy(Player):
    difficulty = 'easy'

    def move(self, cells):
        easy_row = random.randint(0, 2)
        easy_col = random.randint(0, 2)
        return easy_row, easy_col

    def is_ai(self):
        return True


class Medium(Player):
    difficulty = 'medium'

    def move(self, cells):
        win_row, win_col = can_win(cells, self.letter)
        save_row, save_col = can_save(cells, self.letter)
        if win_row is not None and win_col is not None:
            return win_row, win_col
        elif save_row is not None and save_col is not None:
            return save_row, save_col
        else:
            return random.randint(0, 2), random.randint(0, 2)

    def is_ai(self):
        return True


class Hard(Player):
    difficulty = 'hard'

    def move(self, cells):
        letter = self.letter
        move = self.minimax(cells, letter)
        if move['index'] in [0, 1, 2]:
            row = 0
        elif move['index'] in [3, 4, 5]:
            row = 1
        else:
            row = 2
        if move['index'] in [0, 3, 6]:
            col = 0
        elif move['index'] in [1, 4, 7]:
            col = 1
        else:
            col = 2
        return row, col

    def is_ai(self):
        return True

    def minimax(self, cells, letter):
        if letter == 'X':
            opp = 'O'
        else:
            opp = 'X'

        availSpots = get_empty(cells)
        end_score = {}
        if check_winner(cells) == self.letter:
            end_score['score'] = 10
            return end_score
        elif check_winner(cells) == 'Draw':
            end_score['score'] = 0
            return end_score
        elif check_winner(cells) != self.letter and check_winner(cells) is not None:
            end_score['score'] = -10
            return end_score

        moves = []
        for spot in availSpots:
            move = {}
            move['index'] = spot
            newBoard = list(cells)
            newBoard[move['index']] = letter
            newBoard = ''.join(newBoard)

            result = self.minimax(newBoard, opp)
            move['score'] = result['score']
            moves.append(move)

        best_move = {}
        if letter == self.letter:
            best = -100
            for move in moves:
                if move['score'] > best:
                    best = move['score']
                    best_move['index'] = move['index']
                    best_move['score'] = best
        else:
            best = 100
            for move in moves:
                if move['score'] < best:
                    best = move['score']
                    best_move['index'] = move['index']
                    best_move['score'] = best
        return best_move


def get_empty(cells):
    empty = []
    for i, v in enumerate(list(cells)):
        if v == ' ':
            empty.append(i)
    return empty


def get_board(cells):
    rows, cols = [], []
    for i in range(0, 9, 3):
        rows.append([cells[i], cells[i + 1], cells[i + 2]])
    for i in range(3):
        cols.append([cells[i], cells[i + 3], cells[i + 6]])

    diag1, diag2 = [], []
    for i in range(3):
        diag1.append(rows[i][i])
        diag2.append(rows[(i)][-(i + 1)])
    return rows, cols, diag1, diag2


def print_board(rows):
    print('---------')
    for i in range(3):
        print('| ', end='')
        for j in range(3):
            print(rows[i][j] + ' ', end='')
        print('|')
    print('---------')


def can_win(cells, letter):
    rows, cols, diag1, diag2 = get_board(cells)
    r_index, c_index = None, None
    for row in rows:
        if row.count(letter) == 2 and ' ' in row:
            c_index = row.index(' ')
    for col in cols:
        if col.count(letter) == 2 and ' ' in col:
            r_index = col.index(' ')
    return r_index, c_index


def can_save(cells, letter):
    rows, cols, diag1, diag2 = get_board(cells)
    r_index, c_index = None, None
    if letter == 'X':
        opp = 'O'
    else:
        opp = 'X'
    for row in rows:
        if row.count(opp) == 2 and ' ' in row:
            c_index = row.index(' ')
    for col in cols:
        if col.count(opp) == 2 and ' ' in col:
            r_index = col.index(' ')
    return r_index, c_index


def X_turn(X, cells):
    rows, cols, diag1, diag2 = get_board(cells)
    while True:
        X_row, X_col = X.move(cells)
        if rows[X_row][X_col] != ' ':
            print('This cell is occupied! Choose another one!')
            continue
        else:
            break
    rows[X_row][X_col] = X.letter
    if X.is_ai():
        print(f'Making move level "{X.difficulty}"')
    cells = ''
    for row in rows:
        for col in row:
            cells += col
    return cells


def O_turn(O, cells):
    rows, cols, diag1, diag2 = get_board(cells)
    while True:
        O_row, O_col = O.move(cells)
        if rows[O_row][O_col] != ' ':
            print('This cell is occupied! Choose another one!')
            continue
        else:
            break
    rows[O_row][O_col] = O.letter
    if O.is_ai():
        print(f'Making move level "{O.difficulty}"')
    cells = ''
    for row in rows:
        for col in row:
            cells += col
    return cells


def check_winner(cells):
    x_win = ['X', 'X', 'X']
    o_win = ['O', 'O', 'O']
    winnerx, winnero = False, False
    x_count, o_count, empty = 0, 0, 0
    rows, cols, diag1, diag2 = get_board(cells)
    for row in rows:
        x_count += row.count('X')
        o_count += row.count('O')
        empty += row.count(' ')

    if diag1 == x_win or diag2 == x_win or x_win in rows or x_win in cols:
        winnerx = True
    if diag1 == o_win or diag2 == o_win or o_win in rows or o_win in cols:
        winnero = True

    # if abs(x_count - o_count) >= 2:
    #   print('Impossible')
    # elif winnero and winnerx:
    #   print('Impossible')
    if winnero == False and winnerx == False:
        if empty == 0:
            return 'Draw'
    elif winnero:
        return 'O'
    elif winnerx:
        return 'X'
    else:
        return None


def startup():
    while True:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            return None, None
        elif len(command) < 3:
            print('Bad parameters!')
            continue
        break
    if command[0] == 'start':
        if command[1] == 'user':
            X = User('X')
        elif command[1] == 'easy':
            X = Easy('X')
        elif command[1] == 'medium':
            X = Medium('X')
        elif command[1] == 'hard':
            X = Hard('X')
        if command[2] == 'user':
            O = User('O')
        elif command[2] == 'easy':
            O = Easy('O')
        elif command[2] == 'medium':
            O = Medium('O')
        elif command[2] == 'hard':
            O = Hard('O')
        return X, O


def main(X, O):
    cells = ' ' * 9
    rows, cols, diag1, diag2 = get_board(cells)
    winner = None
    while winner == None:
        print_board(rows)
        cells = X_turn(X, cells)
        winner = check_winner(cells)
        if winner is not None:
            return winner, cells
        rows, cols, diag1, diag2 = get_board(cells)
        print_board(rows)
        cells = O_turn(O, cells)
        winner = check_winner(cells)
        if winner is not None:
            return winner, cells
        rows, cols, diag1, diag2 = get_board(cells)


while True:
    X, O = startup()
    if X == None:
        break
    winner, cells = main(X, O)
    rows, cols, diag1, diag2 = get_board(cells)
    print_board(rows)
    if winner == 'X':
        print('X wins')
    elif winner == 'O':
        print('O wins')
    else:
        print('Draw')