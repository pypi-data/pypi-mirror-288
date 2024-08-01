# cli/action.py

import os
import json
import requests
from .auth import get_headers
from .utils import handle_response, API_ENDPOINT

def get_all_actions(names_only=False, label=None, status_only=False):
    try:
        endpoint = f"{API_ENDPOINT}/action"
        params = {}
        if names_only:
            params['name'] = ''
        if label:
            endpoint += f"/label/{label}"
            if status_only:
                params['status_only'] = 'true'
        elif status_only:
            return {"error": "Status-only option requires a label"}
        
        headers = get_headers()
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        actions = handle_response(response)
        
        return actions
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting actions: {e}")
        return {"error": str(e)}

def get_action_status_for_label(label, action=None):
    try:
        endpoint = f"{API_ENDPOINT}/action/label/{label}"
        if action:
            endpoint += f"/{action}"
        headers = get_headers()
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting action status for label: {e}")
        return {"error": str(e)}

def get_specific_action(action, query=None):
    try:
        endpoint = f"{API_ENDPOINT}/action/{action}"
        if query:
            endpoint += f"?{query}"
        headers = get_headers()
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting specific action: {e}")
        return {"error": str(e)}

def store_action(action, steps, include):
    try:
        payload = {
            "action": action,
            "steps": steps,
            "include": include
        }
        headers = get_headers()
        response = requests.post(f"{API_ENDPOINT}/action", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error storing action: {e}")
        return {"error": str(e)}
        
def delete_action(action):
    try:
        payload = {"action": action}
        headers = get_headers()
        response = requests.delete(f"{API_ENDPOINT}/action", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error deleting action: {e}")
        return {"error": str(e)}

def store_action_from_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        action = data.get("action")
        steps = data.get("steps")
        include = data.get("include")
        return store_action(action, steps, include)
    except Exception as e:
        print(f"Error storing action from file: {e}")
        return {"error": str(e)}

def add_all_actions_from_dir(directory):
    try:
        results = []
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                result = store_action_from_file(filepath)
                results.append(result)
        return results
    except Exception as e:
        print(f"Error adding all actions from directory: {e}")
        return {"error": str(e)}

def delete_all_actions():
    try:
        actions = get_all_actions(names_only=True)
        if isinstance(actions, list):
            for action in actions:
                delete_action(action)
        return {"status": "All actions deleted"}
    except Exception as e:
        print(f"Error deleting all actions: {e}")
        return {"error": str(e)}

def handle_action_command(args):
    if args.action_command == "list":
        result = get_all_actions(args.names_only)
        if 'error' not in result:
            if isinstance(result, list):
                print("Available actions:")
                for action in result:
                    print(f"  {action}")
            elif isinstance(result, dict):
                print("Available actions:")
                for action, details in result.items():
                    print(f"  {action}")
                    if not args.names_only:
                        print(f"    Details: {json.dumps(details, indent=4)}")
            else:
                print(f"Unexpected result format: {result}")
        else:
            print(f"Error listing actions: {result['error']}")
    elif args.action_command == "get":
        result = get_specific_action(args.action, args.query)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error getting action: {result['error']}")
    elif args.action_command == "status":
        result = get_action_status_for_label(args.label, args.action)
        if 'error' not in result:            
            if isinstance(result, dict):
                if args.action:
                    # If a specific action was requested
                    action_data = result.get(args.action)
                    if isinstance(action_data, (int, float)):
                        print(f"Progress for action '{args.action}': {action_data:.2f}")
                    elif isinstance(action_data, dict):
                        progress = action_data.get('progress', action_data)
                        if isinstance(progress, (int, float)):
                            print(f"Progress for action '{args.action}': {progress:.2f}")
                        else:
                            print(f"Unexpected progress format for action '{args.action}': {progress}")
                    else:
                        print(f"Unexpected data format for action '{args.action}': {action_data}")
                else:
                    # If no specific action was requested, print progress for all actions
                    print("Progress for all actions:")
                    for action, data in result.items():
                        if isinstance(data, (int, float)):
                            print(f"  {action}: {data:.2f}")
                        elif isinstance(data, dict):
                            progress = data.get('progress', data)
                            if isinstance(progress, (int, float)):
                                print(f"  {action}: {progress:.2f}")
                            else:
                                print(f"  {action}: Unexpected progress format: {progress}")
                        else:
                            print(f"  {action}: Unexpected data format: {data}")
            else:
                print(f"Unexpected result type: {type(result)}")
        else:
            print(f"Error getting action status: {result['error']}")
    elif args.action_command == "store":
        if args.file:
            result = store_action_from_file(args.file)
        else:
            result = store_action(args.action, args.steps, args.include)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error storing action: {result['error']}")
    elif args.action_command == "delete":
        result = delete_action(args.action)
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting action: {result['error']}")
    elif args.action_command == "delete_all":
        result = delete_all_actions()
        if 'error' not in result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting all actions: {result['error']}")
    elif args.action_command == "add_all":
        result = add_all_actions_from_dir(args.directory)
        if 'error' not in result:
            print("Actions added from directory:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error adding actions from directory: {result['error']}")