from gen_gmtk_params import NewInputMaster, NameCollection, MC, Mean, MX, DeterministicCPT, \
    DenseCPT, DPMF, Covar
import gen_gmtk_params

im = NewInputMaster()
col0 = NameCollection("col0", "name1")
col1 = NameCollection("col1", "name2", "name3")
dense_cpt0 = DenseCPT(obj_name="seg_seg", parent_card=3, self_card=3,
                      prob=[[0.333333333333, 0.333333333333, 0.333333333333],
  [0.333333333333, 0.333333333333, 0.333333333333],
  [0.333333333333, 0.333333333333, 0.333333333333]])
det_cpt0 = DeterministicCPT(obj_name="det_cpt0_name", parent_card="CARD_SEG",
                            self_card="CARD_SEGCOUNTDOWN", dt_name="map_seg_segCountDown")
det_cpt1 = DeterministicCPT(obj_name="subseg_subseg_copy", parent_card="CARD_SUBSEG",
                            self_card="CARD_SUBSEG", dt_name=gen_gmtk_params.CP)
mean0 = Mean("mean_name0", 1.0)
mean1 = Mean("mean_name1", 2.0, 3.0)
covar1 = Covar("covar_track1", 0.1, 0.2)
dpmf1 = DPMF("dpmf_name", 0.6, 0.4)
mc1 = MC(obj_name="mc_name1", dim=26, type=gen_gmtk_params.MC_TYPE, mean=mean0,
         covar=covar1)
mc2 = MC(obj_name="mc_name2", dim=26, type=0, mean=mean1, covar=covar1)
mx1 = MX(obj_name="mx_name1", dim=26, dpmf=dpmf1, components=[mc1, mc2])
gmtk_obj = [col0, col1, dense_cpt0, det_cpt0, det_cpt1, mean0, mean1, covar1,
            dpmf1, mc1, mc2, mx1]
im.update(gmtk_obj)
print(im)
