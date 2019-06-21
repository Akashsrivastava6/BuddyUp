import pandas as pd
import re


tweets=[]
def preprocess(twt):
    df = pd.DataFrame()

    df['tweets']=twt
    df['tweets']=remove_non_ascii(df['tweets'])
    df['tweets']=remove_newline(df['tweets'])
    df['tweets']=remove_punctuation(df['tweets']) 
    
    remove_emoticon_replacement(df) 
    df_processed = pd.DataFrame()
    df_processed['tweets'] = tweets
    df_processed['tweets']=remove_non_ascii(df_processed['tweets'])
    df_processed['tweets']=remove_newline(df_processed['tweets'])
    df_processed['tweets']=remove_punctuation(df_processed['tweets'])
    #df_processed['tweets']=remove_unwanted_spaces(df_processed['tweets'])
    df_processed['tweets']=remove_emoticon_replacement(df_processed)

    return df_processed['tweets']

def remove_non_ascii(dff):
    #s2 = str(df) 
    s2 = dff.str.replace("[^\\x00-\\x7F]", "abcde")
    return s2



def remove_newline(dff):
     #s2 = str(df) 
     s2= dff.str.replace("\r\n", " ")
     return s2
  


def remove_punctuation(df):
    #s2 = str(df) 
    s2=df.str.replace('[^\w\s]',' ')
    return s2


# Creating a function remove_unwanted_spaces() to remove all unwanted spaces
def remove_unwanted_spaces(df):
    df= re.sub('\s+',' ',df)
    df=df.strip() # the strip() function removes any trailing spaces from the begining snd the end of the text
    return s
 



def remove_emoticon_replacement(df):
    j=0
    for i in range(len(df['tweets'])):
        x = re.search("(abcde)",df.loc[i]['tweets'])
        if (x):
           j=j+1 
        else:
            tweets.append(df.loc[i]['tweets'])


# df_processed = pd.DataFrame()
# df_processed['tweets'] = tweets