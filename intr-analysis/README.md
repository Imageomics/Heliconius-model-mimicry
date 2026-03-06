# INTR Analysis

This analysis uses interpretable deep learning approaches to identify the wing pattern features used by neural networks to classify mimicry. Specifically, we apply INTR (Paul 2024) and Grad-CAM to visualize model attention and determine which traits contribute most strongly to mimic classification.

We also evaluate how these attention patterns change across different simulated visual acuities.

To run this analysis, clone the [INTR repo](https://github.com/imageomics/INTR), follow their installation instructions, and replace the following two files with those contained in this directory, adding also the `bash_scripts/` directory.
1. `models/intr.py`
2. `main.py`

TODO: Check on this procedure. Where does notebook match in pipeline.
