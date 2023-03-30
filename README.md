<h1>Getting started</h1>

<h3>Requirements</h3>

    - Python 3.10
    - ffmpeg

<h3>Install</h3>

    cd backend
    pip install -r reqirements.txt

    cd ..

    cd frontend
    npm i

<h3>Setting</h3>
create a .env.local file in the root folder with the following content

    DB_NAME=*****
    DB_USER=*****
    DB_PASSWORD=*****
    DB_PORT=5432
    DB_HOST=localhost

<h3>Run</h3>

<h4>backend</h4>

    uvicorn backend.main:app --host localhost

<h4>frontend</h4>

    npm run dev
