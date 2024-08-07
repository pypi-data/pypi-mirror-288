class State(object):
    """
    Representa la classe Estat de Línia. Permet crear diferents estats en funció de la línia del document específica.
    D'aquesta manera, es permet l'abstracció de la màquina d'estats durant la sintaxi d'una línia.
    """
    def __init__(self, ids: int, required: bool = True, strict: bool = True, command: str|None = None, allow_reserved_words: bool = False, error_msg: str = "Undefined error."):
        """
        Crea una instància de la classe State.
        """
        self._id:int = ids
        self._required = required
        self._origin:bool = (command is None and strict is True and required is True) #(command == None and strict == True and required==True)
        self._strict:bool = strict
        self._command:str|None = command
        self._next:list[State] = []
        self._error = False
        self._error_command = None
        self._error_msg = error_msg
        self._use_reserved_word = False
        self._reserved_words=["create","enviroment","situation","var", "fn", "end", "import", "protocol","for","do","each","case"]
        if allow_reserved_words:
            self._reserved_words=[]


    def set_next(self,child) -> bool:
        """
        Afegeix un fill sota aquest estat.
        """
        if isinstance(child,State):
            if self._id != child._id:
                self._next.append(child)
                return True
            else:
                return False
        else:
            return False


    def is_next(self, command: str|None) -> bool:
        """
        Retorna True si la comanda <command> existeix en qualsevol dels estats fills de l'estat actual.
        """
        if command is not None:
            for state in self._next:
                if not state._required:
                    if not state._strict and command != state._command and command not in self._reserved_words:
                        return True
                    elif not state._strict and command != state._command and command in self._reserved_words:
                        self._error = True
                        self._use_reserved_word = True
                        self._error_command = command
                        return False
                    elif state._strict and command == state._command:
                        return True
        for state in self._next:
            if state._required:
                if not state._strict and command != state._command and command not in self._reserved_words:
                    return True
                elif not state._strict and command != state._command and command in self._reserved_words:
                    self._error = True
                    self._use_reserved_word = True
                    self._error_command = command
                    return False
                elif state._strict and command == state._command:
                    return True
        self._error = True
        self._error_command = command
        return False


    def get_next(self, command: str|None):
        """
        Retorna l'estat següent si la comanda <command> existeix en qualsevol dels estats fills de l'estat actual.
        """
        if command is not None:
            for state in self._next:
                if not state._required:
                    if not state._strict and command != state._command:
                        return state
                    elif state._strict and command == state._command:
                        return state
        for state in self._next:
            if state._required:
                if not state._strict and command != state._command:
                    return state
                elif state._strict and command == state._command:
                    return state
        self._error = True
        self._error_command = command
        return None


    def get_error(self) -> str:
        """
        Retorna el missatge d'error per a l'estat actual.
        """
        if self._use_reserved_word:
            return "Used a reserved word ''{}'' after ''{}'' statement.".format(str(self._error_command),self._command)
        return self._error_msg.format(str(self._error_command)) if self._error_command is not None else self._error_msg.format("<empty>")


    def used_reserved_word(self) -> bool:
        return self._use_reserved_word


    def __str__(self) -> str:
        return str(self._id)
    

    def __repr__(self) -> str:
        return repr(self._id)