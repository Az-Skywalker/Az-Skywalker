```
     _             ____  _                        _ _             
    / \    ____   / ___|| | ___   ___      ____ _| | | _____ _ __ 
   / _ \  |_  /___\___ \| |/ / | | \ \ /\ / / _` | | |/ / _ \ '__|
  / ___ \  / /_____|__) |   <| |_| |\ V  V / (_| | |   <  __/ |   
 /_/   \_\/___|   |____/|_|\_\\__, | \_/\_/ \__,_|_|_|\_\___|_|   
                              |___/
```

# Az-SkyWalker

> ## 🚨 Security Advisory — 30 March 2026
>
> **Microsoft has silently remediated SilentReaper.**
>
> As of March 2026, Microsoft have quietly patched the vulnerability underlying the *SilentReaper* technique.
> The Azure Logic Apps Management API **no longer emits SAS URIs** in the `inputsLink` and `outputsLink`
> fields of action run details — these fields now return `null` in the API response.
>
> Additionally, Microsoft have retroactively removed all SAS URI examples from the official
> [`azure-rest-api-specs`](https://github.com/Azure/azure-rest-api-specs) repository, quietly eliminating
> the documented evidence that this data was ever accessible through the API.
>
> The sample output in this README has been updated to reflect the current API behaviour.
> `InputsLink` and `OutputsLink` will now always be `null`. The `-dump_secrets` flag in
> `Skywalker-LogicApps.py` will no longer yield secret values via this technique.

Az-SkyWalker is a project designed to enumerate all secrets in all Azure Key Vaults and Logic Apps across all subscriptions. 
The project includes scripts written in Python, allowing users to execute their tasks seamlessly. The scripts utilize the Azure Management API to retrieve and display secret details, with options to output results to JSON and CSV files.

## Purpose

The purpose of this project is to provide an automated way to gather secret details from Azure Key Vaults and Logic Apps in 
multiple subscriptions. This can be useful for security audits, compliance checks, and general management of secrets and workflow configurations.

## ⚠️ Disclaimer & Legal Notice

	Az-SkyWalker is intended for authorized use only. This tool is designed for security auditing, compliance checks, and legitimate administrative purposes within Azure environments that you own or have explicit permission to access.

	Unauthorized use of this tool to access Azure Key Vaults, Logic Apps, or any cloud resources without explicit authorization is illegal and may violate laws such as:
	•	Computer Fraud and Abuse Act (CFAA) - USA
	•	UK Computer Misuse Act 1990
	•	General Data Protection Regulation (GDPR) - EU
	•	Other applicable cybersecurity and data protection laws in your jurisdiction

	By using this tool, you confirm that:
	•	You have explicit authorization from the Azure tenant owner to enumerate secrets.
	•	You will not use this tool for unauthorized penetration testing, hacking, or any illegal activity.
	•	You assume full legal responsibility for your actions when using this tool.

### Limitation of Liability:
This software is provided "as is", without any warranties or guarantees. The authors assume no responsibility for any legal issues, damages, or consequences resulting from the misuse of this tool.

## 📜 Licensing

This project is licensed under the MIT License. See the LICENSE file for more 


## Repository Structure

```
Az-SkyWalker/
├── docker
│   ├── az-skywalker.dockerfile
├── output/
│   ├── secrets.csv
│   ├── secrets.json
│   ├── logic_apps.csv
│   └── logic_apps.json
├── src/
│   └── Python/
│       ├── Skywalker-CLI.py
│       ├── Skywalker-KeyVaults.py
│       ├── Skywalker-LogicApps.py
│       └── requirements.txt
└── README.md
```

- `docker/`: Contains `az-skywalker.dockerfile` for building a ubuntu container image with everything you need to run Az-SkyWalker
- `output/`: Contains sample output files (`secrets.csv`, `secrets.json`, `logic_apps.csv`, and `logic_apps.json`) demonstrating the results of running the scripts.
- `src/Python/`: Contains the Python scripts `Skywalker-CLI.py`, `Skywalker-KeyVaults.py` and `Skywalker-LogicApps.py`, along with the corresponding `requirements.txt` file.
- `README.md`: Project documentation.

## Running Az-SkyWalker Manually on Ubuntu

### Prerequisites
Before running the scripts manually, ensure your system is up-to-date and has the required software installed.

#### Install Required Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential python3.12 python3.12-venv python3-pip python3-dev libffi-dev
pip install --upgrade pip setuptools wheel
```

#### Clone the Repository
```bash
git clone https://github.com/Az-Skywalker/Az-Skywalker-Dev.git
cd Az-SkyWalker-Dev/src/python
```

#### Set Up and Activate Virtual Environment
```bash
python3 -m venv sky
source sky/bin/activate
pip install -r requirements.txt
```

## Running Az-SkyWalker Using Docker

### Building the Docker Image
```bash
docker build -t az-skywalker .
```

### Running the Docker Container
```bash
docker run -it az-skywalker
```

This will launch the container with all dependencies installed and start a Bash shell where you can execute the scripts inside the `/root/Az-Skywalker-Dev/src/python/` directory.

#### Inside the Container
```bash
cd /root/Az-Skywalker-Dev/src/python
source sky/bin/activate
```

## Usage

## Running and Using `Skywalker-CLI.py`

`Skywalker-CLI.py` is a unified command-line interface that allows users to interactively select and execute security reconnaissance scenarios.

### Running in Interactive Mode

Run the CLI script without arguments to enter the interactive menu:
```bash
python Skywalker-CLI.py
```
The script will prompt you to select a scenario (`logicapps` or `keyvaults`) and configure various options interactively.

### Running with Command-Line Arguments
You can also execute specific reconnaissance scenarios directly:
```bash
python Skywalker-CLI.py keyvaults -json -csv
```
```bash
python Skywalker-CLI.py logicapps -loglevel info
```

#### Available Scenarios
- **keyvaults**: Executes `Skywalker-KeyVaults.py` to retrieve secrets from Azure Key Vaults.
- **logicapps**: Executes `Skywalker-LogicApps.py` to analyze secrets usage in Logic Apps.

#### Common Arguments
- `-json`: Output results to a JSON file.
- `-csv`: Output results to a CSV file.
- `-loglevel [quiet|info|verbose]`: Set the log level.

### Skywalker-KeyVaults.py Script

1. **Prerequisites**:
   - Ensure Python is installed.
   - Install the required Python packages:
     ```bash
     # Navigate to the Python script directory
     cd src/Python

     # Install the dependencies
     pip install -r requirements.txt
     ```

2. **Running the Script**:
   ```bash
   # Navigate to the Python script directory
   cd src/Python

   # Run the script
   python Skywalker-KeyVaults.py -json -csv -noDisplay
   ```

   - `-json`: Output results to a JSON file.
   - `-csv`: Output results to a CSV file.
   - `-noDisplay`: Do not display the secrets on screen but still respect the `-json` and `-csv` options.

### Skywalker-LogicApps.py Script

1. **Prerequisites**:
   - Ensure Python is installed.
   - Install the required Python packages:
     ```bash
     # Navigate to the Python script directory
     cd src/Python

     # Install the dependencies
     pip install -r requirements.txt
     ```

2. **Running the Script**:
   ```bash
   # Navigate to the Python script directory
   cd src/Python

   # Run the script
   python Skywalker-LogicApps.py -json -csv -loglevel info
   ```

   - `-json`: Output results to a JSON file.
   - `-csv`: Output results to a CSV file.
   - `-loglevel [quiet|info|verbose]`: Set the log level (default: `info`).
   - `-dump_secrets`: Retrieve and output the body of `inputsLink` and `outputsLink` URLs. ⚠️ See advisory above — SAS URIs are no longer emitted by the API.
   - `-all_history`: Process all runs of the workflow, not just the most recent.

## Sample Output

### JSON Output (Skywalker-KeyVault.py)

```json
[
    {
        "SubscriptionId": "35563d84-e3af-43c1-a0d3-e7aa84ebf1aa",
        "ResourceGroupName": "first-order-rg",
        "KeyVaultName": "starkiller-base-kv",
        "SecretName": "supreme-leader-key",
        "ContentType": "application/x-pkcs12",
        "Enabled": true,
        "NotBefore": 1734788596,
        "Expires": 1766325196,
        "Created": 1734789196,
        "Updated": 1734789196,
        "SecretUri": "https://starkiller-base-kv.vault.azure.net/secrets/supreme-leader-key",
        "SecretUriWithVersion": "https://starkiller-base-kv.vault.azure.net/secrets/supreme-leader-key/ea87d49179d24f7f89acd6b5b9f01027"
    }
]
```

### CSV Output (Skywalker-KeyVault.py)

```csv
SubscriptionId,ResourceGroupName,KeyVaultName,SecretName,ContentType,Enabled,NotBefore,Expires,Created,Updated,SecretUri,SecretUriWithVersion
35563d84-e3af-43c1-a0d3-e7aa84ebf1aa,first-order-rg,starkiller-base-kv,supreme-leader-key,application/x-pkcs12,True,1734788596,1766325196,1734789196,1734789196,https://starkiller-base-kv.vault.azure.net/secrets/supreme-leader-key,https://starkiller-base-kv.vault.azure.net/secrets/supreme-leader-key/ea87d49179d24f7f89acd6b5b9f01027
```

### JSON Output (Skywalker-LogicApps.py)

> ⚠️ **As of 30 March 2026, `InputsLink` and `OutputsLink` are `null` in the API response.**
> Microsoft have silently remediated SilentReaper — see the advisory at the top of this page.

```json
[
    {
        "SubscriptionId": "35563d84-e3af-43c1-a0d3-e7aa84ebf1aa",
        "ResourceGroupName": "galactic-empire-rg1",
        "LogicAppName": "logi-1",
        "KeyVaultInfo": [
            {
                "KeyVaultName": "keyvault",
                "KeyVaultId": "/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault"
            }
        ],
        "KeyVaultSecretActions": [
            {
                "ActionName": "Get_secret_version",
                "SecretName": "risk-register-admin-password"
            }
        ],
        "InputsLink": null,
        "OutputsLink": null,
        "InputBody": null,
        "OutputBody": null,
        "EndTime": "2024-12-30T17:25:00.4293787Z"
    },
    {
        "SubscriptionId": "35563d84-e3af-43c1-a0d3-e7aa84ebf1aa",
        "ResourceGroupName": "galactic-empire-rg1",
        "LogicAppName": "logi-2",
        "KeyVaultInfo": [
            {
                "KeyVaultName": "keyvault",
                "KeyVaultId": "/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault"
            }
        ],
        "KeyVaultSecretActions": [
            {
                "ActionName": "Get_secret_version",
                "SecretName": "risk-register-admin-password"
            }
        ],
        "InputsLink": null,
        "OutputsLink": null,
        "InputBody": null,
        "OutputBody": null,
        "EndTime": "2024-12-30T17:25:00.4476723Z"
    }
]
```

### CSV Output (Skywalker-LogicApps.py)

```csv
SubscriptionId,ResourceGroupName,LogicAppName,KeyVaultInfo,KeyVaultSecretActions,InputsLink,OutputsLink,InputBody,OutputBody,EndTime
35563d84-e3af-43c1-a0d3-e7aa84ebf1aa,galactic-empire-rg1,logi-1,"[{'KeyVaultName': 'keyvault', 'KeyVaultId': '/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault'}]","[{'ActionName': 'Get_secret_version', 'SecretName': 'risk-register-admin-password'}]",,,,,2024-12-30T17:25:00.4293787Z
35563d84-e3af-43c1-a0d3-e7aa84ebf1aa,galactic-empire-rg1,logi-2,"[{'KeyVaultName': 'keyvault', 'KeyVaultId': '/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault'}]","[{'ActionName': 'Get_secret_version', 'SecretName': 'risk-register-admin-password'}]",,,,,2024-12-30T17:25:00.4476723Z
```

## Contributing

Contributions are welcome! 
Please feel free to submit a Pull Request or raise an issue.
