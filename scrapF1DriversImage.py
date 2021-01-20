import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.statsf1.com/pilotes/photos/")

soup = BeautifulSoup(page.content, 'html.parser')

image_data = []

images = soup.select('.png')
for image in images:
    image_data.append(image.get())

print(image_data)