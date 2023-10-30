# Import Libraries
import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
from nltk.corpus import stopwords
import gradio as gr
from gradio import components

# API Details
API_KEY = '550200ce3eae4e808f1924e695de35ad'
API_URL = 'https://newsapi.org/v2/everything'

# Function to Extract Data from API
def extract_data(query, language, page_size):
    params = {
        'q': query,
        'language': language,
        'pageSize': page_size,
        'apiKey': API_KEY,
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        articles_df = pd.DataFrame(data.get('articles', []))
        return articles_df
    else:
        print("Error: Unable to fetch data. Status code:", response.status_code)
        return pd.DataFrame()

# Data Preprocessing Functions
def preprocess_data(data):
    test = data['source'].reset_index()
    for index in test.index:
        data['source'][index] = test['source'][index]['name']
    dataframe = data[['description']]
    dataframe['description'] = dataframe['description'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    dataframe['description'] = dataframe['description'].str.replace('[^\w\s]', '', regex=True)
    stop = stopwords.words('english')
    dataframe['description'] = dataframe['description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    return dataframe

# Sentiment Analysis Function
def sentiment_analysis(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to Create Pie Chart
def create_pie_chart(dataframe):
    values = dataframe["sentiment"].value_counts()
    labels = dataframe["sentiment"].unique().tolist()
    cdict = {'Positive': '#79DE79', 'Negative': '#FB6962', 'Neutral': '#A8E4EF'}
    fig = px.pie(values=values, names=labels, color=labels, title='Sentiment of Tweets', color_discrete_map=cdict, width=600, height=400)
    fig.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='radial', hovertemplate="Number of Tweets: %{value}")
    return fig

# Gradio Interface Function
def interface(query, language, page_size):
    data = extract_data(query, language, page_size)
    dataframe = preprocess_data(data)
    dataframe['sentiment'] = dataframe['description'].apply(sentiment_analysis)
    fig = create_pie_chart(dataframe)
    return fig # gr.outputs.Plotly(fig)

# Gradio Interface
iface = gr.Interface(
    fn=interface,
    inputs=[
        "text", 
        "text", 
        components.Slider(minimum=1, maximum=100, default=25, step=1)
    ],
    outputs="plot"
)

iface.launch(server_port=7860, server_name="0.0.0.0")

