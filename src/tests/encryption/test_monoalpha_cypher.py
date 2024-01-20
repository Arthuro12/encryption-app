from unittest import TestCase, main
from src.encryption.monoalpha_cypher import MonoAlphaCypher


class TestMonoAlphaCypher(TestCase):
    def test_encrypt_string(self):
        self.assertEqual(MonoAlphaCypher.encrypt_text("~a"), "a~", "a~ must be encrypted in ~a.")


if __name__ == "__main__":
    main()
