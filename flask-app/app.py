import dispenser
import flask
import os
import logging
from time import sleep
import datetime
from coinbase_commerce.client import Client
from threading import Thread, Timer

event_dict = {}
polling = True
sample_lock = False
app = flask.Flask(__name__)

TYPE_CREATED = "charge:created"
TYPE_PENDING = "charge:pending"
API_KEY = os.environ.get("AIRDROPZ_CB_COMMERCE_KEY")
commerce_client = Client(api_key=API_KEY)
connected = False

while not connected:
    print("Attempting to connect to Coinbase Commerce..")
    try:
        commerce_client = Client(api_key=API_KEY)
        test = commerce_client.event.list().data[0]
        if test is not None:
            connected = True
            print("Connected..")
    except Exception as e:
        print("Unable to connect to Coinbase Commerce..retrying")
        logging.error('Error!', exc_info=e)
        sleep(3)


@app.route('/', methods=['GET'])
def home():
    return flask.render_template('index.html')

@app.route('/brewmaster', methods=["GET"])
def sample():
    global sample_lock
    lock = sample_lock
    if lock:
       return "Samples are locked at this time."
    else:
        print("> Have one, on the house!")
        dispenser.execute()
        sample_lock = True
        next_sample = datetime.datetime.now() + datetime.timedelta(minutes=30)
        print(">> Locking next free sample until %s" % next_sample.strftime('%H:%M:%S'))
        lock_thread = Timer(60*30,sample_timeout)
        lock_thread.start()
        return "Have one on the house 🍻\n!"

def sample_timeout():
    sample_lock = False
    print("> Another round? (Free samples are now unlocked)")
    return

def get_recent_event():
    event = commerce_client.event.list().data[0]
    # Check if event_id is in event_dict
    event_data = {
        'created_at': event.created_at,
        'code':event.data.code,
        'id':event.id,        'type':event.type
    }
    return event_data


def start_polling_events():
    # we ignore the first event and don't dispense anything
    first = get_recent_event()
    first_id = first['id']
    event_dict[first_id] = first
    while polling:
        print("Polling...")
        sleep(5)
        event_data = get_recent_event()
        id = event_data['id']
        current_type = event_data['type']
        print("-- Received event %s" % id)
        if id not in event_dict:
            print("--- Event is new..")
            # Transaction not added
            event_dict[id] =  event_data

            if current_type == TYPE_PENDING:
                print('---- Payment PENDING made successfully.')
              # The transaction is not new dispense
                dispenser.execute()
                print("---- Charge completed!")
        else:
            print("--- Event exists..")
            last_type = event_dict[id]['type']

            if last_type == TYPE_CREATED and current_type != last_type:
                print('---- Payment PENDING made successfully.')
                # set the new data in the event dict
                event_dict[id] = event_data
                dispenser.execute()
                print("---- Charge completed.")
        print("\n")

polling_thread = Thread(target = start_polling_events, name="polling_thread")
polling_thread.daemon = True
polling_thread.start()
app.run(host="0.0.0.0")

