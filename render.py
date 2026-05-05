from graph import Graph
from connection import Connection
from zone import Zone
from drone import Drone
from typing import List


class Render:
    def __init__(self,
                 zones: List[Zone],
                 connections: List[Connection]):
        self.zones = zones
        self.connections = connections
