import pyparsing as pp

class Parser:
    """
    This class provides Parsing functionality for code
    """
    def __init__(self):
        self.REG = pp.Regex(r'(?:![^(),]+)|[^(), ]+') ^ pp.Suppress(',')
        self.PATTERN = self.REG + pp.nested_expr('(', ')', content=self.REG)

        # parsing pattern



    def __transform(self, elements):
        """
        recursive function to transform pyparsing result into list
        """
        stack = []
        for element in elements:
            if isinstance(element, list):
                key = stack.pop()
                stack.append({key: self.__transform(element)})
            else:
                stack.append(element)
        return stack

    def parse(self, text):
        assert (len(text)<1, "text parameter is empty")
        elements = self.PATTERN.parse_string(text).as_list()
        result = self.__transform(elements)
        return result

if 1 == 0:
    # A sample
    #string = "db('1', '2', if(ATTRS('Dim 1', !Element Structure, 'ID') = '3','4','5'), 6)"
    string = "DB('1007 P&G Hotel Ppto',!Estructura Hotel Centro-Empresa Ppto,!Conceptos Hotel Ppto,!Escenario,!Version,'EUR','Importe',!Meses);"


    # Operations to parse the sample string
    #elements = pattern.parse_string(string).as_list()
    #result = transform(elements)

    # Assertion
    #assert result == [{'db': ["'1'", "'2'", {'if': [{'ATTRS': ["'Dim 1'", '!Element Structure', "'ID'"]}, '=', "'3'", "'4'", "'5'"]}, '6']}]

    # Show the result

    parser = Parser()
    result = parser.parse(string)
    print(result)
