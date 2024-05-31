@echo off

python server.py
git add .
set currentdatetime=%date% %time%
git commit -m "update at : %currentdatetime%"
git push

echo Done!
pause