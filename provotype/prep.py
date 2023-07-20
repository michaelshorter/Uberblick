import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os.path
import time
import json
import matplotlib as plt
import pandas as pd
import pandas as pd
import numpy as np




def read_text(textfile):

    with open(textfile, 'r') as file:
        data = file.read().rstrip()
    
    print(len(data))
    
    if len(data)>=10000:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 0)
        texts= text_splitter.split_text(data)
        number_splits = len(texts)
        max_response_tokens = round(4096/number_splits-200)
    else:

        texts = data
        number_splits = 1 

    max_response_tokens = round(4096/number_splits-200)
    
    return(texts,number_splits,max_response_tokens)


def prepare_json_topics(repsonse_input):
    
    list_topics=[]
    list_probas =[]

    y=json.loads(repsonse_input[0]['content'])


    for topic in y['topics']:
        
        list_topics.append(topic['topic'])
        list_probas.append(topic['rating'])

    
    return list_topics, list_probas



def prepare_json_scale(repsonse_input):
    
    list_scale=[]
    list_rating =[]


    y=json.loads(repsonse_input[0]['content'])


    for scales in y['scales']:
        list_scale.append(scales['scale'])
        list_rating.append(scales['rating'])

    
    return list_scale, list_rating    




