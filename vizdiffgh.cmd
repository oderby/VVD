VVD-GH-To-CG\VVD-GH-To-CG\bin\Debug\VVD-GH-To-CG.exe %1 %TEMP%.\cgA
python grapher.py %TEMP%.\cgA %2 %TEMP%.\graph.png
rundll32 "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen %TEMP%.\graph.png
