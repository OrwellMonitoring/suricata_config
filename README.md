# suricata_config
Este repositório tem como objetivo ter todos os fichieros necessários para criar de formar simples e rápida um serviço suricata em modo IPS a correr num kibana, utilizando elastic Search.
De salientar que todas as regras que estão a ser utilizadas no suricata são simples e baśicas sendo da responsabilidade da testebed definir quais são as regras que devem estar presentes.
O suricata deve ter acesso a todos os pacotes da rede para eles o detetetar e dar as suas alarmisticas sendo que estes alarmes vão estar a ser enviadas para um slack, com todas as logs sendo que este slack deve também ser alterado os tokens de acesso ao slack para funcionar.
