class Fa:
    def __init__(self, filename) -> None:
        self.states = []
        self.alphabet = []
        self.final_states = []
        self.transitions = []
        self.initial_state = None
        self.filename = filename

    def read_from_file(self):
        with open(self.filename, 'r') as file:
            states = file.readline().strip().split(":")
            self.states = states[1].strip().split(",")
            alphabet = file.readline().strip().split(":")
            self.alphabet = alphabet[1].strip().split(",")
            initial_state = file.readline().strip().split(":")
            self.initial_state = initial_state[1].strip()
            final_states = file.readline().strip().split(":")
            self.final_states = final_states[1].strip().split(",")
            transitions = file.readline().strip().split(":")
            #add them as tuples
            for transition in transitions[1].strip().split(","):
                self.transitions.append(tuple(transition.strip().split(" ")))

    def print_states(self):
        print('States: ', end='')
        for state in self.states:
            print(state, end=' ')
    
    def print_alphabet(self):
        print('Alphabet: ', end='')
        for letter in self.alphabet:
            print(letter, end=' ')

    def print_final_states(self):
        print('Final states: ', end='')
        for state in self.final_states:
            print(state, end=' ')

    def print_initial_state(self):
        print('Initial state: ', end='')
        print(self.initial_state)

    def print_transitions(self):
        print('Transitions: ')
        for transition in self.transitions:
            print(f"{transition[0]} -> {transition[1]} : {transition[2]}")

    def check_if_dfa(self) -> bool:
        for state in self.states:
            for letter in self.alphabet:
                found = False
                for transition in self.transitions:
                    if transition[0] == state and transition[2] == letter:
                        found = True
                        break
                if not found:
                    return False
        return True

    def check_accepted(self, word) -> bool:
        current_state = self.initial_state
        for letter in word:
            found = False
            for transition in self.transitions:
                if transition[0] == current_state and transition[2] == letter:
                    current_state = transition[1]
                    found = True
                    break
            if not found:
                return False
        if current_state in self.final_states:
            return True

if __name__ == '__main__':
    #create a user interface menu
    print('1. Read FA from file')
    print('2. Display states')
    print('3. Display alphabet')
    print('4. Display transitions')
    print('5. Display final states')
    print('6. Display initial state')
    print('7. Check if a sequence is accepted')
    print('8. Check if FA is DFA')
    print('0. Exit')
    while True:
        option = int(input('Choose an option: '))
        if option == 1:
            filename = input('Enter the filename: ')
            fa = Fa(filename)
            fa.read_from_file()
        elif option == 2:
            fa.print_states()
            print()
        elif option == 3:
            fa.print_alphabet()
            print()
        elif option == 4:
            fa.print_transitions()
        elif option == 5:
            fa.print_final_states()
            print()
        elif option == 6:
            fa.print_initial_state()
            print()
        elif option == 7:
            word = input('Enter the word: ')
            if fa.check_accepted(word):
                print('The word is accepted')
            else:
                print('The word is not accepted')
        elif option == 8:
            if fa.check_if_dfa():
                print('The FA is DFA')
            else:
                print('The FA is not DFA')
        elif option == 0:
            break
        else:
            print('Invalid option')