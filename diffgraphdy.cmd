DynamoToCG\DynamoToCG\bin\Debug\DynamoToCG.exe %1 %TEMP%.\cgA
DynamoToCG\DynamoToCG\bin\Debug\DynamoToCG.exe %2 %TEMP%.\cgB
python diffgraph.py %TEMP%.\cgA %TEMP%.\cgB %3