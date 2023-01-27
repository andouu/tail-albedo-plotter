# Prerequisites:

- Python > 3.0
- PyRoot
- alive_progress

# Installation:

- All you need is to clone this repository into your directory of choice and make sure you meet the prerequisites.
    - Either build ROOT from source or download a precompiled binary.
    - Install the `alive_progress` package using your package manager of choice, e.g. pip: `pip install alive_progress`.

# Running:

1. To run the script correctly, you must configure its settings. There are two ways to do this:
    1. **Recommended:** JSON file ([documentation](#json-settings))
    2. Command line ([documentation](#command-line))
    3. Both - you can use the command line for a few arguments and the program will run fine, because any missing settings default to the JSON file.
2. `python run.py` (use command line arguments here if you aren't using the JSON file)
3. Press enter in the terminal once finished to terminate the program.

# Reference:
## Graphable data:
Below are the strings you provide to the program and what data they correlate to.
- **Lyso pentagon:** "lyso-center"
- **Lyso ring 1:** "lyso-inner-ring"
- **Lyso ring 2:** "lyso-outer-ring"
- **Lyso pentagon + ring 1:** "lyso-center,inner-ring"
- **Lyso pentagon + ring 1 + ring 2:** "lyso-center,inner-ring,outer-ring"
- **Entire lyso detector:** "lyso-all"
- **CsI pentagon:** "csi-center"
- **CsI ring 1:** "csi-inner-ring"
- **CsI ring 2:** "csi-outer-ring"
- **CsI pentagon + ring 1:** "csi-center,inner-ring"
- **CsI pentagon + ring 1 + ring 2:** "csi-center,inner-ring,outer-ring"
- **Entire CsI detector:** "csi-all"
- **Reference / ghost plane:** "reference-plane"
- **Neutrons:** "neutron-individual"
- **Photons:** "photon-individual"
- **Electrons:** "electron-individual"
- **Positrons:** "positron-individual"

---

## JSON Settings:

The structure of the JSON file is as follows:
```json
{
  "groups": {
    "example 1": {
      "paths": [
        "/absolute/or/relative/path",
        "/another/path"
      ]
    },
    "example 2": {
      "paths": [
        "/absolute/or/relative/path"
      ]
    }
  },
  "aliases": {
    "lyso-center": ["lc"],
    "lyso-inner-ring": ["lir"],
    "lyso-outer-ring": ["lor"],
    "lyso-center,inner-ring": ["lci"],
    "lyso-center,inner-ring,outer-ring": ["lcio"],
    "lyso-all": ["la"],
    "csi-center": ["cc"],
    "csi-inner-ring": ["cir"],
    "csi-outer-ring": ["cor"],
    "csi-center,inner-ring": ["cci"],
    "csi-center,inner-ring,outer-ring": ["ccio"],
    "csi-all": ["ca"],
    "reference-plane": ["rp", "ref"],
    "neutron-individual": ["ni", "n", "neutron"],
    "photon-individual": ["pi", "p", "photon"],
    "electron-individual": ["ei", "e", "electron"],
    "positron-individual": ["e+i", "e+", "positron"]
  },
  "instructions": {
    "group": "example 1",
    "target": "calo",
    "histogramStackDrawMode": "nostack",
    "histograms": [
      "lyso-center",
      "lyso-center,inner-ring",
      "lor",
      "ca"
    ],
    "logYAxis": true,
    "showLegend": false
  }
}
```
### Breakdown:
- **"groups":** The groups key contains groups. A group represents a collection of paths that contain root files. It has a `name` (which is a key within the **"groups"** key) and list of `paths`, and each path can either be a directory or a file. Every root file inside `paths` will be added to a TChain when the program is run. Multiple groups is used to easily differentiate and switch between different root files.
- **"aliases":** Which histograms to graph (e.g. lyso-center) are specified in the **"histograms"** key of **"instructions"**, but if you want to constantly switch between graphing the "lyso-center" histogram and "lyso-center,inner-ring,outer-ring" histogram, typing the latter can become annoying. Aliases are a way of saying the same thing, based on your definitions. For example, the default alias for "lyso-center,inner-ring,outer-ring" is "lcio" but you can add however many aliases you want in the arrays.
- **"instructions":** Tells the program what to graph. There are six settings:
    - **"group":** The name of the group (root files) you want to analyze. Groups are defined in the **"groups"** key.
    - **"target":** Should be either "calo" or "ghost" depending what data you want.
    - **"histogramStackDrawMode":** What mode the THStack should draw in.
    - **"histograms":** A list of strings which specify what data you want to graph. Check the [reference](#graphable-data) for valid histogram names, or use aliases as specified above.
    - **"logYAxis":** Whether or not the y axis should be on a log scale (this is equivalent to calling `SetLogy()` on the TCanvas).
    - **"showLegend":** Whether to show the legend or not.

---

## Command Line:

If you want to use the command line, there are arguments which you can pass to configure the settings of the program.
- `-path/-P`: A path to either a root file or a directory which contains root files.
- `-target/-T`: Should be either "calo" or "ghost" depending what data you want.
= `-histogram_stack_draw_mode/-D`: What mode the THStack should draw in.
- `graph_histograms`: A list of strings which specify what data you want to graph. Check the [reference](#graphable-data) for valid histogram names. Unlike the JSON settings file, aliases will not work here.
- `log_y_axis/-LYA`: Whether or not the y axis should be on a log scale (this is equivalent to calling `SetLogy()` on the TCanvas).
- `show_legend/-L`: Whether to show the legend or not.