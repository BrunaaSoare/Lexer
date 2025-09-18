# Grupo: Bruna Gabriela Soares de Lima, Ana Julia Grzyb, Patrick Luan Ventura Aragão, Júlio Pedro Santos Monteiro
# Requisitos Python 3.12 e compilador de sua preferência
# digite o código desejado em programa.mc e rode o main

from lexical.scanner import Scanner

if __name__ == "__main__":
    scanner = Scanner("programa.mc")
    token = scanner.next_token()
    while token is not None:
        print(token)
        token = scanner.next_token()
