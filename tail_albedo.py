import os
import glob
import numpy as np
import uproot
import matplotlib.pyplot as plt
import numpy as np
import ROOT

energy = 69
geom = 'sphere_array'

PROTON_MASS = 938.272
NEUTRON_MASS = 939.565
ELECTRON_MASS = 0.511

known = [11,22,2112]

#ring1_lyso = [300003,300005,300007,300009,300011]
#ring2_lyso = [300013,300015,300017,300019,300021,300023,300025,300027,300029,300031]

pent_lyso = [300001]
ring1_lyso = [300021,300041,300061,300081,300101]
ring2_lyso = [300121,300141,300161,300181,300201,300211,300241,300261,300281,300301]

pent_csi = [310001]
ring1_csi = [310021,310041,310061,310081,310101]
ring2_csi = [310121,310141,310161,310181,310201,310221,310241,310261,310281,310301]


libpath = os.path.join(os.getenv("PIONEERSYS"), "install/lib/libPiRootDict.dylib")
ROOT.gSystem.Load(libpath)

os.chdir("/Users/andou/Documents/Repos/tail-albedo-plotter/root files/")
file_list = []
values = []

#for filepath in glob.glob("/home/obeesley/PIONEER/resolution/small_array/69MeV/job*/*/*.root"):
for filepath in glob.glob("/Users/andou/Documents/Repos/tail-albedo-plotter/root files/*.root"):
#for filepath in glob.glob("/mnt/c/Users/Omar/research/pioneer/PIONEER/myscripts/*/inf/*.root"):
    file_list.append(filepath)

chain = ROOT.TChain("sim")
h1 = ROOT.TH1F("h1", "Edep",75, 1, 75)
h1.SetLineColor(1)
#h1.GetXaxis().SetTitle("Energy [MeV]")
h2 = ROOT.TH1F("h2", "Edep",75, 1, 75)
h2.SetLineColor(2)
h3 = ROOT.TH1F("h3", "Edep",75, 1, 75)
h3.SetLineColor(3)
h4 = ROOT.TH1F("h4", "Edep",75, 1, 75)
h4.SetLineColor(4)
h5 = ROOT.TH1F("h5", "Edep",75, 1, 75)
h5.SetLineColor(5)
h6 = ROOT.TH1F("h6", "Edep",75, 1, 75)
h6.SetLineColor(6)
h7 = ROOT.TH1F("h7", "Edep",75, 1, 75)
h7.SetLineColor(7)
h8 = ROOT.TH1F("h8", "Edep",75, 1, 75)
h8.SetLineColor(8)
h9 = ROOT.TH1F("h9", "Edep",100, -0.5, 14.5)
h9.SetLineColor(9)
h10 = ROOT.TH1F("h10", "Edep",100, -0.5, 14.5)
h10.SetLineColor(1)
h11 = ROOT.TH1F("h11", "Edep",100, -0.5, 14.5)
h11.SetLineColor(1)
counterr = 0
count3 = 0
pdg_list = []
for file in file_list:
    chain.Add(file)
for entry in chain:
    #if counter > 1000000:
    #    break
    etot = 0
    etot_pent_lyso = 0
    etot_ring1_lyso = 0
    etot_ring2_lyso = 0
    etot_else_lyso = 0
    etot_pent_csi = 0
    etot_ring1_csi = 0
    etot_ring2_csi = 0
    etot_else_csi = 0
    etot_ref_plane = 0
    etot_gamma = 0
    eind_gamma = 0
    '''
    for calo in entry.calo:
        energy = calo.GetTotalEnergyDeposit()
        energy_ind = calo.GetEdep()
        identity = calo.GetCaloID()
        pdg = calo.GetPDGID()
        #print(identity,energy)
        if (int(identity) in pent_lyso):
            etot_pent_lyso += energy
        elif (int(identity) in pent_csi):
            etot_pent_csi += energy
        elif (int(identity) in ring1_lyso):
            etot_ring1_lyso += energy    
        elif (int(identity) in ring1_csi):
            etot_ring1_csi += energy
        elif (int(identity) in ring2_lyso):
            etot_ring2_lyso += energy
        elif (int(identity) in ring2_csi):
            etot_ring2_csi += energy
#        if int(identity) < 310000:
        elif ((int(identity) < 310000) and (int(identity)> 2000)):
            etot_else_lyso += energy
        elif int(identity) >= 310000:
            etot_else_csi += energy 
        elif (int(identity) < 2000):
            etot_ref_plane += energy
        if (int(identity) < 2000):
            counterr += 1
            if counterr < 5:
                print(pdg)
                print(energy_ind[0])
            if energy_ind[0] != energy:
                print('not the same')
                print(energy_ind)
                print(energy)
            for i in range(len(pdg)):
                h10.Fill(energy_ind[i])
                etot_gamma += energy_ind[i]

    etot_ring1_lyso += etot_pent_lyso
    etot_ring2_lyso += etot_ring1_lyso
    etot_else_lyso += etot_ring2_lyso
    etot_ring1_csi += etot_pent_csi
    etot_ring2_csi += etot_ring1_csi
    etot_else_csi += etot_ring2_csi

    etot_pent = etot_pent_lyso + etot_pent_csi
    etot_ring1 = etot_ring1_lyso + etot_ring1_csi
    etot_ring2 = etot_ring2_lyso + etot_ring2_csi
    etot_else = etot_else_lyso + etot_else_csi

    #h1.Fill(etot_pent)
    #h2.Fill(etot_ring1)
    #h3.Fill(etot_ring2)
    #h4.Fill(etot_else)

    #h3.Fill(etot_ring2)
    #h9.Fill(etot_ref_plane)
    if etot_gamma > 0:
        h9.Fill(etot_gamma)
    '''
    ghost_count = 0
    tot_energy = 0
    list_pdgs = []
    for ghost in entry.ghost:
        ghost_count +=1
        counterr += 1
        if ((counterr % 3) != 1):
            continue
        count3 += 1
        pdg = ghost.GetPDGID()
        #list_pdgs.append(pdg)
        xmom = ghost.GetXmom()
        ymom = ghost.GetYmom()
        zmom = ghost.GetZmom()
        mom_tot_sq = (xmom ** 2) + (ymom ** 2) + (zmom ** 2)
        if pdg == 2112:
            energy = np.sqrt((NEUTRON_MASS ** 2) + mom_tot_sq) - NEUTRON_MASS
            h10.Fill(energy)
        elif pdg == 22:
            energy = np.sqrt(mom_tot_sq)
            h9.Fill(energy)
        elif abs(pdg) == 11:
            energy = np.sqrt((ELECTRON_MASS ** 2) + mom_tot_sq) - ELECTRON_MASS
            #if pdg == 11:
            #    h11.Fill(energy)
            #if pdg == -11:
            #    h9.Fill(energy)
            #h11.Fill(energy)
        elif known.count(pdg) == 0:
            print('Rare particle',pdg)
        tot_energy += energy
        #if tot_energy > 8:
        #    print(list_pdgs)
        #h9.Fill(tot_energy)

print(count3)


#    h1.Fill(etot_pent_lyso)
#    h2.Fill(etot_ring1_lyso)
#    h3.Fill(etot_ring2_lyso)
#    h4.Fill(etot_else_lyso)
#    h5.Fill(etot_pent_csi)
#    h6.Fill(etot_ring1_csi)
#    h7.Fill(etot_ring2_csi)
#    h8.Fill(etot_else_csi)

#frac_pent = h1.Integral(0,56) / h1.Integral()
#frac_ring1 = h2.Integral(0,56) / h2.Integral()
#frac_ring2 = h3.Integral(0,56) / h3.Integral()
#frac_full = h4.Integral(0,56) / h4.Integral()

#print('Tail fraction for pent is {}'.format(frac_pent))
#print('Tail fraction for ring1 is {}'.format(frac_ring1))
#print('Tail fraction for ring2 is {}'.format(frac_ring2))
#print('Tail fraction for full is {}'.format(frac_full))
print(h9.GetEntries())
#print(h11.GetEntries())

canv = ROOT.TCanvas()
hs = ROOT.THStack("hs","Tail Energy Distributions for Albedo;Energy [MeV];Counts")
#hs.Add(h1)
#hs.Add(h2)
#hs.Add(h3)
#hs.Add(h4)
#hs.Add(h5)
#hs.Add(h6)
#hs.Add(h7)
#hs.Add(h8)
hs.Add(h9)
#hs.Add(h10)
hs.Add(h11)
hs.Draw("nostack")

#legend = ROOT.TLegend (0.77 ,0.68 ,0.92 ,0.83)
#legend.AddEntry(h1,"Pent")
#legend.AddEntry(h2 ,"Ring 1 + Pent")
#legend.AddEntry(h3 ,"Ring 1 + 2 + Pent")
#legend.AddEntry(h4 ,"Full Calo")
#legend.AddEntry(h5,"Pent CsI")
#legend.AddEntry(h6 ,"Ring 1 + Pent CsI")
#legend.AddEntry(h7 ,"Ring 1 + 2 + Pent CsI")
#legend.AddEntry(h8 ,"Full Calo CsI")
#legend.SetLineWidth(0)
#legend.Draw(" same ")

#h1.Draw()
#h2.Draw()
#h3.Draw("same")
#h4.Draw()
canv.SetLogy(True)
canv.Update()
canv.Draw()
input()