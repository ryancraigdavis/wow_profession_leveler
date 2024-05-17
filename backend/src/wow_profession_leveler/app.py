from quart import Quart, request, jsonify
from dotenv import load_dotenv
import requests
import os

class BlizzardAPI:
    def __init__(self):
        self.client_id = os.environ.get('BATTLENET_CLIENT_ID')
        self.client_secret = os.environ.get('BATTLENET_CLIENT_SECRET')
        self.token = None

    def get_token(self):
        url = 'https://oauth.battle.net/token'
        data = {'grant_type': 'client_credentials'}
        auth = (self.client_id, self.client_secret)

        try:
            response = requests.post(url, data=data, auth=auth)
            response.raise_for_status()
            self.token = response.json()['access_token']
            print('Token retrieved successfully.')
        except requests.exceptions.RequestException as e:
            print(f'Error occurred while retrieving token: {e}')

    def get_ah_data(self, realm_id, namespace, region, faction_id):
        if not self.token:
            self.get_token()

        url = f'https://{region}.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions/{faction_id}'
        params = {
            'namespace': namespace,
            'locale': 'en_US',
            'access_token': self.token
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f'Error occurred while fetching auction house data: {e}')
            return None

app = Quart(__name__)
blizzard_api = BlizzardAPI()

@app.route('/api/endpoint', methods=['POST'])
async def process_data():
    data = await request.get_json()
    faction = data.get('faction')
    realm = data.get('realm')
    profession = data.get('profession')

    # Get the auction house data using the BlizzardAPI class
    ah_data = blizzard_api.get_ah_data(realm, 'dynamic-us', 'us', faction)

    if ah_data:
        # Process the auction house data
        result = {
            'message': f'Received data - Faction: {faction}, Realm: {realm}, Profession: {profession}',
            'ah_data': ah_data
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Failed to retrieve auction house data'}), 500

if __name__ == '__main__':
    app.run()
