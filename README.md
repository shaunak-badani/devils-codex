# Devil's codex

> A chatbot that helps answer questions regarding Duke curriculums and events.


### How to run

- Frontend
```
cd frontend
npm install
npm run dev
```
- The application is then hosted on `localhost:5173`


- Backend
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```


- Deployment

If you're deploying on vcm, change the vcm base url in `frontend/.env.production`. You can change the link to the url / ip address of the server you are hosting it on, if using GCP or Azure for deployment.

Commands to deploy:

```bash
cd project-2-devils-codex
sudo docker compose -f docker-compose.yml up --build -d
```