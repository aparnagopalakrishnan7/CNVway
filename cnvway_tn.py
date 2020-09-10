from math import sqrt
import sys

from genomedata import Genome
from numpy import array, arcsinh, ndarray 
from path import Path
from segway import run
from segway.input_master import DTParamSpec
import input_master_draft

GENOMEDATA_FILE = "hmmcopy_genomedata/tumour-normal_hmmcopy.genomedata"
TRAINDIR = "36-t-n_segway_output/traindir"
ANNOTATEDIR = "36-t-n_segway_output/annotatedir"

genomedata = Path(GENOMEDATA_FILE)
traindir = Path(TRAINDIR)
annotatedir = Path(ANNOTATEDIR)
print("train-init start")
run.main(["train-init","--num-labels=3", "--resolution=30000","--distribution=norm" , "--include-coords=log2_hmmcopy/tumour-normal_merge_include_coords.bed",genomedata, traindir])
print("train init finish")
# "--seg-table=seg_table.bed"
class DTVariables(input_master_draft.Object):
    num_segs = 3
    seg_countdowns_initial = [1, 1, 1]
    supervision_type = 0 

DTObject = DTVariables 
DT = DTParamSpec(DTObject) 

input_master = input_master_draft.InputMaster() 

input_master["NAME_COLLECTION"][["collection_seg_tn"]] = [["mx_seg0_subseg0_tn","mx_seg1_subseg0_tn", "mx_seg2_subseg0_tn"]]

input_master["DETERMINISTIC_CPT"][["seg_segCountDown", "frameIndex_ruler", "segTransition_ruler_seg_segCountDown_segCountDown", "seg_seg_copy", "subseg_subseg_copy"]] = [[1, "CARD_SEG", "CARD_SEGCOUNTDOWN" , "map_seg_segCountDown"], [1, "CARD_FRAMEINDEX", "CARD_RULER", "map_frameIndex_ruler"], [4, "CARD_SEGTRANSITION", "CARD_RULER", "CARD_SEG" , "CARD_SEGCOUNTDOWN", "CARD_SEGCOUNTDOWN" ,"map_segTransition_ruler_seg_segCountDown_segCountDown"], [1, "CARD_SEG", "CARD_SEG", "internal:copyParent"], [1, "CARD_SUBSEG", "CARD_SUBSEG", "internal:copyParent"]]
# supervisionLabel_seg_alwaysTrue = 2, "CARD_SUPERVISIONLABEL", "CARD_SEG", "CARD_BOOLEAN", "map_supervisionLabel_seg_alwaysTrue"

#input_master["DENSE_CPT"][["start_seg", "seg_subseg", "seg_seg", "seg_subseg_subseg", "segCountDown_seg_segTransition"]] = [[0.333333333333, 0.333333333333, 0.333333333333],[[1.0], [1.0], [1.0]], [[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]], [[[1.0], [1.0], [1.0]]], [[[0.0, 0.909090909091, 0.0909090909091], [0.0, 0.909090909091, 0.0909090909091], [0.0, 0.909090909091, 0.0909090909091]], [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0]]]]

input_master["DENSE_CPT"][["start_seg", "seg_subseg", "seg_seg", "seg_subseg_subseg", "segCountDown_seg_segTransition"]] = [[0.333333333333, 0.333333333333, 0.333333333333],[[1.0], [1.0], [1.0]], [[1/3, 1/3, 1/3], [1/3, 1/3, 1/3], [1/3, 1/3, 1/3]], [[[1.0], [1.0], [1.0]]], [[[0.99, 0.00999, 0.00001], [0.99, 0.00999, 0.00001], [0.99, 0.00999, 0.00001]], [[0.99, 0.01, 0.0], [0.99, 0.01, 0.0], [0.99, 0.01, 0.0]]]]
#[[0.99, 0.00999, 0.00001], [0.99, 0.00999, 0.00001], [0.99, 0.00999, 0.00001]], [[0.99, 0.01, 0.0], [0.99, 0.01, 0.0], [0.99, 0.01, 0.0]]
# evenly spaced means between min-max of log2 copy number values 

input_master["MEAN"][["mean_seg0_subseg0_tn", "mean_seg1_subseg0_tn", "mean_seg2_subseg0_tn"]] = [[-0.4], [-0.11], [0.14]]

input_master["COVAR"][["covar_tn"]] = [[0.0966004105351]]

input_master["DPMF"][["dpmf_always"]] = [[1.0]]

input_master["MC"][["1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_norm_seg0_subseg0_tn", "1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_norm_seg1_subseg0_tn", "1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_norm_seg2_subseg0_tn"]] = ["mean_seg0_subseg0_tn covar_tn", "mean_seg1_subseg0_tn covar_tn", "mean_seg2_subseg0_tn covar_tn"]

input_master["MX"][["1 mx_seg0_subseg0_tn", "1 mx_seg1_subseg0_tn", "1 mx_seg2_subseg0_tn"]]= ["1 dpmf_always mc_norm_seg0_subseg0_tn", "1 dpmf_always mc_norm_seg1_subseg0_tn", "1 dpmf_always mc_norm_seg2_subseg0_tn"]

#print("run train run")
# "--cluster-opt=-p hoffmangroup -t 0-00:20" 
#run.main(["train-run", "--max-train-rounds=15", genomedata, traindir])
#print("finish train run")
#print("train finish")
#run.main(["train-finish", genomedata, traindir])
#print("finished train-finish")


input_master_path = traindir / "params" / "input.master"

### Write out to input master ###
with open(input_master_path, "w") as filename:
    print("#include ", '"', traindir, '/auxiliary/segway.inc"\n\n', sep="", file=filename)
    print(DT, file=filename)
    print(input_master, file=filename)

print("run annotate")
run.main(["annotate", "--include-coords=log2_hmmcopy/tumour-normal_merge_include_coords.bed" , genomedata, traindir, annotatedir])
print("finish annotate")
