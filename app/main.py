class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        # Cada barco será una lista de coordenadas [ (r, c), (r, c)... ]
        self.ships_data = []
        self.field = {}  # Mapeo (r, c) -> índice del barco en self.ships_data
        self.hits = set()
        self.sunk_ships = []

        for start, end in ships:
            ship_coords = self._generate_ship_coords(start, end)
            ship_index = len(self.ships_data)
            self.ships_data.append({"coords": ship_coords, "hits": 0})
            for coord in ship_coords:
                self.field[coord] = ship_index

        # Opcional: self._validate_field()

    def _generate_ship_coords(self, start: tuple[int, int], 
                               end: tuple[int, int]) -> list[tuple[int, int]]:
        coords = []
        r1, c1 = start
        r2, c2 = end
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for c in range(min(c1, c2), max(c1, c2) + 1):
                coords.append((r, c))
        return coords

    def fire(self, cell: tuple[int, int]) -> str:
        if cell not in self.field:
            return "Miss!"

        if cell in self.hits:
            return "Already hit!"  # Manejo de disparos repetidos

        self.hits.add(cell)
        ship_idx = self.field[cell]
        ship = self.ships_data[ship_idx]
        ship["hits"] += 1

        if ship["hits"] == len(ship["coords"]):
            self.sunk_ships.append(ship_idx)
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for r in range(10):
            row_str = ""
            for c in range(10):
                coord = (r, c)
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
        # 1. Validar cantidad total (10 barcos)
        if len(self.ships_data) != 10:
            raise ValueError("Must have exactly 10 ships")

        # 2. Validar tamaños (4x1, 3x2, 2x3, 1x4)
        lengths = [len(s["coords"]) for s in self.ships_data]
        counts = {i: lengths.count(i) for i in range(1, 5)}
        if counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid ship sizes distribution")

        # 3. Validar vecinos (incluyendo diagonales)
        for r, c in self.field:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    neighbor = (r + dr, c + dc)
                    if neighbor in self.field:
                        # Si el vecino pertenece a un barco diferente, error
                        if self.field[neighbor] != self.field[(r, c)]:
                            raise ValueError("Ships are too close!")
