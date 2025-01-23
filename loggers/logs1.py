import logging

# Логгирование ошибок при отправке сообщений
def log_error_w_sending(cur_id, error):
    logging.error(f"Не удалось отправить сообщение пользователю с ID {cur_id}: {error}")