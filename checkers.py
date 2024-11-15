# actual board
board = [["-","r","-","r","-","r","-","r"],
         ["r","-","r","-","r","-","r","-"],
         ["-","r","-","r","-","r","-","r"],
         ["-","-","-","-","-","-","-","-"],
         ["-","-","-","-","-","-","-","-"],
         ["b","-","b","-","b","-","b","-"],
         ["-","b","-","b","-","b","-","b"],
         ["b","-","b","-","b","-","b","-"]]

# testing board
# board = [["-","-","-","-","-","-","-","-"],
#          ["-","-","r","-","-","-","-","-"],
#          ["-","b","-","-","-","-","-","-"],
#          ["-","-","-","-","-","-","-","-"],
#          ["-","-","-","-","-","-","-","-"],
#          ["-","-","-","-","-","-","-","-"],
#          ["-","-","-","-","-","-","-","-"],
#          ["-","-","-","-","-","-","-","-"]]

def print_board():
    # print the numbers on top of the board
    print("   0 1 2 3 4 5 6 7")
    # print the numbers on the side of the board and then the actual board spaces after it
    for x in range(8):
        print(
            f"{x}  " +str(board[x])
            .replace("[", "")
            .replace("]", "")
            .replace(",", "")
            .replace("'",""))

def get_moves(home):
    moves = []
    if board[home[0]][home[1]] == "b":
        moves.append([home[0] - 1])
        moves.append([home[1] - 1, home[1] + 1])
    elif board[home[0]][home[1]] == "r":
        moves.append([home[0] + 1])
        moves.append([home[1] - 1, home[1] + 1])
    elif board[home[0]][home[1]].isupper():
        moves.append([home[0] - 1, home[0] + 1])
        moves.append([home[1] - 1, home[1] + 1])

    # remove invalid moves (off of the board)
    new_moves = []
    buffer = []
    for i in range(len(moves)):
        for j in range(len(moves[i])):
            if 8 > moves[i][j] > -1:
                buffer.append(moves[i][j])

    if len(buffer) == 2:
        new_moves.append([buffer[0]])
        new_moves.append([buffer[1]])
    if len(buffer) == 3:
        new_moves.append([buffer[0]])
        new_moves.append([buffer[1], buffer[2]])
    elif len(buffer) == 4:
        new_moves.append([buffer[0], buffer[1]])
        new_moves.append([buffer[2], buffer[3]])
    return new_moves

def move_piece(home, destination, moves, turn):

    # check turn properly
    # if black turn and piece trying to move is not black
    if turn == 0 and board[home[0]][home[1]].lower() != "b":
        return "WRONG_TURN"
    # if red turn and piece trying to move is not red
    elif turn == 1 and board[home[0]][home[1]].lower() != "r":
        return "WRONG_TURN"

    # check if row move inputted is invalid
    invalid = 0
    for i in range(len(moves[0])):
        if destination[1] != moves[0][i]:
            invalid+=1
    if invalid > len(moves[0]):
        return "INVALID_ROW"

    # check if column move inputted is invalid
    invalid = 0
    for i in range(len(moves[1])):
        if destination[1] != moves[1][i]:
            invalid+=1
    if invalid > len(moves[1]):
        return "INVALID_COLUMN"

    # if jumping destination is valid (there is a piece there)
    if board[destination[0]][destination[1]] != "-":

        # if the jumping destination is able to be jumped (not the same color as you)
        if board[home[0]][home[1]] != board[destination[0]][destination[1]]:

            # set the jumped space to nothing
            board[destination[0]][destination[1]] = "-"

            # repeat the previous vertical movement
            new_row = destination[0] - home[0]
            destination[0] += new_row
            # repeat the previous horizontal movement
            if destination[1] > home[1]:  # moving to the right
                destination[1] += 1
            else:  # moving to the left
                destination[1] -= 1
        else:
            return "INVALID_JUMP"



    # set the board
    if destination[0] == 0 or destination[0] == 7:
        if board[home[0]][home[1]].islower():
            board[destination[0]][destination[1]] = board[home[0]][home[1]].upper()
    else:
        board[destination[0]][destination[1]] = board[home[0]][home[1]]
    board[home[0]][home[1]] = "-"
    return True

def check_game_state():
    red_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].lower() == "r":
                red_count += 1
    black_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].lower() == "b":
                black_count += 1

    if red_count == 0:
        return True, "NO_RED"
    elif black_count == 0:
        return True, "NO_BLACK"
    else:
        return False, red_count, black_count


def start_game():
    turn = 0
    can_move = True
    # every time a move is possible
    while can_move:
        # check if game is over
        if check_game_state()[0]:
            break

        # print board
        print_board()

        # print turn
        if turn == 0:
            print("Black's Turn")
        else:
            print("Red's Turn")

        # get inputs and format properly for moving the piece
        inputs = input("Enter piece to move, and it's destination: \nFormat: \"to_move_row to_move_column destination_row destination_column\"\n")
        inputs = inputs.replace(" ", "")
        home = [int(inputs[0]), int(inputs[1])]
        destination = [int(inputs[2]), int(inputs[3])]
        # attempt to move the piece
        can_move = move_piece(home, destination, get_moves(home), turn)

        match can_move:
            case "WRONG_TURN":
                print("Wrong turn! Move your own piece.")
            case "INVALID_ROW":
                print("Invalid Row! Pick a proper row.")
            case "INVALID_COLUMN":
                print("Invalid Column! Pick a proper column.")
            case "INVALID_JUMP":
                print("Piece is not jump-able! (Same color piece?)")
            case _:
                # change turn
                if turn == 0:
                    turn = 1
                else:
                    turn = 0

    # game is over
    print_board()
    match check_game_state()[1]:
        case "NO_RED":
            print("Black Wins!")
        case "NO_BLACK":
            print("Red Wins!")

start_game()