from .numerics import to_signed_format, to_int_format, convert_hex
from .mask import Mask


class Data(object):
    """
    La classe Data representa la unitat mínima d'informació que podem extreure d'una trama.
    Emmagatzema la informació pertinent d'una variable o funció per posteriorment poder obtenir
    o col·locar informació a una trama determinada.
    """

    def __init__(self, ids:int, name:str, mask:bytes, value:int, is_signed:bool=False) -> None:
        """
        Crea una instància de l'objecte Data. 

        :param var_name: Nom de la dada.
        :type var_name: str
        :param can_id: Identificador del missatge CAN on s'ha definit la variable o funció.
        :type can_id: int
        :param mask: El valor per establir la màscara.
        :type mask: int | bytes
        :param n_bits: El nombre màxim de bits que la variable (o funció) ocupa a la trama.
        :type n_bits: int
        :param value: El valor que es vol assignar a la variable (o funció).
        :type value: int
        :param is_signed: Indica si les dades introduïdes permeten un valor complement a dos.
        :type is_signed: bool (False per omissió)
        :param is_response: Indica si l'objecte Data forma part d'una trama de resposta.
        :type is_response: bool (False per omissió)
        :param is_function: Indica si l'objecte Data és una funció.
        :type is_function: bool (False per omissió)
        """
        self.id = ids
        self.name = name
        self.value = value
        self.mask = Mask(mask)
        self.is_signed = is_signed
        self.frame_value = self._encapsulate(self.mask,self.value,len(self.mask))


    def __int__(self) -> int:
        """
        Retorna el valor enter de l'objecte màscara.

        :return: Valor de la màscara.
        :rtype: int
        """
        return self.value


    def _encapsulate(self, mask:Mask, val:int, n_bits:int) -> int:
        """
        El mètode d'encapsulació privat permet introduir el valor donat en la màscara assignada.
        Aquest mètode permet comprovar ràpidament si el valor rebut és el que s'espera.

        :param mask: Màscara sobre la que realitzar l'encapsulat del valor.
        :type mask: Mask
        :param val: Valor que es vol encapsular.
        :type val: int
        :param n_bits: Nombre de bits que ocupa la variable o funció.
        :type n_bits: int
        :return: Valor de trama.
        :rtype: int
        """
        if val < 0:
            ini_val_str = "{:1>"
            val = to_signed_format(val)
        else:
            ini_val_str = "{:0>"
        mid_val_str = str(n_bits)
        fin_val_str = "}"
        all_val_str = f"{ini_val_str}{mid_val_str}{fin_val_str}"
        val_str = "{0:b}".format(val)
        r = all_val_str.format(val_str)
        mat_exp = list(range(0,8))
        mat_exp.reverse()
        exp = 63
        newval = 0
        for e in mask.get_mask():
            if e != 0:
                for i in mat_exp:
                    if len(r) == 0:
                        break
                    if e & (2**i) != 0:
                        newval += (2**exp)*int(r[0])
                        r = r[1:]
                    exp-=1
            else:
                exp -= 8
        return newval


    def _uncapsulate(self, rxframe_value:int) -> int:
        """
        Extreu el valor de la dada d'una trama CAN de recepció.

        :param rxframe: El valor enter de la trama rebuda.
        :type rxframe: int
        :return: Valor extret de la trama rebuda.
        :rtype: int
        """
        new_val = ""
        mask_val = "{0:b}".format(self.get_mask_value())
        mask_val = "{:0>64}".format(mask_val)
        rec_str = "{0:b}".format(rxframe_value)
        rec_str = "{:0>64}".format(rec_str)
        for i in list(range(len(mask_val))):
            if mask_val[i] == "1":
                new_val += rec_str[i]
        return convert_hex(value=hex(int(new_val,2)),bits=len(self.mask),signed=True if self.get_value_is_signed() else False)


    def check_value_received(self, rxframe_value:int) -> int:
        """
        Retorna el valor obtingut de la variable a través de la trama de recepció.

        :param rxframe: El valor enter de la trama rebuda.
        :type rxframe: int
        :return: El valor de la variable en la trama rebuda.
        :rtype: int
        """
        return self._uncapsulate(rxframe_value)


    def check_is_expected(self, rxframe:int) -> bool:
        """
        Indica si el resultat obtingut de la trama de recepció <rxframe> és el que s'esperava.

        :param rxframe: El valor enter de la trama rebuda.
        :type rxframe: int
        :return: True si coincideixen, False altrament.
        :rtype: bool
        """
        return self._uncapsulate(rxframe) == self.get_expected_value()


    def get_mask(self) -> Mask:
        """
        Retorna la màscara de l'objecte Data.

        :return: Màscara de l'objecte Data.
        :rtype: Mask
        """
        return self.mask


    def get_mask_value(self) -> int:
        """
        Retorna el valor de la màscara de l'objecte Data.

        :return: Valor de la màscara de l'objecte Data.
        :rtype: int
        """
        return int.from_bytes(self.mask.get_mask())


    def get_frame_value(self) -> int:
        """
        Retorna el valor de trama de l'objecte Data.

        :return: Valor de la trama aplicant la màscara de la variable o funció.
        :rtype: int
        """
        return self.frame_value


    def get_name(self) -> str:
        """
        Retorna el nom de la variable o funció del objecte Data.

        :return: El nom de la variable o funció.
        :rtype: str
        """
        return self.name


    def get_value_is_signed(self) -> bool:
        """
        Retorna si la variable o funció són complement a dos.

        :return: Indica si la variable és o no complement a dos.
        :rtype: bool
        """
        return self.is_signed


    def get_expected_value(self) -> int:
        """
        Retorna el valor que l'usuari espera rebre sobre l'objecte Data.

        :return: El valor que l'usuari espera rebre.
        :rtype: int
        """
        return self.value


    def get_number_of_bits(self) -> int:
        """
        Retorna la quantitat de bits de la variable o funció.

        :return: Nombre de bits de la variable o funció.
        :rtype: int
        """
        return len(self.mask)

    def get_id(self) -> int:
        """
        Retorna l'identificador de la dada.

        :return: Identificador de la dada.
        :rtype: int
        """
        return self.id

    def __repr__(self) -> str:
        """
        Representa un objecte del tipus Data.

        :return: Retorna adientment la representació d'un objecte Data.
        :rtype: str
        """
        return "Data Object: "+self.name+" takes up "+str(len(self.mask))+"bits."


class Argument(Data):
    def __init__(self, ids:int, name:str, mask:bytes, value:int, is_signed:bool=False) -> None:
        super().__init__(ids, name, mask, value, is_signed)



class Variable(Data):
    def __init__(self, ids:int, name:str, mask:bytes, value:int, is_signed:bool=False, is_response:bool=False) -> None:
        super().__init__(ids, name, mask, value, is_signed)
        self.is_response:bool = is_response


    def get_is_response(self) -> bool:
        return self.is_response



class Function(object):
    def __init__(self,ids:int,name:str) -> None:
        self.ids:int = ids
        self.name:str = name


# d_unsigned = Data(ids=1, name="Coolant_Temperature", mask=bytes([0x0F]), value=1, is_signed=False)
# d_signed = Data(ids=1, name="Oil_Temperature", mask=bytes([0x0F]), value=-1, is_signed=True)

# print(f"Unsigned value: {d_unsigned._uncapsulate(1)}")
# print(f"Signed value: {d_signed._uncapsulate(1)}")
# print(f"Unsigned expected value: {d_unsigned.get_expected_value()}")
# print(f"Signed expected value: {d_signed.get_expected_value()}")