import openai
import time
from provotype.prep import prepare_json_topics,prepare_json_scale
import json
from time import sleep

model_id = 'gpt-3.5-turbo'

def generate_summarizer(my_tokens,prompt):

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=my_tokens,
        temperature=0.7,
        top_p=0.5,
        frequency_penalty=0.5,
        messages=
       [
         {
          "role": "system",
          "content": "You are a helpful assistant for text summarization.",
         },
         {
          "role": "user",
          "content": f"Can you make a summariziation for following text: {prompt}",
         },
        ],
    )
    return res["choices"][0]["message"]["content"]



def do_summarization(split_text,number_splits,response_max_tokens):

    from time import sleep

    summarized_text = []
    nmb_splits = number_splits
    print(number_splits)
   
    max_tokens = response_max_tokens


    for i in range(nmb_splits):

        if (i % 3) == 0 and i !=0:
            print("waiting for 60 seconds")
            sleep(60)
  
        summ_text = generate_summarizer(max_tokens,split_text[i])
        summarized_text.append(summ_text)
    
      
    return summarized_text




def create_five_topics(text_data):

    prompts = 0
    
    json_str =  """{"topics": {"topic:","","rating:",""}}"""

    conversation = []

    while conversation == []:

        if (prompts % 3) == 0 and prompts !=0:
            print("waiting for 60 seconds")
            sleep(60)


        try:
    
            response = openai.ChatCompletion.create(
                model = model_id,
                messages = [{'role':'system', 'content': 'You are a helpful research assistant.'},
                            {'role': 'user', 'content':f"Give me the five most relevant topics (one word, sorted by highest til lowest) plus a probability between 0 and 1 \
                            in a JSON object like {json_str} of following: {text_data}"},
                           ])
            
            api_usage = response['usage']
            print('Total token consumed: {0}'.format(api_usage['total_tokens']))
          
            conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
            

        except: 
            pass
            prompts = prompts+1



        try:
           
            list_topics, list_rating = prepare_json_topics(conversation)

        except:
            conversation = []
    
    
    return list_topics,list_rating 


def summarize_summarized_texts(summarized_text):
    conversation = []
  
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens = 100,
     
        temperature=0.7,
        top_p=0.5,
        frequency_penalty=0.5,
        messages=
       [
         {
          "role": "system",
          "content": "You are a helpful assistant for text summarization.",
         },
         {
          "role": "user",
          "content": f"Can you make a summariziation with the maximum number of tokens for following text: {summarized_text}",
         },
        ],
    )
    
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    
    return conversation



def scale_conversation(text_data):
    prompts = 0
    json_str =  """{"scales": {"scale:","","rating:",""}}"""
    conversation = []

    while conversation == []:

        if (prompts % 3) == 0 and prompts !=0:
            print("waiting for 60 seconds")
            sleep(60)


        try:

            print('try to get response scale')
            response = openai.ChatCompletion.create(
                model = model_id,
                messages = [{'role':'system', 'content': 'You are a helpful research assistant.'},
                            {'role': 'user', 'content':f"return how emotional between 0 and 10, controversial between 0 and 10, factual between 0 and 10, sensitive\
                        between 0 and 10 in a JSON object like {json_str} is following text (treat the individual strings as complete text): {text_data}"},
                           ])
            
            api_usage = response['usage']
    
  
            conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        except: 
            pass
            print('response scale did not work')
            prompts = prompts+1



        try:
            print('try scale json')

            list_scale, list_rating = prepare_json_scale(conversation)

        except:
            print('json did not work')
            conversation = []
    

       

    return list_scale,list_rating 

