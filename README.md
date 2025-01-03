# MCP-workshop
MCP container and kubernetes workshop

## Introduction
Het doel van deze workshop is om een 

We hebben voor deze workshop een kant en klare WSL image gemaakt die je kan gebruiken om de workshop te volgen.

Deze kan je hier downloaden: https://mcpworkshop.blob.core.windows.net/mcp-workshop/mcp-workshop.tgz
Pak de image uit en importeer deze in WSL met het volgende commando:

```bash
cd %USERPROFILE%\Downloads
tar -xvzf mcp-workshop.tgz
mkdir %USERPROFILE%\wsl
mkdir %USERPROFILE%\wsl\mcp-workshop
cd %USERPROFILE%\wsl\mcp-workshop
wsl --import mcp-workshop . %USERPROFILE%\Downloads\mcp-workshop.tar
```

Herstart Windows Terminal en open een nieuwe shell in de mcp-workshop WSL image.

Clone de GitHub repository:

```bash
cd
git clone https://github.com/kpn-appfactory/MCP-workshop.git
cd ~/MCP-workshop
```

Open VS Code in de root van de MCP-workshop folder:

```bash
code .
```

Bekijk en lees de bestanden in de MCP-workshop folder.

Probeer te begrijpen wat er gebeurt in de verschillende bestanden en folders.

## Docker applicatie

TODO---- INTRO text waarom eerst docker dan kubernetes ------

Voordat jouw gebruiker (mcp-workshop) docker mag starten, moet deze gebruiker aan de groep docker worden toegevoegd.

```bash
sudo usermod -aG docker mcp-workshop
```

Start docker applicatie
```bash
docker run -d jvgemert/sleep

# Controleer of de docker container draait
watch docker ps
```

Na 30 seconden zal de container stoppen met werken en is het docker process niet meer aanwezig


## Deploy applicatie in Kubernetes (k3s)

```bash
cd ~/MCP-workshop/deploy/sleep_demo

# Maak een namespace aan
kubectl apply -f namespace.yaml

kubectl get namespace
```

Je ziet nu dat er een nieuwe namespace "sleepdemo" is aangemaakt

Nu gaan we de overige manifests uitrollen in deze namespace

```bash
cd ~/MCP-workshop/deploy/sleep_demo

kubectl apply -f .

kubectl get pod -n sleepdemo

kubectl get pods -n sleepdemo --watch
```

Docker start je container één keer en laat hem 30 seconden draaien. Daarna stopt hij.
Kubernetes daarentegen houdt je container in de gaten. Zodra hij stopt, start Kubernetes hem automatisch opnieuw op. Dit zorgt ervoor dat je applicatie altijd draait, zelfs als er iets misgaat.

Docker is vooral gericht op het creëren en beheren van individuele containers, terwijl Kubernetes bedoeld is om grote clusters van containers te orchestreren.
Kubernetes zorgt voor zelfherstel door containers automatisch te herstarten als ze crashen of stoppen.

## Deploy podinfo applicatie

```bash
kubectl apply -f deploy/variabele_demo/namespace.yaml

kubectl apply -f deploy/variabele_demo/

#_Nu in de browser naar https://vardemo.local
```

## Deploy vardemo applicatie

Haal het IP van je WSL op
```bash
ip a | grep eth0 | grep inet |awk '{print $2}' | cut -d/ -f1
```

Edit je windows hosts file C:\Windows\System32\drivers\etc\hosts (als admin) en voeg het volgende toe:

```bash
<WSL.IP>    podinfo.local vardemo.local
```

TODO - vardemo - /data persistent maken

TODO - http://vardemo.local/kill killed de draaiende container (niet te snel achter elkaar doen) beschrijven

TODO - Nieuw WSL image maken met user in docker group

TODO - Webapp pod acties
  Redeploy met nieuwe image
  Blue green deployment

TODO - http://vardemo.local/env beschrijven

TODO - Round robin ingress 

TODO - Ingress naar services op verschillende poorten deployments


