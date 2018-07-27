from bottle import route,run,request,response
import time,requests
from PIL import Image, ImageDraw, ImageFont

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        #fix No Access-Control-Allow-Origin header is present on the requested resource on ajax request
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/departure',method='GET')
@enable_cors #add headers
def get_departure_data_from_server():
    starTime = request.query.starTime
    endTime = request.query.endTime
    #print values for debug
    print("WEB starTime: %s , endTime: %s " % (starTime,endTime))

    result = []

    url = "https://new.svo.aero/bitrix/timetable/?direction=departure&dateStart="
    url+= time.strftime("%Y-%m-%d") + "T" + starTime + ":59%2B03:00&dateEnd="
    url+= time.strftime("%Y-%m-%d") + "T" + endTime + ":59%2B03:00&perPage=99999&page=0&locale=ru"

    #print urls for debug
    print("URL : " , url )

    get_departure_data = requests.get(url)
    data =  get_departure_data.json()
    arr = data["items"]

    for x in range(0,len(arr)):
        #if we have accurate time
        #add all data to list
        if arr[x]['t_st'] != None:
            status_time = time.strptime(arr[x]['t_st'][11:16],"%H:%M")
            result.append(time.strftime("%H:%M",status_time)+";"
                                        +arr[x]['co']['code']+";"
                                        +arr[x]['flt']+";"
                                        +arr[x]['term']+";"
                                        +arr[x]['vip_status_rus'])
        #another way set value "Нет точных данных" for time
        else:
            result.append("Нет точных данных",
                            arr[x]['co']['code'],
                            arr[x]['flt'],
                            arr[x]['term'],
                            arr[x]['vip_status_rus'])

    str = "\n".join(result)
    create_image(result)
    return str

#create image for result
def create_image(list):
    #calculate enought size for rows
    size = 300,(len(list)*17)
    font = ImageFont.truetype("Times New Roman.ttf",12)

    im = Image.new("RGB",size,color=(255,255,255))
    d = ImageDraw.Draw(im)
    y=10
    for x in list:
        d.text((10,y),x,fill=0,font=font)
        y+=15
    im.save("image.png")


@route('/arrival',method='GET')
@enable_cors #add headers
def get_arrival_data_from_server():
    starTime = request.query.starTime
    endTime = request.query.endTime

    #print values for debug
    print("WEB starTime: %s , endTime: %s " % (starTime,endTime))

    result = []

    url = "https://new.svo.aero/bitrix/timetable/?direction=arrival&dateStart="
    url+= time.strftime("%Y-%m-%d") + "T" + starTime + ":59%2B03:00&dateEnd="
    url+= time.strftime("%Y-%m-%d") + "T" + endTime + ":59%2B03:00&perPage=99999&page=0&locale=ru"
    #print url for debug
    print("URL : " , url )

    get_arrival_data = requests.get(url)
    data =  get_arrival_data.json()
    arr = data["items"]


    for x in range(0,len(arr)):
        #if we have accurate time
        #add all data to list
        if arr[x]['t_st'] != None:
            status_time = time.strptime(arr[x]['t_st'][11:16],"%H:%M")
            result.append(time.strftime("%H:%M",status_time)+";"
                                        +arr[x]['co']['code']+";"
                                        +arr[x]['flt']+";"
                                        +arr[x]['term']+";"
                                        +arr[x]['vip_status_rus'])
        #another way set value "Нет точных данных"
        else:
            result.append("Нет точных данных",
                            arr[x]['co']['code'],
                            arr[x]['flt'],
                            arr[x]['term'],
                            arr[x]['vip_status_rus'])
    #convert to string for web responce
    str = "\n".join(result)
    #make image
    create_image(result)
    return str

if __name__ == '__main__':
    run(debug=True,reloader=True,port=8080)
