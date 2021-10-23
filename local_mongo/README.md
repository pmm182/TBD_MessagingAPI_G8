## Cria um cluster do mongo com sharding e réplica

Esta configuração visa criar um cluster de mongo com  sharding e réplica. 

Ela foi adaptada de https://github.com/justmeandopensource/learn-mongodb

### Execução

Execute o comando abaixo para iniciar o cluster:

```
./start.sh
```

Execute o comando abaixo para finalizar o cluster:

```
./stop.sh
```

Caso queira excluir os volumes criados, execute:

```
./stop.sh "-v"
```