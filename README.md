# Projeto Prático Tópicos em banco de dados
### Aplicação de Mensageria - Grupo 8

O projeto consiste em desenvolver uma aplicação que utiliza banco de dados NoSQL, cuja funcionalidade principal consiste na troca de mensagens entre usuários. A partir dessa aplicação gostaríamos de verificar como o comportamento do sistema varia conforme as configurações do banco de dados são modificadas.

## Pré-requisitos
Para instalar e utilizar este software, são pré-requisitos:
* Computador com Linux instalado (preferencialmente Ubuntu).
* Python >=3.6.

Pequenas variações a este pré-requisitos podem ser adotadas desde que haja conhecimento mais abrangente da solução e tecnologias aqui utilizadas.

## Instalação
Embora o MongoDB seja um aplicativo bem conhecido, ele não está nos repositórios oficiais do Ubuntu. Portanto, você terá que adicioná-lo manualmente.No entanto, essa é uma grande vantagem porque facilita a instalação e a atualização do aplicativo. Se você estiver usando o Ubuntu 18.04, abra o terminal e adicione a chave PGP do repositório do MongoDB para não comprometer os pacotes baixados:

```console
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```

Depois disso, você pode adicionar o repositório do MongoDB sem qualquer problema. Para fazer isso, execute este comando:

```console
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```

Agora, atualize o comando APT para sincronizar todos os repositórios.

```console
sudo apt update
```

Em seguida, instale o MongoDB usando o APT:

```console
sudo apt-get install -y mongodb
sudo apt install mongodb-org
```

No final da instalação, habilite e inicie o serviço do MongoDB. Com isso, você poderá iniciar usando isso.

```console
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

## Utilização

## Colaboradores

Eduardo Garcia do Nascimento
github.com/egnascimento


Patricia Megumi Matsumoto
github.com/pmm182



