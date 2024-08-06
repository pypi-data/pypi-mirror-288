import os
import json
import base64
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

filepath = "/var/log/sppl.txt"

class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, ws):
        super().__init__()
        self.ws = ws
        self.last_content = None
        self.first_time_modified = True

    def on_modified(self, event):
        if not event.is_directory and event.src_path == filepath:
            current_content = read_file_content(filepath)
            
            if self.first_time_modified:
                # Send incremental changes only on first modification
                if self.last_content is not None:
                    new_changes = find_incremental_changes(self.last_content, current_content)
                    if new_changes:
                        self.send_changes(new_changes)
                self.first_time_modified = False
            else:
                # Find and send incremental changes since last modification
                new_changes = find_incremental_changes(self.last_content, current_content)
                if new_changes:
                    self.send_changes(new_changes)

            self.last_content = current_content

    def send_changes(self, changes):
        message = {
            "message": changes,
            "type": "file_change"
        }
        self.send_message(message)

    def send_message(self, message):
        message_json = json.dumps(message)
        encoded_message = base64.b64encode(message_json.encode('utf-8')).decode('utf-8')
        logging.info(f"Sending base64 encoded message: {encoded_message}")
        
        
        #print(f"Sent message: {message}")
        
        try:
            self.ws.send(encoded_message)
        except Exception as e:
            logging.error(f"Error sending message over WebSocket: {e}")

def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        logging.error(f"Error reading file '{filepath}': {e}")
        return ""

def find_incremental_changes(last_content, current_content):
    if last_content is None:
        return current_content  
    
    last_lines = last_content.splitlines()
    current_lines = current_content.splitlines()
    added_lines = [line for line in current_lines if line not in last_lines]
    return "\n".join(added_lines)

def start_file_watcher(ws):
    logging.info(f"Starting file watcher for {filepath}...")

    event_handler = WatchdogEventHandler(ws)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(filepath), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        logging.info("File watcher stopped.")
    except Exception as e:
        logging.error(f"An error occurred in file watcher: {e}")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('file_watcher.log'),
            logging.StreamHandler()
        ]
    )

    start_file_watcher(None)  

