from collections import OrderedDict
from segway_gmtk_params.py import SegwayInputMaster, SegwayDenseCPT, SegwayDeterministicCPT, SegwayDPMF, SegwayMean, \
    SegwayMC, SegwayMX, SegwayCovar, SegwayNameCollection
from gen_gmtk_params.py import InputMaster, DenseCPT, DeterministicCPT, DPMF, Mean, \
    MC, MX, Covar, NameCollection

im = SegwayInputMaster()
im.track_names = ["t1", "t2"]
im.num_subsegs = 2
im.num_segs = 3
im.mean_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6]
im.covar_values = [0.7, 0.8]
print(im)
