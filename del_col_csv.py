#import pandas as pd 
#f = pd.read_csv("temp_normal_table.csv")
#keep_col = ["chr", "start", "end", "value", "copy"]
#new_f = f[keep_col]
#new_f.to_csv("final_normal_copy_table.csv", index=False)
import csv
with open("log2_hmmcopy/normal_copy_table.csv", "r") as source:
    reader = csv.reader(source, delimiter='\t')
    with open("test.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
            if r[7] == "FALSE":
                writer.writerow((r[1], r[2], r[3], r[11]))
