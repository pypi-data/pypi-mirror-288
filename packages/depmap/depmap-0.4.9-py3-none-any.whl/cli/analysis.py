# cli/analysis.py

import json
import time
import requests
from tqdm import tqdm
from .auth import get_headers
from .utils import handle_response, API_ENDPOINT, format_analysis_result

def start_analysis(label, action, model):
    payload = {"model": model}

    try:
        headers = get_headers()
        response = requests.post(f"{API_ENDPOINT}/analysis/{label}/{action}", json=payload, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {e.response.content}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error starting analysis: {e}")
        return {"error": str(e)}

def get_analysis_status(label, action):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}/{action}/status"
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting analysis status: {e}")
        return {"error": str(e)}

def get_analysis_results(label, action=None, file=None, details=True):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}"
        if action:
            endpoint += f"/{action}"
        params = {}
        if file:
            params['file'] = file
        if details:
            params['details'] = 'true'
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting analysis results: {e}")
        return {"error": str(e)}

def delete_analysis_results(label, action):
    try:
        headers = get_headers()
        endpoint = f"{API_ENDPOINT}/analysis/{label}/{action}"
        response = requests.delete(endpoint, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error deleting analysis results: {e}")
        return {"error": str(e)}

def start_and_poll_analysis(label, action, model):
    try:
        # First, delete any existing analysis results
        delete_result = delete_analysis_results(label, action)
        if 'error' in delete_result:
            print(f"Warning: Failed to delete existing analysis results: {delete_result['error']}")
        else:
            print("Existing analysis results deleted successfully.")

        # Now start the new analysis
        start_result = start_analysis(label, action, model)
        if 'error' in start_result:
            print(f"Failed to start analysis: {start_result['error']}")
            return start_result

        print(f"Analysis started: {json.dumps(start_result, indent=2)}")
        
        pbar = tqdm(total=100, desc="Analyzing", unit="%")
        
        while True:
            time.sleep(2)
            result = get_analysis_status(label, action)

            if 'error' in result:
                print(f"Error polling analysis: {result['error']}")
                break

            status = result.get('status', 'UNKNOWN')
            processed, total = map(int, result.get('processed', '0/0').split('/'))
            progress = (processed / total) * 100 if total > 0 else 0

            pbar.n = min(int(progress), 100)
            pbar.set_postfix_str(f"Status: {status}")
            pbar.refresh()

            if status in ['COMPLETED', 'FAILED']:
                pbar.close()
                final_result = get_analysis_results(label, action)
                if 'error' not in final_result:
                    print(f"\nAnalysis completed: {json.dumps(final_result, indent=2)}")
                return final_result

        pbar.close()
        return result
    except Exception as e:
        print(f"Unexpected error in start_and_poll_analysis: {e}")
        return {"error": str(e)}

def handle_analysis_command(args):
    if args.analysis_command == "start":
        result = start_and_poll_analysis(args.label, args.action, args.model)
        if result and 'error' not in result:
            print("Analysis complete. Check status for details.")
        elif 'error' in result:
            print(f"Error during analysis: {result['error']}")
    elif args.analysis_command == "status":
        result = get_analysis_status(args.label, args.action)
        if 'error' not in result:
            print("Analysis status:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error getting analysis status: {result['error']}")
    elif args.analysis_command == "get":
        result = get_analysis_results(
            args.label,
            args.action,
            file=args.file,
            details=not args.status
        )
        if 'error' not in result:
            print("Analysis results:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error getting analysis results: {result['error']}")
    elif args.analysis_command == "delete":
        result = delete_analysis_results(args.label, args.action)
        if 'error' not in result:
            print("Analysis deletion result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error deleting analysis results: {result['error']}")