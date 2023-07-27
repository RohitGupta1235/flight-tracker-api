from bs4 import BeautifulSoup
from lxml import etree
import requests
import folium
from geopy.geocoders import ArcGIS
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='.')

# def get_db():
#     db = pymysql.connect(host="localhost",user="root",passwd="",database="flight-database")
#     return db
  
def get_info(data:list)->list:
  
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

    regNum = data["data"][0]["aircraft"]["regNumber"]
    URL = f"https://www.jetphotos.com/photo/keyword/{regNum}"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    img = soup.find("a", {"class": "result__photoLink"})
    URL = f"https://www.jetphotos.com{img['href']}"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    img = soup.find_all("img")
    # print(img[2]['srcset'])
    data["image"] = img[2]['srcset']
    return data

def get_map(departure:str,arrival:str):
    nom = ArcGIS()
    lat1 , lon1 = nom.geocode(departure)[1]
    lat2 , lon2 = nom.geocode(arrival)[1]  
    m = folium.Map(location=[lat1, lon1],zoom_start=6)
    folium.Marker(
    [lat1, lon1], popup=f"""<b>{departure}</b>""",icon=folium.DivIcon(html="""<div><img style="filter: brightness(0) invert(0.3);" src='https://gistcdn.githack.com/samrath-sudesh-acharya/6a88e910264def1727ff858157b635c4/raw/b2fa31b378af6593f037bd7869d1df7890cc4544/plane-departure.svg' title='plane-departure' height='32px' width='32px' /></div>""")).add_to(m)
    folium.Marker(
    [lat2, lon2], popup=f"""<b>{arrival}</b>""",icon=folium.DivIcon(html="""<div><img style="filter: brightness(0) invert(0.3);" src='https://gistcdn.githack.com/samrath-sudesh-acharya/d36aedb15a5f492a9a1c4f2701a76421/raw/48a72d62f49b63375944d88d0254a834ac75cf06/plane-arrival.svg' title='plane-arrival' height='32px' width='32px' /></div>""")).add_to(m)
    folium.PolyLine([(lat1,lon1),(lat2,lon2)],color='darkgrey',dash_array='10').add_to(m)
    m.save('app/html/map.html')


