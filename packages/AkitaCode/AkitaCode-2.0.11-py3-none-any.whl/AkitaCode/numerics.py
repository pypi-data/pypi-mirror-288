def to_signed_format(n):
    """
    Aquesta funció converteix un enter negatiu a la seva representació en complement a dos.
    
    :param n: Enter que es vol convertir a complement a dos.
    :type n: int
    :return: Representació en binari signat en complement a dos o False si n no és un enter negatiu.
    :rtype: int (or False)
    """
    if isinstance(n, int):
        if n < 0:
            nstr = "{0:b}".format(n)
            aux = int(nstr[1:],2)
            exp = 0
            for e in list(range(0,64)):
                if (2**e) >= aux:
                    exp = e
                    break
            r = n + (2*(2**exp))
            return r
        else:
            return False
    else:
        return False



def to_int_format(n):
    """
    Aquesta funció converteix un enter en format de complement a dos (utilitzat en la codificació de números negatius) 
    a un enter negatiu.

    :param n: Valor que es vol convertir a format de complement a dos.
    :type n: int
    :return: Valor resultant de la conversió o False si n no és un enter.
    :rtype: int (or False)
    """
    if type(n) == int:
        if n > 0:
            nstr = "{0:b}".format(n)
            newval = 0
            for i in list(range(len(nstr))):
                if i == 0:
                    newval -= 2**((len(nstr)-1)-i)*int(nstr[i])
                else:
                    newval += 2**((len(nstr)-1)-i)*int(nstr[i])
            return newval
        else:
            return False
    else:
        return False
    

def list_to_int(inlist:list):
    """
    Converteix una llista de enters compressos entre 0-255, en un enter.
    """
    return int.from_bytes(bytes(inlist))


def ss_to_signed_format(n):
    """
    Convierte un entero negativo a su representación en complemento a dos.

    :param n: Entero que se quiere convertir a complemento a dos.
    :type n: int
    :return: Representación en binario signado en complemento a dos o False si n no es un entero negativo.
    :rtype: str or bool
    """
    if isinstance(n, int):
        if n < 0:
            # Obtener el número binario sin el signo
            nbits = len(bin(n)[2:])
            binary = bin(n & (2**(nbits)-1))[2:]
            # Extender el número binario a 64 bits si es necesario
            # binary = binary.zfill(64)
            return int(binary,2)
        else:
            return False
    else:
        return False



def ss_to_int_format(n):
    """
    Convierte un entero en formato de complemento a dos a un entero negativo.

    :param n: Valor que se quiere convertir a formato de complemento a dos.
    :type n: int
    :return: Valor resultante de la conversión o False si n no es un entero.
    :rtype: int or bool
    """
    if isinstance(n, int):
        if n & (1 << 63):  # Comprueba si el bit más significativo está encendido
            complement = n ^ ((1 << 64) - 1)  # Calcula el complemento a uno
            return -(complement + 1)  # Calcula el complemento a dos
        else:
            return False
    else:
        return False
    


def convert_hex(value: str, bits: int, signed: bool = False) -> int:
    """
    Convierte un valor hexadecimal a su valor con signo o sin signo.
    
    :param value: El valor hexadecimal como string (por ejemplo, "0xFF").
    :param bits: El tamaño en bits del número (por ejemplo, 8, 16, 32, 64).
    :param signed: Si es True, interpreta el valor como con signo.
    :return: El valor entero convertido.
    """
    # Convertir el valor hexadecimal a un entero sin signo
    unsigned_value = int(value, 16)
    
    if not signed:
        return unsigned_value
    
    # Calcular el valor con signo
    sign_bit = 1 << (bits - 1)
    mask = (1 << bits) - 1
    
    if unsigned_value & sign_bit:
        # Si el bit de signo está establecido, convertir a negativo
        return unsigned_value - mask - 1
    else:
        # Si no, es un valor positivo regular
        return unsigned_value