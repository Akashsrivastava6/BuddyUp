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


 
#method used to preprocess the incoimng tweets
def preprocess1(tmp3):
   words=pd.read_csv("core/impdata3.csv") # loading lexicon list
   neg_words=pd.read_csv("core/NegatingWordList.txt",sep="\\t",header=None,names=['word']) # loading negating words list
   emo=pd.read_csv("core/emoticons.csv",sep=",") # loading emoticon list
 
   emo_dict=dict(zip(emo['Char'],emo['score2'])) # creating dictionary for emoticons

   


   word_dict=dict(zip(words['word'],words['score'])) #creating lexicon dictionary


   tmp4=[]
   
   
   #iterating through tweets
   for a in range(len(tmp3)):
      sum_score=0
      counter=0
      sum_list=""
    
      #iterating through each token of a list    
      for j in tmp3[a]:
            
         for k,val in emo_dict.items(): #for loop to check ift there is matching emoticon
            if j==k: # if match is found
               sum_score=sum_score+val # adding the emoticon score
               counter=counter+1 # incrementing the counter
                     
      
      
      
      #regex = re.compile('[%s]' % re.escape(string.punctuation))
      regex=re.compile('[!.,?:;-]') # compiling the regex
      aa=regex.sub(' . ', tmp3[a]) # replacing the above character in the tweet with " . "
      aa=aa.replace('\n',' ') # replacing next line with space
      #print(aa)
      ll=aa.split(" ")  # splitting the tweet by white space
      flag=0
      pl=[]
      cl=0

      # iterating through the list created by spilting the tweet by white space
      for a1 in ll:
         
         a1=a1.lower() #converting each token to lower case
         #handling the hash tag
         if a1.startswith("#"): # checking if there is hash tag 
            a1=a1[1:] # if hash tag is there then removing the hash tag
         # handling words like looooooove. changing them to looove
         if len(a1)>3:
    
            for i in range(3,len(a1)): # checking if the length of token is greater than 3
        
                if  (a1[i-2]==a1[i-1] and a1[i-1]==a1[i] and a1[i-3]==a1[i-2] ): # if there is a single character repeating consecutively more then thrice
            
                    a1=a1.replace(a1[i]," ",1) # replcaing the occurence of those character with white space
        #             a1=a1.replace(a1[i-1]," ",1)
            
            # removing white space
            a1=a1.replace(" ","")
            # applying spell check code condertinh looove to love
            for i in range(2,len(a1)):
               
                if  (a1[i-2]==a1[i-1] and a1[i-1]==a1[i]):
            
                    a1=a1.replace(a1[i]," ",1) # replcaing three consecutive charater with two
                    a1=a1.replace(a1[i-1]," ",1) 
            a1=a1.replace(" ","") # replacing white space
         a1=spell(a1) # applying spell check
         # checking if there is a negating word present and fliping the polarity of the next three words present
         if neg_words['word'].isin([a1]).any():
            flag=1 # setting flag as 1
                
         elif re.match("[!,.?]$",a1): # checking if there is punctuation is encountered. if encountered then flag is set to 0
                
            flag=0
        
        #for la in l:
        # checking if token if there in lexicon list
         if a1 in word_dict.keys():
                #print(re.match('%s'%str1[ans],a1))
            if flag==0: # checking if there is negating word before the word  
               # following code is executed if negating word is not before the token
               sum_score=sum_score+word_dict[a1]  # matched token score is added to the tweet score
               sum_list=sum_list+a1+" "+str(word_dict[a1])+" "
               counter=counter+1   # counter is incremented
                #print(words.iloc[ans]['word']+" "+str(words.iloc[ans]['score'])+" ")
            else: # following code is executed if negating word is there before the token. the polarity of the matched token is flipped
               sum_score=sum_score+(word_dict[a1]*(-1)) # score of matchong token is added to the tweet score
               sum_list=sum_list+a1+" "+str(word_dict[a1])+" "+" "
               counter=counter+1  # counter is incremented
                #print(words.iloc[ans]['word']+" "+str(words.iloc[ans]['score']*(-1))+" ")
            #print(words[word])
         # follwing is the code to set the flag for negating word to 0 after three tokens in the tweet
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
   tmp4=pd.DataFrame(tmp4,columns=['Tweet','Sum_score','Counter','Score']) # returning the dataframe after preprocessing.
  
   return tmp4