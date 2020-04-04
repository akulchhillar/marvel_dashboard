import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_design_kit as ddk
import components
from dash.dependencies import Output,Input
import time
import requests
import hashlib

public_key = "d21ee0f608a598d055ec4844c765da8c"
private_key = "1a2ef3e7cd4bb9e0ed8d510512dfaae6af94d71b"

app = dash.Dash(__name__)
app.title = "Marvel Universe"

app.layout = ddk.App(children=[ddk.Block(children=components.search_box),
                               ddk.Block(width=18,children=[
                                ddk.Block(children=components.image),
                               ]),
                               ddk.Block(width=72,children=[
                                   ddk.Block(children=components.name),
                                   ddk.Block(children=components.character_description)
                               ]),
                               ddk.Block(children=[ddk.Block(width=20),
                                                   ddk.Block(width=80,children=[
                                                       components.no_comics,
                                                       components.no_events,
                                                       components.no_series,
                                                       components.no_stories

                                                   ])
                                                   ])





                               ])


@app.callback([Output("name","children"),
               Output("image","children"),
               Output("markdown","children"),
               Output("no_comics","value"),
               Output("no_events","value"),
               Output("no_series","value"),
               Output("no_stories","value")

               ],
              [Input("dropdown","value")])
def update_name(value):
    ts = str(time.time())
    hash = hashlib.md5(ts + private_key + public_key).hexdigest()
    url = "https://gateway.marvel.com:443/v1/public/characters/%s?&ts=%s&apikey=d21ee0f608a598d055ec4844c765da8c&hash=%s" % (value,ts, hash)
    req = requests.get(url)
    name = req.json()["data"]["results"][0]["name"]
    image_src= req.json()["data"]["results"][0]["thumbnail"]["path"] + "/portrait_incredible.jpg"
    description = req.json()["data"]["results"][0]["description"]
    comics_available = req.json()["data"]["results"][0]["comics"]["available"]
    comic_url = "https://gateway.marvel.com:443/v1/public/characters/%s/comics?offset=%s&ts=%s&apikey=d21ee0f608a598d055ec4844c765da8c&hash=%s" % (value,comics_available-1,ts, hash)

    events = req.json()["data"]["results"][0]["events"]["available"]
    stories = req.json()["data"]["results"][0]["stories"]["available"]
    series = req.json()["data"]["results"][0]["series"]["available"]


    try:
        comic_name = requests.get(comic_url).json()["data"]["results"][0]["title"]
    except:
        comic_name = "-"
    return name, html.Img(src=image_src), description + "\n\n >First Appeared in:  %s" % (comic_name), comics_available,events,series,stories






if __name__ == "__main__":
    app.run_server(debug=True,port=8116)
