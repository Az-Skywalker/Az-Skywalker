```
     _             ____  _                        _ _             
    / \    ____   / ___|| | ___   ___      ____ _| | | _____ _ __ 
   / _ \  |_  /___\___ \| |/ / | | \ \ /\ / / _` | | |/ / _ \ '__|
  / ___ \  / /_____|__) |   <| |_| |\ V  V / (_| | |   <  __/ |   
 /_/   \_\/___|   |____/|_|\_\\__, | \_/\_/ \__,_|_|_|\_\___|_|   
                              |___/
```

# Az-SkyWalker

Az-SkyWalker is a project designed to enumerate all secrets in all Azure Key Vaults and Logic Apps across all subscriptions. 
The project includes scripts written in Python, allowing users to execute their tasks seamlessly. The scripts utilize the Azure Management API to retrieve and display secret details, with options to output results to JSON and CSV files.

## Purpose

The purpose of this project is to provide an automated way to gather secret details from Azure Key Vaults and Logic Apps in 
multiple subscriptions. This can be useful for security audits, compliance checks, and general management of secrets and workflow configurations.

## Repository Structure

```
Az-SkyWalker/
├── docker
│   ├── az-skywalker.dockerfile
├── outputs/
│   ├── secrets.csv
│   ├── secrets.json
│   ├── logic_apps.csv
│   └── logic_apps.json
├── src/
│   └── Python/
│       ├── Skywalker-KeyVault.py
│       ├── Skywalker-LogicApps.py
│       └── requirements.txt
└── README.md
```

- `docker/`: Contains `az-skywalker.dockerfile` for building a ubuntu container image with everything you need to run Az-SkyWalker
- `outputs/`: Contains sample output files (`secrets.csv`, `secrets.json`, `logic_apps.csv`, and `logic_apps.json`) demonstrating the results of running the scripts.
- `src/Python/`: Contains the Python scripts `Skywalker-KeyVault.py` and `Skywalker-LogicApps.py`, along with the corresponding `requirements.txt` file.
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
- **keyvaults**: Executes `Skywalker-KeyVault.py` to retrieve secrets from Azure Key Vaults.
- **logicapps**: Executes `Skywalker-LogicApps.py` to analyze secrets usage in Logic Apps.

#### Common Arguments
- `-json`: Output results to a JSON file.
- `-csv`: Output results to a CSV file.
- `-loglevel [quiet|info|verbose]`: Set the log level.

### Skywalker-KeyVault.py Script

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
   python Skywalker-KeyVault.py -json -csv -noDisplay
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
   python Skywalker-LogicApps.py -json -csv -noDisplay
   ```

   - `-json`: Output results to a JSON file.
   - `-csv`: Output results to a CSV file.
   - `-noDisplay`: Do not display the secrets and workflow configurations on screen but still respect the `-json` and `-csv` options.

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
        "InputsLink": "https://prod-21.uksouth.logic.azure.com:443/workflows/2c85458e0b2147f3a3ef6bcae0ff7997/runs/08584660273854748250447950450CU09/actions/Get_secret_version/contents/ActionInputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273854748250447950450CU09%2Factions%2FGet_secret_version%2Fcontents%2FActionInputs%2Fread&sv=1.0&sig=84Y8XJ2-2ygulXQ_BHU8XgN-tmClQlRhyshdhFG1FPQ",
        "OutputsLink": "https://prod-21.uksouth.logic.azure.com:443/workflows/2c85458e0b2147f3a3ef6bcae0ff7997/runs/08584660273854748250447950450CU09/actions/Get_secret_version/contents/ActionOutputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273854748250447950450CU09%2Factions%2FGet_secret_version%2Fcontents%2FActionOutputs%2Fread&sv=1.0&sig=2ydUFPj0NTurXoPjwIMzvkTDT-u6FPpFTtdOeyQZa0Y",
        "InputBody": null,
        "OutputBody": {
            "value": "password123",
            "name": "risk-register-admin-password",
            "version": "70ab34121c64481480d806cc048d7f99",
            "contentType": null,
            "isEnabled": true,
            "createdTime": "2024-12-21T13:33:58Z",
            "lastUpdatedTime": "2024-12-21T13:33:58Z",
            "validityStartTime": null,
            "validityEndTime": null
        },
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
        "InputsLink": "https://prod-23.uksouth.logic.azure.com:443/workflows/db10d2ccd0a7470f85cf326bc92cdc8d/runs/08584660273853241947273607938CU08/actions/Get_secret_version/contents/ActionInputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273853241947273607938CU08%2Factions%2FGet_secret_version%2Fcontents%2FActionInputs%2Fread&sv=1.0&sig=LoFa6qsXZmJK95-eUYvYw5RlyW0-LOJmmCLVUIlWSdU",
        "OutputsLink": "https://prod-23.uksouth.logic.azure.com:443/workflows/db10d2ccd0a7470f85cf326bc92cdc8d/runs/08584660273853241947273607938CU08/actions/Get_secret_version/contents/ActionOutputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273853241947273607938CU08%2Factions%2FGet_secret_version%2Fcontents%2FActionOutputs%2Fread&sv=1.0&sig=XQSR1rqhUWA7D-1uQ0xxUpwMQbxO7zfCKtv0oJK5WY0",
        "InputBody": null,
        "OutputBody": {
            "value": "password123",
            "name": "risk-register-admin-password",
            "version": "70ab34121c64481480d806cc048d7f99",
            "contentType": null,
            "isEnabled": true,
            "createdTime": "2024-12-21T13:33:58Z",
            "lastUpdatedTime": "2024-12-21T13:33:58Z",
            "validityStartTime": null,
            "validityEndTime": null
        },
        "EndTime": "2024-12-30T17:25:00.4476723Z"
    }
]
```

### CSV Output (Skywalker-LogicApps.py)

```csv
SubscriptionId,ResourceGroupName,LogicAppName,KeyVaultInfo,KeyVaultSecretActions,InputsLink,OutputsLink,InputBody,OutputBody,EndTime
35563d84-e3af-43c1-a0d3-e7aa84ebf1aa,galactic-empire-rg1,logi-1,"[{'KeyVaultName': 'keyvault', 'KeyVaultId': '/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault'}]","[{'ActionName': 'Get_secret_version', 'SecretName': 'risk-register-admin-password'}]",https://prod-21.uksouth.logic.azure.com:443/workflows/2c85458e0b2147f3a3ef6bcae0ff7997/runs/08584660273854748250447950450CU09/actions/Get_secret_version/contents/ActionInputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273854748250447950450CU09%2Factions%2FGet_secret_version%2Fcontents%2FActionInputs%2Fread&sv=1.0&sig=84Y8XJ2-2ygulXQ_BHU8XgN-tmClQlRhyshdhFG1FPQ,https://prod-21.uksouth.logic.azure.com:443/workflows/2c85458e0b2147f3a3ef6bcae0ff7997/runs/08584660273854748250447950450CU09/actions/Get_secret_version/contents/ActionOutputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273854748250447950450CU09%2Factions%2FGet_secret_version%2Fcontents%2FActionOutputs%2Fread&sv=1.0&sig=2ydUFPj0NTurXoPjwIMzvkTDT-u6FPpFTtdOeyQZa0Y,,"{'value': 'password123', 'name': 'risk-register-admin-password', 'version': '70ab34121c64481480d806cc048d7f99', 'contentType': None, 'isEnabled': True, 'createdTime': '2024-12-21T13:33:58Z', 'lastUpdatedTime': '2024-12-21T13:33:58Z', 'validityStartTime': None, 'validityEndTime': None}",2024-12-30T17:25:00.4293787Z
35563d84-e3af-43c1-a0d3-e7aa84ebf1aa,galactic-empire-rg1,logi-2,"[{'KeyVaultName': 'keyvault', 'KeyVaultId': '/subscriptions/35563d84-e3af-43c1-a0d3-e7aa84ebf1aa/providers/Microsoft.Web/locations/uksouth/managedApis/keyvault'}]","[{'ActionName': 'Get_secret_version', 'SecretName': 'risk-register-admin-password'}]",https://prod-23.uksouth.logic.azure.com:443/workflows/db10d2ccd0a7470f85cf326bc92cdc8d/runs/08584660273853241947273607938CU08/actions/Get_secret_version/contents/ActionInputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273853241947273607938CU08%2Factions%2FGet_secret_version%2Fcontents%2FActionInputs%2Fread&sv=1.0&sig=LoFa6qsXZmJK95-eUYvYw5RlyW0-LOJmmCLVUIlWSdU,https://prod-23.uksouth.logic.azure.com:443/workflows/db10d2ccd0a7470f85cf326bc92cdc8d/runs/08584660273853241947273607938CU08/actions/Get_secret_version/contents/ActionOutputs?api-version=2016-06-01&se=2024-12-30T22%3A00%3A00.0000000Z&sp=%2Fruns%2F08584660273853241947273607938CU08%2Factions%2FGet_secret_version%2Fcontents%2FActionOutputs%2Fread&sv=1.0&sig=XQSR1rqhUWA7D-1uQ0xxUpwMQbxO7zfCKtv0oJK5WY0,,"{'value': 'password123', 'name': 'risk-register-admin-password', 'version': '70ab34121c64481480d806cc048d7f99', 'contentType': None, 'isEnabled': True, 'createdTime': '2024-12-21T13:33:58Z', 'lastUpdatedTime': '2024-12-21T13:33:58Z', 'validityStartTime': None, 'validityEndTime': None}",2024-12-30T17:25:00.4476723Z
```

## License

This project is licensed under the GPL-3.0 License. 
See the LICENSE file for details.

## Contributing

Contributions are welcome! 
Please feel free to submit a Pull Request or raise an issue.
