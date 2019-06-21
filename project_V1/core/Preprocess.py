import pandas as pd
import re


#tweets=[]
def preprocess(tweets):       
   df_processed = pd.DataFrame()
   df_processed['tweets'] = tweets
   df_processed['tweets']=remove_non_ascii(df_processed['tweets'])
   df_processed['tweets']=remove_newline(df_processed['tweets'])
   df_processed['tweets']=remove_punctuation(df_processed['tweets'])
   df_processed['tweets']=remove_unwanted_spaces(df_processed['tweets'])   
   for i in range(len(df_processed['tweets'])):
      df_processed.loc[i]['tweets']=remove_unwanted_spaces(df_processed.loc[i]['tweets'])
   df_processed=remove_emoticon_replacement(df_processed)
   return df_processed

def remove_non_ascii(dff):
   #s2 = str(df) 
   s1 = dff.str.replace("[^\\x00-\\x7F]", "abcde")
   return s1

def remove_newline(dff):
   #s2 = str(df) 
   s2= dff.str.replace("\r\n", " ")
   return s2

def remove_punctuation(df):
   #s2 = str(df) 
   s3=df.str.replace('[^\w\s]',' ')
   return s3
#
# Creating a function remove_unwanted_spaces() to remove all unwanted spaces
def remove_unwanted_spaces(s):
   s4= re.sub('\s+',' ',s)
   s4=s4.strip() # the strip() function removes any trailing spaces from the begining snd the end of the text
   return s4

def remove_emoticon_replacement(df):
   twt = []
   j=0
   for i in range(len(df['tweets'])):
      x = re.search("(abcde)",df.loc[i]['tweets'])
      if (x):
         j=j+1 
      else:
         twt.append(df.loc[i]['tweets'])
   return twt


# df_processed = pd.DataFrame()
# df_processed['tweets'] = tweets