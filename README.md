# suricata_config
Suricata is a Network Security Monitoring (NSM) tool that uses sets of community created and user defined signatures (also referred to as rules) to examine and process network traffic. Suricata can generate log events, trigger alerts, and drop traffic when it detects suspicious packets or requests to any number of different services running on a server.<br>
Este repositório tem como objetivo ter todos os fichieros necessários para criar de formar simples e rápida um serviço suricata em modo IPS, Intrusion Prevention System , a correr num kibana, utilizando elastic Search.<br>
De salientar que todas as regras que estão a ser utilizadas no suricata são simples e baśicas sendo da responsabilidade da testebed definir quais são as regras que devem estar presentes.<br>
O suricata deve ter acesso a todos os pacotes da rede para eles o detetetar e dar as suas alarmisticas sendo que estes alarmes vão estar a ser enviadas para um slack, com todas as logs sendo que este slack deve também ser alterado os tokens de acesso ao slack para funcionar.<br
>

<h2> Como instalar o Suricata </h2>
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt install suricata
sudo systemctl enable suricata.service : <br>
Output a receber:  "suricata.service is not a native service, redirecting to systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable suricata" <br>
sudo systemctl stop suricata.service  -> Se tudo estiver certo, deve-se parar de correr porque ainda não há nada no suricata de regras

<h2> Configurar o yaml do suricata </h2>
sudo nano /etc/suricata/suricata.yaml  -> Colocar la o nosso ficheiro do suricata.yaml que esta neste repositório <br>
Caso se pretenda configurar uma nova interface basta, no ficheiro yaml nas linhas do af-packet: colocar a interface que se pretende e também colocar um valor para o cluster id, salientar que este valor não pode estar a ser utilizado nas outras interfaces.<br>

<h2> Regras do Suricata </h2>
Para importar regras basicas no suricata, basta ir buscar regras por default com o comando: sudo suricata-update<br>
Nota, as regras do surica-update vão para o ficheiro : /var/lib/suricata/rules/suricata.rules <br>

<h2> Testar se as regras estão a dar corretamente </h2>
	sudo suricata -T -c /etc/suricata/suricata.yaml -v
<h2 > Comandos a instalar </h2>
sudo apt update
sudo apt install jq

<h2> Começar a correr o suricata </h2>
	sudo systemctl start suricata.service
	sudo systemctl status suricata.service
  Esperar 1 a 2 minutos, suricata demora a correr :
    sudo tail -f /var/log/suricata/suricata.log  e receber o output : data-- horas - <Info> - All AFP capture threads are running.
	<h2> Colocar o Suricata em IPS </h2>
	Deve se ir a  /etc/default/suricata e alterar a linha: LISTENMODE=af-packet para 
	LISTENMODE=nfqueue
	<h2> Como saber em que modo esta o suricata </h2>
	sudo systemctl status suricata.service -> Nas linhas do fundo deve estar a indicar:Starting suricata in IPS (nfqueue) mode... done.

  <h2> Logs do Suricata </h2>
cat  /var/log/suricata/fast.log -> As logs do suricata estão neste ficheiro, mas as logs deste ficheiro vão passar para o slack <br>
<h3> Pesquisar por logs especificas </h3>
Fazendo o sid da regra pode-se fazer grep de todas as ocorrencias da regra
grep <sid_number> /var/log/suricata/fast.log

<h3>Logs em Json </h3>

sudo apt install jq
cat /var/log/suricata/eve.log
jq 'select(.alert .signature_id==<sid_number>)' /var/log/suricata/eve.json

<h2> Configurar a UFW para enviar trafego para o Suricata </h2>
/etc/ufw/before.rules
/etc/ufw/before6.rules
Correr os comandos:
	sudo iptables -I FORWARD -j NFQUEUE
	sudo iptables -I INPUT -j NFQUEUE
	sudo iptables -I OUTPUT -j NFQUEUE
	sudo iptables -I INPUT -p tcp  -j NFQUEUE
	sudo iptables -I OUTPUT -p tcp -j NFQUEUE
	sudo iptables -I FORWARD -i eth0 -o eth1 -j NFQUEUE

	sudo iptables -I FORWARD -i eth1 -o eth0 -j NFQUEUE
	 sudo ufw enable

Neste ficheiro colocamos, as configurações que para nós serviam, para uma outra rede pode ser necessário a alteração deste ficheiro.

<h2> Como instalar o kibana e elasticSearch </h2>
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list<br>
sudo apt update<br>
sudo apt install elasticsearch kibana<br>

<h2> Configurar o elasticSearch </h2>
/etc/elasticsearch/elasticsearch.yml -> e no onde esta "your private ip" trocar pelo ip da maquina, mas primeiro trocar pelo nosso ficheiro do elasticsearch <br>
# By default Elasticsearch is only accessible on localhost. Set a different<br>
# address here to expose this node on the network:<br>
#<br>
#network.host: 192.168.0.1<br>
network.bind_host: ["127.0.0.1", "your_private_ip"] <br>
#<br>
# By default Elasticsearch listens for HTTP traffic on the first free port it<br>
# finds starting at 9200. Set a specific HTTP port here:<br>

<h2> Como correr o elasticSearch </h2>
sudo ufw allow in on eth<number><br>
sudo ufw allow out on eth<number><br>

sudo systemctl start elasticsearch.service

<h2> Como reduzir o espaço que o elasticSearch ocupa </h2>
sudo  vim /etc/elasticsearch/jvm.options
Dentro do ficheiro colocar:
# JVM Heap Size - see /etc/elasticsearch/jvm.options <br>
-Xms2g <br>
-Xmx2g <br>
E assim fica com 2g para o elasticSearch,se pretender 1Gb, basta meter 
-Xms1g <br>
-Xmx1g <br>
<h2> Passwords geradas de forma automática </h2>
Correr os seguintes comandos: (NOTA ESTES COMANDOS SÓ PODEM SER CORRIDOS 1 VEZ LOGO DEVEM SER GUARDADOS NUM LOCAL SEGUROS AS PASSWORDS)
cd /usr/share/elasticsearch/bin
sudo ./elasticsearch-setup-passwords auto

<h2 > Configurar o Kibana </h2>
cd /usr/share/kibana/bin/
sudo ./kibana-encryption-keys generate -q

sudo vim /etc/kibana/kibana.yml
E com estas passwords geradas, substituir nos campos <key > pela respetiva key, gerada anteriormente e trocar o "your ip" dentro do ficheiro yaml

cd /usr/share/kibana/bin 
sudo ./kibana-keystore add elasticsearch.username -> kibana_system
sudo ./kibana-keystore add elasticsearch.password -> Password do kibana_system gerado em (sudo ./elasticsearch-setup-passwords auto)
sudo systemctl start kibana.service

<h2> Configurar o filebeat </h2>
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install filebeat
sudo nano /etc/filebeat/filebeat.yml e colocar :
# Starting with Beats version 6.0.0, the dashboards are loaded via the Kibana API.
# This requires a Kibana endpoint configuration.<h3> Pesquisar por logs especificas </h3>
setup.kibana:
	host: "your_private_ip:5601" 
output.elasticsearch:
	# Array of hosts to connect to.
	hosts: ["your_private_ip:9200"]
# Protocol - either `http` (default) or `https`.
#protocol: "https"
# Authentication credentials - either API key or username/password.
#api_key: "id:api_key"
username: "elastic"
password: "pass do elastic gerado em  (sudo ./elasticsearch-setup-passwords auto)"
<h2> Colocar o suricata no filebeat </h2>
sudo filebeat modules enable suricata : Output esperado (Enabled suricata) <br>
sudo filebeat setup : Output esperado <br>
Overwriting ILM policy is disabled. Set `setup.ilm.overwrite: true` for enabling.
Index setup finished.
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
Setting up ML using setup --machine-learning is going to be removed in 8.0.0. Please use the ML app instead.
See more: https://www.elastic.co/guide/en/machine-learning/current/index.html
It is not possible to load ML jobs into an Elasticsearch 8.0.0 or newer using the Beat.
Loaded machine learning job configurations
Loaded Ingest pipelines<br>
sudo systemctl start filebeat.service
<h2> Dashboard para ver os dados </h2>
http://your_ip:5601/ 
Colocar o user e a password do elastic que foi gerado anteriormente

type:dashboard suricata  Alerts
type:dashboard suricata  Events
