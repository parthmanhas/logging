from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google_sheets_store import main as add_row_to_google_sheet
import datetime
import os

with open('.env') as f:
    for line in f:
        # Ignore comments and blank lines
        if line.startswith('#') or not line.strip():
            continue
        # Parse the NAME=VALUE pairs and set environment variables
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html


@app.message(":::")
def log_to_google_sheet(message, say):
    print('logging event to google sheets')
    epoch_timestamp = int(message['event_ts'].split('.')[0])

    # Convert the epoch timestamp to a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(epoch_timestamp)

    # Convert the datetime object to the local timezone
    local_datetime_obj = datetime_obj.astimezone()

    # Format the local datetime as a string
    local_datetime_str = local_datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    row_data = [local_datetime_str, *message['blocks'][0]['elements'][0]['elements'][0]['text'].split(":::")]
    try:
        add_row_to_google_sheet(row_data)
        # zapier reads the say message and adds to google sheets :|
        # say("Message logged")
        print("Message Logged")
    except Exception as e:
        print(e)
        say(f'Error: {e}')
    

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
