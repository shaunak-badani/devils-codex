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

### Deployment

#### VCM

If you're deploying on vcm, change the vcm base url in `frontend/.env.production`. You can change the link to the url / ip address of the server you are hosting it on, if using GCP or Azure for deployment.

Commands to deploy:

```bash
cd TemplateProject # You can rename this, just make sure the current directory has the docker compose file
# Change vcm link to your vcm in `docker-compose-vcm.yml` file, then run:
sudo docker compose -f docker-compose-vcm.yml up --build -d
```

#### Azure 


Steps 1-3 need to be executed on **Cloud Shell**.

1. Output resource groups:
```
az group list --output table
```
2. Use any of the resource group mentioned above. Create an App Service Plan. Then check that it has been created:
```
export RESOURCE_GROUP="DefaultResourceGroup-EUS2" # Change this to resource group available you have
export APP_SERVICE_PLAN="devilsplan" # New plan that will be created, you can rename it to any plan you want
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku F1 --is-linux
az appservice plan list --output table
```

3. Create an azure container registry:


4. Build the images **locally**, using the azure build yml docker file:
```
export ACR_NAME=codexregistry # Use the same name as the one used on azure.