DynamoToCG\DynamoToCG\bin\Debug\DynamoToCG.exe %1 %TEMP%.\out.cgx
python applier.py %TEMP%.\out.cgx %2 %TEMP%.\new.cgx
DynamoToCG\CGToDYN\bin\Debug\CGToDYN.exe %TEMP%.\new.cgx %3
