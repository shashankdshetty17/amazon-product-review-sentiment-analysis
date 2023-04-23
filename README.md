# amazon-product-review-sentiment-analysis
amazon product review sentiment analysis using library vader and text blob . the review are scraped from amazon using the product link.the user interface is designed using tkinter .
import needed 
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
