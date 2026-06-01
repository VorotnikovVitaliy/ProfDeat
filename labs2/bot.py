import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time

# --- КОНФИГУРАЦИЯ ---
TOKEN = 'vk1.a.B9LZthRxdcb95NcPObEjfpWqn9UBDuT_vepPP2OVF68mmHjPP9LR8Okts_TV_pVY57SbApAWqLDIFFbKO1TOjjwi2w1AYI0GQL2q8oeFmksl0arBTkYNaIGphKM_CrbjJL2rlMeGY-2gnAhoDI25jcMZEy3edUrQSkBu9B_CS9TBxBAnWDeo7gwNgrZ_0LfQziZMDeqe-PZVuOQvWxe_SA'  # Вставь свой токен

# --- БАЗА ЗНАНИЙ (FAQ) ---
FAQ_DATABASE = {
    "привет": "Привет! Я бот-помощник первокурсника. 🎓\n\nСпроси меня о:\n- Расписании\n- Общежитии\n- Стипендии\n- Деканате\n- Столовой",
    "расписание": "📅 Расписание занятий доступно в личном кабинете на сайте вуза и на стенде 1-го этажа главного корпуса.",
    "общежитие": "🏠 Заявления на общежитие принимаются в деканате до 1 сентября. Нужен паспорт и справка о составе семьи.",
    "стипендия": "💰 Академическая стипендия назначается после первой сессии при отсутствии троек. Социальная — для льготников.",
    "деканат": "🏢 Деканат: корпус А, каб. 101. Работает Пн-Пт с 9:00 до 17:00.",
    "столовая": "🍔 Столовая в главном корпусе на 2-м этаже. Студенческие обеды доступны по льготной цене.",
    "помощь": "Напиши ключевое слово: 'расписание', 'общежитие', 'стипендия', 'деканат' или 'столовая'."
}

# Множество для хранения ID пользователей, которые уже получали приветствие
welcomed_users = set()

def get_answer(user_message):
    """Поиск ответа в базе знаний"""
    msg_lower = user_message.lower().strip()
    
    for key, value in FAQ_DATABASE.items():
        if key in msg_lower:
            return value
            
    return "Я пока не знаю ответа на этот вопрос. 😕 Попробуй написать 'помощь', чтобы увидеть список тем."

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    
    print("Бот запущен. Ожидание сообщений...")

    try:
        for event in longpoll.listen():
            # Реагируем только на новые сообщения в личку от пользователя
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
                
                user_id = event.user_id
                user_message = event.text
                
                # Проверяем, является ли пользователь новым
                if user_id not in welcomed_users:
                    # Отправляем приветственное сообщение
                    welcome_text = (
                        f"Привет, первокурсник! 👋\n"
                        f"Я твой виртуальный помощник.\n\n"
                        f"Задай мне вопрос или выбери тему из списка:\n"
                        f"- Расписание\n"
                        f"- Общежитие\n"
                        f"- Стипендия\n"
                        f"- Деканат\n"
                        f"- Столовая"
                    )
                    
                    vk_session.method('messages.send', {
                        'user_id': user_id,
                        'message': welcome_text,
                        'random_id': 0
                    })
                    
                    # Добавляем пользователя в список "приветствованных"
                    welcomed_users.add(user_id)
                
                # Если сообщение не пустое и не является триггером на само приветствие (опционально)
                # Можно обработать обычный запрос
                if user_message.strip(): 
                    response = get_answer(user_message)
                    
                    # Если ответ совпадает с приветствием, не дублируем его сразу же, 
                    # но в данном случае логика простая: сначала приветствие, потом ответ на запрос
                    
                    vk_session.method('messages.send', {
                        'user_id': user_id,
                        'message': response,
                        'random_id': 0
                    })

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
        main()

if __name__ == '__main__':
    main()
