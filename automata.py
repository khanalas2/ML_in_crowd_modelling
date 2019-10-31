# X_i := {E : empty(white), P: pedistrian(red), O: obstacle(blue), T:target(yellow)}

class Automata:
    def __init__(self, cell_type, pos):
        self.type = cell_type
        self.length = 3
        self.pos = pos
        self.value = 0

    def neighbors(self, num):
        u = self.pos[0]
        v = self.pos[1]
        if num == 4:
            return [(u,v+1), (u+1,v), (u,v-1), (u-1,v)]
        else:
            return [(u-1, v+1),(u, v+1), (u+1,v+1), (u+1,v), (u+1, v-1), (u, v-1), (u-1, v-1), (u-1,v)]
    
    def print_automata(self):
        print("------------------")
        print("| Type: {0}        {1}".format(self.type, '|'))
        print("| Position:{0}{1}".format(self.pos, '|'))
        print("------------------")

    def print_short(self):
        print('  {0}  '.format(self.type), end="")