from lexical.token import Token, TokenType

class Scanner:
    KEYWORDS = {"int", "float", "print", "if", "else"}

    def __init__(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.source_code = list(f.read())
            self.pos = 0
            self.line = 0
            self.column = 1
            self.state = 0
        except FileNotFoundError:
            print(f"Erro: arquivo '{filename}' não encontrado.")
            self.source_code = []
            self.pos = 0
            self.line = 0
            self.column = 1
            self.state = 0

    def next_token(self):
        content = ""
        self.state = 0

        while not self.is_eof():
            current_char = self.source_code[self.pos]
            start_line = self.line
            start_column = self.column

            self.next_char() 

            match self.state:
                case 0:
                    if self.is_letter(current_char):
                        content += current_char
                        self.state = 1
                    elif self.is_digit(current_char):
                        content += current_char
                        self.state = 3
                    elif current_char == ".":
                        content += current_char
                        self.state = 4
                    elif self.is_math_operator(current_char):
                        return Token(TokenType.MATH_OPERATOR, current_char)
                    elif current_char == "=":
                        next_ch = self.peek()
                        if next_ch == "=":
                            self.next_char()
                            return Token(TokenType.REL_OPERATOR, "==")
                        else:
                            return Token(TokenType.ASSIGNMENT, current_char)
                    elif current_char in "<>!":
                        next_ch = self.peek()
                        if next_ch == "=":
                            op = current_char + self.next_char()
                            return Token(TokenType.REL_OPERATOR, op)
                        else:
                            return Token(TokenType.REL_OPERATOR, current_char)
                    elif current_char == "(":
                        return Token(TokenType.LPAREN, current_char)
                    elif current_char == ")":
                        return Token(TokenType.RPAREN, current_char)
                    elif current_char == "#":
                        self.skip_line_comment()
                        continue
                    elif current_char.isspace():
                        continue
                    else:
                        error_msg = f"Erro léxico: caractere inválido '{current_char}' na linha {start_line}, coluna {start_column}"
                        print(error_msg)
                        return None  

                case 1:
                    if self.is_letter(current_char) or self.is_digit(current_char):
                        content += current_char
                    else:
                        self.back()
                        self.state = 0
                        if content in self.KEYWORDS:
                            return Token(TokenType.RESERVED, content)
                        else:
                            return Token(TokenType.IDENTIFIER, content)

                case 3:
                    if self.is_digit(current_char):
                        content += current_char
                    elif current_char == ".":
                        content += current_char
                        self.state = 4
                    else:
                        self.back()
                        self.state = 0
                        return Token(TokenType.NUMBER, content)

                case 4:
                    if self.is_digit(current_char):
                        content += current_char
                    else:
                        if content[-1] == ".":
                            error_msg = f"Erro léxico: número inválido '{content}' na linha {start_line}, coluna {start_column}"
                            print(error_msg)
                            return None  
                        self.back()
                        self.state = 0
                        return Token(TokenType.NUMBER, content)
        return None

    def is_letter(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def is_digit(self, c: str) -> bool:
        return c.isdigit()

    def is_math_operator(self, c: str) -> bool:
        return c in "+-*/"

    def next_char(self) -> str:
        if self.is_eof():
            return ""
        ch = self.source_code[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def peek(self) -> str:
        if self.pos < len(self.source_code):
            return self.source_code[self.pos]
        return ""

    def back(self):
        self.pos -= 1
        self.column -= 1

    def is_eof(self) -> bool:
        return self.pos >= len(self.source_code)

    def skip_line_comment(self):
        while not self.is_eof() and self.source_code[self.pos] != "\n":
            self.next_char()