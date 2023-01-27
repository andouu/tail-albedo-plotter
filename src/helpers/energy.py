import numpy as np

from dataclasses import dataclass
from ..constants.rings import calo_id_to_type, CaloType
from ..constants.particles import pdg_id_to_particle, ParticleType, PARTICLE_MASSES

@dataclass
class _CaloMeasurement:
    calo_total: float = 0
    lyso_center: float = 0
    lyso_inner_ring: float = 0
    lyso_outer_ring: float = 0
    lyso_all: float = 0
    csi_center: float = 0
    csi_inner_ring: float = 0
    csi_outer_ring: float = 0
    csi_all: float = 0
    reference_plane: float = 0

    def __add__(self, other):
        return _CaloMeasurement(
            calo_total=self.calo_total + other.calo_total,
            lyso_center=self.lyso_center + other.lyso_center,
            lyso_inner_ring=self.lyso_inner_ring + other.lyso_inner_ring,
            lyso_outer_ring=self.lyso_outer_ring + other.lyso_outer_ring,
            lyso_all=self.lyso_all + other.lyso_all,
            csi_center=self.csi_center + other.csi_center,
            csi_inner_ring=self.csi_inner_ring + other.csi_inner_ring,
            csi_outer_ring=self.csi_outer_ring + other.csi_outer_ring,
            csi_all=self.csi_all + other.csi_all,
            reference_plane=self.reference_plane + other.reference_plane,
            gamma=self.gamma + other.gamma,
            individual_gamma=self.individual_gamma + other.individual_gamma,
        )
    
    def deposit_energy(self, calo_id: int, amount: float) -> None:
        calo_type = calo_id_to_type(calo_id)

        self.calo_total += amount

        if calo_type is None:
            return
        
        if calo_type is CaloType.LYSO_CENTER:
            self.lyso_center += amount
            self.lyso_all += amount
        elif calo_type is CaloType.LYSO_INNER_RING:
            self.lyso_inner_ring += amount
            self.lyso_all += amount
        elif calo_type is CaloType.LYSO_OUTER_RING:
            self.lyso_outer_ring += amount
            self.lyso_all += amount
        elif calo_type is CaloType.LYSO_OTHER:
            self.lyso_all += amount
        elif calo_type is CaloType.CSI_CENTER:
            self.csi_center += amount
            self.csi_all += amount
        elif calo_type is CaloType.CSI_INNER_RING:
            self.csi_inner_ring += amount
            self.csi_all += amount
        elif calo_type is CaloType.CSI_OUTER_RING:
            self.csi_outer_ring += amount
            self.csi_all += amount
        elif calo_type is CaloType.CSI_OTHER:
            self.csi_all += amount
        elif calo_type is CaloType.REFERENCE_PLANE:
            self.reference_plane += amount

def measure_calo_energies(graph_manager, event) -> None:
    calo_measurements = _CaloMeasurement()
    for calo in event.calo:
        energy = calo.GetTotalEnergyDeposit()
        calo_id = calo.GetCaloID()
        calo_measurements.deposit_energy(calo_id, energy)
    graph_manager.fill_histogram('lyso-center', calo_measurements.lyso_center)
    graph_manager.fill_histogram('lyso-inner-ring', calo_measurements.lyso_inner_ring)
    graph_manager.fill_histogram('lyso-outer-ring', calo_measurements.lyso_outer_ring)
    graph_manager.fill_histogram('lyso-center,inner-ring', calo_measurements.lyso_center + calo_measurements.lyso_inner_ring)
    graph_manager.fill_histogram('lyso-center,inner-ring,outer-ring', calo_measurements.lyso_center + calo_measurements.lyso_inner_ring + calo_measurements.lyso_outer_ring)
    graph_manager.fill_histogram('lyso-all', calo_measurements.lyso_all)
    graph_manager.fill_histogram('csi-center', calo_measurements.csi_center)
    graph_manager.fill_histogram('csi-inner-ring', calo_measurements.csi_inner_ring)
    graph_manager.fill_histogram('csi-outer-ring', calo_measurements.csi_outer_ring)
    graph_manager.fill_histogram('csi-center,inner-ring', calo_measurements.csi_center + calo_measurements.csi_inner_ring)
    graph_manager.fill_histogram('csi-center,inner-ring,outer-ring', calo_measurements.csi_center + calo_measurements.csi_inner_ring + calo_measurements.csi_outer_ring)
    graph_manager.fill_histogram('csi-all', calo_measurements.csi_all)
    graph_manager.fill_histogram('reference-plane', calo_measurements.reference_plane)

def measure_ghost_energies(graph_manager, event) -> None:
    ghost_count = 0
    error_count = 0
    for ghost in event.ghost:
        ghost_count += 1
        error_count += 1
        if error_count % 3 != 1:
            continue
        particle_id = ghost.GetPDGID()
        x_mom = ghost.GetXmom()
        y_mom = ghost.GetYmom()
        z_mom = ghost.GetZmom()
        total_of_squared_moms = (x_mom ** 2) + (y_mom ** 2) + (z_mom ** 2)

        particle = pdg_id_to_particle(abs(particle_id))
        if particle is ParticleType.NEUTRON:
            energy = np.sqrt(PARTICLE_MASSES['neutron'] ** 2 + total_of_squared_moms) - PARTICLE_MASSES['neutron']
            graph_manager.fill_histogram('neutron-individual', energy)
        elif particle is ParticleType.PHOTON:
            energy = np.sqrt(total_of_squared_moms)
            graph_manager.fill_histogram('photon-individual', energy)
        elif particle is ParticleType.ELECTRON:
            energy = np.sqrt(PARTICLE_MASSES['electron'] ** 2 + total_of_squared_moms) - PARTICLE_MASSES['electron']
            graph_manager.fill_histogram('electron-individual', energy)
        else:
            print('Rare particle encountered with pdg', particle_id)

def measure_energy_and_fill_histogram(graph_manager, event, collect_method: str) -> None:
    if collect_method == 'calo':
        measure_calo_energies(graph_manager, event)
    elif collect_method == 'ghost':
        measure_ghost_energies(graph_manager, event)
    else:
        raise ValueError(f'Energy measurement method \'{collect_method}\' is unknown (must be \'calo\' or \'ghost\')')
