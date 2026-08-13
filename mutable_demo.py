"""
Demonstration of the Mutable Class Attribute Trap in Python.
"""

class BrokenRobot:
    # BUG: Shared mutable list across all instances
    logs = []

    def add_log(self, entry: str):
        self.logs.append(entry)


class FixedRobot:
    def __init__(self):
        # CORRECT: Instance attribute created per instance in __init__
        self.logs = []

    def add_log(self, entry: str):
        self.logs.append(entry)


if __name__ == "__main__":
    print("=== Demonstrating the Bug (Shared Class Attribute) ===")
    b1 = BrokenRobot()
    b2 = BrokenRobot()
    b1.add_log("Task 1 completed by b1")
    print("b1 logs:", b1.logs)
    print("b2 logs (unexpected leak):", b2.logs)

    print("\n=== Demonstrating the Fix (Isolated Instance Attribute) ===")
    f1 = FixedRobot()
    f2 = FixedRobot()
    f1.add_log("Task 1 completed by f1")
    print("f1 logs:", f1.logs)
    print("f2 logs (properly isolated):", f2.logs)
# Temporary debug comment
