import io

# from typing import Optional
import math

_SAMPLE_INPUT_STR = """
F10
N3
F7
R90
F11
"""


def get_sample_inputs():
    return io.StringIO(_SAMPLE_INPUT_STR)


PRECISION = 5


class ShipState:
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        waypoint_x: int = 1,
        waypoint_y: int = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.waypoint_x = waypoint_x
        self.waypoint_y = waypoint_y

    # @property
    # def waypoint_radius(self) -> float:
        # return math.sqrt(self.waypoint_x ** 2 + self.waypoint_y ** 2)

    # @property
    # def waypoint_degrees(self) -> float:
        # yx_ratio: float
        # if self.waypoint_x == 0.0:
            # if self.waypoint_y == 0.0:
                # raise ValueError('Cannot have waypoint at origin')
            # yx_ratio = self.waypoint_y * float('inf')
        # else:
            # yx_ratio = self.waypoint_y / self.waypoint_x
        # atan_result = math.degrees(math.atan(yx_ratio))
        # # Quadrant 2
        # if atan_result > 0 and self.x < 0:
            # return atan_result + 180.0
        # # Quadrant 3
        # if atan_result < 0 and self.x < 0:
            # return 180.0 + atan_result
        # return atan_result

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) Waypoint: ({self.waypoint_x}, {self.waypoint_y})"

    def turn(self, degrees_in: int) -> None:
        degrees = degrees_in % 360
        if degrees == 90:
            old_x = self.waypoint_x
            self.waypoint_x = -self.waypoint_y
            self.waypoint_y = old_x
        elif degrees == 180:
            self.waypoint_x = -self.waypoint_x
            self.waypoint_y = -self.waypoint_y
        elif degrees == 270:
            old_x = self.waypoint_x
            self.waypoint_x = self.waypoint_y
            self.waypoint_y = -old_x
        elif degrees != 0:
            raise ValueError('Only multiples of 90 allowed as turns')
        # radius = self.waypoint_radius
        # new_degrees = self.waypoint_degrees + degrees

    def forward(self, distance: int) -> None:
        self.x += distance * self.waypoint_x
        self.y += distance * self.waypoint_y

    def move_y(self, distance: int) -> None:
        self.y += distance

    def move_x(self, distance: int) -> None:
        self.x += distance

    def process_instruction(self, instruction: str) -> None:
        if len(instruction) <= 1:
            raise ValueError("Instruction must be 2 or more characters")
        action = instruction[0].upper()
        value = int(instruction[1:])
        if action == "N":
            self.move_y(value)
        elif action == "S":
            self.move_y(-value)
        elif action == "E":
            self.move_x(value)
        elif action == "W":
            self.move_x(-value)
        elif action == "L":
            self.turn(value)
        elif action == "R":
            self.turn(-value)
        elif action == "F":
            self.forward(value)
        else:
            raise ValueError(f"Unknown action {action}")
        # print(f'instruction: {instruction}; {self}')

    def manhattan_distance(self) -> float:
        return math.fabs(self.x) + math.fabs(self.y)


class ShipStatePart2(ShipState):

    def move_x(self, distance: int) -> None:
        self.waypoint_x += distance

    def move_y(self, distance: int) -> None:
        self.waypoint_y += distance


def process_mahhattan_distance(inputs: io.TextIOBase, ship_state: ShipState) -> int:
    stripped_lines = (line.strip() for line in inputs)
    instructions = (instruction for instruction in stripped_lines if instruction)
    for instruction in instructions:
        ship_state.process_instruction(instruction)
    return ship_state.manhattan_distance()


def solve_part1(inputs: io.TextIOBase) -> int:
    ship_state = ShipState()
    return process_mahhattan_distance(inputs, ship_state)


def solve_part2(inputs: io.TextIOBase) -> int:
    ship_state = ShipStatePart2(
        waypoint_x=10,
        waypoint_y=1,
    )
    return process_mahhattan_distance(inputs, ship_state)


def main():
    print(f"Manhattan distance: {solve_part1(get_sample_inputs())}")
    with open("./inputs.txt") as f:
        print(f"Manhattan distance: {solve_part1(f)}")
    print(f"Manhattan distance: {solve_part2(get_sample_inputs())}")
    with open("./inputs.txt") as f:
        print(f"Manhattan distance: {solve_part2(f)}")


if __name__ == "__main__":
    main()
