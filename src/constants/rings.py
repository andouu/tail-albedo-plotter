from typing import Union
from enum import Enum

LYSO_CENTER_CALO_ID = 300001
LYSO_INNER_CALO_IDS = { 300021,300041,300061,300081,300101 }
LYSO_OUTER_CALO_IDS = { 300121,300141,300161,300181,300201,300211,300241,300261,300281,300301 }

CSI_CENTER_CALO_ID = 310001
CSI_INNER_CALO_IDS = { 310021,310041,310061,310081,310101 }
CSI_OUTER_CALO_IDS = { 310121,310141,310161,310181,310201,310221,310241,310261,310281,310301 }

class CaloType(Enum):
    LYSO_CENTER = { LYSO_CENTER_CALO_ID }
    LYSO_INNER_RING = LYSO_INNER_CALO_IDS
    LYSO_OUTER_RING = LYSO_OUTER_CALO_IDS
    LYSO_OTHER = (2000, 310000)
    CSI_CENTER = { CSI_CENTER_CALO_ID }
    CSI_INNER_RING = CSI_INNER_CALO_IDS
    CSI_OUTER_RING = CSI_OUTER_CALO_IDS
    CSI_OTHER = (310000, 9999999999999)
    REFERENCE_PLANE = (0, 2000)

class DetectorRing:
    """
    Class to represent the detector arrays in geometry.

    Attributes:
    center_id -> int: id of the pentagon detector in the middle of the detector array
    inner_ring_ids -> set[int]: ids of the first level of hexagon detectors surrounding the center
    outer_ring_ids -> set[int]: ids of the second level of hexagon detectors surrounding the first level of rings
    """
    def __init__(self, center_id: int, inner_ring_ids: set[int], outer_ring_ids: set[int]):
        self.center = center_id
        self.inner_ring_ids = inner_ring_ids
        self.outer_ring_ids = outer_ring_ids
  
LYSO_DETECTORS = DetectorRing(
    center_id=LYSO_CENTER_CALO_ID,
    inner_ring_ids=LYSO_INNER_CALO_IDS,
    outer_ring_ids=LYSO_OUTER_CALO_IDS
)

CSI_DETECTORS = DetectorRing(
    center_id=CSI_CENTER_CALO_ID,
    inner_ring_ids=CSI_INNER_CALO_IDS,
    outer_ring_ids=CSI_OUTER_CALO_IDS
)

def calo_id_to_type(calo_id: int) -> Union[CaloType, None]:
    if calo_id is None:
        return None
        
    for type in CaloType:
        if type is CaloType.LYSO_OTHER or type is CaloType.CSI_OTHER or type is CaloType.REFERENCE_PLANE:
            continue
        if calo_id in type.value:
            return type
    # handle edge cases
    for type in [CaloType.LYSO_OTHER, CaloType.CSI_OTHER, CaloType.REFERENCE_PLANE]:
        if calo_id >= type.value[0] and calo_id < type.value[1]:
            return type
    return None
