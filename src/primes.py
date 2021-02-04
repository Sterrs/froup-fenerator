from itertools import count

def possible_primes():
    """
    Very unsophisticated generator that skips some obvious composite numbers.
    """
    yield 2
    yield 3
    for i in count(6, 6):
        yield i - 1
        yield i + 1

def is_prime(p):
    """
    Primality testing by dumb trial division
    """
    for i in possible_primes():
        if i * i > p:
            return True
        if not p % i:
            return False
        i += 1

def primes():
    """
    Generate primes.
    """
    return filter(is_prime, possible_primes())

def prime_factors(n):
    """
    Very bad and slow (but portable!) implementation of prime factorisation.

    This function isn't so mission-critical because there is absolutely no way
    that we are ever working with n > 10 ** 6, and the prime factorisation
    should only be computed once during the execution of this program.

    TODO: at least use the sieve of Eratosthenes or Atkin or something. Frankly
          we should be using something cool like Pollard's rho algorithm.
    """
    if n > 1:
        for p in primes():
            if p * p > n:
                yield n
                break
            while not n % p:
                yield p
                n //= p
            if n == 1:
                break

if __name__ == "__main__":
    from itertools import islice
    print(list(islice(primes(), 100)))
    for k in [*range(1, 37), 1001, 1001 ** 2, 1001 ** 3,
              # primes:
              1000003, 1000033, 1000037, 1000039, 1000081, 1000099,
              1000003 * 1000033, 1000033 ** 2]:
        print(f"{k} = {' * '.join(map(str, prime_factors(k)))}")
