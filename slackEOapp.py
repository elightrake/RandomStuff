from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Initial order of messaging based on user IDs
users_in_order_ids = [
    "U06CPHNG2H1",  # Adam Struck
    "U06CS87NNMS",  # Manny Dodson
    "U06CPKJMASW",  # Gorge
    "U06CLC38BTQ",  # ARS
    "U06D49H40RX",  # Ein
    "U06D2A44JPK"   # Mac Kincheloe
]

# Mapping from user IDs to user names
user_id_to_name = {
    "U06CPHNG2H1": "Adam Struck",
    "U06CS87NNMS": "Manny Dodson",
    "U06CPKJMASW": "Gorge",
    "U06CLC38BTQ": "ARS",
    "U06D49H40RX": "Ein",
    "U06D2A44JPK": "Mac Kincheloe"
}

# Variable to track the last user who sent a message
last_message_user_id = None

@app.route("/slack/events", methods=["POST"])
def slack_events():
    global last_message_user_id
    data = request.json
    if data['type'] == 'url_verification':  # Slack URL verification handshake
        return data['challenge']
    elif data['type'] == 'event_callback':
        event = data['event']
        if event['type'] == 'message' and 'subtype' not in event and event.get('channel') == ethereal_odyssey_channel_id:
            user_id = event['user']
            if user_id in users_in_order_ids:
                last_message_user_id = user_id
                current_index = users_in_order_ids.index(user_id)
                next_user_index = (current_index + 1) % len(users_in_order_ids)  # Find the next user in the queue
                next_user_id = users_in_order_ids[next_user_index]  # Get the next user's ID
                next_user_name = user_id_to_name[next_user_id]  # Get the next user's name for readability
                
                # Prepare the message to post in the #general channel
                response_message = f"<@{next_user_id}> is now up in Ethereal Odyssey: Shadows of the Celestial Realm."
 
                # Posting the message to the #general channel
                post_message_to_channel(response_message, general_channel_id)  # You need to replace 'general_channel_id' with your actual #general channel ID
                
    return jsonify(status=200)

def post_message_to_channel(message, channel_id):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer xoxb-6425024985206-6705158577142-xHfxDvMceEmz4LQqrE41vUuk",  # Replace 'xoxb-your-bot-token' with your actual bot token
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel_id,
        "text": message
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)  # For debugging purposes, to see the response from the Slack API


@app.route("/whosup", methods=["POST"])
def whos_up():
    global last_message_user_id  # Although not necessary to read the global variable, it emphasizes the use of it

    # Check if there is a known last message sender and they are in the predefined list
    if last_message_user_id and last_message_user_id in users_in_order_ids:
        current_index = users_in_order_ids.index(last_message_user_id)  # Find the index of the last message sender
        next_user_index = (current_index + 1) % len(users_in_order_ids)  # Determine the next user's index
        next_user_id = users_in_order_ids[next_user_index]  # Get the next user's ID
        next_user_name = user_id_to_name[next_user_id]  # Lookup the next user's name for the response

        # Craft the response message to mention the next user
        response_message = f"The next person in the queue for Ethereal Odyssey is <@{next_user_id}>."
    else:
        # Fallback message if no last message sender is identified or they're not in the list
        response_message = "well idk what the fuck to do but at least the other thing works"

    # Respond to the slash command with who is up next
    return jsonify({
        "response_type": "in_channel",  # Ensure the response is visible to everyone in the channel
        "text": response_message
    })


# The channel ID for #ethereal-odyssey - replace with the actual ID
ethereal_odyssey_channel_id = "C06F8QKN80G"
general_channel_id = 'C06CPKJNTFC'
slack_bot_token = 'xoxb-6425024985206-6705158577142-xHfxDvMceEmz4LQqrE41vUuk'

#last_message_user_id = "U06CLC38BTQ"

if __name__ == "__main__":
    app.run(debug=True, port=3000)
