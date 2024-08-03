import random
import numpy as np


def sampleList(percentage, maxValueList ):
    values = int(maxValueList * (percentage))
    extracted_List= random.sample(range(1, maxValueList+ 1), values)
    return extracted_List

def generateSubdf(original_df, train_df,column,percentage ):
    rowsToChange=len(original_df[column])*percentage
    dif = original_df[column] != train_df[column]
    diff_number = dif.sum()
    new_rowsToChange=rowsToChange-diff_number
    if new_rowsToChange<=0:
      newPercentage=0
      return train_df,newPercentage
    noise_df= train_df.copy()
    noise_df['id1'] = range(len(noise_df))
    or_df=original_df.copy()
    or_df['id1'] = range(len(or_df))
    mask = or_df[column] == noise_df[column]
    new_df = noise_df[mask]
    new_df = new_df.reset_index(drop=True)
    newPercentage=new_rowsToChange/len(new_df)
    return new_df,newPercentage

def mergeDataframe(noise_df,modified_df):

    merged_df = noise_df.merge(modified_df, on='id1', how='left', suffixes=('_df1', '_df2'))
    new_array = [string for string in noise_df.columns if string != 'id1']
    for col in new_array:
      noise_df[col] = merged_df[col + '_df2'].fillna(merged_df[col + '_df1'])
    noise_df = noise_df.drop('id1', axis=1)
    return noise_df
