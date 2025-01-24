- [MCP-workshop](#mcp-workshop)
  - [Introduction](#introduction)
  - [Voorbereiding](#voorbereiding)
    - [Download en instaleer WSL image (optie 1)](#download-en-instaleer-wsl-image-optie-1)
    - [Configureer je bestaande Ubuntu in WSL (optie 2)](#configureer-je-bestaande-ubuntu-in-wsl-optie-2)
  - [Opdrachten](#opdrachten)
    - [Opdracht 1 (bekijk kubernetes manifests)](#opdracht-1-bekijk-kubernetes-manifests)
    - [Opdracht 2 (Docker applicatie)](#opdracht-2-docker-applicatie)
      - [Bonus](#bonus)
    - [Opdracht 3 (Deploy applicatie in Kubernetes)](#opdracht-3-deploy-applicatie-in-kubernetes)
      - [Bonus](#bonus-1)
    - [Opdracht 4 (Create deployment)](#opdracht-4-create-deployment)
      - [Bonus 1 (Service)](#bonus-1-service)
      - [Bonus 2 (Ingress)](#bonus-2-ingress)
    - [Opdracht 5 (Create deployment met storage)](#opdracht-5-create-deployment-met-storage)
      - [Bonus](#bonus-2)
  - [Bonus opdrachten](#bonus-opdrachten)
    - [Opdracht 6](#opdracht-6)
    - [Opdracht 7](#opdracht-7)
    - [Opdracht 8](#opdracht-8)
  - [Bronnen](#bronnen)

# MCP-workshop

MCP container and kubernetes workshop

## Introduction

In deze workshop gaan we je leren hoe je applicaties kunt draaien in een Kubernetes cluster. We gebruiken hiervoor K3s, een lichtgewicht Kubernetes distributie. Daarnaast zullen we dieper ingaan op de relatie tussen Docker en Kubernetes, zodat je begrijpt hoe deze twee technologieën samenwerken om applicaties op schaal te beheren.

## Voorbereiding

Om deze workshop te kunnen draaien is er een omgeving nodig met daarop K3S en docker. Er zijn 2 opties om die te krijgen:
1. Download de kant en klare WSL image
2. Je beschikt al over een Ubuntu en maakt gebruik van het setup script

### Download en instaleer WSL image (optie 1)

We hebben voor deze workshop een kant en klare WSL image gemaakt die je kan gebruiken om de workshop te volgen.

Deze kan je hier downloaden: <https://mcpworkshop.blob.core.windows.net/mcp-workshop/mcp-workshop.tgz>
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

### Opdracht 1 (bekijk kubernetes manifests)

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

Er is nu een docker applicatie gestart die te bereiken is op <http://localhost:8080> via een browser of curl.

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

### Opdracht 3 (Deploy applicatie in Kubernetes)

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

Verwijderen pod dit kan je doen door het zelfde manifest te gebruiken:  
**Let op!** Als je onderstaande bonus opdracht wil doen moet je de pod nog niet verwijderen. Logging bekijken kan alleen als de pod nog bestaat.


```bash
cd ~/MCP-workshop/deploy/vardemo

# Verwijderen pod
kubectl delete -f pod.yaml
```

#### Bonus

Bekijk de logging van de pod

```bash
kubectl logs --namespace vardemo vardemo-pod
```

Verwijder de pod en bekijk de logs nogmaals, je zal zien dat de logs niet meer beschikbaar zijn.

Zoals je kan zien doen geven we bij het opvragen van de logs en pods steeds het argument mee `--namespace vardemo` mee. In Kubernetes zorgt een **namespace** voor het isoleren van groepen resources binnen een enkele cluster. Dit betekent dat je verschillende omgevingen of teams kunt scheiden, zodat ze niet met elkaars resources in de war raken. Elke resource binnen een namespace moet een unieke naam hebben, maar dezelfde naam kan in verschillende namespaces voorkomen.

Namespaces helpen ook bij het beheren van toegang en het toewijzen van hoeveel resources elk team mag gebruiken. Dit maakt het eenvoudiger om een Kubernetes-cluster georganiseerd en veilig te houden.

### Opdracht 4 (Create deployment)

In deze opdracht gaan we een deploment uitrollen. Een deployment wordt meestal gebruikt voor het configureren van de pods. Hierin is het onder andere mogelijk om aan te geven hoeveel replicas er van een pod moeten komen voor redudantie en het gebruik van eventuele storage (latere opdracht).

Tevens rollen we voor ontsluiting en security extra resources uit waar we hier niet verder op in gaan.

```bash
cd ~/MCP-workshop/deploy/vardemo

# Extra benodigde resources
kubectl apply -f ~/MCP-workshop/config/traefik-config.yml
kubectl apply -f service-account.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

# Deployment
kubectl apply -f deployment_no_storage.yaml

# Bekijk de pods
kubectl get pods -n vardemo -o wide

# Bekijk deployment
kubectl get deployment -n vardemo -o wide
```

Je zal nu zien dat er 2 pods zijn.

De applicatie is nu bereikbaar via een ingress (gaan we hier niet verder op in) welke de ontsluiting regelt via zijn eigen ip. Deze is met het volgende commando te vinden:

```bash
kubectl get ing --namespace vardemo vardemo
```

Het ip adress wat je hier ziet kan je nu gebruiken om verbinding met de applicatie te maken.

Om de applicatie te bereiken is er ook een DNS entry nodig, hiervoor dient de hostfile van je laptop aangepast te worden met de volgende entry.

```text
# Entry voor kubernetes ingress
<JOUW_IP>  vardemo.local podinfo.local
```

De applicatie is nu bereikbaar via <http://vardemo.local> vanuit je browser in Windows.

Backup om verbinding te krijgen via curl

```bash
curl http://<JOUW_IP> -H 'Host: vardemo.local'
```

#### Bonus 1 (Service)
Om pods te ontsluiten wordt er binnen Kubernetes gebruik gemaakt van services. Services hebben een eigen IP/poort en kijken op basis van labels welke pods ze beschikbaar moeten maken. De pods dienen dus als backend van de service. Bekijk hoe de service voor de vardemo applicatie er uit ziet en hoe die werkt.

```bash
kubectl get service --namespace vardemo vardemo -o yaml
```

De output ziet er ongeveer uit zoals hieronder:

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"vardemo","namespace":"vardemo"},"spec":{"ports":[{"name":"http","port":80,"protocol":"TCP","targetPort":"http"}],"selector":{"app":"vardemo"},"type":"ClusterIP"}}
  creationTimestamp: "2025-01-07T11:00:11Z"
  name: vardemo
  namespace: vardemo
  resourceVersion: "25009"
  uid: b66b5283-4819-4aad-bff9-2ab4db977b41
spec:
  clusterIP: 10.43.31.118
  clusterIPs:
  - 10.43.31.118
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: http
  selector:
    app: vardemo
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```

Onder `selector` staat `app: vardemo` wat overeen komt met de pods die door de service worden ontsloten. Kijk of je het label in de pod kan vinden.

```bash
# Bekijk welke pods er zijn
kubectl get pods --namespace vardemo

# Haal het manifest van 1 pod met de naam die hierboven gevonden is
kubectl get pods --namespace vardemo <JOUW-VARDEMO-POD> -o yaml

# Voorbeeld
kubectl get pods --namespace vardemo vardemo-5799b85598-9v4lx -o yaml
```

De output zie er ongeveer uit zoals hieronder:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2025-01-07T11:04:33Z"
  generateName: vardemo-5799b85598-
  labels:
    app: vardemo
    pod-template-hash: 5799b85598
  name: vardemo-5799b85598-9v4lx
  namespace: vardemo
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: vardemo-5799b85598
    uid: b499048d-864f-4c81-947f-04cb48275ef0
  resourceVersion: "25216"
  uid: efd30622-2aa5-4b28-b4ad-450801137cee
spec:
  containers:
  - image: jvgemert/vardemo:1.2
    imagePullPolicy: IfNotPresent
    name: vardemo
    ports:
    - containerPort: 8080
      name: http
      protocol: TCP
    resources:
      limits:
        cpu: 100m
        memory: 32Mi
      requests:
        cpu: 50m
        memory: 8Mi
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-5t78p
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: desktop-oa8vr5k
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: vardemo
  serviceAccountName: vardemo
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: kube-api-access-5t78p
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
```

#### Bonus 2 (Ingress)

Ingresses zijn een mogelijkheid om services van applicatie te ontsluiten naar de buitenwereld.


Ingresses hebben (min of meer) een eigen IP/poort en kijken op basis van labels welke services ze beschikbaar moeten maken. De services dienen dus als backend van de ingess. De complete flow is dus:
Ingress -> Service -> Pod(s)

Bekijk hoe de ingress voor de vardemo applicatie er uit ziet en hoe die werkt.

```bash
kubectl get ingress --namespace vardemo vardemo -o yaml
```

De output hiervan zal vergelijkbaar zijn met wat hieronder staat:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web, websecure
  name: vardemo
  namespace: vardemo
spec:
  ingressClassName: traefik
  rules:
  - host: vardemo.local
    http:
      paths:
      - backend:
          service:
            name: vardemo
            port:
              number: 80
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - vardemo.local
```

In het bovenstaande manifest verwijst het `-backend:` gedeelte naar de achterliggende service. De naam van de service dient dus overeen te komen met vardemo applicatie service naam.

### Opdracht 5 (Create deployment met storage)

De storage die standaard in een pod aanwezig is, is niet permanent. Dit betekend dus dat wanneer een pod wordt gestopt eventuele data verloren gaat. Om dit op te lossen kan er gebruik gemaakt worden van persitent storage welke eventueel deelbaar is tussen pods.

Met een browser of curl kan de applicatie opgevraagd worden. In de output van de applicatie staat een regel met `Requests received`, deze geeft weer hoe vaak de applicatie is benaderd. Zonder de persistent storage zou de telling na iedere herstart weer opnieuw beginnen.

Benader de applicatie zoals beschreven bij vorige opdracht en noteer het aantal `Requests received`

```bash
# Verwijder de pods
kubectl delete pods --force --namespace vardemo -l app=vardemo

# Bekijk de status
kubectl get pods --namespace vardemo -l app=vardemo --watch
```

Het laatste commando met `--watch` kan worden afgebroken met CTRL+C

Benader de applicatie weer en zie dat de telling opnieuw is begonnen.

Met de volgende commandos wordt de applicatie aangepast zodat deze gebruik maakt van persistent storage

```bash
cd ~/MCP-workshop/deploy/vardemo

# Aanmaken persistent storage
kubectl apply -f pvc.yaml

# Deployment met persistent storage
kubectl apply -f deployment_storage.yaml
```

Bekijk het aantal `Requests received` nogmaals en noteer deze.

Herstart de applicatie nogmaals zoals hierboven beschreven en zie dat de telling nu wel door loopt.

#### Bonus

Bekijk de pvc (persistentvolumeclaim). Een pvc creeert een pv (persitentvolume).

```bash
# Bekijk de pvc
kubectl get pvc --namespace vardemo vardemo-pvc -o yaml

# Bekijk de pv
kubectl get pv
```

Vergelijk `deployment_no_storage.yaml` met `deployment_storage.yaml` in VS-code en zoek de verschillen.

n.b. Een pv is niet namespaced

## Bonus opdrachten

### Opdracht 6

Deployment zijn gebaseerd op een (generiek) image. Kleine aanpassingen kunnen gewijzigd worden door het meegeven van environment variables. De environment variables moeten dan in de deployment mee gegeven worden.

Simpele variablen kunnen mee gegeven worden in de deployment. Voor meer complexe of uitgebreide variablen kan hiervoor ook een configmap gebruikt worden (volgende oefening).

De vardemo applicatie luistert bijvoorbeeld standaard op poort 8080, ter demonstratie kan deze op andere poorten luisteren door het meegeven van een environment variable `PORT`.

```yaml
env:
- name: PORT
    value: "8081"
- name: CM_VAR_deploy
    value: "deployment.yaml"
```

Het bovenstaande is de toevoeging die gedaan aan de deployment. Dit heeft tot gevolg dat de applicatie ook gaat luisteren op een andere poort (namelijk 8081). In de deployment zal kubernetes dus ook moeten weten dat dit het geval is. Bekijk wat er nog meer in de yaml is aangepast.

Onderstaande zorgt er voor dat kubernetes ook weet op welke poort de applicatie luistert.

```yaml
ports:
- name: http
    containerPort: 8081
    protocol: TCP
```

Deploy de applicatie:

```bash
cd ~/MCP-workshop/deploy/vardemo

# Deploy
kubectl apply -f deployment_env.yaml
```

Benader de applicatie en bekijk `Container port:`

Probeer nu zelf de deployment aan te passen zodat de applicatie luistert op een andere poort zoals `9090`.

### Opdracht 7 

Naast variablen direct in de deployment te zetten zullen we in deze opdracht ook gebruik maken van een configmap.

Bekijk de configmap `configmap.yaml`
Bekijk de deployment `deployment_env_cm.yaml`

Zie dat het volgende is toegevoegd:

```yaml
envFrom:
- configMapRef:
    name: vardemo-config
```

Deploy nu de configmap en de nieuwe deployment:

```bash
cd ~/MCP-workshop/deploy/vardemo

# Maak configmap
kubectl apply -f configmap.yaml

# Maak nieuwe deployment
kubectl apply -f deployment_env_cm.yaml
```

Controleer of de configmap er is en de pod opnieuw is opgestart:

```bash
kubectl get configmap --namespace vardemo

kubectl get pods --namespace vardemo
```

Aan de `AGE` kan je zien hoe oud een resource is en dat de pod opnieuw is gestart.

Benader de applicatie en bekijk welke variables deze heeft. Standaard worden onder aan de output van de applicatie alle variablen weergegeven die beginnen met `CM_VAR_`. Vergelijk de variabelen in de configmap en de output van de applicatie.

Als je alle environment variablen wil zien kan die door `/env` toe te voegen aan het path.

```bash
curl http://172.30.65.10/env -H 'Host: vardemo.local'
```

Probeer nu zelf variablen toe te voegen via de configmap. In principe wordt een configmap regelmatig ingelezen, het is echter afhankelijk van de applicatie of dit wordt opgepakt.

De vardemo applicatie doet dit niet dus zal die herstart moeten worden voor je aanpassing zichtbaar is.

### Opdracht 8

We hebben nu een applicatie geinstalleerd met daarbij diverse resources die nodig zijn. Om het installeren van applicaties met al hun afhankelijkheden makkelijker te maken wordt er vaak ook gebruik gemaakt van Helm. De applicatie-ontwikkelaar levert dan een helm-chart die gebruikt kan worden om de applicatie inclusief alle bijbehoren de resources te instaleren.

In deze opdracht gaan we een helm chart installeren en upgraden.

TODO: Ondanks een copy van k3s.yaml naar ~/.kube/config werkt het niet. Als workaround even een symbolic link maken. Dit oplossen in de image.

```bash
ln -fs /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

Voeg de helm repo toe:

```bash
# Add podinfo helm repo
helm repo add podinfo https://stefanprodan.github.io/podinfo
```

Beschikbare versies van de applicatie:

```bash
# Bekijk de laatst beschikbare versie
helm search repo podinfo/podinfo

# Bekijk alle beschikbare versies
helm search repo podinfo/podinfo --versions
```

Installeer de applicatie met een specifieke versie, je kan de versie ook weglaten dan wordt de laatste versie geinstalleerd. Voor nu installeren we versie 6.7.0 om straks te kunnen upgraden.
Tijdens de installatie krijg je de melding om een port-forward te doen, negeer deze melding we gaan de applicatie nu nog niet benaderen.

```bash
# Installeer de applicatie met een specifieke versie
helm install podinfo podinfo/podinfo \
--create-namespace \
--namespace=podinfo \
--version 6.7.0
```

Helm heeft nu de podinfo applicatie geinstalleerd in de namespace `podinfo`, controleer of er een pod draait.

```bash
kubectl get pods --namespace podinfo
```

Ter info:
Een helm chart kun je ook met default waardes installeren, sla dit voor nu echter over.

```bash
# Ter info, sla deze stap over
# helm install podinfo podinfo/podinfo
```

Bekijk de installatie status van de geinstalleerde helm charts.

```bash
# Bekijk de installatie status van de helm charts
helm list
# of
helm list --all-namespaces
# of
helm list -n podinfo
```

Ter info:
Upgrade de applicatie met default waardes, sla deze stap over.

```bash
# Ter info, sla deze stap over
# helm upgrade -i podinfo podinfo/podinfo
```

Upgrade de applicatie met extra parameters. De parameters zoals hieronder zijn nodig om de applicatie te laten werken in de huidige omgeving. De beschikbare values zijn ook te vinden in de chart zelf.

Voorbeeld:
<https://github.com/stefanprodan/podinfo/tree/master/charts/podinfo>

Applicaties geinstalleerd met Helm kunnen worden geupgrade / aangepast zonder de applicatie opnieuw te installeren.

```bash
# Upgrade de applicatie met parameters
helm upgrade --install --wait podinfo \
--namespace podinfo \
--set replicaCount=2 \
--version 6.7.0 \
podinfo/podinfo
```

In bovenstaande actie wordt onder andere de `replicaCount` opgehoogd van 1 naar 2 bekijk welk effect dit heeft op de pods.

Bekijk de gebruikte values van de applicatie.

```bash
# Bekijk de gebruikte values
helm get values podinfo --namespace podinfo
```

Exporteer de values naar een file.

```bash
# Dump de values naar een file
helm get values podinfo --namespace podinfo > podinfo_values.yaml
```

Bekijk alle values, deze zijn ook te vinden in de chart zelf.
Voorbeeld:
<https://github.com/stefanprodan/podinfo/tree/master/charts/podinfo>

```bash
# Bekijk alle values
helm get values podinfo --namespace podinfo --all
```

Verwijder de applicatie, we gaan deze nu opnieuw installeren met een aangepaste values file.

```bash
# Verwijder de applicatie
helm delete podinfo --namespace podinfo
```

Voor het ontsluiten van de applicatie hebben we een ingress nodig. Om deze te configureren geven we de settings mee via een values file, op commandline zou dit te complex worden.

Pas de `podinfo_values.yaml` aan naar onderstaande voorbeeld:

```yaml
USER-SUPPLIED VALUES:
image:
  tag: 6.7.0
ingress:
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web, websecure
  enabled: true
  hosts:
    - host: "podinfo.local"
      paths:
        - path: /
          pathType: ImplementationSpecific
replicaCount: 2
```

Installeer de applicatie nu met deze values file:

```bash
helm upgrade --install podinfo --namespace podinfo podinfo/podinfo -f podinfo_values.yaml ; watch -n 1 kubectl get pods --namespace podinfo
```

Bekijk de ingress met het volgende commando:

```bash
# Bekijk ingresses
kubectl get ingress --namespace podinfo

# Bekijk het ingress manifest
kubectl get ingress --namespace podinfo podinfo -o yaml
```

Door het aanmaken van de ingress is de applicatie nu te bereiken op <http://podinfo.local>  
Er is nu een applicatie gestart die te bereiken is op https://<JOUW-IP> via een browser of curl.

```bash
curl https://<JOUW-IP> -H 'Host: podinfo.local'
curl http://<JOUW-IP> -H 'Host: podinfo.local'
```

Upgrade de applicatie naar versie 6.7.1, aangezien de applicatie geen downtime heeft zal je alleen verschil zien in de versies. Het is handig om dit tijdens de upgrade te monitoren in je browser.

Pas hiervoor de values file aan naar de juiste versie, en upgrade de applicatie via het `helm upgrade` comando.

Zoals je ziet is het installeren van een helm chart via een values files een stuk eenvoudiger dan alles via `--set` mee te geven. Deze values file kan ook gebruikt worden om de applicatie te upgraden. Ook is deze values file in versiebeheer te zetten zodat je altijd weet welke configuratie er is gebruikt.

Het is ook mogelijk om de values file te combineren met settings op de commandline. Wanneer je snel een aanpassing wil doen of wil testen.

```bash
helm upgrade --install podinfo \
--namespace podinfo podinfo/podinfo \
--set replicaCount=3 \
-f podinfo_values.yaml
```

Hiermee ben je aan het einde gekomen van deze workshop, veel plezier met Kubernetes en Happy Helming!

## Bronnen

<https://kubernetes.io>  
<https://helm.sh>  
<https://github.com/stefanprodan/podinfo>  
<https://github.com/stefanprodan/podinfo/tree/master/charts/podinfo>  
<https://k3s.io/>  
