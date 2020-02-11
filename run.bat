@echo off
set /p ti=请输入重启时间(单位 秒 通常设置为1800）:
>delay.vbs echo wscript.sleep %ti%000
:loop
start a.bat
call delay.vbs
taskkill /f /t /fi "imagename eq cmd.exe" /fi "windowtitle eq C:\Windows\system32\cmd.exe - bilibiliupnanshou.bat"
goto loop
