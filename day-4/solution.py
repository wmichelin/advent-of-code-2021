import typing
import dataclasses


@dataclasses.dataclass
class Board:
    _board: typing.Optional[typing.List[typing.List[int]]] = None
    _moves: typing.Optional[typing.List[int]] = None

    def compute_score(self, winning_move: int) -> int:
        return self.get_board_sum_score() * winning_move

    def add_move(self, move: int) -> "Board":
        if not self._moves:
            self._moves = []
        self._moves.append(move)
        return self
    
    def get_board_sum_score(self) -> int:
        sum_ = 0
        for row in self.iterate_rows():
            for val in row:
                if val not in self._moves:
                    sum_ += val
        return sum_


    def get_value(self, item: int) -> str:
        if self._moves and item in self._moves:
            return "X"
        
        return str(item)
    
    def iterate_rows(self):
        for i in range(len(self._board)):
            row = []
            for j in range(len(self._board[0])):
                row.append(self._board[i][j])
            yield row

    def iterate_columns(self):
        for i in range(len(self._board)):
            col = []
            for j in range(len(self._board[0])):
                col.append(self._board[j][i])
            yield col

    def is_winner(self):
        if not self._moves:
            return False

        for row in self.iterate_rows():
            if all([n in self._moves for n in row]):
                return True
        
        for col in self.iterate_columns():
            if all([n in self._moves for n in col]):
                return True
        
        return False


    def __repr__(self) -> str:
        ret = ""
        for i, row in enumerate(self._board):
            for j, item in enumerate(row):
                ret += self.get_value(item) + ", "
            ret += "\n"
        return ret
            

@dataclasses.dataclass
class Game:
    _boards: typing.Optional[typing.List[Board]]
    _move_set: "MoveSet"
    _curr_move_idx: int = 0
    _winners: typing.Optional[typing.List[Board]] = None

    def register_winner(self, board: Board):
        if self._winners is None:
            self._winners = []

        self._winners.append(board)


    def play_move(self):
        move = self._move_set.get_move_by_idx(self._curr_move_idx)
        for _board in self._boards:
            if not _board.is_winner():
                _board.add_move(move)
                if _board.is_winner():
                    self.register_winner(_board)

        self._curr_move_idx += 1
        return self.has_winner()

    def get_last_move(self) -> int:
        return self._move_set.get_move_by_idx(self._curr_move_idx - 1)

    def add_board(self, board: Board) -> "Game":
        if not self._boards:
            self._boards = []
        
        self._boards.append(board)
        return self
        
    def has_winner(self) -> bool:
        return self._winners and len(self._winners) > 0

    def get_winner(self) -> typing.Optional[Board]:
        if not self._winners:
            return None
        return self._winners[0]

    def has_all_winners(self) -> bool:
        if not self._winners:
            return False
        return len(self._winners) == len(self._boards)

    def get_last_winner(self) -> typing.Optional[Board]: 
        for _board in reversed(self._winners):
            return _board
        return None



@dataclasses.dataclass
class MoveSet:
    moves: typing.List[int]

    def get_move_by_idx(self, idx: int) -> int:
        return self.moves[idx]


def input_iter():
    with open('./input.txt') as f:
        for line in f.readlines():
            yield line


def parse_input():
    move_set = None
    boards = []
    curr_board_moves = []

    for idx, line in enumerate(input_iter()):
        if idx == 0:  # move set
            move_set = MoveSet(moves=([int(n) for n in line.split(",")]))
            continue
        if line == "\n":
            if curr_board_moves:
                boards.append(
                    Board(_board=curr_board_moves)
                )
            curr_board_moves = []
        else:
            parsed_line = [int(n) for n in line.strip().split(" ") if n]
            curr_board_moves.append(parsed_line)
    if curr_board_moves:
        boards.append(Board(_board=curr_board_moves))
    
    game = Game(
        _boards=boards,
        _move_set=move_set,
    )

    return game


game = parse_input()

while not game.has_winner():
    game.play_move()

winning_board = game.get_winner()
winning_move = game.get_last_move()

print(f"part 1: {winning_board.compute_score(winning_move)}")

while not game.has_all_winners():
    game.play_move()

winning_board = game.get_last_winner()
winning_move = game.get_last_move()

print(f"part 2: {winning_board.compute_score(winning_move)}")
