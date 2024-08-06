import websocket
import json
import base64
import time
import subprocess
import sys

server_url = "wss://saferw.serveo.net?clientId=123&macId=123456"

def on_error(ws, error):
    try:
        error_message = f"Error occurred: {error}"
        print(error_message)
        send_error_log(error_message)
    except Exception as e:
        print(f"Error processing error message: {e}")

def send_error_log(error_message):
    try:
        log_data = {
            "type": "error_log",
            "message": error_message
        }
        log_data_json = json.dumps(log_data)
        encoded_log_data = base64.b64encode(log_data_json.encode('utf-8')).decode('utf-8')

        ws = websocket.WebSocket()
        ws.connect(server_url)
        ws.send(encoded_log_data)
        ws.close()

    except Exception as e:
        print(f"Error sending error log to server: {e}")

def main():
    websocket.enableTrace(True)
    while True:
        try:
            ws = websocket.WebSocketApp(server_url,
                                        on_error=on_error)
            ws.run_forever()
        except Exception as e:
            print(f"An error occurred in error monitoring process: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
