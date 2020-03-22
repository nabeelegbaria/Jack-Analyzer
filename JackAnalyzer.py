from Tokenizer import Tokenizer
import sys
import os

class JackAnalyzer:
    """ A jack parser class """

    Operators = ['+', '-', '*', '/', '|', '=', '&gt', '&amp', '&lt']
    statements_keyword = ["let", "do", "if", "while", "return"]
    Symbols = ['(', ')', '{', '}', '[', ']', ',', ';', '.', '+', '-', '*', '/', '&', '|', '>', '<', '=', '~']

    def __init__(self, file):
        """ A constructor which initializes the members of the class """
        self.tekonizer = Tokenizer(file)
        self.output_file = self.openfile(file)
        self.taps=''
        self.two_taps='  '

    def openfile(self, file):
        """ This function opens a file to write """
        point = file.find('.')
        new_path = file[:point] + '.xml'
        output_file = open(new_path, 'w')
        return output_file



    def compileClass(self):
        """ This function compiles a class state """
        if (self.tekonizer.current_token == "class"):
            self.output_file.write("<class>\n")
            self.taps+=self.two_taps
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.compileClassVarDec()
            self.compileSubroutineDec()
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps + '</'+"class" '>\n')

    def compileVarName(self):
        """ This function compile the names of the var declaration of a class """
        self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
        self.tekonizer.advance()
        if(self.tekonizer.current_token == ','):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.compileVarName()
        elif(self.tekonizer.current_token == ';'):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps+'</'+"classVarDec"+'>'+'\n')
            self.tekonizer.advance()

    def compileClassVarDec(self):
        """ This function compile the names of the var declaration of a class """
        if (self.tekonizer.current_token == "static" or self.tekonizer.current_token == "field" ):
            self.output_file.write(self.taps+'<' + "classVarDec" + '>\n')
            self.taps+=self.two_taps
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps+self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compileVarName()
            self.compileClassVarDec()

    def compileSubroutineDec(self):
        """ This function compile the method \ function \ constructor case """
        if (self.tekonizer.current_token == "method" or self.tekonizer.current_token == "constructor" or
                self.tekonizer.current_token == "function" ):
            self.output_file.write(self.taps+'<subroutineDec>' + '\n')
            self.taps+=self.two_taps
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.compileParameterList()
            self.compileSubrotineBody()
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps + '</'+'subroutineDec'+'>\n')
        if (self.tekonizer.current_token != '}'):
            self.compileSubroutineDec()


    def compileParameterList(self):
        """ This function compiles the parameterlist of the method\function\constructor """
        self.output_file.write(self.taps+'<' + "parameterList" + '>\n')
        self.taps+=self.two_taps
        self.tekonizer.advance()
        self.compileParametrs()

    def compileParametrs(self):
        """ This function compiles the arguments of the method\function\constructor """
        if (self.tekonizer.current_token == ')'):
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps+'</' + "parameterList" + '>\n')
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
        else:
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            if (self.tekonizer.current_token == ','):
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()
                self.compileParametrs()
            else:
                self.compileParametrs()

    def compileSubrotineBody(self):
        """ This function compiles the subroutinebody of the method\function\constructor """
        self.output_file.write(self.taps+'<'+"subroutineBody"+'>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.compileVarDec()
        self.compileStatements()
        self.tekonizer.advance()
        if(self.tekonizer.current_token == '}'):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps + '</' + "subroutineBody" + '>\n')

    def compileVarDec(self):
        """ This function compile the var declaration for a method """
        if (self.tekonizer.current_token == "var"):
            self.output_file.write(self.taps+'<'+"varDec"+'>\n')
            self.taps+=self.two_taps
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compileVarDecName()
            self.compileVarDec()


    def compileVarDecName(self):
        """ This function compile the name of the var declaration for a method """
        self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
        self.tekonizer.advance()
        if (self.tekonizer.current_token == ','):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compileVarDecName()
        if (self.tekonizer.current_token == ';'):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.taps=self.taps[:-2]
            self.output_file.write(self.taps+'</'+"varDec"+'>\n')
            self.tekonizer.advance()

    def compileStatements(self):
        """ This function compiles the statements declaration """
        self.output_file.write(self.taps + '<' + "statements" + '>\n')
        self.taps+=self.two_taps
        self.compile_Statements()
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</' + "statements" + '>\n')

    def compile_Statements(self):
        """ This function checks the current statements and calls the appropriate function """
        if (self.tekonizer.current_token == "if"):
            self.if_statement()
            self.compile_Statements()
        elif (self.tekonizer.current_token == "while"):
            self.while_statement()
            self.compile_Statements()
        elif (self.tekonizer.current_token == "do"):
            self.do_statement()
            self.compile_Statements()
        elif (self.tekonizer.current_token == "let"):
            self.let_statement()
            self.compile_Statements()
        elif (self.tekonizer.current_token == "return"):
            self.return_statement()
            self.compile_Statements()

    def if_statement(self):
        """ This function compile the if statement """
        self.output_file.write(self.taps+'<'+"ifStatement"+'>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
        self.tekonizer.advance()
        self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
        self.tekonizer.advance()
        self.compile_expression()
        self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
        self.tekonizer.advance()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.compileStatements()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        if(self.tekonizer.current_token == 'else'):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compileStatements()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</'+"ifStatement" + '>\n')

    def while_statement(self):
        """ This function compile the while statement """
        self.output_file.write(self.taps+ '<'+"whileStatement"+'>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.compile_expression()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.compileStatements()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps+'</'+"whileStatement"+'>\n')
        self.tekonizer.advance()

    def do_statement(self):
        """ This function compile the do statement """
        self.output_file.write(self.taps + '<' + "doStatement" + '>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.subroutineCall()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</' + "doStatement" + '>\n')



    def let_statement(self):
        """ This function compile the let statement """
        self.output_file.write(self.taps + '<' + "letStatement" + '>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        self.compileLetVarName()
        if (self.tekonizer.current_token == '='):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_expression()
        elif(self.tekonizer.current_token == '['):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_expression()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_expression()
        if(self.tekonizer.current_token == ';'):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</' + "letStatement" + '>\n')

    def return_statement(self):
        """ This function compiles the return statement """
        self.output_file.write(self.taps + '<' + "returnStatement" + '>\n')
        self.taps+=self.two_taps
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        if(self.tekonizer.current_token != ';'):
            self.compile_expression()
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</' + "returnStatement" + '>\n')

    def compileLetVarName(self):
        """ This function compiles the let var name """
        self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
        self.tekonizer.advance()
        if(self.tekonizer.current_token==','):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compileVarName()


    def compile_expression(self):
        """ This function compiles the expression case's """
        self.output_file.write(self.taps+'<'+"expression"+'>\n')
        self.taps+=self.two_taps
        self.compile_term()
        if (self.tekonizer.current_token in self.Operators):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_term()
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps + '</'+"expression"+'>\n')
        if (self.tekonizer.current_token == ','):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_expression()

    def compile_term(self):
        """ This function compiles the term case's """
        self.output_file.write(self.taps+'<'+"term"+'>\n')
        self.taps+=self.two_taps
        term_flag=True
        if (self.tekonizer.current_token.isdigit() or self.tekonizer.current_token.startswith('"') or
                self.tekonizer.current_token == 'this' or self.tekonizer.current_token == 'null'
                or self.tekonizer.current_token == 'true' or self.tekonizer.current_token == 'false'):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
        elif (self.tekonizer.current_token == '-' or self.tekonizer.current_token == '~'):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.compile_term()
        elif(self.tekonizer.current_token == '('):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.compile_expression()
            if (self.tekonizer.current_token == ')'):
                self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
                self.tekonizer.advance()
        else:
            if (self.tekonizer.all_tokens[self.tekonizer.counter+1] == '.' or
                    self.tekonizer.all_tokens[self.tekonizer.counter+1] ==  '('): #identefier
                self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
                self.tekonizer.advance()
                self.subroutineCall()
            elif(self.tekonizer.all_tokens[self.tekonizer.counter+1] == '['):
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()
                self.compile_expression()
                self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n') #term->expreession->current==]
                self.tekonizer.advance()
            elif (self.tekonizer.all_tokens[self.tekonizer.counter+1] == ')'):
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()
            else:
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()
                term_flag=False
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps+'</'+"term"+'>\n')
        if (self.tekonizer.current_token in self.Operators and not term_flag):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            self.compile_term()

    def compile_exclist(self):
        """ This function compiles the expression list case """
        self.output_file.write(self.taps+'<'+"expressionList"+'>'+'\n')
        self.taps+=self.two_taps
        if (self.tekonizer.current_token != ')'):
            self.compile_expression() # if item != )
        self.taps=self.taps[:-2]
        self.output_file.write(self.taps+'</'+"expressionList"+'>\n')

    def subroutineCall(self):
        """ This function compiles the call of a function """
        if (self.tekonizer.return_typetoken() == "identifier"):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
        if (self.tekonizer.current_token == '.'):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
        elif (self.tekonizer.current_token == '('):
            self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
            self.tekonizer.advance()
            self.compile_exclist()
            if (self.tekonizer.current_token == ')'):
                self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
                self.tekonizer.advance()
        if (self.tekonizer.current_token == '('):
            self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
            self.tekonizer.advance()
            if(self.tekonizer.current_token == ')'):
                self.output_file.write(self.taps+'<'+"expressionList"+'>\n')
                self.output_file.write(self.taps+'</'+"expressionList"+'>\n')
                self.output_file.write(self.taps+self.tekonizer.tokenType()+'\n')
                self.tekonizer.advance()
            else:
                self.compile_exclist()
                self.output_file.write(self.taps + self.tekonizer.tokenType() + '\n')
                self.tekonizer.advance()

def main():
        #if the argument is a directory
    if (os.path.isdir(sys.argv[1])):
        for filename in os.listdir(sys.argv[1]):
            if filename.endswith(".jack"):
                parser = JackAnalyzer(sys.argv[1]+"/"+filename)
                parser.compileClass()
                parser.output_file.close()

        # if the argument is a file
    else:
        parser = JackAnalyzer(sys.argv[1])
        parser.compileClass()
        parser.output_file.close()


if __name__ == '__main__':
    main()
