from typing import List
from .volunteer import Volunteer


class Shift:
    def __init__(
        self,
        date: str,
        name: str,
        max_volunteers: int = 3,
        gets_driver: bool = False,
    ):
        self.shift_date = date
        self.shift_name = name
        self.volunteers = []
        self.wanters = []
        self.max_volunteers = max_volunteers
        self.gets_driver = gets_driver

    def __eq__(self, shift) -> bool:
        return (
            shift.shift_date == self.shift_date and shift.shift_name == self.shift_name
        )

    def add_volunteer(self, volunteer: Volunteer) -> None:
        if not volunteer.has_close_shift(self.shift_date):
            volunteer.assign_shift(self)
            self.volunteers.append(volunteer)

    def add_volunteers(self, volunteers: List[Volunteer]) -> None:
        for volunteer in volunteers:
            self.add_volunteer(volunteer)

    def remove_volunteer(self, volunteer: Volunteer) -> None:
        volunteer.remove_assigned_shift(self)
        self.volunteers.remove(volunteer)

    def add_wanter(self, volunteer: Volunteer) -> None:
        volunteer.add_wanted_amount()
        self.wanters.append(volunteer)

    def add_wanters(self, volunteers: Volunteer) -> None:
        for v in volunteers:
            self.add_wanter(v)

    def is_happy(self) -> bool:
        return len(self.volunteers) >= len(self.wanters)

    def get_selfish_volunteer(self) -> Volunteer:
        """
        get the assigned volunteer that has the most shifts
        Returns:
            Volunteer: the volunteer that has the most shifts
        """
        filtered_volunteers: List[Volunteer] = list(
            filter(
                lambda v: v.rank != "נהג" and v.rank != "פאראמדיק", self.volunteers
            )
        )
        ordered_volunteers: List[Volunteer] = sorted(
            filtered_volunteers, key=lambda v: v.get_assigned_shifts_amount(), reverse=True
        )
        if not ordered_volunteers:
            return None
        return ordered_volunteers[0]

    def get_ordered_unsigned_volunteers(self) -> List[Volunteer]:
        """list of unsigned volunteers orders by amount of of shifts

        Returns:
            List[Volunteer]: the ordered list of unsigned volunteers
        """
        unassigned_volunteers: List[Volunteer] = [
            v
            for v in self.wanters
            if (v not in self.volunteers) and (not v.has_close_shift(self.shift_date))
        ]
        unassigned_volunteers = list(set(unassigned_volunteers))
        ordered_wanters = sorted(
            unassigned_volunteers, key=lambda v: v.get_assigned_shifts_amount()
        )
        return ordered_wanters

    def get_best_unsigned_volunteer(self) -> Volunteer:
        """
        finds the unsigned volunteer, with the least amount of shifts
        Returns:
            Volunteer: unsigned volunteer, with the least amount of shifts
        """
        best_unassigned = self.get_ordered_unsigned_volunteers()
        return best_unassigned[0] if best_unassigned else None

    def get_best_unassigned_volunteers(self) -> List[Volunteer]:
        """
        finds the max_volunteers unsigned volunteers, with the least amounts of shifts
        Returns:
            List[Volunteer]: the list of volunteers that have the least amount of shifts
        """
        ordered_wanters = self.get_ordered_unsigned_volunteers()
        max_allowed = self.get_max_volunteers()

        if len(ordered_wanters) >= max_allowed:
            deserved_wanters = ordered_wanters[:max_allowed]
        else:
            deserved_wanters = ordered_wanters[: len(ordered_wanters)]
        return deserved_wanters

    def get_volunteers(self) -> List[Volunteer]:
        return self.volunteers

    def get_wanters(self) -> List[Volunteer]:
        return self.wanters

    def get_max_volunteers(self) -> int:
        return self.max_volunteers
