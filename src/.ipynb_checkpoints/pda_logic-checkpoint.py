class PDA:
    def __init__(self, input_string):
        # Initialize the PDA with the input string and add an epsilon 'ε' at the end
        # 'ε' represents an empty move or end marker
        self.input = input_string.lower() + 'ε'
        self.path = []  # This keeps track of the sequence of moves (used for tracing the successful path)

    def is_palindrome(self):
        """
        Public method to check if the input string is a palindrome using PDA simulation.
        Returns True if it's a palindrome, False otherwise.
        """
        self.path = []  # Reset the path trace before each check
        found = self.explore('q_push', 0, [])  # Start exploring from state 'q_push', position 0, empty stack

        if found:
            return True
        else:
            self.path = []  # Clear the path if not accepted
            return False

    def explore(self, state, position, stack):
        """
        Recursive helper method to simulate the PDA transitions.
        """

        # Base case: ACCEPT state
        if state == 'ACCEPT':
            return True

        # q_push → push onto stack
        if state == 'q_push':
            if position < len(self.input) - 1:
                symbol = self.input[position]
                new_stack = stack + [symbol]

                self.path.append({'state': state, 'position': position, 'stack': stack.copy()})
                if self.explore('q_push', position + 1, new_stack):
                    return True
                self.path.pop()

            # Option 1: Transition to q_pop for even-length palindrome
            self.path.append({'state': state, 'position': position, 'stack': stack.copy()})
            if self.explore('q_pop', position, stack):
                return True
            self.path.pop()

            # Option 2: Transition to q_skip for odd-length palindrome (skip middle symbol)
            if position < len(self.input) - 1:
                self.path.append({'state': state, 'position': position, 'stack': stack.copy()})
                if self.explore('q_skip', position + 1, stack):
                    return True
                self.path.pop()

        # q_skip → skip one symbol and go to q_pop
        elif state == 'q_skip':
            self.path.append({'state': state, 'position': position, 'stack': stack.copy()})
            if self.explore('q_pop', position, stack):
                return True
            self.path.pop()

        # q_pop → pop from stack and match input
        elif state == 'q_pop':
            if position >= len(self.input):
                return False

            symbol = self.input[position]

            if symbol == 'ε' and len(stack) == 0:
                self.path.append({'state': 'ACCEPT', 'position': position, 'stack': stack.copy()})
                return True

            if not stack:
                return False

            top = stack[-1]
            if symbol == top:
                self.path.append({'state': state, 'position': position, 'stack': stack.copy()})
                if self.explore('q_pop', position + 1, stack[:-1]):
                    return True
                self.path.pop()

        return False

