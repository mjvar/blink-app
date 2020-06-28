# Blink

The future of wellness, powered by computer vision and recommendation engines.

## The Problem
The COVID-19 pandemic has left nearly all of us working remotely. This means that we’re spending more time than ever in front of computer screens. Research shows that this can lead to increased eye strain and fatigue. As students who will be taking online classes for extended hours in the near future, we saw a chance to solve this problem with data and optimize our daily grinds. 

## The Solution
To tackle the problem of screen fatigue, we combined the computer vision technology of OpenCV with the usability of a website app. With a Flask backend connecting the Python computer vision app with the user-friendly front end, Blink was born.

Blink is a data-driven wellness and productivity platform that tracks your eye movements and creates intelligent recommendations about optimal times for work and rest. Blink tracks you while you work to see how drowsy you get and how often you leave your screen to rest. If your eyes are getting strained, or if you're not taking enough screen breaks, Blink will send a gentle reminder to your browser notifications.

Blink’s landing page visualizes the user’s eye aspect ratio, which is a measure of their alertness. This graph updates live, showing the user how their data is used in recommendations. Your anonymous eye strain data is constantly stored in our database, which means that Blink is also able to update live and provide notifications when they are most necessary.

With a menu in the top right corner, you can navigate to a video with overlaid information displaying what Blink collects as data. Since Blink uses facial recognition, this video helps you to understand how data is collected from them, and how it relates to the graph displayed on the landing page.

Lastly, the Recommendation page is where Blink. These recommendations are bolstered by our system of notifications, allowing them to take breaks at optimal times, coming back to their online work well rested, happier, and more productive. 

# Technical Details & Installation
Blink has four main components: a frontend in vanilla Javascript that heavily leverages charts.js; a script in OpenCV that conducts eye tracking; a robust backend in Flask with detailed request architectures for both the OpenCV script (to receive eye and face tracking data) and the frontend (to load data into charts.js visualizations); and a database in PostgreSQL.

The frontend and UI are simple but intuitive. The charts.js data visualizations update in real time based on requests to Flask; the live updates are represented with smooth and elegant animations.

The OpenCV script excellently tracks eye fatigue by calculating eye aspect ratio (EAR) and detecting when the user takes breaks. The script persistently tracks EAR, as well as noting when users leave the screen for a prolonged period of time to track breaks. These data points help Blink determine when a user hasn't taken a break for too long, or when their eyes are beginning to strain.

The Flask backend communicates with the frontend, the OpenCV tracking script, and the PostgreSQL database. It is able to simultaneously and smoothly process requests from all three components.

## Requirements
This is a prototype build, so users will need to install dependencies on their machine. Future builds will be hosted remotely so that users can access them with a click of a link.

Specific installation instructions for the Flask server can be found in `docs/USER_GUIDE.md`.

* Python 3
* Flask
* virtualenv
* Postgres.app or equivalent PostgreSQL client

Other dependencies can be installed with `(venv) $ pip install -r requirements.txt` with instructions found in `docs/USER_GUIDE.md`.
