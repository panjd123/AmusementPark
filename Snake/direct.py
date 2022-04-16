class Direct:
    def __init__(self) -> None:
        self.direct_col = [0, 0, -1, 1]
        self.direct_row = [-1, 1, 0, 0]
        self.direct_id_dict = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
