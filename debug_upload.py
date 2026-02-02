import requests

url = 'http://localhost:8000/api/upload/'
files = {'csv_file': open('test_upload.csv', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
