"""Interactive grading tool"""
from __future__ import annotations
import os
import shutil
import curses
import traceback
import argparse

from copy import deepcopy

from .commands import parse_grading_schema, collect_test_scripts, TMP_TESTS_DIR
from .model import GradingSchema
from ..test_runner import run_tests_for, load_tests, GraderTestResult

QUIT_KEY = 'q'
ESCAPE_KEY = 27

GREEN_COLOR = None


def run_tests_interactive_argument_parser(argument_parser: argparse.ArgumentParser) -> None:
    """Add necessary arguments for interactive grading"""
    argument_parser.add_argument('-gs', '--grading-scheme', required=False)


def get_students_folders() -> list[str]:
    """Return a list of student folders from current directory"""
    return [path for path in os.listdir() if os.path.isdir(path) and
            os.path.exists(os.path.join(path, '.submission.yaml'))]


class Panel:

    def __init__(self, window, storage: Model):
        self.window = window
        self.storage = storage
        self.focused = False
        self.rows, self.cols = self.window.getmaxyx()


def is_enter(c: int) -> bool:
    """Check if enter was entered"""
    return c == curses.KEY_ENTER or c == 10 or c == 13


class StudentSidebar(Panel):

    NAME = "student_sidebar"

    def __init__(self, screen, storage):
        super().__init__(screen, storage)

        self.position = 0

        self.width = len(max(self.storage.students_folders, key=len)) + 2
        self.width = max(self.width, len(max(self.storage.problems, key=len)) + 15)

    def draw(self):

        self.window.addstr(0, 1, "STUDENTS:", curses.A_UNDERLINE)

        self.window.vline(0, self.width, curses.ACS_VLINE, 1)
        self.window.vline(1, self.width, curses.ACS_SSSB, 1)
        self.window.vline(2, self.width, curses.ACS_VLINE, self.rows - SummaryPanel.HEIGHT - 2)

        for i, student in enumerate(self.storage.students_folders):
            if i == self.position and self.focused:
                mode = curses.A_REVERSE
            elif i == self.position and not self.focused:
                mode = GREEN_COLOR | curses.A_ITALIC
            else:
                mode = curses.A_NORMAL
            self.window.addstr(i + 1, 1, student, mode)

    def control(self, c):
        if c == curses.KEY_UP and self.position > 0:
            self.position -= 1
        elif c == curses.KEY_DOWN and self.position < len(self.storage.students_folders) - 1:
            self.position += 1
        elif is_enter(c):
            self.storage.set_current_panel(ProblemsTabs.NAME)

        self.storage.current_student = self.storage.students_folders[self.position]


class ProblemsTabs(Panel):
    NAME = 'problem_tabs'

    def __init__(self, window, storage):
        super().__init__(window, storage)

        self.position = 0

        self.problems = [rule.filename for rule in storage.grading_schema.rules]

    def draw(self):

        padding = self.storage.panels[StudentSidebar.NAME].width

        self.window.addstr(0, padding + 2, "FILES:", curses.A_UNDERLINE)
        self.window.hline(1, padding, curses.ACS_HLINE, self.cols - 3)

        padding += 7

        for i, student in enumerate(self.problems):
            if i == self.position and self.focused:
                mode = curses.A_REVERSE
            elif i == self.position and not self.focused:
                mode = GREEN_COLOR | curses.A_ITALIC
            else:
                mode = curses.A_NORMAL

            self.window.addstr(0, padding + 2, student, mode)
            padding += len(student) + 1

    def control(self, c):
        match c:
            case curses.KEY_LEFT if self.position > 0:
                self.position -= 1
            case curses.KEY_RIGHT if self.position < len(self.problems) - 1:
                self.position += 1
            case curses.KEY_ENTER | 10 | 13:
                self.storage.run_test_for_selected_problem()
                self.storage.set_current_panel(TestsResultPanel.NAME)
                self.storage.panels[TestsResultPanel.NAME].reset_cursor()

        self.storage.current_problem_file = self.problems[self.position]


class TestsResultPanel(Panel):
    NAME = 'tests_result_panel'
    TOP_MARGIN = 2

    def __init__(self, window, storage):
        super().__init__(window, storage)

        self.start_y = 0
        self.start_x = 0
        self.margin = 0

        self.visible_vertical_range = self.rows - 3
        self.visible_horizontal_range = 0

        self.x, self.y = 0, 0

        self.lines = None

    def draw(self):

        self.margin = self.storage.panels[StudentSidebar.NAME].width + 2
        self.visible_horizontal_range = self.cols - self.margin

        self.lines = self.storage.get_current_test_output().split('\n')

        for i, line in enumerate(self.lines[self.start_y: self.start_y + self.visible_vertical_range]):
            self.window.addstr(2 + i, self.margin, line[self.start_x:self.start_x + self.visible_horizontal_range])

        if self.focused:
            curses.curs_set(1)
            self.window.move(self.TOP_MARGIN + self.y, self.margin + self.x)
        else:
            curses.curs_set(0)

    def control(self, c):

        length_of_current_line = len(self.lines[self.start_y + self.y])
        max_horizontal_scroll = max(0, length_of_current_line - self.visible_horizontal_range)
        maximum_x = min(self.visible_horizontal_range - 1, length_of_current_line)
        maximum_y = min(len(self.lines), self.visible_vertical_range)

        match c:
            case curses.KEY_UP if self.y > 0:
                self.y -= 1
            case curses.KEY_DOWN if self.y < maximum_y - 1:
                self.y += 1
            case curses.KEY_RIGHT if self.x < maximum_x:
                self.x += 1
            case curses.KEY_LEFT if self.x > 0:
                self.x -= 1
            case curses.KEY_DOWN if self.y == maximum_y - 1:
                self.start_y = min(self.start_y + 1, len(self.lines) - maximum_y - 1)
            case curses.KEY_UP if self.y == 0:
                self.start_y = max(self.start_y - 1, 0)
            case curses.KEY_RIGHT if self.x == maximum_x:
                self.start_x = min(self.start_x + 1, max_horizontal_scroll)
            case curses.KEY_LEFT if self.x == 0:
                self.start_x = max(self.start_x - 1, 0)
            case 36:  # $
                self.start_x = max(0, length_of_current_line - self.visible_horizontal_range)
                self.x = maximum_x
            case 94:  # ^
                self.x = 0
                self.start_x = 0
            case 71:  # G
                self.start_y = max(0, len(self.lines) - maximum_y)
                self.y = maximum_y - 1
            case 103:  # g
                self.start_y = 0
                self.y = 0
            case 114:  # r
                self.storage.run_test_for_selected_problem()

    def reset_cursor(self):
        self.x, self.y = 0, 0


class SummaryPanel(Panel):

    NAME = 'summary_panel'
    HEIGHT = 15

    def __init__(self, window, storage):
        super().__init__(window, storage)

    def draw(self):

        width = self.storage.panels[StudentSidebar.NAME].width
        start_y = self.rows - self.HEIGHT

        self.window.hline(start_y, 0, curses.ACS_HLINE, width)
        self.window.addch(start_y, width, curses.ACS_SBSS)
        self.window.vline(start_y + 1, width, curses.ACS_VLINE, self.HEIGHT)

        self.window.addstr(start_y + 1, 1, "SUMMARY:", curses.A_UNDERLINE)

        total_grade = 0

        for i, rule in enumerate(self.storage.grading_schema.rules):
            test_result = self.storage.test_runner_result[self.storage.current_student].get(rule.filename)

            if test_result is not None:
                max_grade = self.storage.grading_schema.total_grade * rule.weight / 100
                gained_grade = round(test_result.gained_points / test_result.total_points * max_grade, 2)
            else:
                max_grade, gained_grade = 0, 0

            total_grade += gained_grade

            result_string = "No Data" if test_result is None else f"{gained_grade}/{max_grade}"

            self.window.addstr(start_y + i + 2, 1, f" - {rule.filename}: {result_string}")

        self.window.addstr(start_y + len(self.storage.grading_schema.rules) + 2, 2,
                           f"> Total Grade: {total_grade}/{self.storage.grading_schema.total_grade}")

class Model:
    """Class for storing global data of app"""

    def __init__(self, grading_schema: GradingSchema):
        self.current_panel = None
        self.panels = {}

        self.grading_schema = grading_schema

        self.students_folders = get_students_folders()
        self.problems = [rule.filename for rule in self.grading_schema.rules]

        self.current_student = self.students_folders[0]
        self.current_problem_file = grading_schema.rules[0].filename

        self.test_runner_result = {student: {} for student in self.students_folders}
        self.test_cases = {}

        self.load_test_cases()

    def load_test_cases(self) -> None:
        """Load test cases from specified locations in grading schema and write them to self.test_cases"""
        collected_test_scripts = collect_test_scripts(self.grading_schema)

        for rule, copied_path in collected_test_scripts.items():
            self.test_cases[rule] = load_tests(copied_path)

        shutil.rmtree(TMP_TESTS_DIR)

    def add_panel(self, name: str, panel) -> None:
        """Add panel to panel registry"""
        self.panels[name] = panel

    def set_current_panel(self, name: str) -> None:
        """Set current panel"""
        if self.current_panel is not None:
            self.current_panel.focused = False

        self.current_panel = self.panels.get(name)
        self.current_panel.focused = True

    def get_current_test_output(self) -> str:
        if self.current_problem_file not in self.test_runner_result[self.current_student]:
            return ""

        return self.test_runner_result[self.current_student][self.current_problem_file].output

    def get_current_test_result(self) -> GraderTestResult | None:
        if self.current_problem_file not in self.test_runner_result[self.current_student]:
            return None

        return self.test_runner_result[self.current_student][self.current_problem_file]

    def run_test_for_selected_problem(self) -> None:
        script_path = os.path.join(self.current_student, self.current_problem_file)

        grading_rule = next(filter(lambda r: r.filename == self.current_problem_file, self.grading_schema.rules))

        result = run_tests_for(script_path=script_path, suite=deepcopy(self.test_cases[grading_rule]))

        self.test_runner_result[self.current_student][self.current_problem_file] = result


def create_color_pairs() -> None:
    """Init color pairs"""
    global GREEN_COLOR
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    GREEN_COLOR = curses.color_pair(1)


def wrapper(screen, args: argparse.Namespace) -> None:

    create_color_pairs()
    storage = Model(parse_grading_schema(args.grading_schema))

    sidebar = StudentSidebar(screen, storage)
    problem_tabs = ProblemsTabs(screen, storage)
    summary_panel = SummaryPanel(screen, storage)
    test_result_panel = TestsResultPanel(screen, storage)

    # Must be in such order to maintain proper drawing
    storage.add_panel(ProblemsTabs.NAME, problem_tabs)
    storage.add_panel(SummaryPanel.NAME, summary_panel)
    storage.add_panel(StudentSidebar.NAME, sidebar)
    storage.add_panel(TestsResultPanel.NAME, test_result_panel)

    storage.set_current_panel(StudentSidebar.NAME)

    sidebar.draw()
    problem_tabs.draw()
    summary_panel.draw()

    while True:
        screen.erase()

        for panel in storage.panels.values():
            panel.draw()

        c = screen.getch()

        match c:
            case 113:
                break
            case 97:
                storage.set_current_panel(StudentSidebar.NAME)
            case 115:
                storage.set_current_panel(ProblemsTabs.NAME)
            case 100:
                storage.set_current_panel(TestsResultPanel.NAME)

        storage.current_panel.control(c)


def run_tests_interactive(args: argparse.Namespace) -> None:
    """Run the test with terminal interface"""
    try:
        curses.wrapper(wrapper, args)
    except Exception as ex:
        traceback.print_exc()