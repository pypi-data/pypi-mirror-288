MAX_MASK_VALUE = 2**64

class Mask(object):
    """
    La classe "Mask" proporciona les funcionalitats necessàries per a poder comprovar
    i encapsular la informació que es vol validar en una futura trama. És principalment
    responsable de verificar que no hi hagi conflictes entre les variables definides en
    el document, ni repeticions de definició.
    """
    def __init__(self, val=MAX_MASK_VALUE-1):
        """
        Crea una nova instància de la classe "Mask" amb el valor de màscara <val>. 
        El valor màxim de la màscara és (2 ** 64) - 1. Si s'excedeix, s'establirà el valor màxim com valor de la màscara.

        :param val: Estableix un valor a la màscara.
        :type val: int (o bytes)
        """
        if isinstance(val, str):
            v = int(val)
        elif isinstance(val, bytes):
            v = int.from_bytes(val)
        elif isinstance(val, int):
            v = val
        else:
            v = MAX_MASK_VALUE-1
        self.val = v


    def __int__(self):
        """
        Retorna el valor enter de la màscara.

        :return: Valor enter de la màscara.
        :rtype: int
        """
        return self.val


    def get_mask(self):
        """
        Retorna en bytes el valor de la màscara.

        :return: Valor de la màscara en bytes.
        :rtype: bytes
        """
        return self.val.to_bytes(8)


    def __and__(self, othermask):
        """
        Realitza l'operació lògica AND entre dos objectes (el mateix objecte "self" i "<othermask>") del tipus "Mask".

        :param othermask: Segon paràmetre per realitzar una AND lògica entre màscares.
        :type othermask: Mask
        :return: Una màscara amb el resultat de la operació AND lògica.
        :rtype: Mask
        """
        return Mask(self.val & othermask.val)


    def __len__(self):
        """
        Retorna el nombre de bits que conté la màscara.

        :return: Nombre de bits de la màscara.
        :rtype: int
        """
        a = self.val ^ 0
        a = "{0:b}".format(a)
        count = 0
        for b in a:
            if b == "1":
                count+=1
        return count