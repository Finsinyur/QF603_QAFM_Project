import numpy as np
import pandas as pd
from datetime import datetime
import PyPDF2
import re

def read_pdf(fname):
    with open(fname, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the extracted text
        extracted_texts = []

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_num]

            # Extract text from the page
            text = page.extract_text()
            
            # Append the extracted text to the result
            extracted_texts.append(text)

    return extracted_texts

def extract_rebal_changes(textstring, start_page, end_page):
    date_pattern = r'\d{2}-[A-Za-z]{3}-\d{2}'

    records = []

    for extracted_text in textstring[start_page : end_page]:
        
        dates =\
            re\
                .findall(date_pattern, 
                         extracted_text)
        
        idx = extracted_text.index(dates[0])
        shortened_text = extracted_text[idx:]
        
        text_splits =\
            re\
                .split(date_pattern, 
                       shortened_text)
        
        text_splits =\
            [s.strip() 
             for s in text_splits 
             if s.strip()]
        
        for date, text in zip(dates, text_splits):
            year = datetime.strptime(date, '%d-%b-%y').year
            
            if year < 2013:
                continue
            
            if 'Corporate Event' in text:
                continue
                
            alt_text = text.replace('\n', '')
            alt_text = alt_text.replace('  ', '\t')
            
            line_info = alt_text.split('\t')
            
            if len(line_info) > 2:
                print(f'Please check {date};\
                      Add:{line_info[0]}; \
                      Del: {line_info[1]}; \
                      Oth: {line_info[2:]}')
                
                user_input = input("Maunal Intervention? (Y/N) ")
            
                if user_input == 'Y':
                    add = input("Included security: ")
                    delete = input("Excluded security: ")
                    line_info = [add, delete]

            if len(line_info) < 2:
                print(f'Please check {date};\
                    Oth: {line_info}')
                
                user_input = input("Maunal Intervention? (Y/N) ")
                
                if user_input == 'Y':
                    add = input("Included security: ")
                    delete = input("Excluded security: ")
                    line_info = [add, delete]

            records.append({
                'Date':date,
                'Add':line_info[0],
                'Del':line_info[1] 
            })

    return pd.DataFrame(records) 

def clean_df(raw_df, index_name):
    df = raw_df.copy()
    
    # Remove entries not within rebal period
    df['Date'] = pd.to_datetime(df['Date'], format = '%d-%b-%y')
    df['Month'] = df['Date'].dt.month
    df = df[df['Month'].isin([3,6,9,12])]
    
    df = df.replace(' ', np.nan)
    
    sub_df1 = df.iloc[:,0:2].copy()
    sub_df1 = sub_df1.rename(columns = {'Add':'Name'})
    sub_df1 = sub_df1.dropna()
    sub_df1[index_name] = 1
    
    sub_df2 = df.iloc[:,[0,2]].copy()
    sub_df2 = sub_df2.rename(columns = {'Del':'Name'})
    sub_df2 = sub_df2.dropna()
    sub_df2[index_name] = -1
    
    res_df = pd.concat([sub_df1, sub_df2])
    
    return res_df

ftse100 = '../constituent_history/ftse-100-constituent-history.pdf'
ftse250 = '../constituent_history/ftse-250-constituent-history.pdf'

ftse100_text = read_pdf(ftse100)
ftse100_df = extract_rebal_changes(ftse100_text, 1, -2)

ftse250_text = read_pdf(ftse250)
ftse250_df = extract_rebal_changes(ftse250_text, 1, -3)

ftse100_cleaned_df = clean_df(ftse100_df, 'FTSE100')
ftse250_cleaned_df = clean_df(ftse250_df, 'FTSE250')

ten_y_history =\
    ftse100_cleaned_df\
        .merge(ftse250_cleaned_df, 
               on = ['Date','Name'], 
               how = 'outer')

ten_y_history =\
    ten_y_history\
        .sort_values(by = 'Date')\
            .reset_index(drop = True)

ftse100_df.to_csv('../constituent_history/ftse100_history.csv', index = False)
ftse250_df.to_csv('../constituent_history/ftse250_history.csv', index = False)
ten_y_history.to_csv('../constituent_history/ftse_history.csv', index = False)