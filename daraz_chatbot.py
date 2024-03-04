import dash
import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
import nltk
import re
import pandas as pd
import os
import streamlit as st



os.chdir(r"C:\Users\HP\Desktop\Projects\Daraz_chatbot")
data = pd.read_csv("Daraz_data.csv")

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
mobile_phone=["Used Apple iPhone X ", 
              "Redmi Note 12", "Redmi A2",
              "Infinix Note 30 Pro", "Infinix Note 30",
              "Used Apple iPhone SE", "Tecno SPARK 10 PRO",
              "Tecno POVA 5","Realme C33",
              "Samsung Galaxy A34", 
              "Samsung Galaxy A24",
              "Samsung Galaxy A14", 
              "Itel S23", "Samsung Galaxy A04",
              "Samsung Galaxy A54",
              "Samsung Galaxy A04",
              "Samsung Galaxy A04e", 
              "Redmi 12",
              "Nokia C31", 
              "Redmi Note 12", 
              "Redmi A1 Plus",
              "Infinix Hot 30 Play", 
              "Nokia C31",
              "Nokia C31", 
              "Samsung Galaxy A14", 
              "iPhone X ","Infinix Smart 7",
              "Samsung Galaxy Fold",
              "GOOGLE PIXEL 4a", "Samsung A14", "Realme Narzo 50A Prime",
              "Redmi 12C", "Redmi 12C", "Infinix Hot 30", 
              "Redmi A2+","Infinix Note 30",
              "Infinix Note 30", "Infinix Note 30 Pro", 
              "Redmi Note 12","Redmi A2 Plus",
              "Tecno Camon 20", "Tecno Spark 10 Pro", "INFINIX NOTE 30", "Oppo A57",
              "Xiaomi Redmi Note 12", "itel S23", "Tecno Spark Go", "Infinix Hot 30","Xiaomi 13T",
              "Infinix Note 30 Pro", "Infinix Smart 7","Tecno Spark 10 Pro",
              "Xiaomi Poco X5 Pro", "Infinix Hot 30", "Xiaomi Poco X5 Pro",
              "Samsung Galaxy A54", "Infinix Note 30", "Xiaomi Poco X5 Pro",
              "Xiaomi Redmi Note 12", "Redmi Note 12 Pro", "Infinix Hot 30 Play",
              "Xiaomi Redmi Note 12 Pro", "Vivo Y17s", 
              "Redmi Note 12 Pro",
              "Tecno Spark 10C", "Samsung Galaxy Z Flip 4", 
              "Redmi 12C",
              "Xiaomi Redmi Note 12", "Infinix Note 30", 
              "Tecno Camon 20",
              "Samsung Galaxy A04s", "itel A60s", 
              "Tecno CAMON 20","Infinix Hot 30",
              "Infinix Note 30", "Tecno Camon 20", 
              "Used Apple iPhone 8",
              "Tecno Camon 20", "Redmi Note 12", 
              "Itel A60s", "Xiaomi Redmi 12C", "Sparx Neo X",
              "Redmi A2 Plus", "Samsung A54", "Infinix Note 30 Pro",
              "Redmi 12", "Used Apple iPhone 8 Plus", "Xiaomi Redmi 12", "Infinix Note 30 Pro",
              "infinix Smart 7 HD", "Tecno Spark 10 Pro", "Redmi A2 Plus", 
              "Redmi 12C", "Tecno Camon 20", "Oppo A57", "Infinix Note 30 Pro",
              "Infinix Smart 7" , "Vivo Y85","samsung", "vivo","infinix", "iphones", "iphone"
       
]

mobile_phone_lower = [phone.lower() for phone in mobile_phone]

#  stopwords set
stopwords = set(stopwords.words('english'))

# preprocess function
def preprocess(user_query):
    list1 =[]
    wd = WordNetLemmatizer()
    
    for word in nltk.word_tokenize(user_query):
        word = word.lower()
        word = wd.lemmatize(word)
        if word not in stopwords:
            list1.append(word)
    
    return list1

def extract_info(user_text):
    extracted_data={}
    
    
    # Extract product name
    mobile_name_regex = r"(?i)\b(?:{})\b".format('|'.join(mobile_phone_lower))
    mobile_name_match = re.search(mobile_name_regex, user_query)
    if mobile_name_match:
        mobile = mobile_name_match.group()
        print("Mobile:",mobile)
        extracted_data['Mobile'] = mobile
        
    
    # Extract rating
    rating_regex = r"\b([0-5](?:\.[0-9])?)\b"
    rating_match = re.search(rating_regex, user_query)
    if rating_match:
        rating = rating_match.group()
        print("Rating:",rating)
        extracted_data['Product Ratings'] = rating
    
    # Extract battery
    battery_regex = r"\b(\d+)\s*(mAh|mah)\b"
    battery_match = re.search(battery_regex, user_query)
    if battery_match:
        battery = battery_match.group()
        print("Battery",battery)
        extracted_data['Battery']=battery
        
    
    # Extract display
    display_regex = r"\b(\d+(?:\.\d+)?)\s*(inch|inches)\b"
    display_match = re.search(display_regex, user_query)
    if display_match:
        display = display_match.group()
        print("Display", display)
        extracted_data['Display'] = display
    
    # Extract delivery type
    delivery_regex = r"\b(?:free delivery|standard delivery|no delivery|fastest delivery)\b"
    delivery_match = re.search(delivery_regex, user_query)
    if delivery_match:
        delivery = delivery_match.group()
        print("Delivery:", delivery)
        extracted_data['Shipping Status']=delivery
    
    # Extract Shipment On time score
    shipment_score_regex = r'\b([1-9]?[0-9]|100)\b'
    shipment_score_match = re.search(shipment_score_regex, user_query)
    if shipment_score_match:
        shipment = shipment_score_match.group()
        print("Shipment:",shipment)
        extracted_data['Ship On Time Score']=shipment
    

    # RAM
    ram_regex = r"(?i)(\d+)\s*(?:gb|gigabytes|tb|terabytes|mb|megabytes|kb|kilobytes)\s*ram"
    ram_match = re.search(ram_regex, user_query)
    if ram_match:
        ram = ram_match.group()
        print("RAM:", ram)
        extracted_data['RAM'] = ram

    # Camera
    camera_regex = r"(?i)(\d+)\s*(?:mp|megapixel)\s*camera"
    camera_match = re.search(camera_regex, user_query)
    if camera_match:
        camera = camera_match.group()
        print("Camera:", camera)
        extracted_data['Camera'] = camera

        
    # Extract ROM data
    rom_regex = r'(?i)(\d+)\s*(?:gb|gigabytes|tb|terabytes|mb|megabytes|kb|kilobytes)\s*rom'
    rom_match = re.search(rom_regex, user_query)
    if rom_match:
        rom = rom_match.group()
        print("ROM",rom)
        extracted_data['ROM']=rom
    
    #PTA Approved Data
    pta_regex = r"PTA Approved"
    pta_match = re.search(pta_regex, user_query)
    if pta_match:
        pta = pta_match.group()
        print("PTA Approved")
        extracted_data['PTA']=pta
        
    #Price
    price_regex = r"(?i)(?:Rs\.?\s?)?(\d{3,})"
    price_match=re.search(price_regex, user_query)
    if price_match:
        price=price_match.group()
        print("Price:",price)
        extracted_data['Price']=price
        
    # Price Range
    price_range_regex = r"(?i)(?:under|between|under the price of|below|to|upto|less than|over|above|more than)\s*(\d+(?:\.\d+)?)\s*(?:k|K|thousand|million|billion)?"
#     price_range_regex= r'(\d+)k\s*(under|below|above|more than| less than|under the price of)\s*(\d+)(?:k|K)'
    price_range_match = re.findall(price_range_regex, user_query)
    if price_range_match:
        print(price_range_match)
        min_price = int(price_range_match[0]) if price_range_match else 0
        max_price = int(price_range_match[1]) if len(price_range_match) > 1 else 0
        print("Price Range (Min, Max):", min_price, ",", max_price)
    
        extracted_data['Min Price'] = min_price
        extracted_data['Max Price']= max_price

    #Daraz Mall Verified
    mall_regex=r"(daraz\s*mall\s*verified|not\s*available)"
    mall_match=re.search(mall_regex,user_query)
    if mall_match:
        mall=mall_match.group()
        print("Daraz Mall Verified")
        extracted_data['Daraz Mall Status']=mall

    #Extract Color Info
    color_pattern = r"\b(red|blue|green|yellow|orange|purple|gray|grey|black|gold|silver|matte)\b"
    colors = re.search(color_pattern, user_query)
    if colors:
        c=colors.group()
        print(c)
        extracted_data['Color']=c
    
    # Storage Capacity
    storage_regex = r"(?i)(\d+)\s*(?:gb|gigabytes)\s*(?:storage|capacity)"
    storage_match = re.search(storage_regex, user_query)
    if storage_match:
        storage = storage_match.group()
        print("Storage Capacity:", storage)
        extracted_data['Storage Capacity'] = storage
        
        
    return extracted_data


#filter data
def filter_data(data):
    os.chdir(r"C:\Users\HP\Desktop\Projects\Daraz_chatbot")
    data = pd.read_csv("Daraz_data.csv")

    data = data.apply(lambda x: x.astype(str).str.lower())

    filtered_df = data

    # Filter based on Mobile Name
    if 'Mobile' in extracted_data:
        filtered_df = filtered_df[filtered_df['Product Title'].str.contains(extracted_data['Mobile'], case=False, na=False)]

    # Filter based on Product Rating
    elif 'Product Ratings' in extracted_data:
        if not filtered_df[filtered_df['Product Rating'] == float(extracted_data['Product Ratings'])].empty:
            filtered_df = filtered_df[filtered_df['Product_Rating'] == extracted_data['Product Ratings']]
            print(filtered_df)

    elif 'Battery' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['Battery'], case=False, na=False)]

    elif 'Display' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['Display'], case=False, na=False)]

    elif 'Shipping Status' in extracted_data:
        filtered_df = filtered_df[filtered_df['Shipment Status'] == extracted_data['Shipping Status']]
            
    elif 'RAM' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['RAM'], case=False, na=False)]

    elif 'ROM' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['ROM'], case=False, na=False)]

    elif 'Camera' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['Camera'], case=False, na=False)]

    elif 'PTA' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['PTA'], case=False, na=False)]

    # elif 'Price' in extracted_data:
    #     filtered_df = filtered_df[filtered_df['Price'].astype(int) == extracted_data['Price']]

    elif 'Daraz Mall Status' in extracted_data:
        filtered_df = filtered_df[filtered_df['Mall Varification'] == extracted_data['Daraz Mall Status']]

    elif 'Color' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['Color'], case=False, na=False)]

    elif 'Storage Capacity' in extracted_data:
        filtered_df = filtered_df[filtered_df['Specification'].str.contains(extracted_data['Storage Capacity'], case=False, na=False)]

    elif 'Min Price' in extracted_data:
        if extracted_data['Max Price']==0:
            filtered_df = filtered_df[filtered_df['Price'].astype(int) <= extracted_data['Min Price']]
        else:
            filtered_df = filtered_df[(filtered_df['Price'].astype(int) >= extracted_data['Min Price']) & (filtered_df['Price'].astype(int) <= extracted_data['Max Price'])]

    elif 'Max Price' in extracted_data:
        filtered_df = filtered_df[filtered_df['Price'].astype(int) <= extracted_data['Max Price']]
        
    else:
        print("Cannot find any product on your criteria")
        
    # Display the filtered DataFrame
    print("Filtered DataFrame:")
    return filtered_df
    

st.title("Daraz Chat Bot")

user_query = st.text_input("Enter your query here")
if user_query:
    preprocessed_query = preprocess(user_query)
    extracted_data = extract_info(preprocessed_query)
    filtered_data = filter_data( extracted_data)

    if filtered_data.empty:
        st.write('No such data exists')
    else:
        st.write(filtered_data)