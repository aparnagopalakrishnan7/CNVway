## listing 1

from gmtk.input_master import Covar, DPMF, DenseCPT, DiagGaussianMC, InputMaster, MX, Mean, NameCollection

input_master = InputMaster()
input_master.dense_cpt["start"] = DenseCPT.uniform_from_shape(3)
input_master.dense_cpt["transition"] = DenseCPT.uniform_from_shape(3, 3, self=0.5)

input_master.mean["deletion"] = Mean(-0.4)
input_master.mean["neutral"] = Mean(-0.14)
input_master.mean["gain"] = Mean(-0.11)

input_master.covar["tied"] = Covar(0.1)
input_master.dpmf["uniform"] = DPMF.uniform_from_shape(1)

for label in input_master.mean:
    input_master.mc[label] = DiagGaussianMC(mean=label, covar="tied")
    input_master.mx[label] = MX("uniform", label)

input_master.name_collection["emission"] = NameCollection("deletion", "neutral", "gain")

input_master.save("input.master")

## listing 2

from segway import run

run.main(["train-init", "--num-labels=3", "--resolution=30000", "--distribution=norm",
          "--include-coords=include_coords.bed", "--input-master=input.master"
          "--structure=segway.str"
          "tumor-normal.genomedata", "traindir"])

run.main(["annotate", "--include-coords=include_coords.bed",
          "tumor-normal.genomedata", "traindir", "annotatedir"])
