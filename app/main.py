class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships_data = []
        self.field = {}
        self.hits = set()
        self.sunk_ships = []

        for start, end in ships:
            ship_coords = self._generate_ship_coords(start, end)
            ship_index = len(self.ships_data)
            self.ships_data.append({"coords": ship_coords, "hits": 0})
            for coord in ship_coords:
                self.field[coord] = ship_index

    def _generate_ship_coords(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        coords = []
        row_start, col_start = start
        row_end, col_end = end
        for row in range(min(row_start, row_end), max(row_start, row_end) + 1):
            for col in range(
                min(col_start, col_end),
                max(col_start, col_end) + 1
            ):
                coords.append((row, col))
        return coords

    def fire(self, cell: tuple[int, int]) -> str:
        if cell not in self.field:
            return "Miss!"

        if cell in self.hits:
            return "Already hit!"

        self.hits.add(cell)
        ship_idx = self.field[cell]
        ship = self.ships_data[ship_idx]
        ship["hits"] += 1

        if ship["hits"] == len(ship["coords"]):
            self.sunk_ships.append(ship_idx)
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for col in range(10):
                coord = (row, col)
                if coord not in self.field:
                    row_str += "~ "
                elif coord in self.hits:
                    ship_idx = self.field[coord]
                    if ship_idx in self.sunk_ships:
                        row_str += "x "
                    else:
                        row_str += "* "
                else:
                    row_str += "□ "
            print(row_str.strip())

    def _validate_field(self) -> None:
        if len(self.ships_data) != 10:
            raise ValueError("Must have exactly 10 ships")

        lengths = [len(s["coords"]) for s in self.ships_data]
        counts = {i: lengths.count(i) for i in range(1, 5)}
        if counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid ship sizes distribution")

        for row, col in self.field:
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    if d_row == 0 and d_col == 0:
                        continue
                    neighbor = (row + d_row, col + d_col)
                    if neighbor in self.field:
                        if self.field[neighbor] != self.field[(row, col)]:
                            raise ValueError("Ships are too close!")
