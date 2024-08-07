from .keys import State
from .line_state_machine import create_line_state_machine
from .instances import Instance, EndInstance, ForInstance, VariableInstance
from .instances import SituationInstance, FunctionInstance, EnviromentInstance
from .instances import ProtocolInstance, ErrorInstance, SkipInstance, TimeInstance
from .instances import UndefinedInstance
from .messages import StatusMessage


class Line(object):
    """
    La classe Line s'encarrega d'analitzar la sintàxi d'una línia. Aquesta classe comprova automàticament la línia a partir d'un estat inicial.
    """
    def __init__(self, n:int, line:str) -> None:
        """
        Crea una nova instancia de la classe Line.

        :param n: Número de la línia.
        :type n: int
        :param line: El text que conté la línia del document.
        :type line: str
        :param init_state: L'objecte State que conté l'estat inicial.
        :type init_state: State
        """
        self._error = None
        self._error_msg = None
        self._ignore = False
        self._number_line:int = n
        self._parsed:list = self.__parser_line(line)
        self._init_state:State = create_line_state_machine()
        self._used_reserved_word = False
        self.__validate()


    def __parser_line(self,line:str) -> list[str]:
        """
        Mètode privat que parseja la línia instanciada.

        :param line: El text que conté la línia.
        :type line: str
        :return: La línia parsejada.
        :rtype: list
        """
        return line.split()


    def __validate(self) -> bool:
        """
        Indica si una línia és vàlida.

        :return: True si la línia és vàlida, False altrament.
        """
        if self._parsed:
            next_state:State = self._init_state
            prev_state:State = self._init_state
            for word in self._parsed:
                if prev_state.is_next(str(word)):
                    next_state = prev_state.get_next(str(word))
                    prev_state = next_state
                else:
                    self._error_msg = prev_state.get_error()
                    self._error = True
                    self._used_reserved_word = prev_state.used_reserved_word()
                    return False
            if next_state.is_next(None):
                next_state = next_state.get_next(None)
                if next_state == self._init_state:
                    self._error = False
                    return True
                else:
                    self._error_msg = prev_state.get_error()
                    self._error = True
                    self._used_reserved_word = prev_state.used_reserved_word()
                    return False
            else:
                self._error_msg = prev_state.get_error()
                self._error = True
                self._used_reserved_word = prev_state.used_reserved_word()
                return False
        else:
            self._ignore = True
            return False


    def get_error(self) -> str:
        """
        Retorna l'error que conté la linia.

        :return: Missatge d'error de la linia.
        :rtype: str (o None)
        """
        if self._error:
            return StatusMessage(
                msgtype="SyntaxError",
                msg=self._error_msg,
                return_code=6,
                nline=self._number_line
            )
        else:
            return StatusMessage(
                msgtype="Success",
                msg="No errors detected.",
                return_code=7,
                nline=self._number_line
            )


    def ignore(self) -> bool:
        """
        Retorna si la línia pot ser ignorada o no.

        :return: True si es pot ignorar, False si no.
        :rtype: bool
        """
        return self._ignore
    

    def have_error(self) -> bool:
        """
        Retorna si la línia conté errors de sintàxi o no. En cas de que la línia es pugui ignorar, es retornarà False.

        :return: True si conté errors, False si no conté errors o s'ha d'ignorar.
        :rtype: bool
        """
        return self._error if not self._ignore else False


    def get_parsed(self) -> list[str]|None:
        """
        Obté la línia parsejada.

        :return: La línia parsejada.
        :rtype: list[str] | None
        """
        if not self.have_error():
            if not self.ignore():
                return self._parsed


    def convert(self) -> Instance:
        """
        Converteix la linia al tipus de declaració adhient.
        :return: L'objecte del tipus de declaració realitzada.
        :rtype: ProtocolInstance|VariableInstance|FunctionInstance|EndInstance|EnviromentInstance|
        """
        if not self.have_error() and not self.ignore():
            objline = self.get_parsed()
            if "//" in objline:
                return SkipInstance(self._number_line)
            elif "import" and "protocol" in objline:
                return ProtocolInstance(line_parsed=objline,nline=self._number_line)
            elif "var" in objline:
                return VariableInstance(line_parsed=objline,nline=self._number_line)
            elif "fn" in objline:
                return FunctionInstance(line_parsed=objline,nline=self._number_line)
            elif "create" and "enviroment" in objline:
                return EnviromentInstance(line_parsed=objline,nline=self._number_line)
            elif "create" and "situation" in objline:
                return SituationInstance(line_parsed=objline,nline=self._number_line)
            elif "for" in objline:
                return ForInstance(line_parsed=objline, nline=self._number_line)
            elif "end" in objline:
                return EndInstance(line_parsed=objline,nline=self._number_line)
            elif "time" in objline:
                return TimeInstance(line_parsed=objline,nline=self._number_line)
            else:
                self._error = True
                self._error_msg = """
                Unexpected tokenitzation. Report this bug at aamat@ausa.com. 
                Error description: Line.convert() after verified Line object.
                """
                return UndefinedInstance(self._number_line)
        elif not self.have_error() and self.ignore():
            return SkipInstance(self._number_line)
        else:
            return ErrorInstance(self._number_line,self._error_msg)

    def __str__(self):
        """
        Retorna una cadena que conté la clau, la variable i el valor de la linia separats per un espai.

        :return: L'informació de la linia.
        :rtype: str
        """
        return str(self.get_key())+" "+str(self.get_variable())+" "+str(self.get_value())