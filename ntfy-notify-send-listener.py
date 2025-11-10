#!/usr/bin/env python3
import requests
import json
import yaml
import subprocess
import os
import sys

# Default config path as used by the official ntfy client
CONFIG_PATH = os.path.expanduser("~/.config/ntfy/client.yml")
NTFY_DEFAULT_HOST = "https://ntfy.sh"

def load_config():
    """Loads and validates the subscriptions from the client.yml file."""
    if not os.path.exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}. Exiting.")
        sys.exit(1)
        
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
            
        # Extract default host or use ntfy.sh
        default_host = config.get('default-host', NTFY_DEFAULT_HOST).rstrip('/')
        
        subscriptions = []
        for sub in config.get('subscribe', []):
            topic = sub.get('topic')
            command = sub.get('command')
            if topic and command:
                # Construct the full URL for the JSON stream
                url = f"{default_host}/{topic}/json"
                subscriptions.append({
                    'url': url,
                    'topic': topic,
                    'command': command,
                    'user': sub.get('user'),
                    'password': sub.get('password'),
                    'if_condition': sub.get('if', {})
                })
        return subscriptions
    except Exception as e:
        print(f"Error loading config: {e}. Exiting.")
        sys.exit(1)

def run_command(command_template, data):
    """Formats the command and executes it via subprocess."""
    # Mapping ntfy variables to their values
    replacements = {
        '$NTFY_ID': data.get('id', ''), '$id': data.get('id', ''),
        '$NTFY_TIME': str(data.get('time', '')), '$time': str(data.get('time', '')),
        '$NTFY_TOPIC': data.get('topic', ''), '$topic': data.get('topic', ''),
        '$NTFY_MESSAGE': data.get('message', ''), '$m': data.get('message', ''),
        '$NTFY_TITLE': data.get('title', ''), '$t': data.get('title', ''),
        '$NTFY_PRIORITY': str(data.get('priority', '3')), '$prio': str(data.get('priority', '3')), '$p': str(data.get('priority', '3')),
        '$NTFY_TAGS': ','.join(data.get('tags', [])), '$tags': ','.join(data.get('tags', [])), '$ta': ','.join(data.get('tags', [])),
    }

    # Apply substitutions
    final_command = command_template
    for var, val in replacements.items():
        # Using simple string replace for Bash variable syntax
        final_command = final_command.replace(var, val.replace('"', '\\"'))

    try:
        # Execute the command in a shell
        subprocess.run(final_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError:
        print("Command not found (is notify-send installed?).")

def check_condition(data, condition):
    """Checks the 'if' condition for a message."""
    if not condition:
        return True
    
    # Simple priority filter: if: {priority: high,urgent}
    if 'priority' in condition:
        allowed_priorities = [p.strip().lower() for p in condition['priority'].split(',')]
        message_priority = str(data.get('priority', '3')).lower()
        if message_priority not in allowed_priorities:
            return False
            
    # Add other filters (tags, etc.) as needed
    return True

def subscribe_and_listen(subscriptions):
    """Main loop to listen to all subscriptions."""
    
    # We only subscribe to one topic for simplicity in this script, 
    # but the config loader is ready for multiple topics.
    # To handle multiple topics simultaneously, a more complex implementation 
    # using async I/O (like asyncio) or threading would be required. 
    # For a simple script, we'll focus on the first subscription as the primary.
    
    if not subscriptions:
        print("No valid subscriptions found in config. Exiting.")
        return

    # Using only the first subscription for simplicity (to avoid complex async/threading)
    sub = subscriptions[0]
    
    print(f"Listening to topic: {sub['topic']} (URL: {sub['url']})")
    
    auth = (sub['user'], sub['password']) if sub.get('user') else None
    
    # Start the persistent stream
    try:
        with requests.get(sub['url'], auth=auth, stream=True) as response:
            if response.status_code != 200:
                print(f"HTTP Error {response.status_code} for {sub['topic']}. Waiting...")
                return

            for line in response.iter_lines():
                if line:
                    try:
                        # ntfy streams one JSON message per line
                        data = json.loads(line)
                        if data.get('event') == 'message':
                            if check_condition(data, sub['if_condition']):
                                run_command(sub['command'], data)
                        
                    except json.JSONDecodeError:
                        print("Received malformed JSON.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}. Retrying in 10s.")
        
    # The subscription is meant to be permanent. If it exits, we restart in systemd.


if __name__ == "__main__":
    subs = load_config()
    # Continuous loop to handle reconnections (systemd handles the overall restart)
    while True:
        subscribe_and_listen(subs)
        # Sleep briefly before trying to reconnect
        import time
        time.sleep(10)
