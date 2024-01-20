from unittest import TestCase, main
from src.encryption.caeser_cypher import CaesarCypher


class TestCaesarCypher(TestCase):
    def test_encrypt_string(self):
        CaesarCypher.set_vector(1)
        encrypted_text = CaesarCypher.encrypt_text("abc")
        self.assertEqual(encrypted_text, "bcd", "The string encoded for \"abc\" with key n = 1 must "
                                                "be equal to \"bcd\".")

    def test_rotation(self):
        CaesarCypher.set_vector(1)
        self.assertEqual(CaesarCypher.encrypt_text("~"), "a", "The encryption must be cyclic.")

    def test_space(self):
        CaesarCypher.set_vector(1)
        self.assertEqual(CaesarCypher.encrypt_text(" "), " ", "Spaces must remain unchanged.")
        plain_text = "abc d"
        encrypted_text = CaesarCypher.encrypt_text(plain_text)
        self.assertEqual(plain_text.find(" "), encrypted_text.find(" "), "The position of the space must "
                                                                         "be the same in both clear and encrypted "
                                                                         "messages.")

    def test_vector(self):
        CaesarCypher.set_vector(1)
        self.assertGreaterEqual(CaesarCypher.vector, 1, "The offset must be greater than or equal to 1.")
        self.assertLessEqual(CaesarCypher.vector, 1024, "The offset must be less than or equal to 1024.")


if __name__ == "__main__":
    main()
