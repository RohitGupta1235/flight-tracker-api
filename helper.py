from bs4 import BeautifulSoup
from lxml import etree
import requests
import folium
from geopy.geocoders import ArcGIS
from fastapi.responses import HTMLResponse
import codecs
  
def get_info(data:list)->list:
    iata =  data[0]["flight"]["iata"] 
    URL = f"https://www.radarbox.com/data/flights/{iata}"
  
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    tail_number = dom.xpath('//div[@id="value"]/a/text()')
    if(len(tail_number)!=0):
        tail_number= tail_number[3]
        # print(tail_number)
    else:
        for i in range(len(data)):
            data[i]["image"] = "null"
            data[i]["registration number"] = None
        return data

    URL = f"https://www.jetphotos.com/photo/keyword/{tail_number}"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    img = soup.find("a", {"class": "result__photoLink"})
    URL = f"https://www.jetphotos.com{img['href']}"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    img = soup.find_all("img")
    # print(img[2]['srcset'])
    for i in range(len(data)):
        data[i]["image"] = img[2]['srcset']
        data[i]["registration number"] = tail_number
    return data

def get_map(departure:str,arrival:str):
    nom = ArcGIS()
    lat1 , lon1 = nom.geocode(departure)[1]
    lat2 , lon2 = nom.geocode(arrival)[1]  
    m = folium.Map(location=[lat1, lon1],zoom_start=6)
    folium.Marker(
    [lat1, lon1], popup=f"""<b>{departure}</b>""",icon=folium.DivIcon(html="""<div><img style="filter: brightness(0) invert(0.3);" src='plane-departure-solid.svg' title='plane-departure' height='32px' width='32px' /></div>""")).add_to(m)
    folium.Marker(
    [lat2, lon2], popup=f"""<b>{arrival}</b>""",icon=folium.DivIcon(html="""<div><img style="filter: brightness(0) invert(0.3);" src='plane-arrival-solid.svg' title='plane-arrival' height='32px' width='32px' /></div>""")).add_to(m)
    folium.PolyLine([(lat1,lon1),(lat2,lon2)],color='darkgrey',dash_array='10').add_to(m)
    m.save('map.html')
    with codecs.open("map.html", "r") as f :
        index = f.read()
    return HTMLResponse(content=index, status_code=200)

