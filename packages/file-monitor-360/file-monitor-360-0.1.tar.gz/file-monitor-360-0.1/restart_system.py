# import sys
# import subprocess
# import logging


# def restart_system():
#     try:
#         logging.info("Restarting the system...")
#         if sys.platform.startswith('win'):
#             subprocess.call(['shutdown', '/r', '/t', '1'], shell=True)
#         elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
#             subprocess.call(['sudo', 'reboot'])
#     except Exception as e:
#         logging.error(f"Error restarting system: {e}")
       

# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#     restart_system()


import os
import logging

def restart_system():
    logging.info("Restarting the system...")
    try:
        os.system("sudo reboot")
    except Exception as e:
        logging.error(f"Error restarting system: {e}")
       
        try:
            subprocess.run(["sudo", "reboot"])
        except Exception as e:
            logging.error(f"Error restarting system (alternative approach): {e}")