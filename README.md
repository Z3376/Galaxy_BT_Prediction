# Galaxy_BT_Prediction
Galaxy B/T prediction as described in "Predicting bulge to total luminosity ratio of galaxies using deeplearning" submitted at MNRAS.

To predict B/T from galaxy images:
Step 1: git clone <this_repo>
Step 2: pip install requirements.txt
Step 3: python bt_predict.py {optional args}

Optional args:
-h : Help.
-i : Input folder path. The folder should contain 128x128 jpg images. 
-o : Output csv path.
-w : Trained weights path. .h5 file provided in the repo.
-b : Batch size.
