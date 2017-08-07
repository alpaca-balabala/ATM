from ATM.db.dbhelper import *
from ATM.conf.view_template import *
from ATM.core import bankcard
from ATM.core import atm_main
import time


def show_time_page(func):
    def wrapper():
        current_time = time.strftime("%Y:%m:%d", time.localtime())
        current_week = time.asctime().split(" ")[0]
        print(index_default_menu.format(current_time, current_week))
        return func()
    return wrapper()


@show_time_page
def login():
    print("ATM登录".center(73, "="))
    ipt_card_no = input("卡号：").strip()
    if is_in_db(ipt_card_no):
        while True:
            ipt_card_pwd = input("密码：").strip()
            if not ipt_card_pwd:
                continue
            else:
                ipt_card_pwd = int(ipt_card_pwd)
            if (ipt_card_pwd == query_card_info(ipt_card_no)["card_pwd"]) \
                    and (query_card_info(ipt_card_no)["card_status"] == 1):
                print(massage_info.format("登陆成功！"))
                """实例化当前用户的信用卡"""
                current_card = bankcard.CreditCard(ipt_card_no, query_card_info(ipt_card_no))
                atm_main.run(current_card)
                break
            elif (ipt_card_pwd == query_card_info(ipt_card_no)["card_pwd"]) \
                    and (query_card_info(ipt_card_no)["card_status"] == 0):
                print(massage_info.format("账户被冻结，请到用户中心办理解锁业务！"))
                break
            else:
                print(massage_info.format("密码错误！"))
                continue
    else:
        print(massage_info.format("账户不存在！"))
