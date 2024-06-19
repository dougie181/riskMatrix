# riskMatrix
Simple tool to create a riskMatrix image based on a risk register

## installation

1. Please make sure you create a virtual environment before installing any python packages

```
python3 -m venv virtualenvs/riskMatrix 
source virtualenvs/riskMatrix/bin/activate
```

2. Install python packages
```
pip3 install -r requirements.txt  
```

3. change permissions of the script
```
chmod a+x generateRiskMatrix.py
```

4. Run the program
```
generateRiskMatrix.py risk_data.json
```