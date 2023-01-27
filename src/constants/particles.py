# ///------------------------------------------------------
# CONSTANTS ------------------------------------------------
#
from enum import Enum
"""
Ids to reference in root files
https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf

Keys:
- 11: [TODO: FILL]
- 22: [TODO: FILL]
- 2112: [TODO: FILL]
"""

class ParticleType(Enum):
    ELECTRON = 11
    POSITRON = -11
    PHOTON = 22
    NEUTRON = 2112
    UNKNOWN = 999999999999

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

PARTICLE_IDS = [
    11,
    -11,
    22,
    2112
]

PARTICLE_MASSES = {
    "proton": 938.272,
    "neutron": 939.565,
    "electron": 0.511
}

def pdg_id_to_particle(id: int) -> ParticleType:
    return ParticleType(id)