import argparse
from grid import Grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    print(args.filename)
    g = Grid(0)
    g.process_file(args.filename)
    g.print_grid()
    current = g.pedestrians[0]
    result = g.path_movement_dijkstra(current)
    count = 0
    for i in result:
        count +=1
        g.change_ped_state(current, i)
        current = i
        print("Count: ", count)
        g.print_grid()
        print()
    print(result)