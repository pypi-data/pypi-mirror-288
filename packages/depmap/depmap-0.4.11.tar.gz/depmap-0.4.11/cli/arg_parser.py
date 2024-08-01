# cli/arg_parser.py

import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Repository Analysis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analysis commands
    analysis_parser = subparsers.add_parser("analysis", help="Analysis-related commands")
    analysis_subparsers = analysis_parser.add_subparsers(dest="analysis_command")

    start_parser = analysis_subparsers.add_parser("start", help="Start a new analysis")
    start_parser.add_argument("-l", "--label", required=True, help="Label of the uploaded repository")
    start_parser.add_argument("-a", "--action", required=True, help="Action to perform")
    start_parser.add_argument("-m", "--model", default="haiku", choices=["haiku", "sonnet", "opus"], help="Model to use for analysis (default: haiku)")

    get_parser = analysis_subparsers.add_parser("get", help="Get analysis results")
    get_parser.add_argument("-l", "--label", required=True, help="Label of the analyzed repository")
    get_parser.add_argument("-a", "--action", help="Action to retrieve results for (optional)")
    get_parser.add_argument("-f", "--file", help="Specific file to retrieve results for")
    get_parser.add_argument("-s", "--status", action="store_true", help="Show only status information without details")

    delete_parser = analysis_subparsers.add_parser("delete", help="Delete analysis results")
    delete_parser.add_argument("-l", "--label", required=True, help="Label of the analyzed repository")
    delete_parser.add_argument("-a", "--action", required=True, help="Action to delete results for")

    # Action commands
    action_parser = subparsers.add_parser("action", help="Action-related commands")
    action_subparsers = action_parser.add_subparsers(dest="action_command")

    ##### List actions
    list_actions_parser = action_subparsers.add_parser("list", help="List all actions")
    list_actions_parser.add_argument("-n", "--names-only", action="store_true", help="Get only action names")

    ##### Get specific action
    get_action_parser = action_subparsers.add_parser("get", help="Get a specific action")
    get_action_parser.add_argument("action", help="Action name")
    get_action_parser.add_argument("-q", "--query", choices=["steps", "include"], help="Get specific part of the action")

    ##### Get status of actions for a label
    status_parser = action_subparsers.add_parser("status", help="Get status of actions for a label")
    status_parser.add_argument("-l", "--label", required=True, help="Label to get status for")
    status_parser.add_argument("-a", "--action", help="Specific action to get status for (optional)")

    ##### Store a new action
    store_action_parser = action_subparsers.add_parser("store", help="Store a new action")
    store_action_parser.add_argument("action", nargs='?', help="Action name")
    store_action_parser.add_argument("-f", "--file", help="JSON file to load action details from")

    ##### Delete an action
    delete_action_parser = action_subparsers.add_parser("delete", help="Delete an action")
    delete_action_parser.add_argument("action", help="Action name")

    ##### Delete all actions
    delete_all_parser = action_subparsers.add_parser("delete_all", help="Delete all actions")

    ##### Add all actions from a directory
    add_all_parser = action_subparsers.add_parser("add_all", help="Add all actions from 'actions' directory")
    add_all_parser.add_argument("-d", "--directory", default="actions", help="Directory to load action JSON files from")

    # Clone commands
    clone_parser = subparsers.add_parser("clone", help="Clone repositories and upload to S3")
    clone_parser.add_argument("-u", "--url", help="Single repository URL to clone")
    clone_parser.add_argument("-f", "--file", help="File containing repository URLs to clone")
    clone_parser.add_argument("-l", "--label", required=True, help="Label for the upload (used as root folder in S3)")

    # Label commands
    label_parser = subparsers.add_parser("label", help="Label-related commands")
    label_subparsers = label_parser.add_subparsers(dest="label_command")
    
    list_labels_parser = label_subparsers.add_parser("list", help="List all labels")
    list_labels_parser.add_argument("-s", "--status", action="store_true", help="Check if label.zip exists in S3")
    
    delete_label_parser = label_subparsers.add_parser("delete", help="Delete a label")
    delete_label_parser.add_argument("label", help="Label to delete")

    
    return parser