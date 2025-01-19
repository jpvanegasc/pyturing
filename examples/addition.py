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
    "q3": {1: ("H", 1, 1)},
    "H": {0: ("H", 0, 0), 1: ("H", 1, 0)},
}


tape = [0, 1, 1, 1, 0, 1, 1, 1]
transition = TransitionFunction(addition, halt_states=["H"])
tm = TuringMachine(tape, transition)
tm.run()
