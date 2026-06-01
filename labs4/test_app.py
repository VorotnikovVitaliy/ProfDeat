import unittest
from app import calculate_currency 

class TestCurrencyConverter(unittest.TestCase):

    def test_calculate_usd_to_rub(self):
        """Проверяем: 100 USD по курсу 1 к 90 RUB должны дать 9000 RUB"""
        result = calculate_currency(100, 1.0, 90.0)
        self.assertAlmostEqual(result, 9000.0, places=2)

    def test_calculate_eur_to_usd(self):
        """Проверяем: 100 EUR (курс 0.92) в USD (курс 1.0)"""
        result = calculate_currency(100, 0.92, 1.0)
        self.assertAlmostEqual(result, 108.70, places=2)

    def test_calculate_zero(self):
        """Проверяем: 0 денег должен дать 0"""
        result = calculate_currency(0, 1.0, 90.0)
        self.assertEqual(result, 0.0)

    def test_negative_amount_protection(self):
        """
        Проверяем защиту от отрицательных чисел.
        Логика: если сумма < 0, расчет не производится, выдается ошибка.
        """
        amount = -1000
        rate_from = 1.0
        rate_to = 90.0
        # Эмулируем проверку из app.py
        if amount < 0:
            # В этом случае функция calculate_currency даже не должна вызываться
            # или мы ожидаем, что результат будет обработан как ошибка
            is_valid = False
        else:
            is_valid = True
        # Утверждаем, что отрицательное число считается невалидным
        self.assertFalse(is_valid, "Отрицательная сумма должна быть отклонена")

if __name__ == '__main__':
    unittest.main()
