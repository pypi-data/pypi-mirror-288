from transformers import pipeline, AutoTokenizer
from wide_analysis.data.process_data import prepare_dataset
from wide_analysis.utils.helper import send_to_openai
import pandas as pd
from openai import OpenAI
import torch

label_mapping = {
    'delete': [0, 'LABEL_0'],
    'keep': [1, 'LABEL_1'],
    'merge': [2, 'LABEL_2'],
    'no consensus': [3, 'LABEL_3'],
    'speedy keep': [4, 'LABEL_4'],
    'speedy delete': [5, 'LABEL_5'],
    'redirect': [6, 'LABEL_6'],
    'withdrawn': [7, 'LABEL_7']
}

model_dict = {
    "bert-base": "research-dump/bert-base-uncased_deletion_multiclass_complete_Final",
    "bert-large": "research-dump/bert-large-uncased_deletion_multiclass_complete_final",
    "roberta-base": "research-dump/roberta-base_deletion_multiclass_complete_final",
    "roberta-large": "research-dump/roberta-large_deletion_multiclass_complete_final"
}

def extract_response(text, model_name):
    if model_name not in model_dict:
        raise ValueError("Invalid model name. Choose from ['bert-base', 'bert-large', 'roberta-base', 'roberta-large']")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = model_dict[model_name]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = pipeline("text-classification", model=model_name, top_k= None,device= device,max_length = 512,truncation=True)

    # Tokenize and truncate the text
    tokens = tokenizer(text, truncation=True, max_length=512)
    truncated_text = tokenizer.decode(tokens['input_ids'], skip_special_tokens=True)
    
    results = model(truncated_text)
    final_scores = {key: 0.0 for key in label_mapping}
    
    for result in results[0]:
        for key, value in label_mapping.items():
            if result['label'] == value[1]:
                final_scores[key] = result['score']
                break
    
    return final_scores



def get_outcome(url,mode='url', openai_access_token=None, explanation=False):
    model = 'bert-large'
    if mode == 'url':
        date = url.split('/')[-1].split('#')[0]
        title = url.split('#')[-1]
        df = prepare_dataset('title', start_date=date, url=url, title=title)
        text = df['discussion'].iloc[0]
    else:
        text = url
        title = text.split(':')[0]
    res = extract_response(text, model)
    if not explanation:
        result = {'title': title, 'outcome': max(res, key=res.get), 'score': res[max(res, key=res.get)]}
        return result
    else:
        expl = None  
        try:
            expl = send_to_openai(title, res, text, openai_access_token)
        except Exception as e:
            if openai_access_token == '':
                print('Please provide an OpenAI access token to get an explanation')
            else:
                print(f"An error occurred while trying to get an explanation: {e}")
        
        return {'title': title, 'outcome': max(res, key=res.get), 'score': res[max(res, key=res.get)], 'explanation': expl}

