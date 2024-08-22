class Volunteer:
    def __init__(self, name: str, rank: str, amount: str):
        self.name = name
        self.rank = rank
        self.amount = amount
        self.assigned_shifts = []
        self.wanted_shifts_amount = 0

    def __eq__(self, volunteer) -> bool:
        return (
            self.amount == volunteer.amount
            and self.rank == volunteer.rank
            and self.name == volunteer.name
        )

    def __hash__(self):
        return hash(f"{self.amount}{self.rank}{self.name}")

    def assign_shift(self, shift) -> None:
        self.assigned_shifts.append(shift)

    def remove_assigned_shift(self, shift) -> None:
        self.assigned_shifts.remove(shift)

    def get_assigned_shifts_amount(self) -> int:
        return len(self.assigned_shifts)

    def add_wanted_amount(self) -> None:
        self.wanted_shifts_amount += 1

    def get_wanted_amount(self) -> int:
        return self.wanted_shifts_amount

    def has_close_shift(self, shift_date: int) -> bool:
        """check if the volunteer has a signed shift too close to the shift

        Args:
            shift_date (int): shift date number

        Returns:
            bool: true if there is a close shift, and false if not
        """
        for shift in self.assigned_shifts:
            if shift.shift_date in [shift_date - 1, shift_date, shift_date + 1]:
                return True
        return False
