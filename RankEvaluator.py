from collections import defaultdict
from tqdm import tqdm
import numpy as np

def TimeSliceEvaluatorGenerator(df,newsContent, sliceSize=1, verbose=False):
    return lambda P: TimeSliceEvaluator(P,df,newsContent, sliceSize, verbose)

def convertToArray(chunk):
    columns = list(chunk.columns)
    devIdx = columns.index('deviceId') + 1
    tSpentx = columns.index('overallTimeSpent') + 1
    hashIdx = columns.index('hashId') + 1
    timeStampx = columns.index('eventTimestamp') + 1
    
    arr = []
    for c in chunk.itertuples():
        arr.append({
            'deviceId' : c[devIdx],
            'overallTimeSpent' : c[tSpentx],
            'hashId' : c[hashIdx],
            'eventTimestamp' : c[timeStampx]
        })
        
    return arr

def TimeSliceEvaluator(P,df,newsContent, sliceSize=1, verbose=False):
    batchRecommend=True
    scores = []
    global_numerator = 0
    global_denominator = 0
    df=df.copy()
    starttime=min(df['eventTimestamp'])
    df['chunkId']=((df['eventTimestamp']-starttime)//(sliceSize*3600)).astype(int)
    chunks = df.groupby(['chunkId'])
    chunkIds = sorted(chunks.groups.keys())
    
    i = 0
    for _, chunk in tqdm(chunks):
        arr = convertToArray(chunk)
        if(i!=0):
            if(batchRecommend):
                pass
                user_list = chunk['deviceId']
                news_list = chunk['hashId']
                
                predictedScores =  P.recommend(user_list,news_list,newsContent)
                chunk['predictedScores'] = predictedScores
                
                numerator = (chunk['overallTimeSpent']*chunk.groupby(['deviceId'])['predictedScores'].rank(pct=True,ascending=False)).sum()
                denominator = chunk['overallTimeSpent'].sum()
                scores.append((numerator / denominator )* 100)
                global_numerator+=numerator
                global_denominator+=denominator
                #print(np.mean(scores))
                
            else:
                pass
            
        if(i!=len(chunkIds)-1):
            P.feed(arr)
            
        i += 1
    return({'score':100*global_numerator/global_denominator,'score_list':scores})






class RandomRecommenderPolicy:
    
    
    
    def __init__(self):
        """
        To Implement
        """
        pass
    
    
    def recommend(self, user_list, news_list, newsContent): 
        """
        
        for each entry in the user_list you have to recommend a likeness score against the corresponding entry in news_list.
        
        #user_list: list of deviceIds
        #news_list: list of hashIds
        #newsContent: dict containing a map from news hashId to it's meta data like text, category, publisher, etc. 
        

        #return: The return value would be a list of length user_list for above inputs, which will contain the likeness score for the pairs
        [(user_list[0],news_list[0]),(user_list[1],news_list[1]),(user_list[2],news_list[2])]
        
        """
        
        if(len(user_list)!=len(news_list)):
            print('Major Fault, user news list size found unequal')
            print(9/0)
        return np.random.rand(len(user_list))
    
    
    def feed(self, feed_stream):
        
        
        """
        feed_stream: For each (user, news) tuple you returned from recommmend, feed_stream contains one entry as a dictionary 
                     containing four keys "deviceId", "hashId", "overallTimeSpent" (timespent on the particular news) and 
                     "eventTimestamp" (when did this evant happen), these represent the order and timespent on news, actually read by the user in the 
                     next iteration.
        """
        
        
        pass
    
   