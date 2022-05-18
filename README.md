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
sudo nano /etc/suricata/suricata.yaml  -> Colocar la o nosso ficheiro do suricata.yaml que esta neste repositório
