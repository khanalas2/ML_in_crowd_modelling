import argparse
from grid import Grid

if __name__ == '__main__':
    g = Grid(50)
    g.set_target((25,25))
    g.set_pedestrians([(25,10), (40,25), (25,40), (10, 25), (12,12)])
    g.init_trace()
    g.test_path_movement()
    for i in g.trace:
        print(i)
        print()
    print(len(i))