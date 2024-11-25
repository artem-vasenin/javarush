from datetime import datetime
import json
import os.path

from .get_pers_msgs import get_pers_msgs

def save_personal_msg_to_db(login_from: str, login_to: str, msg: str)-> tuple[str, str]:
    """ Сохранение нового сообщения для пользователя в базу данных """
    msgs, msgs_err = get_pers_msgs()

    item = {
        'from': login_to,
        'message': msg,
        'was_read': False,
        'was_answered': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    msgs[login_from] = [item] if (not msgs and msgs_err) or login_from not in msgs else [*msgs[login_from], item]

    with open(os.path.join(os.getcwd(), "messages", "messages.json"), 'w', encoding="utf-8") as file:
        json.dump(msgs, file, indent=2, ensure_ascii=False)

    return 'Сообщение успешно отправлено', ''