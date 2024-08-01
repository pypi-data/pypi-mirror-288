# cli/__init__.py

from .cli import main

'''
from .arg_parser import create_parser
from .clone import handle_clone_command
from .label import handle_label_command
from .action import handle_action_command
from .analysis import handle_analysis_command

def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.command == "analysis":
            handle_analysis_command(args)
        elif args.command == "action":
            handle_action_command(args)
        elif args.command == "clone":
            handle_clone_command(args)
        elif args.command == "label":
            handle_label_command(args)
    except Exception as e:
        print(f"Error: {e}")
'''
