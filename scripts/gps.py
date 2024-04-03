import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy.distance
from PIL import Image, ImageDraw


class GPSVis(object):
    """
        Class for GPS data visualization using pre-downloaded OSM map in image format.
    """
    def __init__(self, data_path, map_path, points):
        """
        :param data_path: Path to file containing GPS records.
        :param map_path: Path to pre-downloaded OSM map in image format.
        :param points: Upper-left, and lower-right GPS points of the map (lat1, lon1, lat2, lon2).
        """
        self.data_path = data_path
        self.points = points
        self.map_path = map_path

        self.result_image = Image
        self.x_ticks = []
        self.y_ticks = []

    def plot_map(self, output='save', save_as='../results/resultMap.png'):
        """
        Method for plotting the map. You can choose to save it in file or to plot it.
        :param output: Type 'plot' to show the map or 'save' to save it.
        :param save_as: Name and type of the resulting image.
        :return:
        """
        self.get_ticks()
        fig, axis1 = plt.subplots(figsize=(10, 10))
        axis1.imshow(self.result_image)
        axis1.set_xlabel('Longitude')
        axis1.set_ylabel('Latitude')
        axis1.set_xticklabels(self.x_ticks)
        axis1.set_yticklabels(self.y_ticks)
        axis1.grid()
        if output == 'save':
            plt.savefig(save_as)
        else:
            plt.show()

    def create_image(self, color, width=2):
        """
        Create the image that contains the original map and the GPS records.
        :param color: Color of the GPS records.
        :param width: Width of the drawn GPS records.
        :return:
        """
        data = pd.read_csv(self.data_path, names=['Latitude', 'Longitude'], sep=',')

        self.result_image = Image.open(self.map_path, 'r')
        img_points = []
        gps_data = tuple(zip(data['Latitude'].values, data['Longitude'].values))
        for d in gps_data:
            x1, y1 = self.scale_to_img(d, (self.result_image.size[0], self.result_image.size[1]))
            img_points.append((x1, y1))
        draw = ImageDraw.Draw(self.result_image)
        draw.line(img_points, fill=color, width=width)

    def scale_to_img(self, lat_lon, h_w):
        """
        Conversion from latitude and longitude to the image pixels.
        It is used for drawing the GPS records on the map image.
        :param lat_lon: GPS record to draw (lat1, lon1).
        :param h_w: Size of the map image (w, h).
        :return: Tuple containing x and y coordinates to draw on map image.
        """
       
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((float(lat_lon[0]) - float(old[0])) * (float(new[1]) - float(new[0])) / (float(old[1]) - float(old[0]))) + float(new[0])
        old = (float(self.points[1]), float(self.points[3]))
        new = (0, h_w[0])
        x = ((float(lat_lon[1]) - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        # y must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        return int(x), h_w[1] - int(y)

    def get_ticks(self):
        """
        Generates custom ticks based on the GPS coordinates of the map for the matplotlib output.
        :return:
        """
        self.x_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[1], self.points[3], num=7))
        y_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[2], self.points[0], num=8))
        # Ticks must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        self.y_ticks = sorted(y_ticks, reverse=True)
        
        
        
        
## class for question 2

class GPSdata:
  def __init__(self,file_path=None,n=500000):
    if file_path !=None:
      self.file_path=file_path
    else:
      print("Please provide valid file path!")
      return
    self.data=pd.read_csv(self.file_path,nrows=n)
    
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
        
    beijing_data=[lat_beijing,lng_beijing]
    return beijing_data
  
  def get_csv_beijing_data(self):
    beijing_data=self.get_csv_beijing_data()
    data=pd.DataFrame(beijing_data, index=['Latitude', 'Longitude']).T
    data.to_csv('beijing_data.csv',header=False,index=False)
    
    
    
######  Main funtion  ########

if __name__=="__main__":
  print("Main function started...")
  print("Please wait a moment for the results to be printed..")
  file_path='../data/combined_trajectories.csv'
  gps_obj=GPSdata(file_path=file_path)
  
  travel_dist=gps_obj.get_travelled_distance()
  print("Travelled distance: \n")
  for key in travel_dist:
    print(f"User id: {key} and distance travelled is: {travel_dist[key]}")
    
  



  vis = GPSVis(data_path='beijing_data.csv',
              map_path='../results/map_beijing.png',  # Path to map downloaded from the OSM.
              points=(40.0399, 116.0760, 39.7232, 116.7188)) # Two coordinates of the map (upper left, lower right)

  vis.create_image(color=(255, 0, 0), width=3)  # Set the color and the width of the GNSS tracks.
  vis.plot_map(output='save')

  print()
        
        