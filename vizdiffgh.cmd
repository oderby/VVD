VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %1 %TEMP%.\cgA
VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %2 %TEMP%.\cgB
VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %1 %1.cgx 
VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %2 %2.cgx
python diffgraph.py %TEMP%.\cgA %TEMP%.\cgB %TEMP%.\dsAB
python grapher.py %TEMP%.\cgA %TEMP%.\dsAB %3
rundll32 "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen %3
