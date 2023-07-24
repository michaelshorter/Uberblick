import openai
import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import configparser
import os.path
import time
import argparse
import os
import urllib
from provotype.prep import read_text
from provotype.promts_gpt import generate_summarizer,do_summarization,summarize_summarized_texts,create_five_topics,scale_conversation,write_a_haiku,create_image
from provotype.generate_output import plot_main_topics,plot_categories,plot_text,generate_image

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
    
    

    if nmb_splits >1:
        text_summarization = do_summarization(split_text,nmb_splits, max_number_tokens)

        text_summarization = " ".join(text_summarization)

        response_summary = summarize_summarized_texts(text_summarization)


    else:
        response_summary = summarize_summarized_texts(split_text)
        
    summary = response_summary[0]['content']
    print(summary)

    plot_text(summary,'summary.png','summary')
    print("summary done!\n")

    haiku = write_a_haiku(summary)
    plot_text(haiku[0]['content'],'haiku.png','haiku')
    print("haiku done!\n")

    image_url=create_image(response_summary[0]['content'])
    print("url image done!\n")
    file_name = "image.png"
    urllib.request.urlretrieve(image_url,file_name)
    print("image done!\n")

     

    sorted_dict_topic  = create_five_topics(text_summarization)
    
    plot_main_topics(sorted_dict_topic)


    print("topics done!\n")
    

    '''list_scale, list_rating_scale = scale_conversation(summary)
    plot_categories(list_scale, list_rating_scale)
    print("scale conversation done!\n")'''



def main(args):
    config = args.configfile
    textfile = args.textfile
    
    if config is not None:
        api_key = parse_config(config)

        openai.api_key = api_key

    
        
        if (textfile is not None) and (os.stat(textfile).st_size != 0):
        
            time.sleep(30)

            while True:
                
                do_job(textfile)

                time.sleep(300)
            
            
         
        else:
            print("no textfile available")
            exit()
        
    



if __name__=='__main__':  
   
    args = get_args()
    main(args)
