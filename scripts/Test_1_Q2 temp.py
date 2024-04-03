import pandas as pd 
import numpy as np 
from geopy.geocoders import Nominatim
import geopy.distance
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

class GPSdata:
  def __int__(self,file_path=None,n=500000):
    if file_path !=None:
      self.file_path=file_path
    else:
      print("Please provide valid file path!")
    self.data=pd.read_csv(self.file_path,chunksize=n)
    
  def show_n_rows(self,data=None,n=5):
    if data!=None:
      print(data.head(n))
    else:
      print("Provide valid dataframe!")
      
  def get_groped_data(self):
    df=self.data
    df1=df.groupby(['individual_id','trajectory_id']).agg(list)
    return df1
  
  def get_travelled_distance(self):
    df=self.get_groped_data()
    traveled_distance={}

    for index,row in df.iterrows():
      current_id=index[0]
      latitutde_list=row['latitude']
      longitude_list=row['longitude']
      for i in range(0,len(latitutde_list)-1):
        lat=latitutde_list[i]
        lng=longitude_list[i]
        lat_next=latitutde_list[i+1]
        lng_next=longitude_list[i+1]
        coords_1=(lat,lng)
        coords_2=(lat_next,lng_next)
        dist=geopy.distance.geodesic(coords_1, coords_2).km
        
        if not current_id in traveled_distance:
          traveled_distance[current_id]=[dist]
        else:
          traveled_distance[current_id].append(dist) 
          
    for i in range(1,4):
      total_dist=0
      for j in range(0,len(traveled_distance[i])):
        total_dist+=traveled_distance[i][j]
      traveled_distance[i]=total_dist
      
    return traveled_distance
  
  def beijing_lat_lng(self):
    df=self.data
    latlist=list(df.latitude)
    lnglist=list(df.longitude)
    lat_beijing=[]
    lng_beijing=[]
    for i in range(0,len(latlist)):
      latitude=latlist[i]
      longitude=lnglist[i]
      if latitude>=39.768824 and latitude <=40.036496 and longitude>=116.129598 and longitude<=116.685552:
        lat_beijing.append(latitude)
        lng_beijing.append(longitude)
    
  