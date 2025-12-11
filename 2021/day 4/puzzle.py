
with open("input") as f:
    input = f.read()

parts = input.strip().split("\n\n")
numbers = [int(x) for x in parts[0].split(",")]

def read_board(board):
    lines = [line.strip() for line in board.split("\n") if line.strip()]
    rows = [[int(x.strip()) for x in line.split(" ") if x.strip()] for line in lines]
    columns = [[row[i] for row in rows] for i in range(len(rows[0]))]
    return [rows, columns]

boards = [read_board(board.strip()) for board in parts[1:]]

def winning_index(board):
    rows, columns = board
    min_index = None
    for line in rows + columns:
        line_index = max(numbers.index(n) for n in line)
        if min_index is None or line_index < min_index:
            min_index = line_index
    return min_index

board_indicies = [(board, winning_index(board)) for board in boards]
best_board, best_index = max(board_indicies, key=lambda x: x[1])
best_rows = best_board[0]

called_numbers = numbers[:(best_index + 1)]
unmarked_sum = sum(sum(x for x in row if x not in called_numbers) for row in best_rows)
print(unmarked_sum * called_numbers[-1])

