import argparse

from typing import List
from src import tail_albedo
from src.helpers.graphs import GraphSettings, parse_settings

def main() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-path', '-P', help='What path to look for root file')
    arg_parser.add_argument('-target', '-T', help='What energy to measure (calo or ghost)')
    arg_parser.add_argument('-histogram_stack_draw_mode', '-D', type=str, help='What draw mode the canvas should use')
    arg_parser.add_argument('-graph_histograms', action='store', type=str, nargs='+', help='What to graph')
    arg_parser.add_argument('-log_y_axis', '-LYA', help='Whether to set the canvas Y to log scale')
    arg_parser.add_argument('-show_legend', '-L', help='Whether to draw legend')
    
    settings = parse_settings(arg_parser)

    tail_albedo.verify_graph_options(*settings.histograms)
    tail_albedo.gather_data_and_graph(settings)

if __name__ == '__main__':
    main()