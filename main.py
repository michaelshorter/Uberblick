import openai
import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import configparser
import os.path
import time
import argparse
import os
from provotype.prep import read_text
from provotype.promts_gpt import generate_summarizer,do_summarization,summarize_summarized_texts,create_five_topics,scale_conversation,write_a_haiku
from provotype.generate_output import plot_main_topics,plot_categories,plot_summary

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', default='/home/wordcloud/wordcloud_keys/config.ini',metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')

    '''parser.add_argument('--configfile', default='config.ini',metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')'''

    parser.add_argument('--textfile', default = '/home/wordcloud/WordCloud/AzureSpeechCC/content.txt', metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')
    '''parser.add_argument('--textfile', default = 'content.txt', metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')'''
    args = parser.parse_args()
    print(args.configfile)
    return args


def parse_config(configfile):
    config = configparser.ConfigParser()   
    config.read(configfile)
    api_key = config['API']['my_api']
    return api_key
   
 


def do_job(text_file):
    
    from time import sleep

    split_text,nmb_splits, max_number_tokens = read_text(text_file)
    print(split_text)
    

    if nmb_splits >1:
        text_summarization = do_summarization(split_text,nmb_splits, max_number_tokens)

        text_summarization = " ".join(text_summarization)

        response_summary = summarize_summarized_texts(text_summarization)


    else:
        response_summary = summarize_summarized_texts(split_text)



    print(response_summary[0]['content'])

    plot_summary(response_summary[0]['content'])
    
    print("summary done!\n")


    haiku= 

    '''topics,rating  = create_five_topics(text_summarization)
    
    plot_main_topics(topics,rating)
    print("topics done!\n")
    

    list_scale, list_rating_scale = scale_conversation(text_summarization)
    print("scale conversation done!\n")
    plot_categories(list_scale, list_rating_scale)'''



def main(args):
    config = args.configfile
    textfile = args.textfile
    
    if config is not None:
        api_key = parse_config(config)

        openai.api_key = api_key

        print(api_key)
        
        if (textfile is not None) and (os.stat(textfile).st_size != 0):
            print(textfile)
            do_job(textfile)
            
            
         
        else:
            print("no textfile available")
            exit()
        
    



if __name__=='__main__':  
   
    args = get_args()
    main(args)
