import numpy as np
import math
import queue
import ast
from automata import Automata

class Grid:
    def __init__(self, size):
        self.size = size
        self.target = ()
        self.pedestrians = []
        self.obstacles = []
        self.trace = []
        self.clock = 0
        lst = []
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(Automata('E',(i,j)))
            lst.append(temp)
        self.cellular_grid = np.array(lst)

    def create_grid(self, side):
        self.size = side
        lst = []
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(Automata('E',(i,j)))
            lst.append(temp)
        self.cellular_grid = np.array(lst)

    def change_celltype(self, pos, ctype):
        self.cellular_grid[pos[0], pos[1]].type = ctype

    def init_trace(self):
        for i in self.pedestrians:
            self.trace.append([i])

    def new_celltype(self, pos, ctype):
        self.cellular_grid[pos[0], pos[1]].type = ctype
        if ctype == 'P':
            self.pedestrians.append(pos)
        if ctype == 'O':
            self.obstacles.append(pos)

    def path_movement(self, pedpos):
        currpos = pedpos
        count = 0
        path = []
        while(currpos != self.target):
            count+=1
            dist_lst = []
            path.append(currpos)
            for i in self.computeNeighbors(currpos):
                dist_lst.append((self.dist(i), i))
            distances = sorted(dist_lst, key=lambda tup: tup[0])
            self.change_ped_state(currpos, distances[0][1])
            currpos = distances[0][1]
            if count > 75:
                break
        path.append(self.target)
        return path, count
    
    def path_movement_dijkstra(self, init):
        visited_nodes, possibility = self.computeDijkstra(init)
        constructed_path = []
        if possibility:
            constructed_path = self.construct_path(init, visited_nodes)
        return constructed_path


    def construct_path(self, init, visited):
        curr = self.target
        path = []
        while(curr != init):
            path.append(curr)
            curr = visited[curr]
        path.append(init) 
        path.reverse() 
        return path
    
    def computeDijkstra(self, init):
        temp = queue.PriorityQueue()
        temp.put(init, 0)
        visited = {}
        cumulativeCost = {}
        visited[init] = None
        cumulativeCost[init] = 0
        while not temp.empty():
            current_node = temp.get()
            if(current_node == self.target):
                return visited, True
            neighbor = self.computeNeighbors(current_node)

            for values in neighbor:
                new_cost = cumulativeCost[current_node] + self.cost_value(values, current_node)
                
                if values not in cumulativeCost or new_cost < cumulativeCost[values]:
                    cumulativeCost[values] = new_cost
                    temp.put(values,new_cost)
                    visited[values] = current_node
        return "No path found!", False

    def costDir(self, coordinate1, coordinate2):
        sideways = [(0,1), (0, -1)]
        up_down = [(1, 0), (-1, 0)]
        diagonal = [(1, 1), (-1, -1),(1, -1), (-1, 1)]
        res = (coordinate1[0] - coordinate2[0], coordinate1[1] - coordinate2[1])
        if res in up_down:
            return 1
        if res in sideways:
            return 1
        if res in diagonal:
            return math.sqrt(2)

    def dist(self, pedpos):
        return math.sqrt(pow(pedpos[0]-self.target[0], 2) + pow(pedpos[1]-self.target[1], 2))

    def cost(self, r1, r2):
        d1 = self.dist(r1)
        d2 =  self.dist(r2)
        if d1 < d2:
            return math.exp(-1/(d1**2 - d2**2))
        else:
            return 0

    def cost_value(self, pedpos, current):
        c1 = self.cost(pedpos, self.target)
        sumcost = 0
        for i in self.pedestrians:
            if i != current:
                if i != pedpos:
                    sumcost += self.cost(pedpos, i)
        return sumcost+c1

    def change_cellvalue(self, pos, value):
        self.cellular_grid[pos[0], pos[1]].value = value

    def boundaryCheck(self, val):
        (x, y) = val
        return 0 <= x < self.size and 0 <= y < self.size
    
    def computeNeighbors(self,coord):
        (x, y) = coord
        neighbors = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1)]
        validNeighbors = []
        for i in neighbors:
            if(self.boundaryCheck(i)):
                validNeighbors.append(i)
        result_neighbors = []
        for j in validNeighbors:
            if j not in self.obstacles:
                if j not in self.pedestrians:
                    result_neighbors.append(j)
        return result_neighbors  
    
    def set_target(self, pos):
        self.target = pos
        self.change_celltype(pos, 'T')

    def set_pedestrians(self, lst):
        self.pedestrians = lst
        for i in lst:
            self.change_celltype(i, 'P')

    def set_obstacles(self, lst):
        self.obstacles = lst
        for i in lst:
            self.change_celltype(i, 'O')


    def get_cellarray(self):
        lst1 = []
        for i in range(self.size):
            lst2 = []
            for j in range(self.size):
                lst2.append(self.cellular_grid[i, j].value)
            lst1.append(lst2)
        return np.array(lst1)

    def get_target(self):
        return self.target

    def get_pedestrians(self):
        return self.pedestrians

    def get_obstacles(self):
        return self.obstacles

    def print_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.cellular_grid[i, j].print_short()
            print()
    
    def process_file(self, filename):
        with open(filename) as f:
            content = f.readlines()
            for i in content:
                line = i.rstrip()
                line = line.split(': ')
                if line[0] == 'size':
                    self.create_grid(int(line[1]))
                elif line[0] == 'target':
                    self.set_target(ast.literal_eval(line[1]))
                elif line[0] == 'pedestrians':
                    self.set_pedestrians(ast.literal_eval(line[1]))
                elif line[0] == 'obstacles':
                    self.set_obstacles(ast.literal_eval(line[1]))

    def cost_path_movement(self, pedpos):
        currpos = pedpos
        count = 0
        path = []
        while(currpos != self.target):
            count+=1
            dist_lst = []
            path.append(currpos)
            for i in self.computeNeighbors(currpos):
                dist_lst.append((self.cost_value(i, currpos)+self.dist(i), i))
            distances = sorted(dist_lst, key=lambda tup: tup[0])
            currpos = distances[0][1]
            if count > 70:
                break
        return path, count

    def change_ped_state(self, before, now):
        if now == self.target:
            self.new_celltype(before, 'E')
            self.pedestrians.remove(before)
        elif before == now:
            pass
        else:
            self.new_celltype(now, 'P')
            self.new_celltype(before, 'E')
            self.pedestrians.remove(before)

    def move_one(self, currpos):
        dist_lst = []
        for i in self.computeNeighbors(currpos):
            dist_lst.append((self.dist(i) + self.cost_value(i, currpos), i))
        distances = sorted(dist_lst, key=lambda tup: tup[0])
        newpos = distances[0][1]
        self.trace[self.clock].append(newpos)
        self.clock += 1
        self.change_ped_state(currpos, newpos)

    def test_path_movement(self):
        count = 0
        reached = 0
        while True:
            count += 1
            #print('COUNT:', count)
            #self.print_grid()
            #print()
            current_peds = []
            for x in self.pedestrians:
                current_peds.append(x)
            for i in current_peds:
                self.move_one(i)
                if i == self.target:
                    reached += 1
            self.clock = 0
            if count > 30 or len(self.pedestrians)==0:
                break
        #print('COUNT:', count)
        #self.print_grid()