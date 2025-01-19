import curses
import time
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class Frame:
    tape: str
    head: str
    state: str

    @classmethod
    def from_machine(cls, machine):
        tape = "|".join(str(s) for s in machine.tape)
        head = " " * (2 * machine.head) + "^"
        return cls(tape, head, machine.state)


class TransitionFunction:
    def __init__(self, transitions, halt_states):
        self.states = list(transitions.keys())
        if not set(halt_states).issubset(self.states):
            raise ValueError("States must contain halt states")
        self.transitions = transitions
        self.halt_states = halt_states

    def __call__(self, state, symbol):
        if state in self.states:
            return self.transitions[state].get(symbol, (None, None, None))
        else:
            raise ValueError("Invalid state")


class TuringMachine:
    def __init__(
        self,
        tape: Iterable[Any],
        transition_function: TransitionFunction,
        *,
        blank_symbol=0,
        input_symbols=(1,),
        initial_state_index=0,
        tape_head_position=0,
    ):
        self.tape = tape
        self.head = tape_head_position
        self.transition_function = transition_function
        self.states = transition_function.states
        self.halt_states = transition_function.halt_states
        self.blank_symbol = blank_symbol
        self.input_symbols = input_symbols
        self.state = self.states[initial_state_index]

    def step(self):
        if self.state in self.halt_states:
            return False
        symbol = self.tape[self.head]
        state, change, move = self.transition_function(self.state, symbol)
        if change:
            self.tape[self.head] = int(not self.tape[self.head])
        self.head += move
        self.state = state
        return True

    def run(self):
        def animate_frame(machine, stdscr):
            frame = Frame.from_machine(machine)
            height, _ = stdscr.getmaxyx()
            middle_y = height // 2
            stdscr.addstr(0, 0, f"State: {self.state}")
            stdscr.addstr(middle_y, 0, frame.tape, curses.A_BOLD)
            stdscr.addstr(middle_y + 1, 0, frame.head, curses.A_BOLD)

        def animate(stdscr):
            curses.curs_set(0)  # Hide the cursor
            stdscr.nodelay(True)  # Non-blocking input
            stdscr.clear()

            run = True

            while True:
                stdscr.clear()
                animate_frame(self, stdscr)

                run = self.step()

                if not run:
                    quit_message = "Press 'q' to quit"
                    stdscr.addstr(1, 0, quit_message, curses.A_DIM)

                stdscr.refresh()

                if run:
                    time.sleep(1)
                else:
                    key = stdscr.getch()
                    if key == ord("q"):
                        break

        curses.wrapper(animate)
