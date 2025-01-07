# MCP-workshop
MCP container and kubernetes workshop

## Introduction
Het doel van deze workshop is om een 

## Voorbereiding
Om deze workshop te kunnen draaien is er een omgeving nodig met daarop K3S en docker. Er zijn 2 opties om die te krijgen:
1. Download de kant en klare WSL image
2. Je beschikt al over een Ubuntu en maakt gebruik van het setup script


### Download en instaleer WSL image (optie 1)
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

### Configureer je bestaande Ubuntu in WSL (optie 2)
Zorg dat er een Ubuntu op je systeem staat waar we docker en k3s kunnen installeren. Dit is getest met Ubuntu 24.04 LTS

Open een Terminal naar je Ubuntu systeem en Clone de Github repository
```bash
cd
git clone https://github.com/kpn-appfactory/MCP-workshop.git
cd ~/MCP-workshop

# Setup de omgeving
./setup.sh
```


## Opdrachten
### Opdracht 1 (bekijk de bestanden)
Open VS Code in de root van de MCP-workshop folder:

```bash
cd ~/MCP-workshop
code .
```

Bekijk en lees de bestanden in de MCP-workshop folder.

Probeer te begrijpen wat er gebeurt in de verschillende bestanden en folders.

### Opdracht 2 (Docker applicatie)

Om begrip te kweken van de voordelen van Kubernetes in plaats van standaard Docker zullen we eerst een korte opdracht doen met Docker containers.

Start docker applicatie

```bash
docker run -p 8080:8080 -d --name vardemo jvgemert/vardemo:1.2

# Controleer of de docker container draait
watch docker ps
```

Er is nu een docker applicatie gestart die te bereiken is op http://localhost:8080 via een browser of curl.

```bash
curl http://localhost:8080
```

Simuleer een applicatie crash:

```bash
curl http://localhost:8080/kill
```

Je zal zien dat de applicatie na het boven staande commando crashed en niet meer terug komt, als je wil dat de applicatie draait zal je hem weer zelf moeten starten. (HINT - later zullen we hier de voordelen van Kubernetes deployment zien.)


#### Bonus

Bekijk de logs van de docker container

```bash
docker logs vardemo

# Stoppen van de docker container
docker stop vardemo

# Verwijderen van de docker container
docker rm vardemo
```


### Opdracht 3 (Deploy applicatie in Kubernetes - k3s)

We gaan nu dezelfde applicatie starten in Kubernetes. Dit gaan we doen door middel van een Pod om dit vergelijkbaar te maken met de Docker implementatie. Later gaan we gebruik maken van een Deployment om de voordelen van Kubernetes te laten zien.

```bash
cd ~/MCP-workshop/deploy/vardemo

# Maak een namespace aan (uitleg in de bonus)
kubectl apply -f namespace.yaml

# Start een pod (hierin leeft de container)
kubectl apply -f pod.yaml

# Bekijk de pod
kubectl get pod --namespace vardemo -o wide
```

**Voorbeeld**

```bash
kubectl get pod --namespace vardemo -o wide
NAME          READY   STATUS    RESTARTS   AGE     IP           NODE              NOMINATED NODE   READINESS GATES
vardemo-pod   1/1     Running   0          4m41s   10.42.0.10   desktop-oa8vr5k   <none>           <none>
```

Zoek in de output van het laatste commando het IP adress van de pod. Zoals in het voorbeeld `10.42.0.10`

Er is nu een applicatie gestart die te bereiken is op http://<JOUW-IP>:8080 via een browser of curl.

```bash
curl http://<JOUW-IP>:8080
```

Simuleer een applicatie crash:

```bash
curl http://<JOUW-IP>:8080/kill
```

#### Bonus

Bekijk de logging van de pod

```bash
kubectl logs --namespace vardemo vardemo-pod
```

Zoals je kan zien doen geven we bij het opvragen van de logs en pods steeds het argument mee `--namespace vardemo` mee. In Kubernetes zorgt een **namespace** voor het isoleren van groepen resources binnen een enkele cluster. Dit betekent dat je verschillende omgevingen of teams kunt scheiden, zodat ze niet met elkaars resources in de war raken. Elke resource binnen een namespace moet een unieke naam hebben, maar dezelfde naam kan in verschillende namespaces voorkomen.

Namespaces helpen ook bij het beheren van toegang en het toewijzen van hoeveel resources elk team mag gebruiken. Dit maakt het eenvoudiger om een Kubernetes-cluster georganiseerd en veilig te houden.

### Opdracht 4 ()



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


## Deploy vardemo applicatie

Haal het IP van je WSL op
```bash
ip a | grep eth0 | grep inet |awk '{print $2}' | cut -d/ -f1
```

Edit je windows hosts file C:\Windows\System32\drivers\etc\hosts (als admin) en voeg het volgende toe:

```bash
<WSL.IP>    podinfo.local vardemo.local
```

TODO - Ingress naar services op verschillende poorten deployments


## Deploy podinfo applicatie via Helmchart


```bash
kubectl apply -f deploy/variabele_demo/namespace.yaml

kubectl apply -f deploy/variabele_demo/

#_Nu in de browser naar https://vardemo.local
```






###### Grote lijnen ######
- Deployment uitleggen met replica's
- Uitleg deploy, service, ingress (text) simple deploy in bonus extra uitleg
- Deployment met persistent storage
- Bonus deplyment Evironment, inclusief pod op andere poort laten luisteren.
- Bonus Configmap
- Helm deployment podinfo inclusief upgrade (geen downtime) Beschrijven round robin loadbalancing ingress

