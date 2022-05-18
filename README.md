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
Como ponto inicial pode-se também utilizar as regras que temos no ficheiro : suricata.rules, voltar a salientar que é tudo regras básicas e onde não entra qualquer tipo de drop, ou seja, temos apenas alertar.<br>
Nota, as regras do surica-update vão para o ficheiro : /var/lib/suricata/rules/suricata.rules <br>

<h2> Testar se as regras estão a dar corretamente </h2>
	sudo suricata -T -c /etc/suricata/suricata.yaml -v

<h2> Começar a correr o suricata </h2>
	sudo systemctl start suricata.service
	sudo systemctl status suricata.service
  Esperar 1 a 2 minutos, suricata demora a correr :
    sudo tail -f /var/log/suricata/suricata.log  e receber o output : data-- horas - <Info> - All AFP capture threads are running.
  
  <h2> Logs do Suricata </h2>
cat  /var/log/suricata/fast.log -> As logs do suricata estão neste ficheiro, mas as logs deste ficheiro vão passar para o slack
  <h3> Pesquisar por logs especificas </h3>
  Fazendo o sid da regra pode-se fazer grep de todas as ocorrencias da regra
   grep <sid_number> /var/log/suricata/fast.log

	<h3>Logs em Json </h3>
	
	sudo apt install jq
	cat /var/log/suricata/eve.log
	jq 'select(.alert .signature_id==<sid_number>)' /var/log/suricata/eve.json
