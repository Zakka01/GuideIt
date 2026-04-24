from zone import Zone


class Connection:

    def __init__(self, from_dst: Zone, to_dst: Zone, capacity: int):
        self.connection_name = from_dst.name + "-" + to_dst.name
        self.from_dst = from_dst
        self.to_dst = to_dst
        self.capacity = capacity
