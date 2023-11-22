import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime

# Define the event handler class
class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            # File created
            print(f"File created: {event.src_path}")
        elif event.event_type == 'modified':
            # File modified
            print(f"File modified: {event.src_path}")
        elif event.event_type == 'deleted':
            # File deleted
            print(f"File deleted: {event.src_path}")

# Create an observer and pass in the event handler
observer = Observer()
event_handler = MyHandler()

# Set the path to the directory you want to monitor
path = '/path/to/Directory'

# Schedule the observer to watch the path
observer.schedule(event_handler, path, recursive=True)

# Start the observer
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the observer if Ctrl+C is pressed
    observer.stop()

# Wait until the observer thread finishes its execution
observer.join()


# import requests

# base_url = "www.google.com"
# response = requests.get(base_url)
# data = response.json()
# print(data)