import argparse
import subprocess
import re
import questionary
import readchar  # Instant keypress detection
import sys  # For clean Ctrl + C handling

# Mapping of available scenarios to their respective script files
SCENARIOS = {
    "logicapps": "Skywalker-LogicApps.py",
    "keyvaults": "Skywalker-KeyVaults.py",
}

def extract_arguments_from_script(script_path):
    """Extract arguments from the script, distinguishing flags, choices, and normal arguments."""
    flag_args = []
    choice_args = []
    value_args = []

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            content = file.readlines()

        # Regex to detect argparse.add_argument() calls
        arg_pattern = re.compile(
            r'parser\.add_argument\(\s*[\'"](-[\w-]+)[\'"],'  # Capture argument name
            r'(?:[^)]*?action=["\']store_true["\'])?'  # Detect store_true arguments (flags)
            r'(?:[^)]*?help=["\'](.*?)["\'])?'  # Capture help description (optional)
            r'(?:[^)]*?choices\s*=\s*\[(.*?)\])?'  # Capture choices
            r'(?:[^)]*?default\s*=\s*["\']?([^,"\'\]]+)["\']?)?',  # Capture default value
            re.DOTALL | re.MULTILINE
        )

        loglevel_pattern = re.compile(r"-loglevel\s+(quiet|info|verbose)")

        for line in content:
            match = arg_pattern.search(line)
            if match:
                arg_name = match.group(1)
                is_flag = "store_true" in line  # Detect flag arguments
                arg_help = match.group(2) if match.group(2) else "No description available"
                arg_choices = match.group(3)  # Extract choices
                arg_default = match.group(4)  # Extract default value

                if arg_choices:
                    parsed_choices = [choice.strip().strip("\"'") for choice in arg_choices.split(",")]
                    choice_args.append({
                        "name": arg_name,
                        "help": arg_help,
                        "choices": parsed_choices,
                        "default": arg_default
                    })
                elif is_flag:
                    flag_args.append({"name": arg_name, "help": arg_help})
                else:
                    value_args.append({"name": arg_name, "help": arg_help})

            # Check for -loglevel and manually assign choices
            loglevel_match = loglevel_pattern.search(line)
            if loglevel_match:
                if not any(arg["name"] == "-loglevel" for arg in choice_args):
                    choice_args.append({
                        "name": "-loglevel",
                        "help": "Set log level",
                        "choices": ["quiet", "info", "verbose"],
                        "default": "info"
                    })

    except FileNotFoundError:
        print(f"[ERROR] Could not find script: {script_path}")

    return flag_args, choice_args, value_args

def get_yes_no_input(prompt):
    """Handle Yes/No inputs with instant keypress detection."""
    print(prompt + " (Y/N)", end=" ", flush=True)
    try:
        while True:
            key = readchar.readchar().lower()  # Read a single keypress
            if key in ["y", "n"]:
                print(key.upper())  # Show user input
                return key == "y"  # Return True for Yes, False for No
            elif key == "\r":  # Enter key
                print("Skipping")
                return False  # Treat Enter as skipping
    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")  # Allow clean Ctrl + C exit
        sys.exit(0)

def interactive_menu():
    banner = r"""
     _             ____  _                        _ _             
    / \    ____   / ___|| | ___   ___      ____ _| | | _____ _ __ 
   / _ \  |_  /___\___ \| |/ / | | \ \ /\ / / _` | | |/ / _ \ '__|
  / ___ \  / /_____|__) |   <| |_| |\ V  V / (_| | |   <  __/ |   
 /_/   \_\/___|   |____/|_|\_\\__, | \_/\_/ \__,_|_|_|\_\___|_|   
                              |___/
    """
    """Interactive CLI menu for selecting a scenario and its arguments."""
    print(banner)
    print("\n=== Skywalker Recon CLI ===")

    selected_scenario = questionary.select(
        "Select a recon scenario:",
        choices=list(SCENARIOS.keys())
    ).ask()

    script_path = SCENARIOS[selected_scenario]
    flag_args, choice_args, value_args = extract_arguments_from_script(script_path)

    user_args = []

    # Step 1: Process Flag-Based Arguments (Yes/No)
    for arg in flag_args:
        if get_yes_no_input(f"Do you want to set {arg['name']}?"):
            user_args.append(arg["name"])  # Add flag (e.g., `-json`)

    # Step 2: Process Choice-Based Arguments (Dropdown)
    for arg in choice_args:
        selected_value = questionary.select(
            f"{arg['name']} - {arg['help']}",
            choices=arg["choices"],
            default=arg["default"] if arg["default"] in arg["choices"] else None
        ).ask()
        user_args.append(arg["name"])
        user_args.append(selected_value)

    # Step 3: Process Normal Value Arguments (Prompt for Input)
    for arg in value_args:
        if arg["name"] == "-loglevel":  # Handle -loglevel separately
            log_level = questionary.select(
                f"{arg['name']} - {arg['help']}",
                choices=["quiet", "info", "verbose"],
                default=arg.get("value", "info")
            ).ask()
            user_args.append(arg["name"])
            user_args.append(log_level)
        else:
            user_input = questionary.text(f"Enter value for {arg['name']} ({arg['help']}):").ask()
            if user_input:
                user_args.append(arg["name"])
                user_args.append(user_input)
                
    if not user_args:
        print("\n[INFO] No arguments selected. Exiting.")
        sys.exit(0)

    command_string = " ".join(user_args)
    confirm = questionary.confirm(
        f"Execute {selected_scenario} with arguments: {command_string}?"
    ).ask()

    if confirm:
        run_scenario(selected_scenario, user_args)
    else:
        print("\nExecution cancelled.")

def run_scenario(scenario, user_args):
    """Run the selected recon scenario script with user-specified arguments."""
    script_path = SCENARIOS.get(scenario)
    if not script_path:
        print(f"[ERROR] Invalid scenario '{scenario}'. Use --help to see available options.")
        return

    cmd = ["python3", script_path] + user_args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Script '{script_path}' failed with error: {e}")

def main():
    """Main CLI entry point."""
    try:
        parser = argparse.ArgumentParser(
            description="Skywalker Recon CLI - Unified tool for security reconnaissance."
        )
        parser.add_argument(
            "scenario",
            nargs="?",  # Makes it optional
            choices=SCENARIOS.keys(),
            help="Choose a recon scenario to execute."
        )
        parser.add_argument(
            "args",
            nargs=argparse.REMAINDER,
            help="Additional arguments to pass to the selected script."
        )

        args = parser.parse_args()

        if not args.scenario:
            interactive_menu()
        else:
            run_scenario(args.scenario, args.args)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
