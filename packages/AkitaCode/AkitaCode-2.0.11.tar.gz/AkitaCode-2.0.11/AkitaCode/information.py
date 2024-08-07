TESTBENCH_RESULT_OK = "ok"
TESTBENCH_RESULT_NOK = "nok"

class Information(object):
    def __init__(self, ids, situation, itype, msg_id, frame, mask, var, expected, val):
        """
        Crea una instancia de la classe Information amb les dades assignades.

        :param ids: Identificador únic del testeig.
        :type ids: int
        :param situation: Nom de la situació a la que pertany la dada.
        :type situation: str
        :param type: Identifica si la trama és de recepció (RX) o de transmissió (TX).
        :type type: str
        :param msg_id: Identificador de la trama CAN.
        :type msg_id: int
        :param frame: Valor de la trama enviada o rebuda.
        :type frame: int
        :param mask: Valor de la màscara de la dada associada.
        :type mask: int
        :param var: Nom de la variable o funció.
        :type var: str
        :param expected: Valor que l'usuari espera rebre.
        :type expected: int
        :param val: Valor que s'ha obtingut del sistema de testeig.
        :type val: int
        """
        self.ids = ids
        self.situation = situation
        self.type = itype
        self.msg_id = msg_id
        self.frame = frame
        self.mask = mask
        self.var = var
        self.expected = expected
        self.val = val
        self.result = TESTBENCH_RESULT_OK if self.expected == self.val else TESTBENCH_RESULT_NOK


    def dict(self):
        """
        Retorna un diccionari amb les dades que conté la classe Information.
        """
        d = dict()
        d["Situation"] = self.situation
        d["Type"] = self.type
        d["COB ID"] = hex(self.msg_id)
        d["Variable Name"] = self.var
        d["Expected Value"] = self.expected
        d["Received Value"] = self.val
        d["Check"] = self.result
        return d