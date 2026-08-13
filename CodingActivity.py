import abc
import functools
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class InsufficientBatteryError(Exception):
    """Raised when a robot does not have enough battery to perform a task."""
    def __init__(self, robot_name: str, required: int, available: int):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        message = f"{robot_name} needs {required}% battery for this task but only has {available}%."
        super().__init__(message)


class Robot(abc.ABC):
    manufacturer = "Cyberdyne Systems"
    population = 0

    def __init__(self, name: str, battery: int = 100):
        self.name = name
        self.battery = battery  # Triggers property setter clamping
        Robot.population += 1

    @property
    def battery(self) -> int:
        return self._battery

    @battery.setter
    def battery(self, value: int):
        if value < 0:
            self._battery = 0
        elif value > 100:
            self._battery = 100
        else:
            self._battery = value

    def use_battery(self, amount: int):
        if self.battery < amount:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    def __str__(self) -> str:
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery})"

    @classmethod
    def from_config(cls, config: dict):
        return cls(**config)

    @abc.abstractmethod
    def perform_task(self, **kwargs):
        """Abstract method to be implemented by all concrete subclasses."""
        pass

        def log_action(func):
    """Decorator that logs method execution details while preserving metadata."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"Starting {func.__name__} on {self.name}")
        result = func(self, *args, **kwargs)
        logging.info(f"Finished {func.__name__} on {self.name}")
        return result
    return wrapper


class CleaningRobot(Robot):
    def __init__(self, name: str, battery: int = 100, dust_capacity: int = 500):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    @log_action
    def perform_task(self, area_sqft: int = 100):
        battery_cost = 20
        self.use_battery(battery_cost)
        return f"{self.name} cleaned {area_sqft} sq ft of space."


def fleet_report(robots: list):
    """Prints a status line for each robot using dynamic polymorphism."""
    for robot in robots:
        print(str(robot))

        class DroneRobot(Robot):
    def __init__(self, name: str, battery: int = 100, max_altitude: int = 120):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self, altitude: int = 50):
        battery_cost = 35
        if altitude > self.max_altitude:
            return f"{self.name} cannot fly above maximum altitude of {self.max_altitude}m."
        self.use_battery(battery_cost)
        return f"{self.name} surveyed terrain at {altitude}m altitude."

        def run_task_safely(robot: Robot, **kwargs):
    """Executes a task inside a complete try/except/else/finally block."""
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as error:
        logging.error(error)
    else:
        print(f"Task Output: {result}")
    finally:
        print(f"Status Check: {robot.name} current battery level is {robot.battery}%\n")


if __name__ == "__main__":
    roomba = CleaningRobot("Roomba-v1", battery=100, dust_capacity=300)
    drone = DroneRobot.from_config({"name": "Aqua-Drone", "battery": 15})

    print("--- Fleet Report ---")
    fleet_report([roomba, drone])
    print(f"Total Robots Created: {Robot.population}\n")

    print("--- Safe Task Executions ---")
    run_task_safely(roomba, area_sqft=250)
    run_task_safely(drone, altitude=40)

    print("--- Decorator Metadata Check ---")
    print(f"Wrapped method name: {CleaningRobot.perform_task.__name__}")