directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class SliderPuzzle:

    def solve(self):
        return


class SearchNode:
    board: list
    free: tuple

    step: 0

    def get_distance(self):
        distance = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != i * len(self.board[i]) + j + 1:
                    distance += abs(i - (self.board[i][j] - 1) // len(self.board[i])) + abs(
                        j - (self.board[i][j] - 1) % len(self.board[i]))
        return distance + self.step


