#Importing Libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as sql
from time import sleep

etsy_website="https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page="
browser=None

def scrap_page(url):
    source=requests.get(url).text
    soup=BeautifulSoup(source,"lxml")


    #Searching for anchor tags for each product pictures and extracting the url from href
    a_tags=soup.findAll('a',class_="display-inline-block listing-link")
    links=[]
    for a_tag in a_tags:

        links.append(a_tag.get("href"))

    page_reviews=[]
    #Collecting all links in a page and scrapping reviews from them into a single list
    for link in links:
        page_reviews=page_reviews+scrap_product_reviews(link)

    return page_reviews

def scrap_all_data():
    global etsy_website
    i=1

    mega_reviews=[]
    #Collecting all reviews from all pages into a single list
    while i<=250:
        website=etsy_website+str(i) #getting page url by page number
        mega_reviews=mega_reviews+scrap_page(website)
        print("Page {} Scrapped".format(i))
        i=i+1

    return mega_reviews

#Main function
def main():
    global etsy_website
    print("Scrapping Data")

    scrapped_reviews=scrap_all_data()#Getting all reviews from 250 pages
    #Converting to csv
    print("Converting to csv")
    scrapped_reviews_df=pd.DataFrame(scrapped_reviews)
    scrapped_reviews_df.to_csv("reviews_from_etsy.csv")
    #Storing in a database
    print("Connecting to database")
    conn=sql.connect('reviews.db')

    scrapped_reviews_df.to_sql('reviews_table',conn)

#calling main function
if __name__=='__main__':
    main()