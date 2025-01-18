from __future__ import annotations
from tkinter import HORIZONTAL
from typing import Coroutine
from textual.app import App, ComposeResult
from textual.events import MouseDown
from textual.widget import Widget
from textual.widgets import Header, Footer, Static, Tabs, Tab, Button, Label, ListView, ListItem, OptionList
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer, Container, Horizontal, VerticalScroll, Grid
from textual.binding import Binding
from typing import Any
from textual.widgets.option_list import Option, Separator
from textual import log
import logging
from textual.logging import TextualHandler

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)

class QuestionWithOptionsModal(ModalScreen):
    """Screen with a dialog to quit."""

    DEFAULT_CSS = """
    QuestionWithOptionsModal {
        align: center middle;
    }

    #dialog {
        width: 60%;
        height: 70%;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
    }

    #options {
        width: 70%;
    }

    #cancel {
    }
    """
    BINDINGS = [("c", "cancel", "Cancel")]

    def __init__(self, question: str, options: list[Option | Separator]) -> None:
        super().__init__()
        self.question = question
        self.options = options

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.question, id="question"),
            OptionList(*self.options, id="options"),
            Button("(c) Cancel", variant="default", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

    def action_cancel(self) -> None:
        self.app.pop_screen()


class WorkItem(Container):
    """A widget to display a work item with title, owner, total, and left."""

    BINDINGS = [("e", "edit", "Edit")]

    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        """Create child widgets to display the task details."""
        owner = "John Doe"
        total = 5
        left = 0.5

        yield Static(self.title, classes="title")
        yield Static(f"Owner: {owner}", classes="owner")
        yield Static(f"{left} / {total}")

    # def on_mouse_down(self, event: MouseDown) -> None:
    # self.add_class("selected")

    # def action_edit(self) -> None:
    #     self.app.push_screen(WorkItemEdit(self.title))

    def action_pressed(self) -> None:
        print("hello")

class SprintColumn(ListView):
    def __init__(self, title: str, idx: int):
        super().__init__(id=title)
        self.title = title
        self.border_title = f"[{idx}] {title}"

    BINDINGS = [
        ("a", "add", "Add"),
        ("e", "edit", "Delete"),
        ("d", "delete", "Delete"),
        ("m", "move", "Move"),
        ("left", "move_column_focus_left", "Move focus left"),  # TODO hide this
        ("right", "move_column_focus_right", "Move focus right"),  # TODO hide this
    ]

    def add_work_item(self, item: WorkItem) -> None:
        self.append(ListItem(item))
        item.scroll_visible()

    def action_add(self) -> None:
        self.add_work_item(WorkItem("Another bug"))

    def action_delete(self) -> None:
        if self.highlighted_child is not None:
            self.highlighted_child.remove()

    def action_move(self) -> None:
        if self.highlighted_child is not None:
            self.app.push_screen(
                QuestionWithOptionsModal(
                    "Move to",
                    [
                        Option("Do", id="do"),
                        Option("Doing", id="doing"),
                        Option("Done", id="done"),
                        Separator(),
                        Option("Backlog", id="backlog"),
                    ],
                )
            )

    def action_move_column_focus_right(self) -> None:
        self._move_column_focus(1)

    def action_move_column_focus_left(self) -> None:
        self._move_column_focus(-1)

    def _move_column_focus(self, direction: int) -> None:
        parent_board = self.parent
        columns = parent_board.query(SprintColumn).nodes
        cur_col_index = columns.index(self)
        cur_item_index = self.index
        logging.info(f"cur_col_index: {cur_col_index}, cur_item_index: {cur_item_index}")
        target_col_index = cur_col_index + direction
        if 0 <= target_col_index < len(columns):
            self.index = None
            target_col = columns[cur_col_index + direction]
            target_col.focus()
            next_item_index = cur_item_index if cur_item_index < len(target_col) else len(target_col) - 1
            logging.info(f"next_item_index: {next_item_index}")
            target_col.index = next_item_index

    def on_blur(self, event: events.Blur) -> None:
        self.index = None

    # def on_list_view_selected(self, event: ListView.Selected):
    #     work_item: WorkItem = event.item.children[0]
    #     print("selected", work_item.title)
    #     print("index", event.item.index)
    # print("chosen", self.query_one("#chosen"))


class SprintBoard(Horizontal):
    BINDINGS = [
        # ("a", "add", "Add"),
        Binding("1", "focus_do", show=False),
        Binding("2", "focus_doing", show=False),
        Binding("3", "focus_done", show=False),
    ]

    def action_focus_do(self) -> None:
        self.query_one("#Do").focus()

    def action_focus_doing(self) -> None:
        self.query_one("#Doing").focus()

    def action_focus_done(self) -> None:
        self.query_one("#Done").focus()

    def compose(self) -> ComposeResult:
        yield SprintColumn("Do", 1)
        yield SprintColumn("Doing", 2)
        yield SprintColumn("Done", 3)

    def action_add(self) -> None:
        # new_item = WorkItem("Another bug")
        # self.query_one("#Do").query("ListView").append(new_item)
        # new_item.scroll_visible()
        pass


class CeleroApp(App):
    """A Textual app to manage celero."""

    CSS_PATH = "style.tcss"

    # BINDINGS = [
    #     Binding("down", "cursor_down", "Down", show=False),
    #     Binding("end", "last", "Last", show=False),
    #     Binding("enter", "select", "Select", show=False),
    #     Binding("home", "first", "First", show=False),
    #     Binding("pagedown", "page_down", "Page down", show=False),
    #     Binding("pageup", "page_up", "Page up", show=False),
    #     Binding("up", "cursor_up", "Up", show=False),
    # ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        print("app compose")
        yield Header()
        yield Footer()
        yield SprintBoard(id="sprint_board")


if __name__ == "__main__":
    app = CeleroApp()
    app.run()
