WARNING EDUCATION PURPOSES ONLY DO NOT USE FOR MALICIOUS ACTIVITIES

THIS is a tool that can take pictures of the victim machine(Windows) using a script that disguise itself as a calculator but sent the secreatly taken pictures to a webserver



first u need to install python and following modules

pip install flask

pip install requests

pip install PyQt5

pip install pyinstaller


then u need to install ngrok and set up authtoken
the u need to start a ngrok tunnel at port 5000,copy the public URL 
paste the ngrok public URL into the calcuator.py then compile the calculator.py into  a exe using pyinstaller
then run the server.py and send the exe to the victim 



taken webcam pictures are sent to the localhost:5000 URL 

you can access the photos using 

/list




/photos/{image name}
