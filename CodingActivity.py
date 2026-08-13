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