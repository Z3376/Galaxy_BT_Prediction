import argparse
import subprocess
import os
import time

def get_model(im_size):
    inpt = keras.layers.Input((im_size,im_size,3))
    base_model = keras.applications.Xception(input_tensor=inpt,weights=None,include_top=False,pooling='avg')
    x = base_model.output
    out = keras.layers.Dense(1,activation='sigmoid')(x)
    inf_model = keras.models.Model(inpt,out)
    return inf_model

def get_pred(model,generator):
    pred = model.predict_generator(generator,steps=len(ls)//batch_size+1)
    pred = pred[:,0]
    return pred

parser = argparse.ArgumentParser()
parser.add_argument("-i",help="Input file path",default="input")
parser.add_argument("-o",help="Output file path",default="results.csv")
parser.add_argument("-w",help="Trained weights path", default="bt_xception_80_20.h5")
parser.add_argument("-b",type=int,help="Batch size. Higher value means faster processing but more memory utilisation.", default=256)
args = parser.parse_args()

import keras
import pandas as pd

input_path = args.i
csv_path = args.o
weights_path = args.w
batch_size = args.b
im_size = 128

inf_model = get_model(im_size)
inf_model.load_weights(weights_path)

p = subprocess.Popen(['ls',input_path],stdout=subprocess.PIPE)
ls = str(p.communicate()[0],'utf-8').split('.jpg\n')[:-1]

i = 0
while(i<len(ls)):
    try:
        size = os.path.getsize(input_path+'/'+ls[i]+'.jpg')
        if(size==0):
            ls.pop(i)
            print(ls[i]+" will not be used. This file is empty.")
            i-=1
    except:
        ls.pop(i)
        print(ls[i]+" will not be used. This file is not a jpeg.")
        i-=1
    finally:
        i+=1

label_df = pd.DataFrame([ls[i]+'.jpg' for i in range(len(ls))])
label_df.columns = ["Image"]

test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_dataframe(dataframe=label_df,
                                                  directory=input_path,
                                                  x_col="Image",
                                                  class_mode=None,
                                                  target_size=(im_size,im_size),
                                                  batch_size=batch_size,
                                                  shuffle=False)

t0 = time.time()
pred = get_pred(inf_model,test_generator)
t1 = time.time()
print("Prediction done in "+str(t1-t0)+" seconds.")

label_df['B/T'] = pred
label_df.to_csv(csv_path,index=None)

