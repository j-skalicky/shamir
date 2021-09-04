from math import ceil, sqrt

class Prime:
    prime: int

    def __init__(self, p: int = None) -> None:
        self.set_prime(p)
    
    def is_valid(self) -> bool:
        return self.prime is not None and self.is_prime(self.prime)

    def is_prime(self, n: int) -> bool:
        # corner cases
        if n <= 1:
            return False
        if n <= 3:
            return True
    
        # quick and easy checks
        if (n % 2 == 0) or (n % 3 == 0):
            return False

        for i in range(5, ceil(sqrt(n)), 6):
            if (n % i == 0) or (n % (i+1) == 0):
                return False
        
        return True

    def next_prime(self, n: int) -> int:
        i = ceil((n / 2)) * 2 + 1
        while not self.is_prime(i):
            i += 2

        return i
        
    def get_prime(self) -> int:
        return self.prime

    def set_prime(self, n: int) -> None:
        if n is None:
            self.prime = None
        elif self.is_prime(n):
            self.prime = n
        else:
            self.prime = self.next_prime(n)

    def def_prime_to_contain(self, i: int) -> None:
        self.prime = self.next_prime(i)
