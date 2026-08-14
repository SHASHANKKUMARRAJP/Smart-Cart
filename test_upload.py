import urllib.request
import json
import base64

# Download image from pngmart
req = urllib.request.Request('https://www.freepnglogos.com/uploads/lipstick-png/mac-lipstick-png-transparent-mac-lipstick-images-12.png', headers={'User-Agent': 'Mozilla/5.0'})
try:
    img_data = urllib.request.urlopen(req).read()
    
    # Upload to imgur
    client_id = '546c25a59c58ad7'
    req_imgur = urllib.request.Request('https://api.imgur.com/3/image', 
        headers={'Authorization': f'Client-ID {client_id}'}, 
        data=base64.b64encode(img_data), 
        method='POST')
    
    response = urllib.request.urlopen(req_imgur)
    data = json.loads(response.read())
    print(data['data']['link'])
except Exception as e:
    print('Error:', e)
