api_key = 'AIzaSyBOBKE6rrqZqy-tnJGm9An0uweh5e9WA-E'

import googlemaps
import pandas as pd
import time

gmaps = googlemaps.Client(key=api_key)

def get_place_details(college_name, city, state):
    full_address = f"{college_name}, {city}, {state}"
    geocode_result = gmaps.geocode(full_address)
    
    if not geocode_result:
        return None, None
    
    location = geocode_result[0]['geometry']['location']
    return location['lat'], location['lng']


df = pd.read_excel("list of schools.xlsx") 

if 'latitude' not in df.columns:
    df['latitude'] = None
if 'longitude' not in df.columns:
    df['longitude'] = None

for idx, row in df.iterrows():
    lat, lng = get_place_details(row['college_name'], row['city'], row['state'])
    df.at[idx, 'latitude'] = lat
    df.at[idx, 'longitude'] = lng
    print(f"Processed: {row['college_name']} -> Lat: {lat}, Lng: {lng}")
    
    time.sleep(0.1)  

df.to_excel("list_of_schools_with_coordinates.xlsx", index=False)
print("✅ Done! File saved as colleges_with_coordinates.xlsx")