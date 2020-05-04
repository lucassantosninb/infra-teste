# infra-teste

Aplicação simples feita em Flask e recursos de infraestrutura para log e monitoramento. 
<br>

- Todos os containers que necessitam de persistencia de dados, utilizam de alguma forma um volume (mount/bind).
- Criado um Loadbalancer através do Nginx para servir a aplicação.
- Aplicação replicada para 2 instâncias

<br>

Dois fatores me levaram a segregação em arquivos docker-composes:<br>

1. baixa performace do MySQL devido aos volumes <br>

2. configuração manual dos Inputs do Graylog

<br>

*PS.: Não foi implementado a coleta de logs da aplicação web através do Prometheus*

<br>
<br>

## Pré-requisitos:

- [docker](https://docs.docker.com/engine/install/) instalado.
- [docker-compose](https://docs.docker.com/compose/install/) instalado.

<br>

## Subir infraestrutura "base":

```
$ docker-compose -f docker-compose.base.yml up -d
```
Acompanhar os logs de inicialização até que o serviços mysql, mongo, graylog estejam disponíveis:
```
$ docker-compose -f docker-compose.base.yml logs -f
```
<br>

**Configurar Graylog:**

<br>

Acessar painel: http://localhost:9000

<br>

User: *admin* <br>

Password: *mygraylog*

<br>

Acessar System > Inputs <br>

Selecionar input: "GELF UDP" <br>

Clicar em "Launch new input" <br>

Selecionar o checkbox "Global" <br>

Adicionar Title: "Docker GELF" <br>

Clicar em "Save" <br>

<br>

Pronto, agora nossos hosts estão aptos a enviar logs para o Graylog.

<br>

Vamos adicionar um Dashboard para uma visualização.

<br>

Acessar "Dashboard" <br>

Clicar em "Create new dashboard" <br>

Clicar no simbolo de "+" no menú à esquerda. <br>

Clicar em "Message Table" <br>

Um novo painel surgirá. <br>

<br>

Clicar na seta para baixo "v" ao lado de "Query#1". <br>

Clicar em "Edite Title" <br>

Substituir o Title "Query#1" por "Last Logs" <br>

Clicar em "Save" <br>

<br>

Vamos salvar o Dashboard:

<br>

Clicar ao lado direito superior "Save as" <br>

Adicionar Title: "My Dashboard" <br>

Adicionar Summary: "Last Logs" <br>

Clicar em "Save"

<br>
<br>

## Subir as aplicações junto com o "coletor" de logs:

```
$ docker-compose -f docker-compose.web.yml up -d
```
Acompanhar os logs de inicialização até que o serviços balancer, app1, app2, e logspout estejam disponíveis:
```
$ docker-compose -f docker-compose.web.yml logs -f
```

<br>

A aplicação (bem modesta) foi criada em Python utilizando o Framework Flask e disponibilizada em 2 instâncias: app1 e app2. <br>

Existe um Load Balancer, um nginx, servindo as aplicações. <br>

A mesma está disponível através da url http://localhost <br>

<br>

*PS.: já é possível acessar o Graylog (http://localhost:9000/dashboards > "My Dashboard") e visualizar alguns dos logs.*

<br>
<br>

## Subir o monitoramento:

```
$ docker-compose -f docker-compose.metric.yml up -d
```
Acompanhar os logs de inicialização até que o serviços promethes, node-exporter, e grafana estejam disponíveis:
```
$ docker-compose -f docker-compose.metric.yml logs -f
```

<br>

Acesso Grafana: http://localhost:3000

<br>

User: *admin* <br>
Password: *mygrafana* <br>

<br>
<br>

Durante o startup foi adicionado um template para monitoraramento "1 Node Exporter for Prometheus Dashboard EN v20191102". <br>

É possível acessa-lo clicando em dashboard seguido de seu nome. <br>

Para uma melhor experiência, troque o tempo de exibição para "Last 15 min" no canto superior direito. <br>

<br>

Acesso Prometheus: http://localhost:9090

