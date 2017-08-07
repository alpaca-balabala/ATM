import os
import json


credit_card_db_path = "".join((os.path.dirname(os.path.abspath(__file__)), "//credit_card.db"))


def query_card_info(card_no):
    """查询卡号为card_no的信息"""
    with open(credit_card_db_path, "r") as credit_card_db:
        try:
            data = json.loads(credit_card_db.read())[card_no]
            return data
        except Exception:
            pass


def create_new_card(card_no, card_user, card_pwd, card_status, credit_card_line):
    """新建银行卡"""
    new_card_dict = {"card_user": card_user,
                     "card_pwd": card_pwd,
                     "card_status": card_status,
                     "credit_card_line": credit_card_line}
    with open(credit_card_db_path, "r") as old_db:
        """新建数据添加到credit_card.db的字典中"""
        old_credit_card_db = json.loads(old_db.read())
        old_credit_card_db[card_no] = new_card_dict
    with open(credit_card_db_path, "w") as new_db:
        new_db.write(json.dumps(old_credit_card_db))


def update_card_info(card_no, key, value):
    """修改用户信息"""
    with open(credit_card_db_path, "r") as old_db:
        old_card_info = json.loads(old_db.read())
        if card_no in old_card_info:
            old_card_info[card_no][key] = value
        else:
            raise KeyboardInterrupt
    with open(credit_card_db_path, "w") as new_db:
        new_db.write(json.dumps(old_card_info))


def is_in_db(card_no):
    """判断卡号是否存在"""
    with open(credit_card_db_path, "r") as card_db:
        card_db_info = json.loads(card_db.read())
        if card_no in card_db_info:
            return True
        else:
            return False
