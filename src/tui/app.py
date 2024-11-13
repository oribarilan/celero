from tkinter import HORIZONTAL
from typing import Coroutine
from textual.app import App, ComposeResult
from textual.events import MouseDown
from textual.widgets import Header, Footer, Static, Tabs, Tab, Button, Label, ListView, ListItem
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer, Container, Horizontal, VerticalScroll, Grid
from textual.binding import Binding
from typing import Any


class WorkItemEdit(ModalScreen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()


class WorkItem(Button):
    """A widget to display a work item with title, owner, total, and left."""

    BINDINGS = [("e", "edit", "Edit")]

    def compose(self) -> ComposeResult:
        """Create child widgets to display the task details."""
        title = "Fix the bug"
        owner = "John Doe"
        total = 5
        left = 0.5

        yield Static(title, classes="title")
        yield Static(f"Owner: {owner}", classes="owner")
        yield Static(f"{left} / {total}")

    # def on_mouse_down(self, event: MouseDown) -> None:
    # self.add_class("selected")

    def action_edit(self) -> None:
        self.app.push_screen(WorkItemEdit())


class SprintColumn(VerticalScroll):
    def __init__(self, title: str, idx: int):
        super().__init__(id=title)
        self.title = title
        self.border_title = f"[{idx}] {title}"

    BINDINGS = [("a", "add", "Add")]

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(WorkItem()),
            ListItem(WorkItem()),
            ListItem(WorkItem()),
        )

    def action_add(self) -> None:
        new_item = WorkItem()
        self.mount(new_item)
        new_item.scroll_visible()


class SprintBoard(Horizontal):
    BINDINGS = [("a", "add", "Add")]

    def compose(self) -> ComposeResult:
        yield SprintColumn("Do", 1)
        yield SprintColumn("Doing", 2)
        yield SprintColumn("Done", 3)

    def action_add(self) -> None:
        new_item = WorkItem()
        self.query_one("#Do").mount(new_item)
        new_item.scroll_visible()


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
        yield Header()
        yield Footer()
        yield SprintBoard(id="sprint_board")


if __name__ == "__main__":
    app = CeleroApp()
    app.run()
