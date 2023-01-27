"""
Helper functions to grab root files
"""
import os
import ROOT

from alive_progress import alive_bar
from glob import glob
from typing import Any

def add_directory_to_chain(directory: str, chain) -> None:
    file_paths = glob('*.root', root_dir=directory)
    for local_file in file_paths:
        file_path = os.path.join(directory, local_file)
        chain.Add(file_path)

def grab_files(*directories) -> Any:
    """
    Grabs root files at provided paths and returns respective TChains.

    Attributes:
    *directories -> List[str]: list of directories to graph

    Returns:
    chain -> TChain
    """

    chain = ROOT.TChain("sim")
    with alive_bar(len(directories), title='Attaching directories to TChain...') as bar:
        for directory in directories:
            if not os.path.exists(directory):
                raise ValueError(f"Path '{directory}' does not exist!")
            if os.path.isfile(directory):
                if directory.endswith('.root'):
                    chain.Add(directory)
            else:
                add_directory_to_chain(directory, chain)
            
            bar()
    
    return chain