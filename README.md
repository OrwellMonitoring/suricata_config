# suricata_config
Suricata is a Network Security Monitoring (NSM) tool that uses sets of community created and user defined signatures (also referred to as rules) to examine and process network traffic. Suricata can generate log events, trigger alerts, and drop traffic when it detects suspicious packets or requests to any number of different services running on a server.  
Este repositório tem como objetivo ter todos os fichieros necessários para criar de formar simples e rápida um serviço suricata em modo IPS, Intrusion Prevention System , a correr num kibana, utilizando elastic Search.  
De salientar que todas as regras que estão a ser utilizadas no suricata são simples e baśicas sendo da responsabilidade da testebed definir quais são as regras que devem estar presentes.  
O suricata deve ter acesso a todos os pacotes da rede para eles o detetetar e dar as suas alarmisticas sendo que estes alarmes vão estar a ser enviadas para um slack, com todas as logs sendo que este slack deve também ser alterado os tokens de acesso ao slack para funcionar.  

## Como instalar o Suricata 
**sudo add-apt-repository ppa:oisf/suricata-stable**   
**sudo apt install suricata**
**sudo systemctl enable suricata.service**  
Output a receber:  
"suricata.service is not a native service, redirecting to systemd-sysv-install.  
Executing: /lib/systemd/systemd-sysv-install enable suricata"  
**sudo systemctl stop suricata.service**  -> Se tudo estiver certo, deve-se parar de correr porque ainda não há nada no suricata de regras  


## Configurar o yaml do suricata 
**sudo nano /etc/suricata/suricata.yaml**  -> Colocar la o nosso ficheiro do suricata.yaml que esta neste repositório  
Caso se pretenda configurar uma nova interface basta, no ficheiro yaml nas linhas do **af-packet**: colocar a interface que se pretende e também colocar um valor para o cluster id, salientar que este valor não pode estar a ser utilizado nas outras interfaces.   

## Regras do Suricata 
Para importar regras basicas no suricata, basta ir buscar regras por default com o comando: **sudo suricata-update**     
Nota, as regras do surica-update vão para o ficheiro : **/var/lib/suricata/rules/suricata.rules**  
Podem também serem criadas regras, e essas podem ser colocadas no **/var/lib/suricata/rules/local.rules** que já se encontra configurado no ficheiro yaml do suricata para aceitar as regras presentes neste ficheiro.  

## Testar se as regras estão a dar corretamente 
**sudo suricata -T -c /etc/suricata/suricata.yaml -v**
## Comandos a instalar 
**sudo apt update**  
**sudo apt install jq**

## Começar a correr o suricata 
**sudo systemctl start suricata.service**
**sudo systemctl status suricata.service**
Notas:  
Esperar 1 a 2 minutos, suricata demora a correr  
**sudo tail -f /var/log/suricata/suricata.log**  e receber o output : data-- horas - <Info> - All AFP capture threads are running.  
## Colocar o Suricata em IPS 
Deve se ir a  /etc/default/suricata e alterar a linha:    
**LISTENMODE=af-packet** para **LISTENMODE=nfqueue**
## Como saber em que modo esta o suricata 
**sudo systemctl status suricata.service**  
Nas linhas do fundo deve estar a indicar:Starting suricata in **IPS** (nfqueue) mode... done.

## Logs do Suricata 
**cat  /var/log/suricata/fast.log** ou  **cat  /var/log/suricata/eve.json**  
As logs aqui presentes estão a ser enviadas para um slack.   

### Pesquisar por logs especificas 
Fazendo o sid da regra pode-se fazer grep de todas as ocorrencias da regra.  
**grep <sid_number> /var/log/suricata/fast.log**

### Logs em Json 

**sudo apt install jq**
**cat /var/log/suricata/eve.log**
**jq 'select(.alert .signature_id==<sid_number>)' /var/log/suricata/eve.json**

## Configurar a UFW para enviar trafego para o Suricata 
A definir pelo sistema no nosso sistema atual estamos a usar os ficheiros presentes no repositório sendo eles before.rules e before6.rules.    
Sitio onde colocar o before. rules, **/etc/ufw/before.rules**  
Sitio onde colocar o before6. rules,**/etc/ufw/before6.rules**  
**sudo ufw enable**  
Neste ficheiro colocamos, as configurações que para nós serviam, para uma outra rede pode ser necessário a alteração deste ficheiro.  

## Como instalar o kibana e elasticSearch ##
**curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -**  
**echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list**  
**sudo apt update**  
**sudo apt install elasticsearch kibana** 

## Configurar o elasticSearch 
Pode importar o ficheiro  elasticsearch.yml presente no nosso repositório e colocar em  **/etc/elasticsearch/elasticsearch.yml** onde deve apenas alterar o campo onde diz "your_private_ip".  
Onde encontrar o your_private ip:  
# By default Elasticsearch is only accessible on localhost. Set a different  
# address here to expose this node on the network:  
#network.host: 192.168.0.1  
network.bind_host: ["127.0.0.1", "your_private_ip"]  
# By default Elasticsearch listens for HTTP traffic on the first free port it  
# finds starting at 9200. Set a specific HTTP port here:  

## Como correr o elasticSearch 
Para as interfaces que pretende monitorizar colocar no comando abaixo
**sudo ufw allow in on eth<number>**
**sudo ufw allow out on eth<number>**

**sudo systemctl start elasticsearch.service**  
**sudo systemctl enable elasticsearch.service**  
## Como reduzir o espaço que o elasticSearch ocupa 
**sudo  vim /etc/elasticsearch/jvm.options**
Dentro do ficheiro colocar:  
# JVM Heap Size - see /etc/elasticsearch/jvm.options 
-Xms2g   
-Xmx2g   
E assim fica com 2g para o elasticSearch,se pretender 1Gb, basta meter   
-Xms1g 
-Xmx1g 
## Passwords geradas de forma automática 
Correr os seguintes comandos: (NOTA ESTES COMANDOS SÓ PODEM SER CORRIDOS 1 VEZ LOGO DEVEM SER GUARDADOS NUM LOCAL SEGUROS AS PASSWORDS)  
**cd /usr/share/elasticsearch/bin**  
**sudo ./elasticsearch-setup-passwords auto**  
## Configurar o Kibana 
Correr os seguintes comandos: (NOTA ESTES COMANDOS SÓ PODEM SER CORRIDOS 1 VEZ LOGO DEVEM SER GUARDADOS NUM LOCAL SEGUROS AS PASSWORDS)    
**cd /usr/share/kibana/bin/**
**sudo ./kibana-encryption-keys generate -q**

Pode importar o nosso ficheiro de configuração do kibana.yml e altera-lo em **sudo vim /etc/kibana/kibana.yml** , sendo apenas necessário depois colocar passwords geradas substituir nos campos <key > pela respetiva key gerada anteriormente e trocar o "your ip" dentro do ficheiro yaml.  

**cd /usr/share/kibana/bin **  
**sudo ./kibana-keystore add elasticsearch.username** -> colocar: kibana_system  
**sudo ./kibana-keystore add elasticsearch.password** -> Password do kibana_system gerado em (sudo ./elasticsearch-setup-passwords auto)  
**sudo systemctl start kibana.service**
**sudo systemctl enable kibana.service**
	

## Configurar o filebeat 
**curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -**  
**echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list**  
**sudo apt update**  
**sudo apt install filebeat**  
**sudo nano /etc/filebeat/filebeat.yml** e colocar :  
# Starting with Beats version 6.0.0, the dashboards are loaded via the Kibana API.  
# This requires a Kibana endpoint configuration.<h3> Pesquisar por logs especificas  
setup.kibana:  
	**host: "your_private_ip:5601" **  
output.elasticsearch:  
	# Array of hosts to connect to.  
	**hosts: ["your_private_ip:9200"]**
# Protocol - either `http` (default) or `https`.  
#protocol: "https"  
# Authentication credentials - either API key or username/password.  
#api_key: "id:api_key"  
username: "elastic"  
password: "pass do elastic gerado em  (sudo ./elasticsearch-setup-passwords auto)"  

## Colocar o suricata no filebeat 
**sudo filebeat modules enable suricata**  , output esperado : (Enabled suricata)  
**sudo filebeat setup** : Output esperado :  
Overwriting ILM policy is disabled. Set `setup.ilm.overwrite: true` for enabling.  
Index setup finished.  
Loading dashboards (Kibana must be running and reachable)  
Loaded dashboards  
Setting up ML using setup --machine-learning is going to be removed in 8.0.0. Please use the ML app instead.  
See more: https://www.elastic.co/guide/en/machine-learning/current/index.html  
It is not possible to load ML jobs into an Elasticsearch 8.0.0 or newer using the Beat.  
Loaded machine learning job configurations  
Loaded Ingest pipelines  

Após isto executar  
**sudo systemctl start filebeat.service**  
**sudo systemctl enable filebeat.service**  
	
## Dashboard para ver os dados 
http://your_ip:5601/ 
Colocar o user e a password do elastic que foi gerado anteriormente  

type:dashboard suricata  Alerts  
type:dashboard suricata  Events  
	
