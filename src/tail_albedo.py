import os
import ROOT

from halo import Halo
from typing import List
from alive_progress import alive_bar
from .helpers.setup import grab_files
from .helpers.graphs import GraphManager, GraphSettings

libpath = os.path.join(os.getenv("PIONEERSYS"), "install/lib/libPiRootDict.dylib")
ROOT.gSystem.Load(libpath)

def verify_graph_options(*histograms) -> bool:
    valid_histogram_names = list(GraphManager.histograms.keys())
    for histogram in histograms:
        if histogram not in valid_histogram_names:
            raise ValueError(f"Histogram '{histogram}' does not exist")
    return True

# @Halo(text='Running...', spinner='dots')
def gather_data(target: str, directories: List[str]) -> GraphManager:
    chain = grab_files(*directories)
    
    graph_manager = GraphManager.read_chain(chain, target)
    return graph_manager
    
def graph(graph_manager: GraphManager, settings: GraphSettings) -> None:
    graph_manager.add_to_histogram_stack(*settings.histograms)
    if settings.show_legend:
        graph_manager.draw_legend()
    else:
        graph_manager.draw_canvas(settings.histogram_stack_draw_mode, settings.log_y_axis)

def gather_data_and_graph(settings: GraphSettings) -> None:
    graph_manager = gather_data(settings.target, settings.paths)
    graph(graph_manager, settings)
