<h1>Getting started</h1>

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

	uvicorn backend.main:app --host 0.0.0.0 --port 3000
<h4>frontend</h4>

	cd frontend
	npm run dev
