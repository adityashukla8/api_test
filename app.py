from flask import Flask, request, jsonify, json
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/api', methods=['GET'])
def returnFirstName():
    l = []
    d = {}

    city_input = str(request.args['location'])
    category_input = str(request.args['category'])
    
    place_list_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + category_input + '%20places%20in%20' + city_input + '&key=AIzaSyAZMObBqR2-8Qt1wE8W30JGax3AIHvbVao'
    place_temp_url = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' +
                       city_input + '&appid=63814ea7eed2ddc68b270edc74b96122&units=metric')

    response = requests.request("GET", place_list_url)

    # location_name = str(city_input)
    for i in range(0, len(response.json()['results'])):
        place_id = response.json()['results'][i]['place_id']
        place_name = response.json()['results'][i]['name']
        place_lat_long = [response.json()['results'][i]['geometry']['location']['lat'], response.json()['results'][1]['geometry']['location']['lng']]

        try:
            place_open = response.json()['results'][i]['opening_hours']['open_now']
        except KeyError:
            place_open = None
        try: 
            place_temp = place_temp_url.json()['main']['temp']
        except KeyError:
            place_temp = None
        try:
            place_photos = response.json()['results'][i]['photos'][0]['html_attributions'][0]
        except KeyError:
            place_photos = None
            
        place_ratings = [response.json()['results'][i]['rating'], response.json()['results'][i]['user_ratings_total']]
        palce_type = response.json()['results'][i]['types']

        # current_temp = place_temp_url.json()['main']['temp']
        # category = str(category_input)

        # d['location_name'] = location_name
        d['place_id'] = place_id
        d['place_name'] = place_name
        d['place_lat_long'] = place_lat_long
        d['place_open'] = place_open
        d['place_temp'] = place_temp
        d['place_photos'] = place_photos
        d['place_ratings'] = place_ratings
        d['palce_type'] = palce_type

        l.append(d)

    # d['location_temp'] = current_temp
    # d['category'] = category

    # print(current_temp)
    
    return str(json.dumps(l))


if __name__ == '__main__':
    app.run(debug=True)
