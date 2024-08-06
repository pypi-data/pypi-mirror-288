import websocket
import json
import base64
import logging
import socket
import uuid

server_url = "ws://server.saferpanichub.com/?clientId=1234&macId=12345678"

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        logging.error(f"Error getting IP address: {e}")
        return "unknown"

def get_mac_address():
    try:
        return ':'.join(format(uuid.getnode().to_bytes(6, 'big'), '02x')[i:i+2] for i in range(0, 12, 2))
    except Exception as e:
        logging.error(f"Error getting MAC address: {e}")
        return "unknown"


def send_client_info_to_server(ws):
    try:
        mac_address = get_mac_address()
        ip_address = get_ip_address()
        
        client_info = {
            "type": "client_info",
            "mac_address": mac_address,
            "ip_address": ip_address
        }
        
        client_info_json = json.dumps(client_info)
        encoded_client_info = base64.b64encode(client_info_json.encode('utf-8')).decode('utf-8')
        ws.send(encoded_client_info)
        
        logging.info(f"MAC address {mac_address} and IP address {ip_address} sent to server.")
    except Exception as e:
        logging.error(f"Error sending client info to server: {e}")

def on_open(ws):
    logging.info("Connection established.")
    inner_send_client_info(ws)

def on_close(ws, close_status_code, close_msg):
    logging.info(f"Connection closed with status: {close_status_code}, message: {close_msg}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,  # Use DEBUG for detailed logging
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('send_client_info.log'),
            logging.StreamHandler()
        ]
    )

    try:
        ws = websocket.WebSocketApp(server_url,
                                    on_open=on_open,
                                    on_close=on_close)
        ws.run_forever()
    except Exception as e:
        logging.error(f"WebSocket connection failed: {e}")
        import traceback
        traceback.print_exc()

