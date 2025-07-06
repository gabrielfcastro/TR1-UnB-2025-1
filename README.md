# Teleinformática de Redes 1 - 2025/1 

Este repositório contém o projeto final da disciplina de Teleinformática de Redes 1 (2025/1) da Universidade de Brasília. Desenvolvido pelos alunos Gabriel Francisco (Matrícula: 20/2066571), Henrique Givisiez (Matrícula: 21/1027563) e André Rodrigues Modesto (Matrícula: 21/1068324).

Este projeto utiliza a biblioteca **GTK 3** com **Python** para a construção da interface gráfica do simulador das camadas Física e de Enlace.

## Requisitos

- Python 3.6 ou superior
- Linux (Debian, Ubuntu ou derivados)
- GTK 3
- PyGObject (bindings Python para GTK)

## Dependências

Execute os comandos abaixo no terminal:

```bash
sudo apt update
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

Para mais informações, consulte a documentação:
https://python-gtk-3-tutorial.readthedocs.io/en/latest/
https://lazka.github.io/pgi-docs/#Gtk-3.0


## Uso com ambiente virtual

1. Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências via pip
```bash
pip install -r requirements.txt
```

## Rodando o projeto
A simulação foi desenvolvida por meio de 2 interfaces principais, a interface do transmissor e a interface do receptor.
Para rodar ambas as interfaces, rode os comandos abaixo:
- Interface transmissor
```bash
python3 transmissor.py
```

- Interface receptor
```bash
python3 receptor.py
```

Caso você receba o erro 
```bash
/usr/bin/python3: symbol lookup error: /snap/core20/current/lib/x86_64-linux-gnu/libpthread.so.0: undefined symbol: __libc_pthread_init, version GLIBC_PRIVATE
```

Experimente trocar os comandos por:
```bash
env -i DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY HOME=$HOME /usr/bin/python3 receptor.py
```
