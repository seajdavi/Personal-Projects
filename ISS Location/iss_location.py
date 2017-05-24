import requests, turtle, time
from math import radians, cos, sin, asin, sqrt

# idea and part of code from here:
# https://codeclubprojects.org/en-GB/python/iss/

# haversine function from url below:
# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula 
    dlong = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles. Use 6371 for kilometers
    #r += 249 # orbital height of space station is 249 miles
    return c * r


def GetLocation():
    result = requests.get('http://api.open-notify.org/iss-now.json')
    json_result = result.json()

    long,lat = (json_result['iss_position']['longitude'],
                json_result['iss_position']['latitude'])

    # convert from strings to floats
    long = float(long)
    lat = float(lat)

    return(long, lat)


def main():
    # for background picture
    screen = turtle.Screen()
    screen.setup(1280,640) #size of pic
    screen.setworldcoordinates(-180,-90,180,90)
    screen.bgpic('world.gif') #bgpic only accepts .gif

    # for iss picture
    screen.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.pencolor('white')
    iss.penup()
    
    


    # begin tracking distance and time
    total_distance = 0
    start_time = time.time()

    # get previous coordinates and update picture once before the while loop
    prev_long, prev_lat = GetLocation()
    iss.goto(prev_long, prev_lat)
    iss.pendown()

    while True:
        # "A single client should try and keep polling to about once every 5 seconds."
        # From http://open-notify.org/Open-Notify-API/ISS-Location-Now/
        time.sleep(20)
        
        long, lat = GetLocation() #get current latitude and longitude
        iss.goto(long, lat) #move it correct position on picture
        distance = haversine(prev_lat, prev_long, lat, long) #calculate distance iss has traveled since last location check 
        total_distance += distance
        
        print('Current Latitude:', lat)
        print('Current Longitude:', long)
        print('Total Distance Traveled Since Starting This:', round(total_distance, 1), 'miles')
        print('Time Elapsed Since Starting This:', int(time.time() - start_time), 'seconds\n')
        
        prev_long = long
        prev_lat = lat


main()
