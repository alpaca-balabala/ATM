import os
import json

user_history_log_path = "".join((os.path.dirname(os.path.abspath(__file__)), "//user_history_log.db"))


def record(card_no, record_list):
    with open(user_history_log_path, "r") as old_log:
        data = json.loads(old_log.read())
        if is_card_exist(card_no):
            data[card_no].append(record_list)
        else:
            data[card_no] = []
            data[card_no].append(record_list)
    with open(user_history_log_path, "w") as new_log:
        new_data = data
        new_log.write(json.dumps(new_data))


def show_card_history(card_no):
    with open(user_history_log_path, "r") as log:
        data = json.loads(log.read())[card_no]
        return data


def is_card_exist(card_no):
    with open(user_history_log_path, "r") as log:
        data = json.loads(log.read())
        if card_no in data:
            return True
        else:
            return False
