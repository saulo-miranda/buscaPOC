
# BuscaTCC-PT-BR

Sistema desenvolvido em meu projeto orientado em computação na UFV.


## Instalação

Para facilitar a instalação e portabilidade do projeto utilizei o Docker para lidar com as dependências do sistema, para executar basta acessar a pasta raiz do projeto e executar:

```bash
  docker-compose up
```
    
## Stack utilizada

**Front-end:** Bootstrap

**Back-end:** Django + PostgreSQL


## FAQ

#### Qualquer erro inicial na primeira execução do projeto

```bash
  python manage.py migrate
```
para migrar o sistema para o seu banco de dados local


