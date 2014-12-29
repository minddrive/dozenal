"""Core module for managing dozenal numbers"""

import math
import re


class Dozenal():
    """Basic class for handling dozenal"""

    doz_digits = list('0123456789XE')

    def __init__(self, num, decimal=False):
        """Keep track of decimal value of dozenal for arithmetic"""

        if decimal:
            self.decimal = num
            self.dozenal = self.dec_to_doz(num)
        else:
            self.dozenal = num
            self.decimal = self.doz_to_dec(num)

    def __repr__(self):
        """Display dozenal value"""

        return self.dozenal

    def __add__(self, other):
        """Add two dozenal numbers"""

        dec_sum = self.decimal + other.decimal

        return Dozenal(dec_sum, decimal=True)

    def __mul__(self, other):
        """Multiply two dozenal numbers"""

        dec_prod = self.decimal * other.decimal

        return Dozenal(dec_prod, decimal=True)

    def __sub__(self, other):
        """Subtract two dozenal numbers"""

        dec_diff = self.decimal - other.decimal

        return Dozenal(dec_diff, decimal=True)

    def __truediv__(self, other):
        """Divide two dozenal numbers (not integral result)"""

        dec_div = self.decimal / other.decimal

        return Dozenal(dec_div, decimal=True)

    @staticmethod
    def _validate(num, dozenal=True):
        """Ensure dozenal or decimal number is valid"""

        if dozenal:
            digits = '[0-9XE]'
        else:
            digits = '[0-9]'

        prog = re.compile(r'^([+-])?(%s+)(\.(%s+))?$' % (digits, digits))
        result = re.match(prog, num)

        if result is None:
            raise ValueError(num)

        sign, whole, fraction = result.group(1, 2, 4)

        if not dozenal:
            if whole is not None:
                whole = int(whole)
            if fraction is not None:
                fraction = int(fraction)

        return sign, whole, fraction

    def doz_to_dec(self, doz_num):
        """Convert dozenal to decimal"""

        try:
            sign, whole, fraction = self._validate(doz_num)
        except ValueError as exc:
            raise ValueError('%s is not a valid dozenal number' % exc)

        negative = False

        if sign == '-':
            negative = True

        decimal = 0

        for digit in whole:
            decimal = ((decimal << 3) + (decimal << 2)
                       + self.doz_digits.index(digit))

        if fraction is not None:
            fractional = 0

            for digit in fraction:
                fractional = ((fractional << 3) + (fractional << 2)
                              + self.doz_digits.index(digit))

            decimal += fractional / (12 ** len(fraction))

        return -decimal if negative else decimal

    def dec_to_doz(self, dec_num):
        """Convert decimal to dozenal"""

        try:
            sign, whole, fraction = self._validate(str(dec_num),
                                                   dozenal=False)
        except ValueError as exc:
            raise ValueError('%s is not a valid decimal number' % exc)

        negative = False

        if sign == '-':
            negative = True

        dozenal = ''

        while True:
            dozenal += self.doz_digits[whole % 12]
            whole //= 12

            if whole == 0:
                break

        dozenal = dozenal[::-1]

        if fraction is not None:
            fractional = []
            fraction /= 10 ** (int(math.log10(fraction)) + 1)

            for idx in range(12):
                fraction *= 12
                fractional.append(self.doz_digits[int(fraction)])
                fraction -= int(fraction)

                if fraction == 0:
                    break

            dozenal += '.' + ''.join(fractional)

        return '-' + dozenal if negative else dozenal
