import pandas as pd
import re
from autocorrect import spell
  

# def preprocess(twt):
   
#    df_processed = pd.DataFrame()
#    df_processed['tweets'] = twt
#    df_processed['tweets']=remove_non_ascii(df_processed['tweets'])
#    df_processed['tweets']=remove_newline(df_processed['tweets'])
#    df_processed['tweets']=remove_punctuation(df_processed['tweets'])
#    #df_processed['tweets']=remove_unwanted_spaces(df_processed['tweets'])
#    for i in range(len(df_processed['tweets'])):
#       df_processed.loc[i]['tweets']=remove_unwanted_spaces(df_processed.loc[i]['tweets'])
#    tweet,ind=remove_emoticon_replacement(df_processed)

#    return tweet,ind

# def remove_non_ascii(dff):
#     #s2 = str(df) 
#    s2 = dff.str.replace("[^\\x00-\\x7F]", "abcde")
#    return s2



# def remove_newline(dff):
#      #s2 = str(df) 
#    s2= dff.str.replace("\r\n", " ")
#    return s2
  


# def remove_punctuation(df):
#     #s2 = str(df) 
#    s2=df.str.replace('[^\w\s]',' ')
#    return s2


# # Creating a function remove_unwanted_spaces() to remove all unwanted spaces
# def remove_unwanted_spaces(s):
#    s= re.sub('\s+',' ',s)
#    s=s.strip() # the strip() function removes any trailing spaces from the begining snd the end of the text
#    return s
 



# def remove_emoticon_replacement(df):
#    tweets=[]
#    ind=[]
#    j=0
#    for i in range(len(df['tweets'])):
#       x = re.search("(abcde)",df.loc[i]['tweets'])
#       if (x):
#          ind.append(i)
#          tweets.append("abcde")
#       else:
#          tweets.append(df.loc[i]['tweets'])
#    return tweets,ind
# df_processed = pd.DataFrame()
# df_processed['tweets'] = tweets

def preprocess1(tmp3):
   words=pd.read_csv("core/impdata3.csv")
   neg_words=pd.read_csv("core/NegatingWordList.txt",sep="\\t",header=None,names=['word'])
   emo=pd.read_csv("core/emoticons.csv",sep=",")
 
   emo_dict=dict(zip(emo['Char'],emo['score2']))

   


   word_dict=dict(zip(words['word'],words['score']))


   tmp4=[]
   
   
   for a in range(len(tmp3)):
      sum_score=0
      counter=0
      sum_list=""
    
    
      for j in tmp3[a]:
            
         for k,val in emo_dict.items():
            if j==k:
               sum_score=sum_score+val
               counter=counter+1
                     
      
      
      
      #regex = re.compile('[%s]' % re.escape(string.punctuation))
      regex=re.compile('[!.,?:;-]')
      aa=regex.sub(' . ', tmp3[a])
      aa=aa.replace('\n',' ')
      #print(aa)
      ll=aa.split(" ")
      flag=0
      pl=[]
      cl=0
      for a1 in ll:
        
         a1=a1.lower()
         if a1.startswith("#"):
            a1=a1[1:]
         if len(a1)>2:
    
            for i in range(2,len(a1)):
               if (a1[i-2]==a1[i-1] and a1[i-1]==a1[i]):
                  a1=a1.replace(a1[i]," ",1)
            
            
         a1=a1.replace(" ","")
        
         if neg_words['word'].isin([a1]).any():
            flag=1
                
         elif re.match("[!,.?]$",a1):
                
            flag=0
        
        #for la in l:
        
         if a1 in word_dict.keys():
                #print(re.match('%s'%str1[ans],a1))
            if flag==0:
               
               sum_score=sum_score+word_dict[a1]
               sum_list=sum_list+a1+" "+str(word_dict[a1])+" "
               counter=counter+1  
                #print(words.iloc[ans]['word']+" "+str(words.iloc[ans]['score'])+" ")
            else:
               sum_score=sum_score+(word_dict[a1]*(-1))
               sum_list=sum_list+a1+" "+str(word_dict[a1])+" "+" "
               counter=counter+1  
                #print(words.iloc[ans]['word']+" "+str(words.iloc[ans]['score']*(-1))+" ")
            #print(words[word])
         if flag==1:
            cl=cl+1
         if cl==4:
            #print("  "+a1)
            flag=0;
            cl=0;      #print(words[word])

      if counter!=0:
         tmp4.append([tmp3[a],sum_score,counter,sum_score/counter])
      else:
         tmp4.append([tmp3[a],sum_score,counter,0])
   tmp4=pd.DataFrame(tmp4,columns=['Tweet','Sum_score','Counter','Score']) 
  
   return tmp4