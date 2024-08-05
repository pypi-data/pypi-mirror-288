import pandas as pd
from datetime import datetime
from wide_analysis.data.collect_data import collect_deletion_discussions, process_data


label_mapping = {
    'soft delete': 'delete',
    'keep': 'keep',
    'delete': 'delete',
    'merge': 'merge',
    'no consensus': 'no consensus',
    'userfy for beanie': 'userfy',
    'redirect': 'redirect',
    'speedy keep': 'speedy keep',
    'moved to\n  \n   wp:draft\n  \n  space': 'draftify',
    'keep.': 'keep',
    'draftify': 'draftify',
    'speedy delete': 'speedy delete',
    'speedily deleted': 'speedy delete',
    'speedy close': 'speedy close',
    'snow keep': 'keep',
    'nomination withdrawn': 'withdrawn',
    'speedy keep, nomination withdrawn': 'speedy keep',
    'procedural close': 'no consensus',
    'move to draft': 'draftify',
    'draftified': 'draftify',
    'withdrawn': 'withdrawn',
    'snow delete': 'delete',
    'redirect to\n  \n   colorado college tigers football, 1882–1909#1882': 'redirect',
    'userfy': 'userfy',
    'withdrawn by nominator': 'withdrawn',
    'will nominated individually for a fair discussion': 'withdrawn',
    'keep/redirect:': 'keep',
    'nominator withdrew': 'withdrawn',
    'delete and redirect': 'delete',
    'merge and redirect': 'merge',
    'speedily deleted under\n  \n   wp:a7': 'speedy delete',
    'delete.': 'delete',
    'speedy delete as\n  \n   wp:g11': 'speedy delete',
    'snow\n  \n  keep': 'keep',
    'closed': 'no consensus',
    'move to\n  \n   bids for the 2034 winter olympics': 'draftify',
    'withdraw': 'withdrawn',
    'trainwreck': 'no consensus',
    'procedural keep': 'keep',
    'article deleted by its original creator': 'delete',
    'keep/nomination withdrawn': 'keep',
    'withdrawn by nominator.': 'withdrawn',
    'keep and revert': 'keep',
    "wp:g5ed\n  \n  because it's been created by a lta\n  \n   liamb2011\n  \n  (\n  \n   talk\n  \n\n   ·\n  \n\n   contribs\n  \n  )": 'delete',
    'speedy deleted': 'speedy delete',
    'mixed outcome': 'no consensus',
    'rename': 'rename',
    'speedy keep (sock nom, no delete votes)': 'speedy keep',
    'merge one; no consensus for rest': 'merge',
    'speedy keep.': 'speedy keep',
    'restore to disambig': 'redirect',
    'speedily deleted under g3': 'speedy delete',
    'this is the only consensus i can discern from this discussion as few editors commented on the other articles. no penalty for future afds on this other articles.': 'no consensus',
    'draftify then create redirect from this page title.': 'draftify',
    'keep/withdaw': 'keep',
    'speedy delete g12': 'speedy delete',
    'convert to disambiguation page': 'redirect',
    'convert to dab': 'redirect',
    'withdrawn to draftify': 'draftify',
    'a snow keep': 'keep',
    'speedy keep per\n  \n   wp:csk\n  \n  #3: no accurate deletion rationale has been provided': 'speedy keep',
    'userify': 'userfy',
    'keep\n  \n   leinster chess leagues': 'keep',
    'draftify.': 'draftify',
    'move to project space and redirect': 'redirect',
    'moot': 'no consensus',
    'draftified by creator.': 'draftify',
    'no consensus to delete; consensus to rename to\n  \n   next tasmanian state election': 'no consensus',
    'nom withdrawn': 'withdrawn',
    'move to\n  \n   glenwood south': 'draftify',
    'withdrawn; speedy keep': 'speedy keep',
    'restore dab': 'redirect',
    'speedy deleted via g5': 'speedy delete',
    'deleted g11': 'speedy delete',
    'drafify': 'draftify',
    'no action.': 'no consensus',
    'reinstate previous redirect.': 'redirect',
    'perform a\n  \n   wp:mergeprop\n  \n  instead': 'merge',
    'transwiki': 'no consensus',
    'duplicate afd': 'no consensus',
    'redirected': 'redirect',
    'already deleted': 'delete',
    'speedy': 'speedy delete'
}



def prepare_dataset(mode = 'date', start_date=None, end_date=None, url=None, title=None, output_path=None):
    if mode == 'date_range':
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            df = collect_deletion_discussions(start_date, end_date)
        else:
            raise ValueError("start_date and end_date must be provided for mode 'date_range'")
    
    elif mode == 'date':
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            df = collect_deletion_discussions(start_date, start_date)
        else:
            raise ValueError("start_date must be provided for mode 'date'")
    
    elif mode == 'title':
        if url and title:
            if url.endswith('/'):
                start_date =datetime.strptime(start_date, '%Y-%m-%d')
                start_date = start_date.strftime('%Y_%B_%d')
                url = f'{url}{start_date}#{title}'
            df = process_data(url,start_date)
        else:
            raise ValueError("url and title must be provided for mode 'title'")
    
    else:
        raise ValueError("Invalid mode. Choose from ['date_range', 'date', 'title']")

    if not df.empty:
        if mode == 'date' or mode == 'date_range':
            df = df[['log_date', 'title', 'text_url','discussion_cleaned','proper_label','confirmation']]
            df = df.rename(columns={'log_date':'date','title':'title','text_url':'url','discussion_cleaned':'discussion','proper_label':'label','confirmation':'confirmation'})
        if mode == 'title':
            df = df[['date','title','text_url', 'discussion_cleaned','label','confirmation']]
            df = df.rename(columns={'discussion_cleaned':'discussion'})
        df['label'] = df['label'].str.lower()
        df['label'] = df['label'].map(label_mapping)
        df = df.drop_duplicates(subset=['title', 'discussion'])
        df = df.dropna()
        if output_path:
            df.to_csv(output_path, index=False)
            return df
        else:
            return df
    
    return df
