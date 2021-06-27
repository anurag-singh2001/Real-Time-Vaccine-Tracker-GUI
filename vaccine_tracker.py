from tkinter import *
import requests
import time
import tkinter.messagebox as tmsg
root =Tk()
root.geometry("655x333")
root.title("Vaccine Tracker by Anurag Singh")
root.iconbitmap('icon.ico')
def getvals():
    state=statevalue.get()
    district=districtvalue.get()
    date=datevalue.get()
    print(state)
    print(district)
    print(date)
    url_state='https://cdn-api.co-vin.in/api/v2/admin/location/states'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    state_result=requests.get(url_state,headers=header)
    state_response_json=state_result.json()
    state_data=state_response_json["states"]
    for each in state_data:
        if((each["state_name"]==state)):
            state_id=each["state_id"]
            print(each)
            print(state_id)
         
    url_district='https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state_id)
    district_result=requests.get(url_district,headers=header)
    district_response_json=district_result.json()
    district_data=district_response_json["districts"]
    for districts in district_data:
        if((districts["district_name"]==district)):
            district_id=districts["district_id"]
            print(districts)
            print(district_id)

    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(district_id, date)

    def findAvailability():
        counter=0
        result=requests.get(URL,headers=header)
        response_json=result.json()
        data=response_json["sessions"]
        for vaccine in data:
            if((vaccine["available_capacity"]>0)&(vaccine["min_age_limit"] == 18)):
                counter += 1
                print(vaccine["name"])
                print(vaccine["pincode"])
                print(vaccine["address"])
                print(vaccine["vaccine"])
                print(vaccine["available_capacity"])
                msg='Center: {}\n Pincode: {} \nAddress: {}\n Vaccine: {} \n Available Slot: {} '.format(vaccine["name"],vaccine["pincode"],vaccine["address"],vaccine["vaccine"],vaccine["available_capacity"])
                tmsg.showinfo("Vaccine center information", msg) 
                return True
        if(counter == 0):
            print("No Available Slots")
            tmsg.showinfo("Vaccine center information", "No Available Slots")
            return False


    findAvailability()



Label(root,text="Vaccine Tracker",font="comicsansms 13 bold ",justify='center',pady=15).grid(row=0,column=3)

state=Label(root,text="State")
district=Label(root,text="District")
date=Label(root,text="Date")

state.grid(row=1,column=2)
district.grid(row=2,column=2)
date.grid(row=3,column=2)

statevalue=StringVar()
districtvalue=StringVar()
datevalue=StringVar()

stateentry=Entry(root,textvariable=statevalue)
districtentry=Entry(root,textvariable=districtvalue)
dateentry=Entry(root,textvariable=datevalue)

stateentry.grid(row=1,column=3)
districtentry.grid(row=2,column=3)
dateentry.grid(row=3,column=3)

Button(text="submit", command=getvals).grid(row=7,column=3)
root.mainloop()