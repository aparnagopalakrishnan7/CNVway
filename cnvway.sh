#!/bin/bash
#SBATCH --mem=32000
#SBATCH --time=0-10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aparna.gopalakrishnan@mail.utoronto.ca
#SBATCH -o cnvway-%j.out
#SBATCH -J cnvway

conda init --all
conda activate segway

from math import sqrt
import sys

from genomedata import Genome
from numpy import array, arcsinh
from path import Path
from segway import run
from segway.input_master import DTParamSpec
from segway.gmtk.input_master import (Covar, DenseCPT, DeterministicCPT,
                                      DPMF, InlineSection,
                                      InputMaster, Mean, NameCollection,
                                      Object)

GENOMEDATA_FILE = "genomedata"
TRAINDIR = "segway_output/traindir"
ANNOTATEDIR = "segway_output/annotatedir"

### Set up Directories and run train-init to generate all important files ###
genomedata = Path(GENOMEDATA_FILE)
traindir = Path(TRAINDIR)
annotatedir = Path(ANNOTATEDIR)

run.main(["train-init", "--num-labels=3", "--resolution=50", genomedata, traindir])

### Create InputMaster object and begin adding sections, starting with DT ###
class DTVariables(Object):
    num_segs = 3
    seg_countdowns_initial = [1, 1, 1]
    supervision_type = 0


DTObject = DTVariables
DT = DTParamSpec(DTObject)

input_master = InputMaster()
input_master["NAME_COLLECTION"][["collection_seg_LogR"]] = [["mx_seg0_subseg0_LogR", "mx_seg1_subseg0_LogR", "mx_seg2_subseg0_LogR"]]
input_master["DETERMINISTIC_CPT"][["seg_segCountdown", "frameIndex_ruler", "segTransition_ruler_seg_segCountDown_segCountDown", "seg_seg_copy", "subseg_subseg_copy"]] = [[[1, "CARD_SEG", "CARD_SEGCOUNTDOWN", "map_seg_segCountDown"], [1, "CARD_FRAMEINDEX", "CARD_RULER",  "map_frameIndex_ruler"], [4, "CARD_SEGTRANSITION", "CARD_RULER", "CARD_SEG", "CARD_SEGCOUNTDOWN", "CARD_SEGCOUNTDOWN", "map_segTransition_ruler_seg_segCountDown_segCountDown"], [1, "CARD_SEG", "CARD_SEG", "internal:copyParent"], [1, "CARD_SUBSEG", "CARD_SUBSEG","internal:copyParent"]]

input_master["DENSE_CPT"][["start_seg", "seg_subseg", "seg_seg", "seg_subseg_subseg", "segCountDown_seg_segTransition"]] = [[1/3, 1/3, 1/3], [[1.0], [1.0], [1.0]], [[0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]], [[[1.0]], [[1.0]], [[1.0]]], [[[0.99, 0.00999, 0.00001],
        [0.99, 0.00999, 0.00001],
        [0.99, 0.00999, 0.00001]],
        [[0.99, 0.01, 0.0],
        [0.99, 0.01, 0.0],
        [0.99, 0.01, 0.0]]]]

with Genome(genomedata) as genome:
    sums = genome.sums
    sums_squares = genome.sums_squares
    num_datapoints = genome.num_datapoints

mean = sums / num_datapoints
var = (sums_squares / num_datapoints) - mean ** 2

sd = sqrt(var)
means = [mean - 2 * sd, mean, mean + 2 * sd]
var_transformed = arcsinh(var)
means_transformed = arcsinh(means)

input_master["MEAN"][["mean_seg0_subseg0_LogR",  "mean_seg1_subseg0_LogR", "mean_seg2_subseg0_LogR"]] = [means_transformed[0], means_transformed[1], means_transformed[2]]
input_master["COVAR"][["covar_LogR"]] = [var_transformed]
input_master["DPMF"][["dpmf_always"]] = [1.0]
input_master["MC"][["1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_asinh_norm_seg0_subseg0_LogR", "1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_asinh_norm_seg1_subseg0_LogR", "1 COMPONENT_TYPE_DIAG_GAUSSIAN mc_asinh_norm_seg2_subseg0_LogR"]] = ["mean_seg0_subseg0_LogR covar_LogR", "mean_seg1_subseg0_LogR covar_LogR", "mean_seg2_subseg0_LogR covar_LogR"]
input_master["MX"][["1 mx_seg0_subseg0_LogR", "1 mx_seg1_subseg0_LogR", "1 mx_seg2_subseg0_LogR"]] = ["1 dpmf_always mc_asinh_norm_seg0_subseg0_LogR", "1 dpmf_always mc_asinh_norm_seg1_subseg0_LogR", "1 dpmf_always mc_asinh_norm_seg2_subseg0_LogR"]
input_master_path = traindir / "params" / "input.master"

### Write out to input master ###
with open(input_master_path, "w") as filename:
    print("#include ", '"', traindir, '/auxiliary/segway.inc"\n\n', sep="",
          file=filename)
    print(DT, file=filename)
    print(input_master, file=filename)

run.main(["annotate", genomedata, traindir, annotatedir])
