import time  # Import the time module for delaying AI moves

# Constants for player symbols
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
# Define the Tic Tac Toe board size
BOARD_SIZE = 3


# Function to print the game board
def print_board(board):
    print("---------------------")
    print("|                   |")
    for i in range(len(board)):
        print("|     ", end="")
        for j in range(len(board[0])):
            if j < len(board[0]) - 1:
                print(board[i][j], end=" | ")
            else:
                print(board[i][j], end="")
                print("     |")
        if i != len(board) - 1:
            print("|     ", end = "")
            print(".........", end="")
            print("     |")
    print("|                   |")
    print("---------------------")


# Function to check if the game is over
def is_game_over(board):
    # Check rows, columns, and diagonals for a win
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return True
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True

    # Check for a draw
    for row in board:
        if EMPTY in row:
            return False
    return True


# Function to check if a player has won
def is_winner(board, player):
    # Check rows and columns for a win
    for i in range(BOARD_SIZE):
        row_win = True
        col_win = True
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                row_win = False
            if board[j][i] != player:
                col_win = False
        if row_win or col_win:
            return True

    # Check for a win in the main diagonal
    main_diagonal_win = True
    for i in range(BOARD_SIZE):
        if board[i][i] != player:
            main_diagonal_win = False
            break

    # Check for a win in the secondary diagonal
    secondary_diagonal_win = True
    for i in range(BOARD_SIZE):
        if board[i][BOARD_SIZE - i - 1] != player:
            secondary_diagonal_win = False
            break

    if main_diagonal_win or secondary_diagonal_win:
        return True

    return False


# Function to evaluate the board for the AI player
def evaluate_board(board, player):
    if player == PLAYER_X:
        opponent = PLAYER_O
    else:
        opponent = PLAYER_X

    if is_winner(board, player):
        return 1
    if is_winner(board, opponent):
        return -1
    return 0


# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player, player):
    if is_game_over(board) or depth == 0:
        return evaluate_board(board, player)

    if maximizing_player:
        max_eval = -float("inf")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = player
                    eval = minimax(board, depth - 1, alpha, beta, False, player)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = get_opponent(player)
                    eval = minimax(board, depth - 1, alpha, beta, True, player)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


# Function to get the opponent's symbol
def get_opponent(player):
    if player == PLAYER_X:
        opponent = PLAYER_O
    else:
        opponent = PLAYER_X
    return opponent


# Function to make the AI's move in Human vs AI and AI vs. AI move
def make_ai_move(board, player, depth, ai):
    best_move = None
    best_eval = -float("inf")
    alpha = -float("inf")
    beta = float("inf")

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                board[i][j] = player
                eval = minimax(board, depth, alpha, beta, False, player)
                board[i][j] = EMPTY
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = player
    if ai:
        time.sleep(1)  # Delay for a second to visualize


# Main game loop
flag = False
choice = ''
while True:
    if flag == False:
        print('\n\n')
        print("------------xxxxxxx------------")
        print("|    Tic Tac Toe (AI) Game    |")
        print("------------xxxxxxx------------")
        print("")
        print("-------------------------")
        print("|    Select Method:     |")
        print("|    1. Human vs. AI    |")
        print("|    2. AI vs. AI       |")
        print("|    0 To Exit          |")
        print("-------------------------")
        print("")
        choice = input("Choose game mode (1 or 2) or Exit (0): ")
        if choice == '0':
            print('Thank You! See You Soon!')
            break
    flag = False
    board = []
    for _ in range(BOARD_SIZE):
        row = []
        for _ in range(BOARD_SIZE):
            row.append(EMPTY)
        board.append(row)

    
    current_player = PLAYER_X
    depth = 3

    if choice == '1':
        print("\nTic Tac Toe - Human vs. AI")
        symbol = input("\nChoose Your Symbol: Press 'X' for X or Press 'O' for O: ")
        if symbol == 'O':
            current_player = PLAYER_O
        elif symbol != 'X':
            print("Invaild Symbol! Please Enter the right Symbol!")
            while True:
                symbol = input("Choose Your Symbol: Press 'X' for X or Press 'O' for O: ")
                if symbol == 'O':
                    current_player = PLAYER_O
                elif symbol == 'X':
                    break

        print_board(board)

        while not is_game_over(board):
            if current_player == symbol:
                row, col = map(int, input("\n\nEnter your move (row and column): ").split())
                if row < 0 or row > 2 or col < 0 or col > 2:
                    while True:
                        print("\n Invaild Row or Column Value!")
                        row, col = map(int, input("\nEnter your move (row and column): ").split())
                        if row >= 0 and row <= 2 and col >= 0 and col <= 2:
                            break
                if board[row][col] == EMPTY:
                    board[row][col] = current_player
                else:
                    print("Invalid move (Cell Already Occupied). Try again.")
                    continue
            else:
                print("\nOpponants Move:")
                make_ai_move(board, current_player, depth,ai=False)

            print_board(board)
            current_player = get_opponent(current_player)

        result = evaluate_board(board, PLAYER_X)
        if result == 1:
            print("\n-----YOU Win! CONGRATULATIONS...-----")
        elif result == -1:
            print("\n-----AI wins!-----")
        else:
            print("It's a draw!")
        print("\n\n-----------------------")
        print("|   1. Restart        |")
        print("|   2. Change Mode    |")
        print("|   0 To Exit         |")
        print("-----------------------")
        choice2 = input("\nChoose Restart ('1') or Change Mode ('2') or Exit ('0'): ")
        if choice2 == '0':
            print('Thank You! See You Soon!')
            break
        elif choice2 == '1':
            flag = True

    elif choice == '2':
        print("\nTic Tac Toe - AI vs. AI")
        print_board(board)
        count=1
        while not is_game_over(board):
            if(count%2==0):
                print("\nPlayer O's Move:")
            else:
                print("\nPlayer X's Move:")
            make_ai_move(board, current_player, depth,ai=True)
            print_board(board)
            count=count+1
            current_player = get_opponent(current_player)

        result = evaluate_board(board, current_player)
        if result == -1:
            print("Player X (AI) wins!")
        elif result == 1:
            print("Player O (AI) wins!")
        else:
            print("It's a draw!")
        print("\n\n-----------------------")
        print("|   1. Restart        |")
        print("|   2. Change Mode    |")
        print("|   0 To Exit         |")
        print("-----------------------")
        choice2 = input("\nChoose Restart ('1') or Change Mode ('2') or Exit ('0'): ")
        if choice2 == '0':
            print('Thank You! See You Soon!')
            break
        elif choice2 == '1':
            flag = True
    else:
        print("Invalid choice. Please select '1' for Human vs. AI or '2' for AI vs. AI or '0' for Exit.")
