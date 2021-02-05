import unittest, sys

from primes import is_prime, primes, prime_factors, factors

class TestPrimesFunctions(unittest.TestCase):
    def test_is_prime(self):
        # Let's just check all the most important numbers
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(35))
        self.assertTrue(is_prime(101))
        self.assertFalse(is_prime(1001))
        self.assertTrue(is_prime(1009))
        self.assertTrue(is_prime(2017))
        self.assertFalse(is_prime(2021))

    def test_primes(self):
        for i, p in zip(range(50), primes()):
            if i == 0:
                self.assertEqual(p, 2)
            if i == 1:
                self.assertEqual(p, 3)
            if i == 9:
                self.assertEqual(p, 29)
            if i == 49:
                self.assertEqual(p, 229)

    def test_prime_factors(self):
        self.assertEqual(tuple(prime_factors(2)), (2,))
        self.assertEqual(tuple(prime_factors(6)), (2,3))
        self.assertEqual(tuple(prime_factors(2000)), (2,2,2,2,5,5,5))
        self.assertEqual(tuple(prime_factors(2017)), (2017,))
        self.assertEqual(tuple(prime_factors(2021)), (43, 47))

    def test_factors(self):
        self.assertEqual(tuple(factors(2)), (1,2))
        self.assertEqual(tuple(factors(6)), (1,2,3,6))
        self.assertEqual(tuple(factors(25)), (1,5,25))
        self.assertEqual(tuple(factors(2017)), (1,2017))
        self.assertEqual(tuple(factors(100)), (1,2,4,5,10,20,25,50,100))


if __name__ == "__main__":
    # This doesn't work :(
    unittest.main()

