from turing import TransitionFunctionBase, TuringMachine


class AdditionTransitionFunction(TransitionFunctionBase):
    def __call__(self, state, symbol):  # -> state, change, move (1: right, -1: left):
        if state == "q0":
            if symbol == 1:
                return "q1", 0, 1
            else:
                return "q0", 0, 1
        if state == "q1":
            if symbol == 1:
                return "q1", 0, 1
            else:
                return "q2", 1, -1
        if state == "q2":
            if symbol == 1:
                return "q2", 0, -1
            else:
                return "q3", 0, 1
        if state == "q3":
            if symbol == 1:
                return "q3", 1, 1

        raise RuntimeError("Undefined state/symbol pair")


tape = [0, 1, 1, 0, 1, 1, 1]
states = ["q0", "q1", "q2", "q3"]
tm = TuringMachine(tape, states, AdditionTransitionFunction, final_state_indices=[3])
tm.run()
