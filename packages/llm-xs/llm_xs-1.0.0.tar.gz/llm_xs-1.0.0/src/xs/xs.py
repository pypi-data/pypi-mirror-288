#xs.py

from flask import Flask, request, jsonify
from pyngrok import ngrok, exception
# import threading
from waitress import serve
import requests
import socket


# initializing the flask app
app = Flask(__name__)


#used to find available port and then return out a random port
def find_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


#used in llm side for creation of api(endpoint) for access by remote device
def forward(ngrok_api, port):
  while True:
    try:
      ngrok.set_auth_token(ngrok_api)
      public_url = ngrok.connect(port)
      print('-----------------')
      print(f'API : {public_url}')
      print('-----------------')
      serve(app, host = '0.0.0.0', port = port)

    except exception.PyngrokNgrokError as e:
      print(f"Ngrok tunnel error: {e}")
      print('-----------------')
      print('If max tunnel limit kicks in then use the flush() function to clear out previous tunnels. Like xs.flush()...')
      print('-----------------')
      break


#just in case if tunnel limit kicks in then use this flush to clear out previous tunnels
def flush():
  tunnels = ngrok.get_tunnels()
  for tunnel in tunnels:
      print("all tunnels flushed...")
      ngrok.disconnect(tunnel.public_url)


# -------------------------xxxxxxxxxxxxxxxxxxxxxxx-----------------------------------
#used in remote device side, to access and use the api & use generate text option
def connect_text(public_url, data):
    endpoint = f"{public_url}/generate"
    data = {"prompt": f'{data}'}
    response = requests.post(endpoint, json=data)
    try:
        output = response.json()
        result = output[0]
        # formatting for the response from the model
        # to provide only output as a response
        print(list(result.values())[0])
       
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        print(response.text) 


#generate is empty because we can configure it at runtime with our own generate function 
# its just like function overwriting for our own better usage
def generate(prompt):
  pass


#this is a specific route for the api(endpoint) in which we can post prompt and get inference responses
#YOUR LLM GENERATION FUNCTION SHOULD BE NAMED WITH :: generate :: elsewise it wont work
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    print(data)
    prompt = data.get('prompt', '')
    response = generate(prompt)
    return jsonify(response)
# -------------------------xxxxxxxxxxxxxxxxxxxxxxx-----------------------------------


#FUTURE FEATURES---------------------------------------------------------------------

#WOULD BE INSIDE NAME==MAIN FUNCTION LOOP
"""ports_to_free = [11434]  # Add ports you want to free
    for port in ports_to_free:
        kill_process_using_port(port)"""

# WOULD BE A FUNCTION for deallocation of the assigned port elsewise if we reaccess with the same port, it would show that PORT BUSY
"""def kill_process_using_port(port):
    try:
        result = subprocess.run(['lsof', '-t', f'-i:{port}'], stdout=subprocess.PIPE, text=True)
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid:
                os.kill(int(pid), 9)
                print(f"Killed process {pid} using port {port}")
    except Exception as e:
        print(f"Error killing process using port {port}: {e}")"""

#MADE BY PRABHUDAYAL VAISHNAV, added coz to somehow 100 lines of code, haha