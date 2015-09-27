VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %1 %TEMP%.\cgA
VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %2 %TEMP%.\cgB
python diffgraph.py %TEMP%.\cgA %TEMP%.\cgB %3