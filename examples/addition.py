from turing import TransitionFunction, TuringMachine

addition = {
    "q0": {
        0: ("q0", 0, 1),
        1: ("q1", 0, 1),
    },
    "q1": {
        0: ("q2", 1, -1),
        1: ("q1", 0, 1),
    },
    "q2": {
        0: ("q3", 0, 1),
        1: ("q2", 0, -1),
    },
    "q3": {1: ("q3", 1, 1)},
}


tape = [0, 1, 1, 0, 1, 1, 1]
transition = TransitionFunction(addition, halt_states=["q3"])
tm = TuringMachine(tape, transition)
tm.run()
