import tifffile
from glob2 import glob
import numpy as np
import pandas as pd

data_dir = r"/example_data"

# mask_files = glob(data_dir + "/*.tif")[:5]
#
# masks = []
#
# for path in mask_files:
#
#     mask = tifffile.imread(path)
#
#     masks.append(mask)
#
# masks = np.stack(masks)
#
# tifffile.imwrite("../../example_data/mask_stack.tif", masks)


csv_files = glob(data_dir + "/*.csv")

df = pd.read_csv(csv_files[0])

df = df[df["frame"] <=5]

df.to_csv(csv_files[0], index=False)

with open('celllist.pickle', 'wb') as handle:
    pickle.dump(celllist, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('celllist.pickle', 'rb') as handle:
    celllist = pickle.load(handle)