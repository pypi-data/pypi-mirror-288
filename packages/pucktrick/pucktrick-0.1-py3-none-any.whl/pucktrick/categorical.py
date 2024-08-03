
import random
from pucktrick.utils import *
import numpy as np

def noiseCategoricalStringNewExistingValues(train_df,column,percentage):
  extracted_list=sampleList(percentage,len(train_df[column]))
  noise_df= train_df.copy()
  unique_values = noise_df[column].unique()
  for i, value in enumerate(extracted_list):
     while True:
        new_value=np.random.choice(unique_values)
        if new_value != noise_df.loc[i, column]:
            noise_df.loc[i, column] = new_value
            break
  return noise_df


def noiseCategoricalStringExtendedExistingValues(original_df, train_df,column,percentage):
    noise_df= train_df.copy()
    noise_df['id1'] = range(len(noise_df))
    new_df,newPercentage=generateSubdf(original_df, noise_df,column,percentage)
    if newPercentage==0:
      return train_df
    modified_df= noiseCategoricalStringNewExistingValues(new_df,column,newPercentage)
    noise_df=mergeDataframe(noise_df,modified_df)
    return noise_df

def noiseCategoricalStringNewFakeValues(train_df,column,percentage):
  extracted_list=sampleList(percentage,len(train_df[column]))
  noise_df= train_df.copy()
  unique_values = noise_df[column].unique()
  for i, value in enumerate(extracted_list):
    noise_df.loc[i, column] = ''.join(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=5))
  return noise_df

def noiseCategoricalStringExstendedFakeValues(original_df, train_df,column,percentage):
    noise_df= train_df.copy()
    noise_df['id1'] = range(len(noise_df))
    new_df,newPercentage=generateSubdf(original_df, noise_df,column,percentage)
    if newPercentage==0:
      return train_df
    modified_df= noiseCategoricalStringNewFakeValues(new_df,column,newPercentage)
    noise_df=mergeDataframe(noise_df,modified_df)
    return noise_df


