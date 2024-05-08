from django.shortcuts import render
from rest_framework.views import APIView    
from rest_framework.response import Response
from decouple import config
import requests
import json

# Create your views here.
def auth_fedex():
    try:
        #input data
        data = {
            'grant_type':'client_credentials',
            'client_id':  config('FEDEX_API_KEY'),
            'client_secret':  config('FEDEX_SECRET_KEY'),

        }
        # headers
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        # make api call
        response= requests.post(f"{config('FEDEX_BASE_API_URL')}/oauth/token",data=data, headers=headers)
        return response.json()


    except Exception as e:
        print('Error authenticating with FedEx API:',e)
        raise ValueError("Failed to authenticate with FedEx API")


class FedexTrackingView(APIView):
    def get(self,req):
        authRes = auth_fedex()
        #input data
        data = json.dumps({
            'includeDetailedScans':True,
            'trackingInfo':[
                {
                    'trackingNumberInfo':{
                        'trackingNumber': 122816215025810
                    }
                }
            ]
        })
        headers = {
             'content-type':"application/json",
             'x-locale':"en_US",
             'authorization':"Bearer "+authRes['access_token']
        }

        #make API call
        response= requests.post(f"{config('FEDEX_BASE_API_URL')}/track/v1/trackingnumbers",data=data, headers=headers)
        print(response)

        if response.status_code == 200:
             #making incoming data into dictionary form to make readable data  by response.json() code

            data = response.json()['output']['completeTrackResults'][0]['trackResults'][0]["scanEvents"]
            #Extract eventdescription and cities using list comprehensions
            tracking_details = [{eventDescription}, for event in data ]


            return Response({"Tracking Details": data})   
        else:
            return Response({'error': 'Failed to fetch tracking information'}, status=response.status_code)


        # return Response({"Auth Res":authRes['access_token']})   
        return Response({"Tracking Details": response.text})   