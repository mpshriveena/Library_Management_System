Setup & Installation
    -->In backend
        Make sure you have the latest version of Python installed.
        pip install virtualenv
        virtualenv mad2
        source mad2/bin/activate
        pip install -r requirements.txt
    -->In frontend
        npm install vue-router
        npm install axios
        npm install vue-toastification

Running The App
    -->Backend server
        python3 app.py
    -->Frondend server
        npm run dev
    -->Redis server
        redis-server
    -->celery worker
        celery -A app.celery_app worker -l info
    -->celery beat
        celery -A app.celery_app beat --max-interval 5 -l info

Viewing The App
    Go to http://localhost:5173/