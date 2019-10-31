import argparse
from grid import Grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    print(args.filename)
    g = Grid(0)
    g.process_file(args.filename)
    for i in g.pedestrians:
        result = g.path_movement(i)
    print(result)