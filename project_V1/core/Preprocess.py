import pandas as pd
import re
  

def preprocess(twt):
   
   df_processed = pd.DataFrame()
   df_processed['tweets'] = twt
   df_processed['tweets']=remove_non_ascii(df_processed['tweets'])
   df_processed['tweets']=remove_newline(df_processed['tweets'])
   df_processed['tweets']=remove_punctuation(df_processed['tweets'])
   #df_processed['tweets']=remove_unwanted_spaces(df_processed['tweets'])
   for i in range(len(df_processed['tweets'])):
      df_processed.loc[i]['tweets']=remove_unwanted_spaces(df_processed.loc[i]['tweets'])
   tweet,ind=remove_emoticon_replacement(df_processed)

   return tweet,ind

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
def remove_unwanted_spaces(s):
   s= re.sub('\s+',' ',s)
   s=s.strip() # the strip() function removes any trailing spaces from the begining snd the end of the text
   return s
 



def remove_emoticon_replacement(df):
   tweets=[]
   ind=[]
   j=0
   for i in range(len(df['tweets'])):
      x = re.search("(abcde)",df.loc[i]['tweets'])
      if (x):
         ind.append(i)
         tweets.append("abcde")
      else:
         tweets.append(df.loc[i]['tweets'])
   return tweets,ind
# df_processed = pd.DataFrame()
# df_processed['tweets'] = tweets

def preprocess1(tmp3):
   words=pd.read_csv("EmotionLookupTableGeneral.txt",sep="\\t",header=None,names=['word','score'])
   neg_words=pd.read_csv("NegatingWordList.txt",sep="\\t",header=None,names=['word'])

 


   str1=""
   for a in range(len(words['word'])):
      if a != len(words['word'])-1:
         str1=str1+"^[#]*"+words.iloc[a]['word']+"$,"
      else:
         str1=str1+"^[#]*"+words.iloc[a]['word']+"$"
   str1=str1.split(",")





   tmp4=[]

   for a in range(len(tmp3)):
      sum_score=0
      counter=0
      sum_list=""
      #regex = re.compile('[%s]' % re.escape(string.punctuation))
      regex=re.compile('[!.,?]')
      aa=regex.sub(' . ', tmp3[a])
      #print(aa)
      ll=aa.split(" ")
      flag=0
      for a1 in ll:
         a1=a1.lower()
         
         if neg_words['word'].isin([a1]).any():
                  flag=1
         elif re.match("[!,.?]$",a1):
                  
                  flag=0
         #for la in l:
         for ans,item in enumerate(str1):
               #print(str)
               if re.match('%s'%item,a1):
                  #print(re.match('%s'%str1[ans],a1))
                  if flag==0:
                     sum_score=sum_score+words.iloc[ans]['score']
                     sum_list=sum_list+words.iloc[ans]['word']+" "+str(words.iloc[ans]['score'])+" "
                     counter=counter+1  
                  else:
                     sum_score=sum_score+(words.iloc[ans]['score']*(-1))
                     sum_list=sum_list+words.iloc[ans]['word']+" "+str(words.iloc[ans]['score'])+" "
                     counter=counter+1  
               #print(words[word])
      if counter!=0:
         tmp4.append([tmp3[a],sum_score,counter,sum_score/counter])
      else:
         tmp4.append([tmp3[a],sum_score,counter,0])
   tmp4=pd.DataFrame(tmp4,columns=['Tweet','Sum_score','Counter','Score'])    

   return tmp4