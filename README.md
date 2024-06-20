# riskMatrix
Simple tool to create a riskMatrix image based on a risk register

## Local nstallation

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