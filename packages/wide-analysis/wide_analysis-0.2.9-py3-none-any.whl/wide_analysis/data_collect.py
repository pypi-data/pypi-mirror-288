from datetime import datetime
from wide_analysis.data.process_data import prepare_dataset
from datasets import load_dataset

def collect(mode, start_date=None, end_date=None, url=None, title=None, output_path=None):
    if mode not in ['date_range', 'date', 'title','wide_2023']:
            raise ValueError("Invalid mode. Choose from ['date_range', 'date', 'title','wide_2023']")
    if mode == 'wide_2023':
        dataset = load_dataset('hsuvaskakoty/wide_analysis')
        print('Datset loaded successfully as huggingfaece dataset')
        print('The dataset has the following columns:', dataset.column_names)
        return dataset 
    
    if mode in ['date_range', 'date', 'title']:
        return prepare_dataset(
            mode=mode,
            start_date=start_date,
            end_date=end_date,
            url=url,
            title=title,
            output_path=output_path
        )
    else:
        print("Invalid input. Choose existing_data option from ['date_range', 'date', 'title','wide_2023']")