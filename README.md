in the logic of the maza generating we'll have to define a "cell" calss
this class uses one value to decide if a wall is open out of the 4 walls,
        self.north: bool = bool(value & 1)
        self.east: bool = bool(value & 2)
        self.south: bool = bool(value & 4)
        self.west: bool = bool(value & 8)
it uses the bitmasking to store multiple boolian values in one int,
1 in binary is 0001 (checks the 1st bit for the North wall)
2 in binary is 0010 (checks the 2nd bit for the East wall)
4 in binary is 0100 (checks the 3rd bit for the South wall)
8 in binary is 1000 (checks the 4th bit for the West wall)