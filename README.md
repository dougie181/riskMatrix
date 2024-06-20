# riskMatrix
Simple tool to create a riskMatrix image based on a risk register

## Local Installation (macOS)

1. Change directory to local folder
```
cd local
```
2. Please make sure you create a virtual environment before installing any python packages
```
python3 -m venv virtualenvs/riskMatrix 
source virtualenvs/riskMatrix/bin/activate
```
3. Install python packages
```
pip3 install -r requirements.txt  
```
4. change permissions of the script
```
chmod a+x generateRiskMatrix.py
```
5. Run the program
```
generateRiskMatrix.py risk_data.json example.jpg
```
or
```
./showRiskMatrix.py risk_data.json
```

## Azure installation

1. Change directory to azure folder
```
cd azure
```
1. Install the Azure CLI -ref: [https://learn.microsoft.com/en-us/cli/azure/install-azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
    - macOS: ```brew update && brew install azure-cli```
2. Open project in VSCode
3. Install the **Azure Functions** Extension
4. Right click the functionApp folder and select "Deploy to function App..."
5. Open a terminal session
6. Retrieve the function name nad resource group, using: 
   
    ```az functionapp list --output table```
7. Update the **RESOURCE_GROUP** and **FUNCTION_APP_NAME** in the testFunction.sh script
8. Run the test script 
    ```scripts/testFunction.sh```
9. open the image file
    ```open example_risk_matrix.png```