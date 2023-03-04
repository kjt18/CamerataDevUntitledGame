import hashlib
import unittest

import bcrypt

from accounts import Accounts

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.accounts = Accounts()

class TestHash(TestAccounts):
    def test_hash_password(self):
        passTest = "password"
        hashTest = hashlib.sha256(passTest.encode()).hexdigest()
        self.assertNotEqual(passTest, self.accounts.hash_password(passTest))
        self.assertNotEqual(hashTest, self.accounts.hash_password(passTest))
        self.assertTrue(bcrypt.checkpw(passTest.encode(), self.accounts.hash_password(passTest)))