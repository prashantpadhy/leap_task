# leap_task
#Installation

pip install flask
pip install flask flask_pymongo

#to run the app

python app.py

#end points
1.To store like events 
POST -H "Content-Type: application/json" -d '{"user_id":"123","content_id":"456"}' http://localhost:5000/likes

2.To check if a user has liked a particular content:
GET "http://localhost:5000/likes/check?user_id=123&content_id=456"

3.To get the total likes for a content:
"http://localhost:5000/likes/total?content_id=456"
