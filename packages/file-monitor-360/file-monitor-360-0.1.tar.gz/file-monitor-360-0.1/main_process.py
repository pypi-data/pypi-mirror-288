import websocket
import json
import base64
import threading
import time
import subprocess
import logging
import sys
import os
from file_watcher import start_file_watcher

MAX_SIZE_BYTES = 4 * 1024 * 1024

def get_mac_address():
    try:
        
        mac_address_output = subprocess.check_output(['cat', '/sys/class/net/enp1s0/address'], stderr=subprocess.STDOUT)
        mac_address = mac_address_output.decode('utf-8').strip()
        return mac_address
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving MAC address: {e}")
    except Exception as e:
        logging.error(f"Unexpected error retrieving MAC address: {e}")

    return None

mac_address = get_mac_address()

def get_serial_number():
    """ Find OS and run appropriate read mobo serial num command"""
    os_type = sys.platform.lower()

    if "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    elif "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "dmidecode -t system | grep 'Serial Number'"
    return os.popen(command).read().replace("\n", "").replace("  ", "").replace(" ", "").replace("SerialNumber:", "").strip()

serial_no = get_serial_number()
print(serial_no,"SERIAL_NO")
server_url = f"ws://server.saferpanichub.com/?clientId={serial_no}&macId={mac_address}"


anydesk_password = None
anydesk_id = None
connect_to_server = True
anydesk_connected = False

ws = None

def on_message(ws, message):
    global anydesk_connected, anydesk_id

    decoded_message = base64.b64decode(message).decode('utf-8')
    logging.info(f"Decoded JSON message: {decoded_message}")

    try:
        message_data = json.loads(decoded_message)
    except json.JSONDecodeError as json_error:
        logging.error(f"JSON decode error: {json_error}")
        send_error_to_server(e)
        return

    logging.info(f"JSON data: {message_data}")

    if "type" in message_data:
        command_type = message_data["type"]

        if command_type == "set_anydesk_password":
            logging.info("Received set AnyDesk password command from server...")
            anydesk_password = message_data.get("password")
            if anydesk_password:
                set_anydesk_password(anydesk_password)
                anydesk_password = None
            else:
                logging.error("AnyDesk password not provided by the server.")

        elif command_type == "get_anydesk_id":
            logging.info("Received get AnyDesk ID command from server...")
            send_anydesk_id_to_server(ws)

        elif command_type == "restart":
            logging.info("Restart command received from server. Restarting the system...")
            restart_system()

        elif command_type == "start_anydesk":
            if not anydesk_connected:
                logging.info("Received start AnyDesk command from server...")
                start_anydesk(anydesk_id)
                anydesk_connected = True
            else:
                logging.warning("AnyDesk is already in the process of starting or connected.")

        else:
            logging.warning(f"Unknown command type received: {command_type}")

    else:
        logging.warning("Message received from server does not contain 'type' field.")

def on_error(ws, error):
    logging.error(f"Error occurred: {error}")
    send_error_to_server(str(error))

def send_error_to_server(error_message):
    try:
        if ws and ws.sock and ws.sock.connected:
            error_data = {
                "type": "error_log",
                "message": str(error_message),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            error_data_json = json.dumps(error_data)
            encoded_error_message = base64.b64encode(error_data_json.encode('utf-8')).decode('utf-8')
            ws.send(encoded_error_message)
            logging.info("Error log sent to server.")
        else:
            logging.error("WebSocket connection lost. Cannot send error log to server.")
    except Exception as e:
        logging.error(f"Error sending error log to server: {e}")
        

def on_close(ws, close_status_code, close_msg):
    logging.info(f"Connection closed with status code: {close_status_code}, message: {close_msg}")
    logging.info("Attempting to reconnect...")
    reconnect()
    
def on_open(ws):
    global anydesk_id
    logging.info("Connection established.")
    
    # Start heartbeat thread
    threading.Thread(target=send_heartbeat, args=(ws,), daemon=True).start()
    
    # Start file watching
    threading.Thread(target=start_file_watcher, args=(ws,), daemon=True).start()
 
    if not anydesk_id:
        anydesk_id = get_anydesk_id()
        
def main():
    global ws

    if connect_to_server:
        try:
            ws = websocket.WebSocketApp(server_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close,
                                        on_open=on_open)
            ws.run_forever()
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Cleaning up and exiting.")
            if ws:
                ws.close()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            send_error_to_server(e)
            import traceback
            traceback.print_exc()
    else:
        logging.info("WebSocket connection is disabled.")

def reconnect():
    logging.info("Attempting to reconnect...")
    time.sleep(5)
    main()

def get_anydesk_id():
    try:
        anydesk_id_output = subprocess.check_output(['anydesk', '--get-id'], stderr=subprocess.STDOUT)
        anydesk_id = anydesk_id_output.decode('utf-8').strip()
        return anydesk_id
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving AnyDesk ID: {e}")
        send_error_to_server(e)
    except Exception as e:
        logging.error(f"Unexpected error retrieving AnyDesk ID: {e}")
        send_error_to_server(e)

    return None

def set_anydesk_password(password):
    logging.info("Setting AnyDesk password...")
    try:
        result = subprocess.run(['sudo', 'anydesk', '--set-password', password], capture_output=True, text=True, check=True)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting AnyDesk password: {e}")
        send_error_to_server(e)
        logging.error(f"Command output: {e.output}")
    except Exception as e:
        logging.error(f"Unexpected error setting AnyDesk password: {e}")
        send_error_to_server(e)
        anydesk_connected = False

def start_anydesk(anydesk_id):
    global anydesk_connected

    logging.info(f"Connecting to AnyDesk ID: {anydesk_id}")
    try:
        result = subprocess.run(['anydesk', '--connect', '--remote-id', anydesk_id], capture_output=True, text=True, check=True)
        logging.info(result.stdout)
        anydesk_connected = True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error starting AnyDesk: {e}")
        send_error_to_server(e)
        logging.error(e.output)
        anydesk_connected = False
    except Exception as e:
        logging.error(f"Unexpected error starting AnyDesk: {e}")
        send_error_to_server(e)
        anydesk_connected = False

def send_heartbeat(ws):
    while True:
        try:
            if ws and ws.sock and ws.sock.connected:  # Check if WebSocket is connected
                heartbeat_message = {"status": "active", "type": "heartbeat"}
                heartbeat_message_json = json.dumps(heartbeat_message)
                encoded_heartbeat_message = base64.b64encode(heartbeat_message_json.encode('utf-8')).decode('utf-8')
                ws.send(encoded_heartbeat_message)
                logging.info("Heartbeat sent.")
            else:
                logging.error("WebSocket connection lost. Attempting to reconnect...")
                reconnect()
                break  # Exit heartbeat loop to avoid multiple reconnect attempts

            time.sleep(5)
        except Exception as e:
            logging.error(f"Error sending heartbeat: {e}")
            send_error_to_server(e)
            time.sleep(5)  # Wait before retrying

def send_anydesk_id_to_server(ws):
    global anydesk_id
    if anydesk_id:
        try:
            message = {
                "type": "anydesk_id",
                "anydesk_id": anydesk_id
            }
            message_json = json.dumps(message)
            encoded_message = base64.b64encode(message_json.encode('utf-8')).decode('utf-8')
            ws.send(encoded_message)
            logging.info("AnyDesk ID sent to server.")
        except Exception as e:
            logging.error(f"Error sending AnyDesk ID to server: {e}")
            send_error_to_server(e)
    else:
        logging.error("AnyDesk ID is not available.")
        

def restart_system():
    logging.info("Restarting system...")
    try:
        result = subprocess.run(['sudo', 'reboot'], capture_output=True, text=True, check=True)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error restarting system: {e}")
        send_error_to_server(e)
        logging.error(e.output)
        
def manage_log_size(log_filename, max_size_bytes):
    if os.path.exists(log_filename):
        log_size = os.path.getsize(log_filename)
        if log_size > max_size_bytes:
            print(f"Log file '{log_filename}' size exceeds {max_size_bytes} bytes. Truncating...")
            with open(log_filename, 'w'):  
                pass        

if __name__ == "__main__":
    manage_log_size('client.log',MAX_SIZE_BYTES)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('client.log'),
            logging.StreamHandler()
        ]
    )

    logging.info("Starting client processes...")

    anydesk_id = get_anydesk_id()
    main()







