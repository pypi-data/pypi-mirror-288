import matplotlib.pyplot as plt
from glob2 import glob
import pandas as pd
import tifffile
import numpy as np
import os
import bactfit
from glob2 import glob
from bactfit.cell import CellList, Cell, ModelCell
from bactfit.preprocess import data_to_cells, mask_to_cells
import pickle
from bactfit.fileIO import save, load


if __name__ == '__main__':

    mask = tifffile.imread("mask2.tif") # Load mask stack
    locs = pd.read_csv("localisations2.csv") # Load picasso localisations

    celllist = mask_to_cells(mask)  # Create celllist from binary mask
    celllist.add_localisations(locs)  # Add localisations to celllist



