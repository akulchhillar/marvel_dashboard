import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_design_kit as ddk
import pandas as pd

df = pd.read_excel("consolidated.xlsx")
id_2 = df["id"].to_list()
name_2 = df["name"].to_list()

character_names_dict = dict(zip(id_2,name_2))

character_names_list = []

for k,v in character_names_dict.iteritems():
    character_names_list.append({"label": v,"value": k})

search_box = ddk.ControlCard(rounded=True,children=[ddk.ControlItem(children=[dcc.Dropdown(id="dropdown",options=character_names_list, value=1009368)])])

image = ddk.Card(id="image", children=html.Img(src="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55/portrait_incredible.jpg"),rounded=True)

name = ddk.Card(style={"height": 120},children=html.H1(id="name",children="Iron Man",style={"textAlign": "center", "height": 75}), rounded=True)

character_description = ddk.Card(rounded=True, children=dcc.Markdown(id="markdown",children=
    '''
    Wounded, captured and forced to build a weapon by his enemies, billionaire industrialist Tony Stark instead created an advanced suit of armor to save his life and escape captivity. Now with a new outlook on life, Tony uses his money and intelligence to make the world a safer, better place as Iron Man.
    

   > %s
    '''
%("First Appeared in: Marvel Masterworks The Invincible Iron Man Vol. 1 (Hardcover)")))

no_comics = ddk.DataCard(id="no_comics",label="Comic Appearances",value=2561,width=20)
no_events = ddk.DataCard(id="no_events",label="Events",value=31,width=20)
no_series = ddk.DataCard(id="no_series",label="Series",value=626,width=20)
no_stories = ddk.DataCard(id="no_stories",label="Stories",value=3880,width=20)
