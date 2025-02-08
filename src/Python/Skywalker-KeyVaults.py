import argparse
import json
import csv
import requests
from azure.identity import DeviceCodeCredential

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

def get_resource_groups(subscription_id, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups?api-version=2014-04-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting resource groups for subscription {subscription_id}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting resource groups for subscription {subscription_id}: {err}")
    return []

def get_key_vaults(subscription_id, resource_group_name, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.KeyVault/vaults?api-version=2016-10-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting key vaults for resource group {resource_group_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting key vaults for resource group {resource_group_name}: {err}")
    return []

def get_secrets(subscription_id, resource_group_name, key_vault_name, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.KeyVault/vaults/{key_vault_name}/secrets?api-version=2016-10-01"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting secrets for key vault {key_vault_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred while getting secrets for key vault {key_vault_name}: {err}")
    return []

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
    management_access_token = get_access_token(credential, "https://management.azure.com/.default")
    
    subscriptions = get_subscriptions(management_access_token)
    
    all_secrets = []
    subscription_count = 0
    resource_group_count = 0
    key_vault_count = 0
    secret_count = 0
    
    for subscription in subscriptions:
        subscription_id = subscription["subscriptionId"]
        subscription_count += 1
        resource_groups = get_resource_groups(subscription_id, management_access_token)
        
        for resource_group in resource_groups:
            resource_group_name = resource_group["name"]
            resource_group_count += 1
            key_vaults = get_key_vaults(subscription_id, resource_group_name, management_access_token)
            
            for key_vault in key_vaults:
                key_vault_name = key_vault["name"]
                key_vault_count += 1
                secrets = get_secrets(subscription_id, resource_group_name, key_vault_name, management_access_token)
                
                for secret in secrets:
                    secret_count += 1
                    secret_details = {
                        "SubscriptionId": subscription_id,
                        "ResourceGroupName": resource_group_name,
                        "KeyVaultName": key_vault_name,
                        "SecretName": secret["name"],
                        "ContentType": secret["properties"].get("contentType", ""),
                        "Enabled": secret["properties"]["attributes"]["enabled"],
                        "NotBefore": secret["properties"]["attributes"].get("nbf", ""),
                        "Expires": secret["properties"]["attributes"].get("exp", ""),
                        "Created": secret["properties"]["attributes"].get("created", ""),
                        "Updated": secret["properties"]["attributes"].get("updated", ""),
                        "SecretUri": secret["properties"]["secretUri"],
                        "SecretUriWithVersion": secret["properties"]["secretUriWithVersion"]
                    }
                    
                    all_secrets.append(secret_details)
                    if not args.noDisplay:
                        print(secret_details)
    
    if args.json and all_secrets:
        with open("secrets.json", "w") as json_file:
            json.dump(all_secrets, json_file, indent=4)
    elif args.json:
        print("No secrets found. Skipping JSON generation.")
    
    if args.csv and all_secrets:
        with open("secrets.csv", "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=all_secrets[0].keys())
            writer.writeheader()
            writer.writerows(all_secrets)
    elif args.csv:
        print("No secrets found. Skipping CSV generation.")
    
    summary = {
        "TotalSecrets": secret_count,
        "TotalKeyVaults": key_vault_count,
        "TotalResourceGroups": resource_group_count,
        "TotalSubscriptions": subscription_count
    }
    
    print("\nSummary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enumerates all secrets in all Key Vaults in all subscriptions using the Azure Management API.")
    parser.add_argument("-json", action="store_true", help="Output results to a JSON file.")
    parser.add_argument("-csv", action="store_true", help="Output results to a CSV file.")
    parser.add_argument("-noDisplay", action="store_true", help="Do not display the secrets on screen but still respect the json and csv options.")
    args = parser.parse_args()
    main(args)
