DynamoToCG\DynamoToCG\bin\Debug\DynamoToCG.exe %1 %TEMP%.\cgA
python grapher.py %TEMP%.\cgA %2 %TEMP%.\graph.png
rundll32 "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen %TEMP%.\graph.png