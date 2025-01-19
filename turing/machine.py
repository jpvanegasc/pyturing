import curses
import time
from typing import Any, Iterable


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
            return False, None, None, None
        symbol = self.tape[self.head]
        self.state, change, move = self.transition_function(self.state, symbol)
        if change:
            self.tape[self.head] = int(not self.tape[self.head])
        self.head += move
        return True, self.state, change, move

    def run(self):
        def animate(stdscr):
            curses.curs_set(0)  # Hide the cursor
            stdscr.nodelay(True)  # Non-blocking input
            stdscr.clear()

            run = True

            while True:
                stdscr.clear()
                tape = "|".join(str(s) for s in self.tape)
                head = " " * (2 * self.head) + "^"

                # Get screen size and center the message
                height, _ = stdscr.getmaxyx()
                y = height // 2

                stdscr.addstr(0, 0, f"State: {self.state}")
                stdscr.addstr(y, 0, tape, curses.A_BOLD)
                stdscr.addstr(y + 1, 0, head, curses.A_BOLD)

                run, _, _, _ = self.step()

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
