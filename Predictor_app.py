import dash
import webbrowser 
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State

import plotly.graph_objs as go
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from wordcloud import WordCloud,STOPWORDS
from io import BytesIO
import base64
import time

project_name=None
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
scrappedetsyReviews = None
pickle_model = None
vocab = None
stopwords=None

# Defining My Functions

#def open_browser():
 #   webbrowser.open_new('http://127.0.0.1:8050/')


def load_model():
    print("Loading model...")
    global pickle_model
    file = open(r"pickle_model_1.pkl", 'rb')
    pickle_model = pickle.load(file)

    global vocab
    file= open(r'features.pkl', 'rb')
    vocab = pickle.load(file)


def load_csv():
    print("Loading csv...")
    global scrappedetsyReviews
    scrappedetsyReviews = pd.read_csv(r"reviews_etsy.csv", index_col=False, skiprows=[0], names=["SNo", "Review"])
    scrappedetsyReviews['sentiment'] = [pred_review(x)[0] for x in scrappedetsyReviews['Review']]



def pred_review(reviewText):

    transformer=TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=vocab)
    vectorised_review = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))

    return pickle_model.predict(vectorised_review)


def figure():
    labels=["Positive","Negative"]
    reviews_df=scrappedetsyReviews
    posnegcount = [len(reviews_df[reviews_df['sentiment']==1]),len(reviews_df[reviews_df['sentiment']==0])]

    exp = (0, 0.1, 0, 0)

    pie = go.Pie(labels=labels,values=posnegcount)
    fig=go.Figure(data=[pie])
    return fig



def wordsentence():
    print("Collecting words....")
    sentence=[]
    sentence.append(scrappedetsyReviews['Review'][0])

    for review in scrappedetsyReviews['Review']:
        sentence.append(review);
    sentencestring=" ".join(sentence)
    return sentencestring


def wordcloud():
    sentence=wordsentence()
    stopwords=set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(sentence)
    wordcloud=wordcloud.to_image()
    img=BytesIO()
    wordcloud.save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


def app_ui():
    main_layout=html.Div(
        [
            html.H1(children="Sentimental Analysis with Insights",style={'text-align':'center','font-family':'Impact','color':'#ffffff','font-size':'80px'}),
            dbc.NavbarSimple(
                children=[

                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem(children="Sections", header=True),
                            dbc.DropdownMenuItem(html.A(children="Pie Chart", href="#pie_div")),
                            dbc.DropdownMenuItem(html.A(children="Wordcloud", href="#wordcloud_div")),
                            dbc.DropdownMenuItem(html.A(children="Dropdown Evaluator", href="#dropdown_div")),
                            dbc.DropdownMenuItem(html.A(children="Text Evaluator", href="#text_div")),

                        ],
                        nav=True,
                        in_navbar=True,
                        label="Explore",
                    ),
                ],
                brand="Sections on this page",
                brand_href="#",
                color="#0A043C",
                dark=True,
            ),
            html.Div([
            dbc.Jumbotron([
                html.H1(children="Percentage of Positive and Negative Reviews"),
                dcc.Graph(id="pie", figure=figure())
            ],
                style={'background-color':'#7FB3D5'}
            )

            ],
                style={'width':'80%', 'margin-top':'20px'},
                id="pie_div"

            ),
            html.Div([
                dbc.Jumbotron([
                    html.H1(children="Wordcloud"),
                    html.Img(id="wordcloud", src=wordcloud())
                ]
                ,style={'background-color':'#7FB3D5'}
                ),


            ],
            style = {'width': '80%', 'margin-left': '270px'},
                id="wordcloud_div"
            )
            ,
            html.Div([
                dbc.Jumbotron([
                    html.H1(children="Choose a Review from the dropdown below"),
                    dcc.Dropdown(
                        id='review_dropdown',
                        options=[{'label': scrappedetsyReviews['Review'][i], 'value': scrappedetsyReviews['Review'][i]}
                                 for i in range(0, 1001)],
                        value="Select from below",
                        style={'width': '80%', 'height': 40, 'margin-left': '120px', 'margin-bottom': '30px'}

                    ),
                    dbc.Button(id="dropdown_submit", children="Click to evaluate", n_clicks=0, color='dark',
                               style={'width': '20%', 'margin-left': '400px','margin-bottom':'20px'}),
                    dbc.Button(id='dropdown_result', children="Result appears here",
                               style={'width': '80%', 'height': 50, 'margin-left': '120px', 'margin-bottom': '30px'},
                               disabled=True
                               )
                ],
                style={'background-color':'#7FB3D5'}
                )
            ]
            , style = {'width': '80%'}, id="dropdown_div"
            )
            ,
            html.Div([
                dbc.Jumbotron([
                    html.H1(children="Enter a review"),
                    dcc.Textarea(
                        id='review_text',
                        placeholder="Enter review here",
                        style={'width': '80%', 'height': 40, 'margin-left': '120px', 'margin-bottom': '30px'}

                    ),
                    dbc.Button(id="text_submit", children="Click to evaluate", n_clicks=0, color='dark',
                               style={'width': '20%', 'margin-left': '400px','margin-bottom':'20px'}),
                    dbc.Button(id='text_result', children="Result appears here",
                               style={'width': '80%', 'height': 50, 'margin-left': '120px', 'margin-bottom': '30px'},
                               disabled=True
                               )
                ]
                , style={'background-color':'#7FB3D5'}
                )
            ],
                style={'width': '80%', 'margin-left': '270px'}, id="text_div"
            )




        ],
        style={'background-color': '#154360'}
    )
    return main_layout


@app.callback(
    [
        Output('dropdown_result','children'),
        Output('dropdown_result','style')
    ],
    [
        Input('dropdown_submit','n_clicks')
    ],
    [
        State('review_dropdown','value'),
        State('dropdown_result','style')
    ]
)
def update_submit_dropdown(n_clicks,reviewtext,style):
    print("Data Type = ", str(type(n_clicks)))
    print("Value = ", str(n_clicks))

    print("Data Type = ", str(type(reviewtext)))
    print("Value = ", str(reviewtext))

    print("Data Type = ", str(type(style)))
    print("Value = ", style)

    if(n_clicks>0):
        response=pred_review(reviewtext)[0]
        result=[]

        if(response==1):
            result.append("Positive")
            style['background-color']='green'
            result.append(style)
        elif(response==0):
            result.append("Negative")
            style['background-color'] = 'red'
            result.append(style)
        else:
            result.append("Undetermined")
            result.append(style)

        return result


@app.callback(
    [
        Output('text_result','children'),
        Output('text_result','style')
    ],
    [
        Input('text_submit','n_clicks')
    ],
    [
        State('review_text','value'),
        State('text_result','style')
    ]
)
def update_submit_text(n_clicks,reviewtext,style):
    print("Data Type = ", str(type(n_clicks)))
    print("Value = ", str(n_clicks))

    print("Data Type = ", str(type(reviewtext)))
    print("Value = ", str(reviewtext))

    print("Data Type = ", str(type(style)))
    print("Value = ", style)

    if(n_clicks>0):
        response=pred_review(reviewtext)[0]
        result=[]

        if(response==1):
            result.append("Positive")
            style['background-color']='green'
            result.append(style)
        elif(response==0):
            result.append("Negative")
            style['background-color'] = 'red'
            result.append(style)
        else:
            result.append("Undetermined")
            result.append(style)

        return result




#main
def main():
    load_model()

    load_csv()
    #open_browser()

    global app
    global project_name
    global scrappedetsyReviews
    global pickle_model
    global vocab
    global stopwords

    print("Starting...")
    project_name="Sentimental Analysis and Insights"
    app.title=project_name
    app.layout=app_ui()
    app.run_server(host='0.0.0.0', port=8050)
    print("Ended...")
    app=None
    project_name = None

    scrappedetsyReviews = None
    pickle_model = None
    vocab = None
    stopwords = None



if __name__=="__main__":
    main()
