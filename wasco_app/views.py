from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wasco_app.models import DeviceSettings, DeviceData, LogData
from django.utils import timezone
import datetime
import json
from datetime import datetime, timezone
from django.utils import timezone
import datetime
import pytz
import json
from base64 import b64decode
import codecs
import base64

# Create your views here.

def notification():
    info = []
    notif_dict = {}
    data = DeviceData.objects.all()
    for notif in data:
        if notif.bin_state > 75:
            info.append({
                "data":"Wasco:{} ({}vt - {}%)".format(notif.imei_code, notif.battery, notif.bin_state)
            })
    notif_dict["notif_list"] = info
    return notif_dict


def color():
    pass
        

def index(request):
    context = {}
    context["marker"] = DeviceData.objects.all()
    data = DeviceSettings.objects.all()
    # print(data)
    # d_data = DeviceSettings.objects.all()
    result = []
    test = []
    order = 0

    device_settings_data = DeviceSettings.objects.all()
    for item in device_settings_data:
        d_data = DeviceSettings.objects.get(dev_id=item.dev_id).bin_height
        print(d_data)

    for item in data:
        order = order + 1
        try:
            d_data = DeviceData.objects.get(dev_id=item.dev_id)
            # print(d_data.bin_state)

            if d_data.bin_state<25:
                color = "bg-success"
            elif d_data.bin_state<51:
                color = "yellow"
            elif d_data.bin_state<75:
                color = "orange"
            else:
                color = "bg-danger"
        
            result.append({
                "coords": {"lat": item.latitude, "lng": item.longitude},
                "text": "{} {} {} {}".format(order, item.dev_id or int(0), d_data.battery or int(0), d_data.bin_state or int(0)).split(),
                # "battery": "bg-danger" if (int(d_data.bin_state) or 0) >= 75  else "bg-success",
                "battery": color,
                "device_icon": d_data.device_icon()
            })
        except DeviceData.DoesNotExist:
            result.append({
            "coords": {"lat": item.latitude, "lng":item.longitude},
            "text": "{} {} {} {} {}".format(order, item.dev_id, int(0), int(0), int(0)).split(),
            "battery": "bg-danger",
            "device_icon": "/static/wasco/images/green.png",
            })

    context["object_list"] = result
    return render(request, "index.html", context)


@csrf_exempt
def data(request):
    if request.method =="POST":

        # now = datetime.datetime.utcnow()+datetime.timedelta(hours=4)
        # now = datetime.datetime.now()
        
        a = request.body.decode()
        # type of "a" is str
        # type(a)=string
        print(a)

        # type of "data" is dictionary
        data = json.loads(a)

        
        # print(type(data))

        if type(data) == dict:
            taym = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
            my_data = base64.b64decode(data["payload_raw"]).decode('utf-8')
            my_data = my_data.split(',')
            print(my_data)
            my_data[0] = round((((int(my_data[0]) - 1768)* 8.3) /307) + 91.6, 1) 
            my_data[1] = int(my_data[1])
            print(my_data[0])
            print(my_data[1])

            device_settings_data = DeviceSettings.objects.all()
            for item in device_settings_data:
                d_data = (DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1]*100)/DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1]*100
                # print(d_data)

            LogData.objects.filter(dev_id=data["dev_id"]).create(dev_id=data["dev_id"], battery=my_data[0], bin_state=(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1])*100/DeviceSettings.objects.get(dev_id=item.dev_id).bin_height, request_time=taym)

            if DeviceSettings.objects.filter(dev_id=data["dev_id"]) and DeviceData.objects.filter(dev_id=data["dev_id"]):
                if my_data[1] <= 25:
                    DeviceData.objects.filter(dev_id=data["dev_id"]).update(battery=my_data[0], bin_state="95")
                else:
                    DeviceData.objects.filter(dev_id=data["dev_id"]).update(battery=my_data[0], bin_state=(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1])*100/(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height))


                # if DeviceSettings.objects.get(dev_id=item.dev_id).bin_height < my_data[1]:
                #     DeviceData.objects.filter(dev_id=data["dev_id"]).update(battery=my_data[0], bin_state="-")
                # else:
                #     DeviceData.objects.filter(dev_id=data["dev_id"]).update(battery=my_data[0], bin_state=(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1])*100/(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height))
                print("Updated!")

            elif DeviceSettings.objects.filter(dev_id=data["dev_id"]) and not DeviceData.objects.filter(dev_id=data["dev_id"]):
                if my_data[1] <= 25:
                    DeviceData.objects.filter(dev_id=data["dev_id"]).create(dev_id=data["dev_id"], battery=my_data[0], bin_state="95")
                else:
                    DeviceData.objects.filter(dev_id=data["dev_id"]).create(dev_id=data["dev_id"], battery=my_data[0], bin_state=(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height-my_data[1])*100/(DeviceSettings.objects.get(dev_id=item.dev_id).bin_height))
                print("Created!")

            else:
                print("Error raised! I guess device that sent data is unknown.")
        
        else:
            taym = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
            incoming_data = data.strip()
            if ',' in incoming_data:
                parsed_data = incoming_data.split(',')
            else:
                parsed_data = incoming_data

            LogData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]),request_time=taym)
                
            if DeviceSettings.objects.filter(imei_code=parsed_data[2]) and DeviceData.objects.filter(imei_code=parsed_data[2]):
                DeviceData.objects.filter(imei_code=parsed_data[2]).update(battery=parsed_data[0],bin_state=int(parsed_data[1]))
                print("Update olundu")

            elif DeviceSettings.objects.filter(imei_code=parsed_data[2]) and not DeviceData.objects.filter(imei_code=parsed_data[2]):
                DeviceData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]))
                print("Elave olundu")
            else:
                print("Xeta baş verdi. Cihaz tanınmadı")
            

    return HttpResponse('200')




# @csrf_exempt
# def data(request):
#     if request.method =="POST":

#         # now = datetime.datetime.utcnow()+datetime.timedelta(hours=4)
#         # now = datetime.datetime.now()
        
#         a = request.body.decode()
#         # type of "a" is str
#         # type(a)=string
#         print(a)

#         # type of "data" is dictionary
#         data = json.loads(a)

        
#         # print(type(data))

#         if type(data) == dict:
#             taym = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
#             status = data['data']
#             my_data = base64.b64decode(data["data"])

#             my_data = str(codecs.encode(my_data, 'hex'))
#             my_data = my_data.strip("b").strip("'")
#             # print(type(my_data))


#             coded_data = [0,0]

#             coded_data[0] = my_data[(len(my_data)//2):len(my_data)]
#             coded_data[1] = my_data[0:(len(my_data)//2)]
#             print(coded_data[0])
#             print(coded_data[1])
#             print("")

#             coded_data[0] = int(coded_data[0],16)
#             coded_data[1] = int(coded_data[1],16)

#             print(coded_data[0])
#             print(coded_data[1])
#             print("")



#             coded_data[0] = round(((int(coded_data[0]) - 3350) / 583) * 100, 1) 
#             coded_data[1] = int(coded_data[1])

#             device_settings_data = DeviceSettings.objects.all()
#             for item in device_settings_data:
#                 d_data = (DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20-coded_data[1]*100)/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20-coded_data[1]*100
#                 print(d_data)

#             LogData.objects.filter(deviceName=data["deviceName"]).create(deviceName=data["deviceName"], battery=coded_data[0], bin_state=(DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1])*100/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height, request_time=taym)

#             if DeviceSettings.objects.filter(deviceName=data["deviceName"]) and DeviceData.objects.filter(deviceName=data["deviceName"]):
#                 if DeviceSettings.objects.get(deviceName=item.deviceName).bin_height < coded_data[1]:
#                     DeviceData.objects.filter(deviceName=data["deviceName"]).update(battery=coded_data[0], bin_state="-")
#                 else:
#                     DeviceData.objects.filter(deviceName=data["deviceName"]).update(battery=coded_data[0], bin_state=(DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20-coded_data[1])*100/(DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20))
#                 print("Updated!")

#             elif DeviceSettings.objects.filter(deviceName=data["deviceName"]) and not DeviceData.objects.filter(deviceName=data["deviceName"]):
#                 DeviceData.objects.filter(deviceName=data["deviceName"]).create(deviceName=data["deviceName"], battery=coded_data[0], bin_state=(DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20-coded_data[1])*100/(DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-20))
#                 print("Created!")

#             else:
#                 print("Error raised! I guess device that sent data is unknown.")
        
#         else:
#             taym = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
#             incoming_data = data.strip()
#             if ',' in incoming_data:
#                 parsed_data = incoming_data.split(',')
#             else:
#                 parsed_data = incoming_data

#             LogData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]),request_time=taym)
                
#             if DeviceSettings.objects.filter(imei_code=parsed_data[2]) and DeviceData.objects.filter(imei_code=parsed_data[2]):
#                 DeviceData.objects.filter(imei_code=parsed_data[2]).update(battery=parsed_data[0],bin_state=int(parsed_data[1]))
#                 print("Update olundu")

#             elif DeviceSettings.objects.filter(imei_code=parsed_data[2]) and not DeviceData.objects.filter(imei_code=parsed_data[2]):
#                 DeviceData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]))
#                 print("Elave olundu")
#             else:
#                 print("Xeta baş verdi. Cihaz tanınmadı")
            

#     return HttpResponse('200')





# @csrf_exempt
# def data(request):
#     taym = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
#     incoming_data = request.GET.get("query").strip() #request.body.decode().strip()
#     if ',' in incoming_data:
#         parsed_data = incoming_data.split(',')
#     else:
#         parsed_data = incoming_data

#     LogData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]),request_time=taym)
    
#     if DeviceSettings.objects.filter(imei_code=parsed_data[2]) and DeviceData.objects.filter(imei_code=parsed_data[2]):
#         DeviceData.objects.filter(imei_code=parsed_data[2]).update(battery=parsed_data[0],bin_state=int(parsed_data[1]))
#         print("Update olundu")

#     elif DeviceSettings.objects.filter(imei_code=parsed_data[2]) and not DeviceData.objects.filter(imei_code=parsed_data[2]):
#         DeviceData.objects.filter(imei_code=parsed_data[2]).create(imei_code=parsed_data[2],battery=parsed_data[0],bin_state=int(parsed_data[1]))
#         print("Elave olundu")
#     else:
#         print("Xeta baş verdi. Cihaz tanınmadı")
#     return HttpResponse(parsed_data)
