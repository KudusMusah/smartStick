import requests

# The URL to your API endpoint
url = "http://172.20.10.6:8000/detect/"  # Adjust this if your endpoint URL is different

# The path to the image file you want to test
image_path = r"C:\Users\hp\Downloads\wolf-schram-19t6J2RVqQE-unsplash.jpg"

# Prepare the file to be sent in the request
files = {'image': open(image_path, 'rb')}

# Send the POST request to the API
response = requests.post(url, files=files)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
