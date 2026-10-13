class Puzzle:
    def __init__(self, size=8, invalid=None, pieces=None):
        self.size = size
        self.invalid = list(invalid) if invalid is not None else []
        self.pieces = list(pieces) if pieces is not None else [
            (1, 4), (1, 5),  # strips
            (3, 3), (2, 2),  # squares
            (2, 3), (2, 4), (2, 5), (3, 4)  # rectangles
        ]
        self._count = 0

        self.grid = [[0] * size for _ in range(size)]

        for r, c in self.invalid:
            if not (0 <= r < size and 0 <= c < size):
                raise ValueError(f"Invalid coordinate: {(r, c)}")
            self.grid[r][c] = -1


    def can_place(self, row, col, height, width):
        """Check whether a rectangle fits at (row, col)."""
        if row + height > self.size or col + width > self.size:
            return False

        for i in range(row, row + height):
            for j in range(col, col + width):
                if self.grid[i][j] != 0:
                    return False

        return True

    def place_piece(self, row, col, height, width, piece_id):
        """Place a piece using its unique ID."""
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.grid[i][j] = piece_id

    def remove_piece(self, row, col, height, width):
        """Undo a piece placement."""
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.grid[i][j] = 0


    def solve(self):
        """Solve the puzzle using backtracking"""
        def _solve(index):
            self._count += 1
            if index == len(self.pieces):
                return True
    
            h, w = self.pieces[index]
            piece_id = index + 1

            for curr_h, curr_w in {(h, w), (w, h)}:
                for r in range(self.size - curr_h + 1):
                    for c in range(self.size - curr_w + 1):
    
                        if self.can_place(r, c, curr_h, curr_w):
                            self.place_piece(r, c, curr_h, curr_w, piece_id)
                            if _solve(index + 1):
                                return True 
                            self.remove_piece(r, c, curr_h, curr_w)
            return False

        return _solve(0)

    def solve_bitmask(self):
        """Bitmask solver with Minimum Remaining Values (MRV)."""
        size = self.size
        occupied = sum(1 << (r * size + c) for r, c in self.invalid)
    
        # Precompute placements for each piece
        placements = []
    
        for h, w in self.pieces:
            options = []
    
            for H, W in {(h, w), (w, h)}:
                row_bits = (1 << W) - 1
    
                for r in range(size - H + 1):
                    for c in range(size - W + 1):
                        mask = 0
                        for i in range(H):
                            mask |= row_bits << ((r + i) * size + c)
                        if mask & occupied == 0:
                            options.append((r, c, H, W, mask))
    
            placements.append(options)
    
        self._count = 0
        remaining = set(range(len(self.pieces)))
    
        def _solve(occupied):
            self._count += 1
    
            if not remaining:
                return True
    
            # MRV: choose the piece with the fewest valid placements
            best_piece = None
            best_options = None
    
            for index in remaining:
                valid_options = [
                    option
                    for option in placements[index]
                    if option[4] & occupied == 0
                ]
    
                # No placement available: prune immediately
                if not valid_options:
                    return False
    
                if (best_options is None
                    or len(valid_options) < len(best_options)
                    or (
                        len(valid_options) == len(best_options)
                        and self.pieces[index][0] * self.pieces[index][1]
                        > self.pieces[best_piece][0] * self.pieces[best_piece][1]
                    )
                ):
                    best_piece = index
                    best_options = valid_options
    
            remaining.remove(best_piece)
    
            # Try each valid placement for the selected piece
            for r, c, h, w, mask in best_options:
                self.place_piece(r, c, h, w, best_piece + 1)
    
                if _solve(occupied | mask):
                    return True
    
                self.remove_piece(r, c, h, w)
    
            remaining.add(best_piece)
            return False
    
        return _solve(occupied)

    def __str__(self):
        lines = []
        for row in self.grid:
            row_str = []
            for cell in row:
                row_str.append(f" {cell:2d}")
            lines.append("".join(row_str))
        return "\n".join(lines)