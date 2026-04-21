class Hub:
    def __init__(self, config) -> None:
        self.name = config["name"]
        self.y = config["y"]
        self.x = config["x"]
        self.zone_type = config["zone"]
        self.color = config["color"]
        self.max_drones = config["max_drones"]

    def is_zone_blocked(self):
        return self.zone_type == "blocked"

    def is_zone_resticted(self):
        return self.zone_type == "restricted"

    def is_zone_normal(self):
        return self.zone_type == "normal"

    def is_zone_priority(self):
        return self.zone_type == "priority"
