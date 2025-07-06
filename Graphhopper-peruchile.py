import requests
import urllib.parse


route_url = "https://graphhopper.com/api/1/route?"
key = "af5c6b59-c520-4b70-ac60-2c1ddeddb79a" ## API KEY de usuario de graphhopper

def geocoding (location, key):
    while location == "":
        location = input("ingresa la dirección nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1",
"key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""

        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0: 
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geolocalizando lugar: " + new_loc + " (Location Type: " + value + ")\n")
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " +
json_data["message"]) 
    return json_status,lat,lng,new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfil de vehiculos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Elige un perfil de vehiculo de la lista de arriba(o 's' para salir): ")
    if vehicle == "s" or vehicle == "salir":
        print("=============================================")
        print(".........has salido de la aplicación.........")
        print("=============================================")
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("perfil de vehiculo invalido, usando perfil de car.")
    loc1 = input("Ciudad de origen(o 's' para salir): ")
    if loc1 == "salir" or loc1 == "s":
        print("=============================================")
        print(".........has salido de la aplicación.........")
        print("=============================================")
        break
    orig = geocoding(loc1, key)
    
    loc2 = input("Ciudad de destino(o 's' para salir): ")
    if loc2 == "salir" or loc2 == "s":
        print("=============================================")
        print(".........has salido de la aplicación.........")
        print("=============================================")
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        #print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" +
    #paths_url)
    print("=================================================")
    print("Direcciones de ruta desde " + orig[3] + " a " + dest[3] + " en " + vehicle)
    print("=================================================")
    if paths_status == 200:
        miles = (paths_data["paths"][0]["distance"])/1000/1.61
        km = (paths_data["paths"][0]["distance"])/1000
        sec = int(paths_data["paths"][0]["time"]/1000%60)
        min = int(paths_data["paths"][0]["time"]/1000/60%60)
        hr = int(paths_data["paths"][0]["time"]/1000/60/60) 
        print("Distancia del viaje: {0:.1f} millas / {1:.1f} km".format(miles, km))
        print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
        print("=================================================") 
        for each in range(len(paths_data["paths"][0]["instructions"])):
            path = paths_data["paths"][0]["instructions"][each]["text"]
            distance = paths_data["paths"][0]["instructions"][each]["distance"]
            print("{0} ( {1:.1f} km / {2:.1f} millas )".format(path, distance/1000,
            distance/1000/1.61))
        print("=============================================")
    else:
        print("Error: " + paths_data["message"])
        print("*************************************************")     