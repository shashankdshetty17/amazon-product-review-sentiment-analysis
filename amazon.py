import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re
import math
import time
import tkinter as tk
from tkinter import font
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
global j
headers = {
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}


def get_page_html(page_url: str) -> str:
    resp = requests.get(page_url, headers=headers)
    return resp.text


def get_reviews_from_html(page_html: str) -> BeautifulSoup:
    soup = BeautifulSoup(page_html, "lxml")
    reviews = soup.find_all("div", {"class": "a-section celwidget"})
    return reviews


def get_review_date(soup_object: BeautifulSoup):
    date_string = soup_object.find("span", {"class": "review-date"}).get_text()
    return date_string


def get_review_text(soup_object: BeautifulSoup) -> str:
    try:
        review_text = soup_object.find(
            "span", {"class": "a-size-base review-text review-text-content"}
        ).get_text()
        return review_text.strip()
    except AttributeError:
        print("attr1",end="")

def get_review_header(soup_object: BeautifulSoup) -> str:
    try:
        review_header = soup_object.find(
            "a",
            {
                "class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"
            },
        ).get_text()
        return review_header.strip()
    except AttributeError:
        print("attr2",end="")

def get_number_stars(soup_object: BeautifulSoup) -> str:
    try:
        stars = soup_object.find("span", {"class": "a-icon-alt"}).get_text()
        return stars.strip()
    except AttributeError:
        print("attr3",end="")

def get_product_name(soup_object: BeautifulSoup) -> str:
    try:
        product = soup_object.find(
            "a", {"class": "a-size-mini a-link-normal a-color-secondary"}
        ).get_text()
        return product.strip()
    except AttributeError:
        print("attr4",end="")

def orchestrate_data_gathering(single_review: BeautifulSoup) -> dict:
    return {
        "review_text": get_review_text(single_review),
        "review_date": get_review_date(single_review),
        "review_title": get_review_header(single_review),
        "review_stars": get_number_stars(single_review),
        "review_product": get_product_name(single_review),
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    all_results = []
    URLS = []
    #ulr generation
    try:
        def generate_review_urls( base_url,rev,j):
            
            reviewerType = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
            for page_number in range(0,rev):
                url = base_url + "/ref=cm_cr_arp_d_paging_btm_next_" + str(page_number) + reviewerType + str(page_number)
                response = requests.get(url, headers=headers)
                print("generating url:"+str(page_number+1))
                ####
                text.insert("end", f"Line {j}:generating url:"+str(page_number+1)+" \n")
                j+=1
                text.see("end") # Scroll to the end of the text box
                root.update()
                ####
                if response.status_code != 200:
                    print("End of pages reached!")
                    break
                URLS.append(url)
            return j
    except requests.exceptions:
        print("Connection error occurred. Please check your internet connection and try again.")       
    #count number of reviews
    def get_input():
        global url
        url = input_field.get()
        root.destroy()

    root = tk.Tk()
    root.geometry("1320x620+100+100")
    root.configure(bg='black')
    root.title("Amazon Reviews")

    heading_font = font.Font(family='Helvetica', size=40, weight='bold')
    heading_font2 = font.Font(family='Helvetica', size=20, weight='bold')

    heading_label = tk.Label(root, text="Amazon Review Analysis", font=heading_font, bg='black',fg='white', padx= 25, pady= 25)
    heading_label.pack()

    input_label = tk.Label(root, text="Enter Amazon Product URL :", font=heading_font2, bg='black',fg='white', padx= 25, pady= 25)
    input_label.pack()

    input_field = tk.Entry(root,bg='white',width=100)
    input_field.pack()

    input_label = tk.Label(root, text="", bg='black', padx= 25, pady= 25)
    input_label.pack()

    submit_button = tk.Button(root, text="Submit", command=get_input, bg='black',fg='white')
    submit_button.pack()

    
    root.mainloop()
    print(url)
    ####   

    def run_code():
    # Code to run
        i = 0
        while i < 6:
            labell["text"] = "Loading"+"." * (i)
            root.update()
            time.sleep(0.5)
            i += 1
        
        
        j=1
        ##output
        text.insert("end", f"Line {j}: GENERATING URL!!!!\n")
        j+=1
        text.see("end") # Scroll to the end of the text box
        root.update()
        ##output
        new_url = re.sub("/dp/", "/product-reviews/", url)
        new_url = re.sub("ref=.*$", "ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews", new_url)
        resp = requests.get(new_url, headers=headers)
        if resp.status_code != 200:
            print("internet or browser error!!!")
            ##output
            text.insert("end", f"Line {j}: internet or browser error!!!!\n")
            j+=1
            text.see("end") # Scroll to the end of the text box
            root.update()
            ##output
            exit()
        soup = BeautifulSoup(resp.text, "lxml")
        reviewsn = soup.find_all("div", {"class":"a-row a-spacing-base a-size-base"})
        if not reviewsn:
            print("review not found")
            ##output
            text.insert("end", f"Line {j}: Review not found!!!!\n")
            j+=1
            text.see("end") # Scroll to the end of the text box
            root.update()
            ##output
            exit()
        text1 = reviewsn[0].get_text()

        review_count = re.search(r'(\d+(,\d+)?)\s+with reviews', text1).group(1)
        review_count = int(review_count.replace(",", ""))
        tots="Total review = "+str(review_count)
        print(tots)
        ##output
        text.insert("end", f"Line {j}: "+tots+"s\n")
        j+=1
        text.see("end") # Scroll to the end of the text box
        root.update()
        ##output
        rev=math.ceil(review_count/10)
        #--------------------------------

        j=generate_review_urls(new_url,rev,j)


        for u in URLS:
            logging.info(u)
            text.insert("end", f"Line {j}:Visiting URL:"+u+" \n")
            j+=1
            text.see("end") # Scroll to the end of the text box
            root.update()
            html = get_page_html(u)
            reviews = get_reviews_from_html(html)
            for rev in reviews:
                data = orchestrate_data_gathering(rev)
                all_results.append(data)

        out = pd.DataFrame.from_records(all_results)
        logging.info(f"{out.shape[0]} Is the shape of the dataframe")
        global save_name
        save_name = str(review_count)+"_reviews"+".csv"
        logging.info(f"saving to {save_name}")
        text.insert("end", f"Line {j}:File Saved : "+save_name+" \n")
        j+=1
        text.see("end") # Scroll to the end of the text box
        root.update()
        out.to_csv(save_name)
        logging.info('extract done')
        text.insert("end", f"Line {j}:Extraction Done \n")
        j+=1
        text.see("end") # Scroll to the end of the text box
        root.update()
        ########
        time.sleep(3) # Simulate a long-running operation

    def show_loading_page():
    # Create the loading page
        root = tk.Tk()
        root.geometry("1320x620+100+100")
        root.configure(bg='black')
        root.title("Amazon Reviews")
        global labell
        labell = tk.Label(root, text="Loading.", font=("Helvetica", 24))
        labell.pack()
        global text
        text = tk.Text(root, height=30, width=150, bg="black", fg="white")
        text.pack()
        root.update()

        run_code()

        root.destroy()

    show_loading_page()

    def do_senti(filename):
    
        df = pd.read_csv(filename)
        print(df)
        print(filename)
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(columns=['review_date'])
        df = df.drop(columns=['review_title'])
        df = df.drop(columns=['review_product'])
        df['review_stars'] = df['review_stars'].replace(r' out of.*', '', regex=True).astype(float)


        df.dropna(inplace=True)
        # add new column for sentiment
        df['sentiment-using-textblob'] = ''
        df['sentiment-using-Vader'] = ''
        rows=0
        sid = SentimentIntensityAnalyzer()
        for index, row in df.iterrows():
            text1 = row['review_text']
            rows=rows+1
            analysis = TextBlob(text1)
            sentiment_dict = sid.polarity_scores(text1)
            sentiment = analysis.sentiment.polarity
            df.at[index, 'sentiment-using-Vader'] =sentiment_dict['compound']
            df.at[index, 'sentiment-using-textblob'] = sentiment

        print(df)
        column1_sum = df['sentiment-using-textblob'].sum()
        column2_sum = df['sentiment-using-Vader'].sum()
        column3_sum = df['review_stars'].sum()
        
        testavg=column1_sum/rows
        vadavg=column2_sum/rows
        revavg=column3_sum/rows

        print("average sentiment score based on textblob:"+str(testavg))
        print("average sentiment score based on Vader:"+str(vadavg))
        print("average sentiment score based on user reviews:"+str(revavg))
        str1=""
        if(testavg>0.4 and vadavg>0.4 and revavg>4.0):
            str1="product has best reviews "
        elif(testavg>0.1 and vadavg>0.1 and revavg>1.0):
            str1="product has good and average reviews "
        elif(testavg>-0.5 and vadavg>-0.5 and revavg<3.0):
            str1="product has bad reviews"
        else:
            str1="product has worst reviews!!!dont BUY"
        print(str1)

        root = tk.Tk()
        root.geometry("1420x620+100+100")
        root.configure(bg='black')
        root.title("Amazon Reviews")

        heading_font = font.Font(family='Helvetica', size=40, weight='bold')
        heading_font2 = font.Font(family='Helvetica', size=15, weight='bold')

        heading_label = tk.Label(root, text="Amazon Review Analysis", font=heading_font, bg='black',fg='white', padx=6,pady=6)
        heading_label.pack()

        input_label = tk.Label(root, text="Average sentiment score based on textblob : "+str(testavg), font=heading_font2, bg='black',fg='white', padx= 6, pady= 6)
        input_label.pack()

        input_label = tk.Label(root, text="Average sentiment score based on Vader : "+str(vadavg), font=heading_font2, bg='black',fg='white', padx= 6, pady= 6)
        input_label.pack()

        input_label = tk.Label(root, text="Average sentiment score based on user reviews : "+str(revavg), font=heading_font2, bg='black',fg='white', padx= 6, pady= 6)
        input_label.pack()

        input_label = tk.Label(root, text=str1, font=heading_font2, bg='black',fg='red', padx= 6, pady= 6)
        input_label.pack()

        global text
        text = tk.Text(root, height=5000, width=150, bg="black", fg="white")
        text.pack()
        pd.set_option('display.max_rows', None)
        text.insert("end",df)
        text.see("end") # Scroll to the end of the text box
        root.update()
        root.mainloop()
    do_senti(save_name)