from random import randint
from math import log, ceil
#from base64 import b32decode, b32encode, decode

class ShamirSecretShare:
    
    # define default values in the constructor
    def __init__(self) -> None:
        self.prime = 14693679385278593849609206715278070972733319459651094018859396328480215743184089660644531
        self.holders = 5
        self.threshold = 3
        self.shares = {}
        self.secret = ''
        self.update_max_bytes()
    
    # alter the prime value
    def change_prime(self, prime: int) -> None:
        if prime < 2:
            raise ValueError("Hodnota prvočísla nesmí být záporná a musí být větší než 2")

        # verify that the prime supplied is actually a prime
        # TODO

        self.prime = prime
        self.update_max_bytes()

    # alter the number of holders
    def change_holders(self, holders: int) -> None:
        if holders < 1 or holders < self.threshold:
            raise ValueError("")

        self.holders = holders

    # change the number of thresholds
    def change_threshold(self, threshold: int) -> None:
        if threshold < 2 or threshold > self.holders:
            raise ValueError('')

        self.threshold = threshold

    def update_max_bytes(self) -> None:
        self.max_bytes = ceil(log(self.prime, 2) / 8)

    # set secret message
    def set_message(self, secret: str) -> None:
        if secret is None:
            raise ValueError('')

        self.secret = secret

    # get secret message
    def get_message(self) -> str:
        return self.secret

    # get number of valid shares
    def get_shares_count(self) -> int:
        return len(self.shares)

    # get the threshold value
    def get_threshold(self) -> int:
        return self.threshold

    # get the number of holders
    def get_holders(self) -> int:
        return self.holders

    # get the total number of bytes representable within the current prime number
    def get_max_bytes(self) -> int:
        return self.max_bytes

    # are there already enough shares to compute the secret?
    def is_solvable(self) -> bool:
        return len(self.shares) >= self.threshold

    # convert secret message to int
    def message_to_int(self) -> int:
        if len(self.secret) < 1:
            raise ValueError('')

        secretBytes = str.encode(self.secret, 'utf-8')
        return int.from_bytes(secretBytes, byteorder='big')

    # convert int to string
    def int_to_message(self, i: int) -> str:
        if i < 1 or i >= self.prime:
            raise ValueError('')

        b = (i).to_bytes(self.max_bytes, byteorder='big')
        return b.decode('utf-8')

    # add share to the collection
    def add_share(self, i: int, val: int) -> None:
        if i < 1 or i > self.holders:
            print('Špatné číslo tajemství, povolené hodnoty jsou 1 až {:d}\n'.format(self.holders))
        elif i not in self.shares:
            self.shares[i] = val
        else:
            print('HEJ! Tuto část už mám! Nepodvádějte! :-)\n')

    # split secret message into parts
    def split_secret(self) -> dict:
        """
        Turns an integer into a number of shares given a modulus and a
        number of parties.
        """
        # initialize values and convert string to int
        self.shares = {}
        value = self.message_to_int()

        # check that the secret value is smaller than the prime
        if value >= self.prime:
            raise ValueError('')
        
        # generate random polynomial
        polynomial = [value] + [randint(0, self.prime-1) for _ in range(1,self.threshold)]

        # Compute each share such that shares[i] = f(i).
        for i in range(1, self.holders+1):
            self.shares[i] = polynomial[0]
            for j in range(1, len(polynomial)):
                self.shares[i] = (self.shares[i] + polynomial[j] * pow(i,j)) % self.prime

        return self.shares

    # reconstruct secret message from individual parts
    def reconstruct_secret(self) -> str:
        x = list(self.shares)

        if len(x) < self.threshold:
            raise ValueError('')

        # Compute the Langrange coefficients at 0.
        coefficients = {}
        for i in x:
            coefficients[i] = 1
            for j in x:
                if j != i:
                    coefficients[i] = (coefficients[i] * (0-j) * self.inv(i-j)) % self.prime

        value = 0
        for i in x:
            value = (value + self.shares[i] * coefficients[i]) % self.prime

        self.secret = self.int_to_message(value)
        return self.secret

    def inv(self, a):
        return pow(a, self.prime-2, self.prime)