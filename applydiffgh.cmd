VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %1 %TEMP%.\out.cgx
python applier.py %TEMP%.\out.cgx %2 %TEMP%.\new.cgx
VVD-GH-To-CG\CGToGH\bin\Debug\CGToGH.exe %TEMP%.\new.cgx %3
