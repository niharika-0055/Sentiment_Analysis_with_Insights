import pandas as pd
import numpy as np

df_reader = pd.read_json(r"D:\100 days internship project\final_project\Clothing_Shoes_and_Jewelry.json", lines =  True ,chunksize = 1000000 )

counter = 1
for chunk in df_reader:
    new_df = pd.DataFrame(chunk[['overall', 'reviewText','summary']])
    
    new_df1 = new_df[new_df['overall'] == 1].sample(4000)
    new_df2 = new_df[new_df['overall'] == 2].sample(4000)
    new_df3 = new_df[new_df['overall'] == 4].sample(4000)
    new_df4 = new_df[new_df['overall'] == 5].sample(4000)
    new_df5 = new_df[new_df['overall'] == 3].sample(8000)
    
    new_df6 = pd.concat([new_df1, new_df2, new_df3, new_df4, new_df5], axis = 0,ignore_index = True)
    
    new_df6.to_csv(str(counter)+'.csv', index = False)
    counter = counter+1
    
    

from glob import glob
#the glob module is used to retrieve the files
#or pathnames matching a pattern

filenames = glob('*.csv')

#['1.csv','2.csv',..........,'33.csv']

dataframes = []

for f in filenames:
    dataframes.append(pd.read_csv(f))

#[..........]
    

finaldf = pd.concat(dataframes, axis = 0, ignore_index = True)

finaldf.to_csv(r"D:\100 days internship project\final_project\balanced_reviews.csv", index = False)
