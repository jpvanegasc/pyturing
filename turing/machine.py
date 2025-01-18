import abc
import curses
import time
from typing import Any, Iterable


class TransitionFunctionBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self, state, symbol):
        pass


class TuringMachine:
    def __init__(
        self,
        tape: Iterable[Any],
        states,
        transition_function_class,
        *,
        blank_symbol=0,
        input_symbols=(1,),
        initial_state_index=0,
        final_state_indices=None,
        tape_head_position=0,
    ):
        self.tape = tape
        self.head = tape_head_position
        self.states = states
        self.blank_symbol = blank_symbol
        self.input_symbols = input_symbols
        self.state = self.states[initial_state_index]

        if final_state_indices is None:
            self.accepting_states = states
        else:
            self.accepting_states = [states[i] for i in final_state_indices]

        if not issubclass(transition_function_class, TransitionFunctionBase):
            raise TypeError(
                "transition_function_class must be a subclass of TransitionFunctionBase"
            )
        self.transition_function = transition_function_class()

    def step(self):
        if self.state in self.accepting_states:
            return False
        symbol = self.tape[self.head]
        self.state, change, move = self.transition_function(self.state, symbol)
        if change:
            self.tape[self.head] = int(not self.tape[self.head])
        self.head += move
        return True

    def run(self):
        def animate(stdscr):
            curses.curs_set(0)  # Hide the cursor
            stdscr.nodelay(True)  # Non-blocking input
            stdscr.clear()

            run = True

            while run:
                stdscr.clear()
                tape = "|".join(str(s) for s in self.tape)
                head = " " * (2 * self.head) + "^"

                # Get screen size and center the message
                height, width = stdscr.getmaxyx()
                y = height // 2

                stdscr.addstr(y, 0, tape, curses.A_BOLD)
                stdscr.addstr(y + 1, 0, head, curses.A_BOLD)
                stdscr.refresh()

                time.sleep(1)  # Wait for 1 second
                run = self.step()

            # Exit if 'q' is pressed
            key = stdscr.getch()
            if key == ord("q"):
                return

        curses.wrapper(animate)
