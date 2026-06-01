from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def get_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data['rates']
    except:
        return {"RUB": 90.0, "EUR": 0.92, "KZT": 450.0, "BYN": 3.2, "USD": 1.0}

def calculate_currency(amount, rate_from, rate_to):
    """Чистая функция для расчета."""
    if rate_from == 0:
        return 0
    return (amount / rate_from) * rate_to

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    amount = 0
    from_currency = 'USD'
    to_currency = 'RUB'
    
    rates = get_rates()
    currencies = sorted(rates.keys())

    if request.method == 'POST':
        try:
            # Получаем сумму и преобразуем в float
            amount = float(request.form.get('amount'))
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')

            # >>> НОВАЯ ПРОВЕРКА НА ОТРИЦАТЕЛЬНОЕ ЧИСЛО <<<
            if amount < 0:
                result = "Ошибка: Сумма не может быть отрицательной!"
            else:
                rate_from = rates[from_currency]
                rate_to = rates[to_currency]
                
                converted_amount = calculate_currency(amount, rate_from, rate_to)
                result = f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
            
        except ValueError:
            result = "Пожалуйста, введите корректное число!"
        except KeyError:
            result = "Ошибка выбора валюты."

    return render_template('index.html', 
                           result=result, 
                           currencies=currencies,
                           default_from=from_currency,
                           default_to=to_currency,
                           # Передаем введенное значение обратно в форму, чтобы оно не стиралось при ошибке
                           saved_amount=request.form.get('amount', '')
                           )

if __name__ == '__main__':
    app.run(debug=True)
