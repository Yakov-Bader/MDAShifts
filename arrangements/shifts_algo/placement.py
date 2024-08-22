import os
import statistics, requests, re
from .shift import Shift
from .volunteer import Volunteer
from typing import List
from bs4 import BeautifulSoup


class Placement:
    def __init__(self) -> None:
        self.volunteer_list: List[Volunteer] = []
        self.shifts_list: List[Shift] = []
        self.ranks = ["driver", "adults", "EMT_tutee", "tutors", "teenager", "tutee"]
        self.table = []

    def create_table_from_link(self, month: str, station_id: int) -> list:
        """
        create a two dimensional table, from the html of the requests page
        Args:
            month (int): wanted month
            station_id (int): station number

        Raises:
            Exception: if there is table not only one table

        Returns:
            list: two dimensional list of the table converted into python
        """
        url = os.getenv("SHIFTS_LINK")
        url+= f"month={month}&station_id={station_id}"
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, "html.parser")
        # with open("dd.html", "r", encoding="utf-8") as file:
        #     html_content = file.read()
        # soup = BeautifulSoup(html_content, "html.parser")
        html_tables = soup.findAll("table")
        if len(html_tables) != 1:
            raise Exception("only one table is allowed")
        html_table = html_tables[0]
        for row in html_table.find_all("tr"):
            cells = [cell.get_text() for cell in row.find_all(["th", "td"])]
            self.table.append(cells)

    def read_data(self) -> None:
        """
        Create shifts from the table, and add to them the users that wanted the shift
        """
        header_row: list = self.table[0]
        # create_shift
        for row in self.table[1:]:
            for i, cell in enumerate(row[1:]):
                shift_full_name = header_row[i + 1]
                date = re.findall(r"\b\d{2}/\d{2}\b", row[0])
                day = date[0][:2]
                modulus = 0
                if "בוקר" in shift_full_name:
                    modulus = 1
                elif "ערב" in shift_full_name:
                    modulus = 2
                shift_date = int(day) * 3 + modulus
                shift_name = shift_full_name
                max_volunteers = 3
                if 'אט"ן' in shift_name:
                    max_volunteers = 2
                new_shift = Shift(shift_date, shift_name, max_volunteers)
                more_of_same: List[Shift] = []
                for v in cell.split("בקשות)"):
                    if v.strip():
                        volunteer: tuple = self._get_name_rank_amount(v.strip() + ")")
                        name = " ".join(volunteer[0].split())
                        rank = " ".join(volunteer[1].split())
                        amount = int(volunteer[2].strip())
                        volunteer: Volunteer = self._get_volunteer_or_create(
                            name, rank, amount
                        )
                        if (
                            rank == "נהג"
                            and "תגבור" not in shift_name
                            and 'אט"ן' not in shift_name
                        ) or (
                            rank == "פאראמדיק"
                            and 'אט"ן' in shift_name
                            and len(more_of_same) < 1
                        ):
                            same_shift = Shift(
                                shift_date, shift_name, max_volunteers, True
                            )
                            same_shift.add_volunteer(volunteer)
                            more_of_same.append(same_shift)
                        else:
                            new_shift.add_wanter(volunteer)

                self.shifts_list.append(new_shift)
                for same_shift in more_of_same:
                    same_shift.add_wanters(new_shift.get_wanters())
                    self.shifts_list.append(same_shift)

    def assign_volunteers_to_shifts(self) -> List[Shift]:
        """
        Here the is a algorithm that assigns volunteers to the shifts they wanted, so that maximum volunteers get maximum shifts,
        in other words that the standard division of the list of amount of shifts will be the smallest.
        Returns:
            List[Shift]: list of the shifts, with the users assigned to them
        """
        for shift in self.shifts_list:
            shift_wanters: List[Volunteer] = shift.get_wanters()
            if len(shift_wanters) <= shift.get_max_volunteers():
                for wanter in shift_wanters:
                    if not wanter.has_close_shift(shift.shift_date):
                        shift.add_volunteer(wanter)

        for shift in self.shifts_list:
            best_volunteers = shift.get_best_unassigned_volunteers()
            shift.add_volunteers(best_volunteers)

        standard_deviation = self._get_standard_deviation()

        standard_deviation_shrunk = True
        while standard_deviation_shrunk:
            print(standard_deviation)
            standard_deviation_shrunk = False
            for shift in self.shifts_list:
                if not shift.is_happy():
                    selfish_volunteer: Volunteer = shift.get_selfish_volunteer()
                    best_volunteer: Volunteer = shift.get_best_unsigned_volunteer()
                    if (
                        best_volunteer
                        and selfish_volunteer.get_assigned_shifts_amount()
                        > best_volunteer.get_assigned_shifts_amount()
                    ):
                        shift.add_volunteer(best_volunteer)
                        shift.remove_volunteer(selfish_volunteer)
                        new_standard = self._get_standard_deviation()
                        if new_standard < standard_deviation:
                            standard_deviation_shrunk = True
                            standard_deviation = new_standard
                        else:
                            shift.add_volunteer(selfish_volunteer)
                            shift.remove_volunteer(best_volunteer)
        return self.shifts_list

    def change_shifts_for_MDA_Modiin(self, shifts: List[Shift]) -> List[Shift]:
        for shift in shifts:
            ranks = [v.rank for v in shift.get_volunteers()]
            if "חניך" in ranks and "חונך" not in ranks:
                ordered_wanters = []
                ordered_volunteers = []
                tutees = []
                tutors = []
        return shifts

    def _get_volunteer_or_create(self, name, rank, amount) -> Volunteer:
        """
        to make sure the same volunteer is not created twice, we return the volunteer if he was already createdS
        Args:
            name (_type_): volunteer name
            rank (_type_): volunteer rank
            amount (_type_): volunteer amount of shifts he signed up to

        Returns:
            Volunteer: the volunteer that fits the name rank and shifts amount
        """
        new_volunteer = Volunteer(name, rank, amount)
        for volunteer in self.volunteer_list:
            if volunteer == new_volunteer:
                return volunteer

        self.volunteer_list.append(new_volunteer)
        return new_volunteer

    def _get_name_rank_amount(self, volunteer_str: str) -> tuple:
        """
        converts volunteer string into volunteer object fields
        Args:
            volunteer_str (str): volunteers string of the table

        Raises:
            Exception: if the is too much numbers in the string

        Returns:
            tuple: of (name, rank, amount of shifts)
        """
        match = re.search(r"\(([^()]*)\)(?!.*\([^()]*\))", volunteer_str)
        if match:
            v_rank_and_v_amount: str = match.group(1)
            v_name: str = volunteer_str[: match.start()] + volunteer_str[match.end() :]
        v_rank, v_amount = v_rank_and_v_amount.split(",")
        v_amount: list = re.findall(r"\d+", v_amount)
        if len(v_amount) > 1:
            raise Exception("v has too much numbers")
        v_amount: str = v_amount[0]
        return (v_name.strip(), v_rank.strip(), v_amount.strip())

    def _get_standard_deviation(self) -> float:
        """
        calculates the standard division of the list of amount of shifts of the volunteers
        Returns:
            float: the standard division
        """
        volunteers_shifts_amount = [
            volunteer.get_assigned_shifts_amount() for volunteer in self.volunteer_list
        ]
        return statistics.stdev(volunteers_shifts_amount)

