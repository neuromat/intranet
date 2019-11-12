# -*- coding:UTF-8 -*-
# fonte: http://www.python.org.br/wiki/VerificadorDeCPF

import re
from django.utils.translation import ugettext_lazy as _


# traduz 123.456.789-10 para 12345678910
def _translate(cpf):
    return ''.join(re.findall(r"\d", cpf))


def _exceptions(cpf):
    """Se o número de CPF estiver dentro das exceções é inválido

    """
    if len(cpf) != 11:
        return True
    else:
        s = ''.join(str(x) for x in cpf)
        cpf_exceptions = ['00000000000', '11111111111', '22222222222', '33333333333', '44444444444', '55555555555',
                          '66666666666', '77777777777', '88888888888', '99999999999']
        if s in cpf_exceptions:
            return True
    return False


def _gen(cpf):
    """Gera o próximo dígito do número de CPF

    """
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res

    return 0


class CPF(object):

    _gen = staticmethod(_gen)
    _translate = staticmethod(_translate)

    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:

        12345678910
        123.456.789-10

        ou uma lista ou tuple
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0)

        """

        if isinstance(cpf, str):
            if not cpf.isdigit():
                cpf = self._translate(cpf)
        else:
            raise TypeError(_('CPF values must be passed as strings'))
        self.cpf = [int(x) for x in cpf]

    def __getitem__(self, index):
        """Retorna o dígito em index como string

        """

        return self.cpf[index]

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:
                eval(repr(cpf)) == cpf
        """

        return "CPF('%s')" % ''.join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF

        """

        return isinstance(other, CPF) and self.cpf == other.cpf

    def __str__(self):
        """Retorna uma representação do CPF na forma:

        123.456.789-10

        """

        d = iter("..-")
        s = list(map(str, self.cpf))
        for i in range(3, 12, 4):
            s.insert(i, d.__next__())
        r = ''.join(s)
        return r

    def isValid(self):
        """Valida o número de cpf

        """

        if _exceptions(self.cpf):
            return False

        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]
