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
        return {"RUB": 90.0, "EUR": 0.92, "KZT": 450.0, "BYN": 3.2}

def calculate_currency(amount, rate_from, rate_to):
    if rate_from == 0:
        return 0
    return (amount / rate_from) * rate_to

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    amount = 0
    from_currency = 'USD'
    to_currency = 'RUB'
    
    # Получаем текущие курсы
    rates = get_rates()
    # Список валют для выпадающего списка
    currencies = sorted(rates.keys())

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')

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
                           default_to=to_currency)

if __name__ == '__main__':
    app.run(debug=True)

    
