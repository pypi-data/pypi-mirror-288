# cli/label.py
import json
import requests
from .auth import get_headers
from .utils import handle_response, API_ENDPOINT

def get_labels(status=False):
    try:
        headers = get_headers()
        url = f"{API_ENDPOINT}/label"
        if status:
            url += "?check_s3=true"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error getting labels: {e}")
        return {"error": str(e)}

def delete_label(label):
    try:
        headers = get_headers()
        response = requests.delete(f"{API_ENDPOINT}/label/{label}", headers=headers)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error deleting label: {e}")
        return {"error": str(e)}

def handle_label_command(args):
    if args.label_command == "list":
        result = get_labels(status=args.status)
        if 'error' not in result:
            print("Labels:")
            labels = result if isinstance(result, list) else result.get('labels', [])
            if isinstance(labels, list):
                for label_info in labels:
                    if isinstance(label_info, dict):
                        label = label_info.get('label', 'Unknown')
                        exists_in_s3 = label_info.get('exists_in_s3', 'Unknown')
                        print(f"  {label} (Exists in S3: {exists_in_s3})")
                    elif isinstance(label_info, str):
                        print(f"  {label_info}")
                    else:
                        print(f"  Unexpected label format: {label_info}")
            elif isinstance(labels, dict):
                for label, exists_in_s3 in labels.items():
                    print(f"  {label} (Exists in S3: {exists_in_s3})")
            else:
                print(f"Unexpected format for labels: {labels}")
        else:
            print(f"Error listing labels: {result['error']}")
    elif args.label_command == "delete":
        result = delete_label(args.label)
        if 'error' not in result:
            print(f"Successfully deleted label: {args.label}")
        else:
            print(f"Error deleting label: {result['error']}")