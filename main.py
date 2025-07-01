from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from realtime import fetch_vehicle_feed, fetch_trip_feed, parse_vehicle_positions, parse_trip_updates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/vehicle_positions")
def get_vehicle_positions():
    feed = fetch_vehicle_feed()
    return JSONResponse(parse_vehicle_positions(feed))

@app.get("/trip_updates")
def get_trip_updates():
    feed = fetch_trip_feed()
    return JSONResponse(parse_trip_updates(feed))
