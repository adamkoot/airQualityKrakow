from tkinter import *
import requests
import json

root = Tk()
root.title("Air quality")

# centrowanie okna na ekranie
appWidth = 450
appHeight = 300

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)

root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

root.configure(background='white')

modes = []
id=[]
#ciagniemy jak slota
try:
    apiRequestsCity = requests.get("http://api.gios.gov.pl/pjp-api/rest/station/findAll")
    apiCity = json.loads(apiRequestsCity.content)
    for sensor in apiCity:
        if 'Kraków' in sensor['city']['name']:
            #x = sensor['stationName']
            #y = sensor['id']

            #modes.append((x,y))
            modes.append(sensor['stationName'])
            id.append(sensor['id'])


except Exception as apiError:
    api = "Error..."

for x in modes:
    print(x)
for x in id:
    print(x)
pizza = StringVar()
pizza.set("pusto")

n=0
for mode in modes:
    Radiobutton(root, text=mode, variable=pizza, value=mode, bg="white").grid(column=0, row=n, columnspan=1, sticky=EW)
    n+=1

n+=1
myButton = Button(root, text="sprawdz!", command=lambda: userOption(pizza.get()))
myButton.grid(column=0, row=n, columnspan=1, sticky=N)

cityLabel = Label(root, font=('Helvetica', 10))
cityLabel.grid(column=1, row=0, columnspan=2, sticky=EW)

pm10LabelName = Label(root, font=('Helvetica', 10))
pm10LabelName.grid(column=1, row=2, sticky=NS)
pm10LabelValue = Label(root, font=('Helvetica', 10))
pm10LabelValue.grid(column=2, row=2, sticky=NS)

co2LabelName = Label(root, font=('Helvetica', 20))
co2LabelName.grid(column=1, row=1, sticky=NS)
co2LabelValue = Label(root, font=('Helvetica', 10))
co2LabelValue.grid(column=2, row=1, sticky=NS)

pm25LabelName = Label(root, font=('Helvetica', 10))
pm25LabelName.grid(column=1, row=3, sticky=NS)
pm25LabelValue = Label(root, font=('Helvetica', 10))
pm25LabelValue.grid(column=2, row=3, sticky=NS)

def userOption(city):
    pad = 0
    for index, value in enumerate(modes):
        if value == city:
            print(index)
            pad = index
    print(pad)
    tak = id[pad]
    print(tak)

    ipa = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/"+str(tak)
    apiRequestsSensors = requests.get(ipa)
    co2 = "co2"
    pm10 = "pm10"
    pm25 = "pm25"

    cy = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/"+str(tak)
    apiValue = requests.get(cy)
    apiValue = json.loads(apiValue.content)

    if apiValue['coIndexLevel'] != None:
        co2Value = apiValue['coIndexLevel']['indexLevelName']
    else:
        co2Value = "blad"

    if apiValue['pm10IndexLevel'] != None:
        pm10Value = apiValue['pm10IndexLevel']['indexLevelName']
    else:
        pm10Value = "blad"

    if apiValue['pm25IndexLevel'] != None:
        pm25Value = apiValue['pm25IndexLevel']['indexLevelName']
    else:
        pm25Value = "blad"

    cityLabel["text"] = city

    color = "black"

    if co2Value == 'Bardzo dobry':
        color = 'green'
    elif co2Value == 'Dobry':
        color = 'orange'
    elif co2Value == 'Umiarkowany':
        color = '#000000'
    else:
        color = 'pink'

    co2LabelName["text"] = co2
    co2LabelValue["text"] = co2Value
    co2LabelValue["fg"] = color

    if pm10Value == 'Bardzo dobry':
        color = 'green'
    elif pm10Value == 'Dobry':
        color = 'orange'
    elif pm10Value == 'Umiarkowany':
        color = '#000000'
    else:
        color = 'pink'

    pm10LabelName["text"] = pm10
    pm10LabelValue["text"] = pm10Value
    pm10LabelValue["fg"] = color

    if pm25Value == 'Bardzo dobry':
        color = 'green'
    elif pm25Value == 'Dobry':
        color = 'orange'
    elif pm25Value == 'Umiarkowany':
        color = '#000000'
    else:
        color = 'pink'

    pm25LabelName["text"] = pm25
    pm25LabelValue["text"] = pm25Value
    pm25LabelValue["fg"] = color


root.mainloop()