from transformers import pipeline, AutoTokenizer
from wide_analysis.data.process_data import prepare_dataset
import pandas as pd
import pysbd
import torch

def extract_response(text, model_name, access_token):
    label_mapping = {
            'delete': 0,
            'keep': 1,
            'merge': 2,
            'comment': 3
        }
    if access_token is None:
        raise ValueError("Please provide a valid access token")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    pipe = pipeline("text-classification", model=model_name, tokenizer=tokenizer, top_k=None,device= device,max_length = 512,truncation=True)
    
    # Tokenize and truncate the text
    tokens = tokenizer(text, truncation=True, max_length=512)
    truncated_text = tokenizer.decode(tokens['input_ids'], skip_special_tokens=True)
    
    results = pipe(truncated_text)
    
    final_scores = {key: 0.0 for key in label_mapping}
    for result in results[0]:
        for key, value in label_mapping.items():
            if result['label'] == f'LABEL_{value}':
                final_scores[key] = result['score']
                break
    
    return final_scores

def get_stance(url,mode='url', access_token=''):
    if mode == 'url':
        date = url.split('/')[-1].split('#')[0]
        title = url.split('#')[-1]
        df = prepare_dataset('title', start_date=date,url=url, title=title)
        text = df['discussion'].iloc[0]
    else:
        text = url
    seg = pysbd.Segmenter(language="en", clean=False)
    text_list = seg.segment(text)
    model = 'research-dump/bert-large-uncased_wikistance_v1'
    res_list = []
    
    for t in text_list:
        res = extract_response(t, model, access_token)
        highest_key = max(res, key=res.get)
        highest_score = res[highest_key]
        result = {'sentence': t, 'stance': highest_key, 'score': highest_score}
        res_list.append(result)
    
    return res_list
