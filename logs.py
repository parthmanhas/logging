from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google_sheets import main as add_row_to_google_sheet
import datetime

with open('slack_creds.txt', 'r') as f:
    SLACK_APP_TOKEN = f.readline().split('=')[1].strip()
    SLACK_BOT_TOKEN = f.readline().split('=')[1].strip()
    SLACK_SIGNING_SECRET = f.readline().split('=')[1].strip()


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
    add_row_to_google_sheet(row_data)
    # zapier reads the say message and adds to google sheets :|
    # say("Message logged")
    print("Message Logged")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
