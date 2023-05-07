COL_CNT = 7
ROW_CNT = 8


class Board:
    def __init__(self):
        self.state = []
        for _ in range(0, ROW_CNT):
            row = []
            for _ in range(0, COL_CNT):
                row.append(None)
            self.state.append(row)
