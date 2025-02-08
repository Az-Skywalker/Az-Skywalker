import argparse
import json
import csv
import requests
from urllib.parse import quote, urlsplit, urlunsplit
from azure.identity import DeviceCodeCredential
import gzip
import io

def get_access_token(credential, scope):
    try:
        token = credential.get_token(scope)
        return token.token
    except Exception as e:
        print(f"Error getting access token: {e}")
        exit(1)

def get_subscriptions(access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://management.azure.com/subscriptions?api-version=2014-04-01", headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting subscriptions: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting subscriptions: {err}")
    return []

def get_logic_apps(subscription_id, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{quote(subscription_id)}/providers/Microsoft.Logic/workflows?api-version=2016-06-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting logic apps for subscription {subscription_id}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting logic apps for subscription {subscription_id}: {err}")
    return []

def get_logic_app_definition(subscription_id, resource_group_name, logic_app_name, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{quote(subscription_id)}/resourceGroups/{quote(resource_group_name)}/providers/Microsoft.Logic/workflows/{quote(logic_app_name)}?api-version=2016-06-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting logic app definition for {logic_app_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting logic app definition for {logic_app_name}: {err}")
    return {}

def get_run_history(subscription_id, resource_group_name, logic_app_name, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{quote(subscription_id)}/resourceGroups/{quote(resource_group_name)}/providers/Microsoft.Logic/workflows/{quote(logic_app_name)}/runs?api-version=2016-06-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting run history for {logic_app_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting run history for {logic_app_name}: {err}")
    return []

def extract_key_vault_info(logic_app_definition):
    key_vault_info = []
    parameters = logic_app_definition.get("properties", {}).get("parameters", {})
    connections = parameters.get("$connections", {}).get("value", {})
    key_vault_connection = connections.get("keyvault", {})
    
    if key_vault_connection:
        key_vault_name = key_vault_connection.get("connectionName")
        key_vault_id = key_vault_connection.get("id")
        key_vault_info.append({
            "KeyVaultName": key_vault_name,
            "KeyVaultId": key_vault_id
        })
    
    return key_vault_info

def extract_secret_actions(logic_app_definition):
    secret_actions = []
    actions = logic_app_definition.get("properties", {}).get("definition", {}).get("actions", {})
    
    for action_name, action in actions.items():
        inputs = action.get("inputs", {})
        host = inputs.get("host", {})
        connection = host.get("connection", {})
        
        if connection.get("name") == "@parameters('$connections')['keyvault']['connectionId']":
            path = inputs.get("path", "")
            if "/secrets/" in path and "outputs" not in action.get("runtimeConfiguration", {}).get("secureData", {}).get("properties", []):
                secret_name = path.split("/secrets/")[1].split("'")[1]
                secret_actions.append({
                    "ActionName": action_name,
                    "SecretName": secret_name
                })
    
    return secret_actions

def get_action_details(subscription_id, resource_group_name, logic_app_name, run_id, action_name, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # URL encode the entire URL
        url = f"https://management.azure.com/subscriptions/{quote(subscription_id)}/resourceGroups/{quote(resource_group_name)}/providers/Microsoft.Logic/workflows/{quote(logic_app_name)}/runs/{quote(run_id)}/actions/{quote(action_name)}?api-version=2016-06-01"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting action details for {action_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting action details for {action_name}: {err}")
    
    return {}

def get_link_body(link):
    try:
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(link, headers=headers)
        response.raise_for_status()
              
        content_encoding = response.headers.get('Content-Encoding')
        if content_encoding == 'gzip':
            try:
                buf = io.BytesIO(response.content)
                with gzip.GzipFile(fileobj=buf) as f:
                    content = f.read().decode('utf-8')
            except OSError:
                content = response.content.decode('utf-8')
        else:
            content = response.content.decode('utf-8')
        
        json_content = json.loads(content)
        return json_content.get("body", json_content)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting link body: {http_err}")
        return {"error": str(http_err), "response": response.text}
    except Exception as err:
        print(f"An error occurred while getting link body: {err}")
        return {"error": str(err)}

def main(args):
    banner = r"""
     _             ____  _                        _ _             
    / \    ____   / ___|| | ___   ___      ____ _| | | _____ _ __ 
   / _ \  |_  /___\___ \| |/ / | | \ \ /\ / / _` | | |/ / _ \ '__|
  / ___ \  / /_____|__) |   <| |_| |\ V  V / (_| | |   <  __/ |   
 /_/   \_\/___|   |____/|_|\_\\__, | \_/\_/ \__,_|_|_|\_\___|_|   
                              |___/
    """
    print(banner)
    credential = DeviceCodeCredential()

    access_token = get_access_token(credential, "https://management.azure.com/.default")
    
    subscriptions = get_subscriptions(access_token)
    
    all_logic_apps = []
    subscription_count = 0
    logic_app_count = 0
    input_links_retrieved = 0
    output_links_retrieved = 0
    input_links_errors = 0
    output_links_errors = 0
    
    for subscription in subscriptions:
        subscription_id = subscription["subscriptionId"]
        
        if args.loglevel in ["info", "verbose"]:
            print(f"Scanning subscription id: {subscription_id}")
        
        subscription_count += 1
        logic_apps = get_logic_apps(subscription_id, access_token)
        
        for logic_app in logic_apps:
            logic_app_name = logic_app["name"]
            resource_group_name = logic_app["id"].split("/")[4]  # Extract resource group name from the ID
            
            if args.loglevel in ["info", "verbose"]:
                print(f"Scanning logic app: {logic_app_name} in resource group: {resource_group_name}")
            
            logic_app_count += 1
            logic_app_definition = get_logic_app_definition(subscription_id, resource_group_name, logic_app_name, access_token)
            run_history = get_run_history(subscription_id, resource_group_name, logic_app_name, access_token)
            
            if not args.all_history and run_history:
                run_history = [run_history[0]]  # Only process the most recent run
            
            key_vault_info = extract_key_vault_info(logic_app_definition)
            secret_actions = extract_secret_actions(logic_app_definition)
            
            for run in run_history:
                run_id = run["name"]
                
                if args.loglevel in ["info", "verbose"]:
                    print(f"Scanning run_id: {run_id}")
                
                actions_url = f"https://management.azure.com/subscriptions/{quote(subscription_id)}/resourceGroups/{quote(resource_group_name)}/providers/Microsoft.Logic/workflows/{quote(logic_app_name)}/runs/{quote(run_id)}/actions?api-version=2016-06-01"
                actions_response = requests.get(actions_url, headers={"Authorization": f"Bearer {access_token}"})
                actions_response.raise_for_status()
                actions = actions_response.json()["value"]
                
                for action in actions:
                    action_name = action["name"]
                    action_status = action["properties"]["status"]
                    
                    if action_status != "Succeeded":
                        continue
                    
                    if args.loglevel in ["info", "verbose"]:
                        print(f"Scanning action: {action_name}")
                    
                    action_details = get_action_details(subscription_id, resource_group_name, logic_app_name, run_id, action_name, access_token)
                    inputs_link = action_details.get("properties", {}).get("inputsLink", {}).get("uri")
                    outputs_link = action_details.get("properties", {}).get("outputsLink", {}).get("uri")
                                       
                    end_time = action_details.get("properties", {}).get("endTime")
                    
                    input_body = get_link_body(inputs_link) if args.dump_secrets and inputs_link else None
                    output_body = get_link_body(outputs_link) if args.dump_secrets and outputs_link else None
                    
                    if input_body:
                        if "error" in input_body:
                            input_links_errors += 1
                        else:
                            input_links_retrieved += 1
                    
                    if output_body:
                        if "error" in output_body:
                            output_links_errors += 1
                        else:
                            output_links_retrieved += 1
                    
                    logic_app_details = {
                        "SubscriptionId": subscription_id,
                        "ResourceGroupName": resource_group_name,
                        "LogicAppName": logic_app_name,
                        "KeyVaultInfo": key_vault_info,
                        "KeyVaultSecretActions": secret_actions,
                        "InputsLink": inputs_link,
                        "OutputsLink": outputs_link,
                        "InputBody": input_body,
                        "OutputBody": output_body,
                        "EndTime": end_time
                    }
                    
                    all_logic_apps.append(logic_app_details)
                    
                    if args.loglevel == "verbose":
                        print(logic_app_details)
    
    if all_logic_apps:
        if args.json:
            with open("logic_apps.json", "w") as json_file:
                json.dump(all_logic_apps, json_file, indent=4)
        
        if args.csv:
            with open("logic_apps.csv", "w", newline='') as csv_file:
                fieldnames = ["SubscriptionId", "ResourceGroupName", "LogicAppName", "KeyVaultInfo", "KeyVaultSecretActions", "InputsLink", "OutputsLink", "InputBody", "OutputBody", "EndTime"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_logic_apps)
    else:
        print("No Logic Apps found with the specified criteria.")
    
    summary = {
        "TotalLogicApps": logic_app_count,
        "TotalSubscriptions": subscription_count,
        "InputLinksRetrieved": input_links_retrieved,
        "OutputLinksRetrieved": output_links_retrieved,
        "InputLinksErrors": input_links_errors,
        "OutputLinksErrors": output_links_errors
    }
    
    print("\nSummary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enumerates all Logic Apps in all resource groups in all subscriptions using the Azure Management API.")
    parser.add_argument("-json", action="store_true", help="Output results to a JSON file.")
    parser.add_argument("-csv", action="store_true", help="Output results to a CSV file.")
    parser.add_argument("-loglevel", choices=["quiet", "info", "verbose"], default="info", help="Set the logging level.")
    parser.add_argument("-dump_secrets", action="store_true", help="Retrieve and output the body of inputsLink and outputsLink URLs.")
    parser.add_argument("-all_history", action="store_true", help="Process all runs of the workflow.")
    args = parser.parse_args()
    main(args)
