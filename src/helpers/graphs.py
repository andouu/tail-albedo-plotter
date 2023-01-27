from __future__ import annotations

import os
import json
import ROOT

from typing import List, Literal
from alive_progress import alive_bar
from dataclasses import dataclass
from .energy import measure_energy_and_fill_histogram

class GraphManager:
    """
    Class to process data into graphs
    """
    
    histograms = {
        "lyso-center": ROOT.TH1F("Lyso Pent Calo", "Edep", 75, 1, 75),
        "lyso-inner-ring": ROOT.TH1F("Lyso Inner", "Edep", 75, 1, 75),
        "lyso-outer-ring": ROOT.TH1F("Lyso Outer", "Edep", 75, 1, 75),
        "lyso-center,inner-ring": ROOT.TH1F("Lyso Center + Inner Ring", "Edep", 75, 1, 75),
        "lyso-center,inner-ring,outer-ring": ROOT.TH1F("Lyso Center + Inner Ring + Outer Ring", "Edep", 75, 1, 75),
        "lyso-all": ROOT.TH1F("Lyso All", "Edep", 75, 1, 75),
        "csi-center": ROOT.TH1F("CsI Pent", "Edep", 75, 1, 75),
        "csi-inner-ring": ROOT.TH1F("CsI Inner", "Edep", 75, 1, 75),
        "csi-outer-ring": ROOT.TH1F("CsI Outer", "Edep", 75, 1, 75),
        "csi-center,inner-ring": ROOT.TH1F("CsI Center + Inner Ring", "Edep", 75, 1, 75),
        "csi-center,inner-ring,outer-ring": ROOT.TH1F("CsI Center + Inner Ring + Outer Ring", "Edep", 75, 1, 75),
        "csi-all": ROOT.TH1F("CsI All", "Edep", 75, 1, 75),
        "reference-plane": ROOT.TH1F("Ref Plane", "Edep", 100, -0.5, 14.5), 
        "neutron-individual": ROOT.TH1F("Neutron Individual", "Edep", 100, -0.5, 14.5),
        "photon-individual": ROOT.TH1F("Photon Individual", "Edep", 100, -0.5, 14.5),
        "electron-individual": ROOT.TH1F("Electron Individual", "Edep", 100, -0.5, 14.5),
        "positron-individual": ROOT.TH1F("Positron Individual", "Edep", 100, -0.5, 14.5)
    }

    def _init_canvas(self) -> None:
        self._canvas = ROOT.TCanvas()
        self._canvas.SetWindowSize(1000, 750)

    def _init_histograms(self) -> None:
        for i, histogram in enumerate(self.histograms.values()):
            if i + 1 < 10:
                histogram.SetLineColor(i + 1)
            else:
                histogram.SetLineColor(1)

    def _init_legend(self, x1: float=0.77, y1: float=0.68, x2: float=0.92, y2: float=0.83) -> None:
        legend = ROOT.TLegend(x1, y1, x2, y2)
        legend.AddEntry(self.histograms['lyso-center'], 'Lyso Center')
        legend.AddEntry(self.histograms['lyso-center,inner-ring'], 'Lyso Center + Inner Ring')
        legend.AddEntry(self.histograms['lyso-center,inner-ring,outer-ring'], 'Lyso Center + Inner Ring + Outer Ring')
        legend.AddEntry(self.histograms['lyso-all'], 'Lyso Full Calo')
        legend.AddEntry(self.histograms['csi-center'], 'CsI Center')
        legend.AddEntry(self.histograms['csi-center,inner-ring'], 'CsI Center + Inner Ring')
        legend.AddEntry(self.histograms['csi-center,inner-ring,outer-ring'], 'CsI Center + Inner Ring + Outer Ring')
        legend.AddEntry(self.histograms['csi-all'], 'CsI Full Calo')
        legend.SetLineWidth(0)
        self._legend = legend

    def __init__(self, graph_title='Tail Energy Distributions for Albedo;Energy [MeV];Counts') -> None:
        self.histogram_stack = ROOT.THStack('hs', graph_title)
        self._init_histograms()
        self._init_canvas()
        self._init_legend()

    def fill_histogram(self, name: str, amount: float) -> None:
        self.histograms[name].Fill(amount)
    
    @classmethod
    def read_chain(cls, chain, collect_method: str) -> GraphManager:
        graph_manager = GraphManager()
        with alive_bar(chain.GetEntries(), title='Reading entries in TChain...') as bar:
            for event in chain:
                measure_energy_and_fill_histogram(graph_manager, event, collect_method)
                bar()
        return graph_manager

    def fractional_integral(self, graph_name: str, left_bound=0, right_bound=56) -> float:
        graph = self.histograms[graph_name]
        integral = graph.Integral(left_bound, right_bound) / graph.Integral()

        print(f'Tail fraction for {graph_name} is {integral}')
        return integral

    def add_to_histogram_stack(self, *graph_names: List[Literal['lyso-center', 'lyso-inner-ring', 'lyso-outer-ring', 'lyso-center,inner-ring', 'lyso-center,inner-ring,outer-ring', 'lyso-all', 'csi-center', 'csi-inner-ring', 'csi-outer-ring', 'csi-center,inner-ring', 'csi-center,inner-ring,outer-ring', 'csi-all', 'reference-plane', 'neutron-individual', 'photon-individual', 'positron-individual']]) -> None:
        for graph_name in graph_names:
            self.histogram_stack.Add(self.histograms[graph_name])

    def draw_canvas(self, histogram_stack_draw_mode: str, log_y_axis=True) -> None:
        self.histogram_stack.Draw(histogram_stack_draw_mode)
        self._canvas.SetLogy(log_y_axis)
        self._canvas.Update()
        self._canvas.Draw()
        input('Graphed! Press enter to stop running the script.')
        return self._canvas

    def draw_legend(self) -> None:
        self._legend.Draw(" same ")

@dataclass
class GraphSettings():
    paths: List[str] = None
    target: str = 'calo'
    histograms: List[str] = None
    histogram_stack_draw_mode: str = 'nostack'
    log_y_axis: bool = True
    show_legend: bool = False

def parse_histograms_list(json_settings) -> List[str]:
    histogram_aliases = json_settings['aliases']
    histograms = json_settings['instructions']['histograms']
    parsed_histograms_list = []
    for histogram in histograms:
        for name, aliases in histogram_aliases.items():
            if histogram == name or histogram in aliases:
                parsed_histograms_list.append(name)
                break
    
    return parsed_histograms_list

def parse_root_paths(json_settings) -> List[str]:
    target_group = json_settings['instructions']['group']
    return json_settings['groups'][target_group]['paths']

def parse_settings(arg_parser) -> GraphSettings:
    settings_json_path = os.path.abspath(os.path.join(__file__, '../../../settings.json'))
    json_settings = None
    with open(settings_json_path, 'r') as file:
        json_settings = json.load(file)

    graph_settings = GraphSettings()
    args = arg_parser.parse_args()
    
    if not args.target:
        graph_settings.target = json_settings['instructions']['target']
    else:
        graph_settings.target = args.target
    
    if not args.histogram_stack_draw_mode:
        graph_settings.histogram_stack_draw_mode = json_settings['instructions']['histogramStackDrawMode']
    else:
        graph_settings.histogram_stack_draw_mode = args.histogram_stack_draw_mode
    
    if not args.log_y_axis:
        graph_settings.log_y_axis = json_settings['instructions']['logYAxis']
    else:
        graph_settings.log_y_axis = args.log_y_axis

    if not args.show_legend:
        graph_settings.show_legend = json_settings['instructions']['showLegend']
    else:
        graph_settings.show_legend = args.show_legend

    if not args.path:
        graph_settings.paths = parse_root_paths(json_settings)
    else:
        graph_settings.paths = [args.path]
    
    if not args.graph_histograms:
        graph_settings.histograms = parse_histograms_list(json_settings)
    else:
        graph_settings.histograms = args.graph_histograms
    
    return graph_settings
