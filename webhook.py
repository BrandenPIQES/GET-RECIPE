# @author: Phathutshedzo Netshitangani


from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os



app = Flask(__name__)

key = os.getenv("API_KEY") # obtain hidden ApiKey

# get_random_recipe: using the spoonacular API to get random recipes and use the ID of that recipe to get recipe card. RETURNS: url of the recipe card
def get_random_recipe():
    url = f'https://api.spoonacular.com/recipes/random?number=1&apiKey={key}'
    response = requests.get(url)

    if response.status_code == 200: # successful call
        data = response.json()
        recipe = data['recipes'][0]
        recipe_id = recipe['id']

        url = f'https://api.spoonacular.com/recipes/{recipe_id}/card?mask=ellipseMask&backgroundImage=background1&backgroundColor=ffffff&fontColor=33333&apiKey={key}'
        response = requests.get(url)

        card_data = response.json()
        card_url = card_data.get('url')
        
        return card_url
    else:
        return None

# whatapp_webhook: gets message from WhatsApp, if hungry it sends a recipe card
@app.route('/', methods=['POST'])
def whatsapp_webhook():
    message = request.form.get('Body').lower()
    response = MessagingResponse()

    # keeps on recommending until you say YES
    if 'hungry' in message or 'no' in message:
        card_url = get_random_recipe()
        if card_url:
            response.message('Here is a recipe').media(card_url)
        else:
            response.message('Sorry I couldn\'t load recipe, maybe you should fast...')
    else:
        response.message('Thank you for the message, do let me know if you need more recipes :)')

    return str(response)

if __name__ == '__main__':
    app.run()
