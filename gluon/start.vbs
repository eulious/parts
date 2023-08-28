Set fs = CreatObject("Scripting.FileSystemObject")
Set ws = CreateObject("WScript.Shell")

if fs.FileExists(".\node.exe") Then
    ws.run ".\node.exe index.js", vbhide
Else
    ws.run "node index.js", vbhide
End If