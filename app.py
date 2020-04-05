import dash
import dash_html_components as html
import dash_design_kit as ddk
import components
from dash.dependencies import Output,Input
import time
import requests
import hashlib

public_key = "yourkey"
private_key = "yourkey"

app = dash.Dash(__name__)
server = app.server
app.title = "Marvel Universe"

theme = {
    "accent": "#ED1D24",
    "accent_negative": "#ff2c6d",
    "accent_positive": "#33ffe6",
    "background_content": "#F9F9F9",
    "background_page": "#F2F2F2",
    "border": "#e2e2e2",
    "border_style": {
        "name": "underlined",
        "borderTopWidth": 0,
        "borderRightWidth": 0,
        "borderLeftWidth": 0,
        "borderBottomWidth": "1px",
        "borderBottomStyle": "solid",
        "borderRadius": 0,
        "inputFocus": {
            "outline": "transparent"
        }
    },
    "breakpoint_font": "1200px",
    "breakpoint_stack_blocks": "700px",
    "colorway": [
        "#fa4f56",
        "#4c78a8",
        "#f58518",
        "#72b7b2",
        "#54a24b",
        "#eeca3b",
        "#b279a2",
        "#ff9da6",
        "#9d755d",
        "#bab0ac"
    ],
    "colorscale": [
        "#fa4f56",
        "#fe6767",
        "#ff7c79",
        "#ff908b",
        "#ffa39d",
        "#ffb6b0",
        "#ffc8c3",
        "#ffdbd7",
        "#ffedeb",
        "#ffffff"
    ],
    "font_family": "Raleway",
    "font_size": "17px",
    "font_size_smaller_screen": "15px",
    "font_family_header": "Roboto",
    "font_size_header": "24px",
    "font_family_headings": "Roboto",
    "text": "#606060",
    "report_font_family": "Computer Modern",
    "report_font_size": "12px",
    "report_background_page": "white",
    "report_background_content": "#FAFBFC",
    "report_text": "black"
}

app.layout = ddk.App(theme=theme,children=[ddk.Block(children=components.search_box),
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
    url = "https://gateway.marvel.com:443/v1/public/characters/%s?&ts=%s&apikey=yourkey&hash=%s" % (value,ts, hash)
    req = requests.get(url)
    name = req.json()["data"]["results"][0]["name"]
    image_src= req.json()["data"]["results"][0]["thumbnail"]["path"] + "/portrait_incredible.jpg"
    description = req.json()["data"]["results"][0]["description"]
    comics_available = req.json()["data"]["results"][0]["comics"]["available"]
    comic_url = "https://gateway.marvel.com:443/v1/public/characters/%s/comics?offset=%s&ts=%s&apikey=yourkey&hash=%s" % (value,comics_available-1,ts, hash)

    events = req.json()["data"]["results"][0]["events"]["available"]
    stories = req.json()["data"]["results"][0]["stories"]["available"]
    series = req.json()["data"]["results"][0]["series"]["available"]


    try:
        comic_name = requests.get(comic_url).json()["data"]["results"][0]["title"]
    except:
        comic_name = "-"
    return name, html.Img(src=image_src), description + "\n\n >First Appeared in:  %s" % (comic_name), comics_available,events,series,stories

if __name__ == "__main__":
    app.run_server(port=8116)
