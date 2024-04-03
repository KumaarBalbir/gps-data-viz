import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import time

# for OSMnX and plotting 
import osmnx as ox
import networkx as nx

ox.settings.log_console=True
ox.settings.use_cache=True

class BikeTrip:
  """
  Class for Solving problems related to Bike trip data.
  """
  def __init__(self,file_path=None):
    if file_path !=None:
      self.file_path=file_path
    else:
      print("Please provide valid file path!")
      return
    self.data=pd.read_csv(self.file_path)
    
  def get_processed_data(self):
    df=self.data
    df['started_at']=pd.to_datetime(df['started_at'])
    df['ended_at']=pd.to_datetime(df['ended_at'])
    df['trip_duration']=(df.ended_at - df.started_at) / pd.Timedelta(minutes=1)
    return df
    
  def show_n_rows(self,data=None,n=5):
    if data!=None:
      print(data.head(n))
    else:
      print("Provide valid dataframe!")
 
  def get_non_zero_trip_data(self):
    df=self.get_processed_data()
    df1=df.loc[df['trip_duration']!=0.0]
    return df1
  
  def maximum_trip_duration(self):
    df=self.get_non_zero_trip_data()
    max_trip_duration=df['trip_duration'].max()
    return max_trip_duration
  
  
  def minimum_trip_duration(self):
    df=self.get_non_zero_trip_data()
    minimum_trip_duration=df['trip_duration'].min()
    return minimum_trip_duration
  
  
  def count_minimum_trip_duration(self):
    df=self.get_non_zero_trip_data()
    count_min_dur=len(df.loc[df['trip_duration']==1.0])
    return count_min_dur
  
  def circular_trip_perc(self):
    df=self.get_non_zero_trip_data()
    circular_trip_count=len(df.loc[(df['start_lat']==df['end_lat']) & (df['start_lng']==df['end_lng'])])
    circular_trip_percentage=(circular_trip_count/len(df))*100
    return circular_trip_percentage
  
  def filter_data(self,start='2023-01-02 06:00:00',end='2023-01-02 18:00:00'):
    df=self.get_processed_data()
    df1=df.loc[(df['started_at'] >= start) & (df['ended_at'] <=end)]
    df1.reset_index(drop=True)
    return df1

  def get_feasible_trips(self):
    df=self.filter_data()
    trip_list=[]
    for index, row in df.iterrows():
      trip_list.append([row['started_at'],row['ended_at'],row['start_lat'],row['end_lat'],row['start_lng'],row['end_lng']])
      
    feasible_trips=[]  
    for i in range(0,len(trip_list)):
      for j in range(i,len(trip_list)):
        if ((trip_list[j][0] >= trip_list[i][1]) and (trip_list[j][2]==trip_list[i][3]) and (trip_list[j][4] == trip_list[i][5])):
          feasible_trips.append([i+1,j+1])
    return(len(feasible_trips))
  
  
  def get_unique_depots(self,FROM=1,TO=100):
    df=self.get_processed_data()
    df1=df.loc[(df['trip_id']>=FROM) & (df['trip_id']<=TO)]
    
    depots_list=[] 
    for index,row in df1.iterrows():
      current_node_start=[row['start_lat'],row['start_lng']]
      current_node_end=[row['end_lat'],row['end_lng']]
      if current_node_start not in depots_list:
        depots_list.append(current_node_start)
      if current_node_end not in depots_list:
        depots_list.append(current_node_end) 
        
    return depots_list
  
  def get_graph(self):
    # plotting a example of shortest path
    # washington,US was found by using a sample latitude and longitude
    place = 'Washington, United States' 
    # finding shortest route based on mode of travel 
    mode='bike' #  'walk' , 'drive' , 'bike'
      
    # finding shortest path based on 
    optimizer='length' # 'time' , 'length' 
    graph=ox.graph_from_place(place, network_type = mode)
    return graph
    
  
  def get_shortest_route_map(self,start_lat=38.90546971,start_lng=-77.00213045,end_lat=38.906299,end_lng=-76.983221):
    graph=self.get_graph()
    # finding shortest path based on 
    optimizer='length' # 'time' , 'length' 

    
    # find the nearest node to the start location
    orig_node = ox.distance.nearest_nodes(graph, start_lng,start_lat)
    # find the nearest node to the end location
    dest_node = ox.distance.nearest_nodes(graph, end_lng,end_lat)
    
    # find the shortest path
    shortest_route = nx.shortest_path(graph,orig_node,dest_node,weight=optimizer,method='dijkstra')
    shortest_route_map = ox.plot_route_folium(graph, shortest_route,tiles='openstreetmap')
    return shortest_route_map
  
  def get_shortest_length(self,start_lat=40,start_lng=116,end_lat=40.3324,end_lng=116.00233):
    graph=self.get_graph()
    orig_node = ox.distance.nearest_nodes(graph, start_lng,start_lat)
    dest_node = ox.distance.nearest_nodes(graph, end_lng,end_lat)
        
    shortest_length=0
    try:
        shortest_length = nx.shortest_path_length(G=graph, source=orig_node, target=dest_node, weight='length')
    except nx.NetworkXNoPath:
        shortest_length=-1  
    return shortest_length 
  
  def get_all_pair_shortest_length(self,node_count=3):
    # taking only 5 pairs shortest length for time complexity
    pairwise_shortest_length= [ [-2]*node_count for i in range(node_count)]
    for i in range(0,node_count):
      pairwise_shortest_length[i][i]=0
      
    depots_list=self.get_unique_depots()
    for i in range(0,node_count):
      for j in range(i+1,node_count):
        dist=self.get_shortest_length(depots_list[i][0],depots_list[i][1],depots_list[j][0],depots_list[j][1])
        pairwise_shortest_length[i][j]=dist
        pairwise_shortest_length[j][i]=dist
    
    min_val=0
    max_val=0
    all_pos_val=[]
    for lst in pairwise_shortest_length:
      for ele in lst:
        if ele>0:
          all_pos_val.append(ele)
          
    min_val=min(all_pos_val)
    max_val=max(all_pos_val)
    print(f"Pairwise shortest length for {node_count} depots:\n") 
       
    for i in range(0,len(pairwise_shortest_length)):
      for j in range(0,len(pairwise_shortest_length[i])):
        print(f"Distance between {i+1} and {j+1} is: {pairwise_shortest_length[i][j]} \n")
    print(f"Maximum shortest distance: {max_val}")
    print(f"Minimum shortest distance : {min_val}")
    return
    


### Main function #####
    
if __name__=="__main__":
  print("Hello\n")
  file_path='../data/bike_data_new.csv'
  trip_obj=BikeTrip(file_path=file_path)
  
  print("Main funtion started:")
  beg=time.time()
  
  mx=trip_obj.maximum_trip_duration()
  print(f"Maximum duration of the trip is: {mx} \n")
  
  mn=trip_obj.minimum_trip_duration()
  print(f"Minimum duration of the trip is: {mn} \n")
  
  mn_cnt=trip_obj.count_minimum_trip_duration()
  print(f"Count of Minimum duration of the trip is: {mn_cnt} \n")
  
  perc_circular=trip_obj.circular_trip_perc()
  print(f"Percentage of the circular trip is: {perc_circular} \n")
  
  endt=time.time()
  
  print(f"Total runtime of all the above functions are: {endt-beg} seconds \n")
  
  
  beg=time.time()
  
  df=trip_obj.filter_data()
  print("Printing first 5 rows of data from 6AM to 6PM..\n")
  print(df.head(5))
  
  feasible_cnt=trip_obj.get_feasible_trips()
  print(f"Number of feasible trips are: {feasible_cnt} \n")
  
  endt=time.time()
  print(f"Runtime for this function is: {endt-beg} seconds \n")
  
  depot_cnt=trip_obj.get_unique_depots()
  depot_cnt=len(depot_cnt)
  print(f"The unique depots count: {depot_cnt} \n")
  
  print("Printing a sample of shortest route path on map..\n")
  # print(trip_obj.get_shortest_route_map())
  
  beg=time.time()
  print("Pairwise shortest path distance: \n")
  trip_obj.get_all_pair_shortest_length()
  endt=time.time()
  print(f"Runtime for the above function is: {endt-beg} seconds \n")
  
  print("End of the Program!!")
  
  
  
    
    
    
    

  
  
  
  

    
     
    
    
    
    
    
    
    
    