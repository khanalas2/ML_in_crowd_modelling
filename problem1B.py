import argparse
from grid import Grid

if __name__ == '__main__':
    # Reading Scenarios from file
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    print(args.filename)
    g = Grid(0)
    g.process_file(args.filename)
    # current this function moves the pedestrian, later move_one is adapted with distance.
    print('BEFORE: ')
    g.print_grid()
    g.change_ped_state(g.pedestrians[0], (3,0))
    print('AFTER: ')
    g.print_grid()