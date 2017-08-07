from ATM.conf.view_template import *
from ATM.db.dbhelper import *
from ATM.core import bankcard
import time


def run(card_obj):

    while True:
        print(index_ATM.format(cardno=card_obj.card_no, carduser=card_obj.card_user, avail=card_obj.card_total))
        ipt_choice = input("请输入功能选项：").strip()
        if ipt_choice == "1":
            """我的信用卡"""
            mycard(card_obj)
            # continue
        elif ipt_choice == "2":
            """提现"""
            my_withdrawals(card_obj)
        elif ipt_choice == "3":
            """转账"""
            my_transfer(card_obj)
        elif ipt_choice == "4":
            """存款/还款"""
            my_deposit(card_obj)
        elif ipt_choice == "5":
            """退卡"""
            print(massage_info.format("程序结束！"))
            exit()


def mycard(card_obj):
    """
    我的信用卡功能
        查看历史账单
        修改密码
        返回上一层
    """
    print(card_info.format(cardno=card_obj.card_no, owner=card_obj.card_user,
                           total=card_obj.credit_line, balance=1000,
                           status=card_obj.card_status))
    print("功能选项".center(73, "*"))
    mycard_opt_list = ["查看历史账单", "修改密码", "返回"]
    for i, j in enumerate(mycard_opt_list):
        print(i + 1, j)
    while True:
        ipt_choice_1 = input("请输入功能选项：").strip()
        if ipt_choice_1 == "1":
            """查看历史账单"""
            my_log(card_obj)
            break
        elif ipt_choice_1 == "2":
            """修改密码功能"""
            print("密码修改".center(73, "*"))
            ipt_old_pwd = int(input("请输入原密码：").strip())
            if ipt_old_pwd == card_obj.card_pwd:
                ipt_new_pwd = int(input("请输入新密码：").strip())
                card_obj.reset_pwd(ipt_new_pwd)   # 调用对象的绑定方法
                print(massage_info.format("操作成功！"))
                time.sleep(2)   # 延迟2秒模拟数据处理的真实操作
                break
            else:
                print(massage_info.format("原密码输入错误！"))
        elif ipt_choice_1 == "3":
            break


def my_log(card_obj):
    """查看历史账单，前端逻辑"""
    data_log = card_obj.show_log()
    print(card_log.format(bill_total=card_obj.bill_total))
    for i in data_log:
        print(i)


def my_withdrawals(card_obj):
    """取现功能，前端逻辑"""
    ipt_withdrawals_money = int(input("请输入取现金额：").strip())
    if ipt_withdrawals_money <= card_obj.card_total:
        card_obj.withdrawals(ipt_withdrawals_money)
        card_obj.record_log("取款", ipt_withdrawals_money, "ATM机")
        print(massage_info.format("验钞中，请耐心等待"))
        time.sleep(2)
        print(massage_info.format("操作成功,请尽快取走现金！"))
    else:
        print(massage_info.format("您的余额不足，请重新确认取现金额！"))


def my_transfer(card_obj):
    """转账功能，前端逻辑"""
    ipt_accept_card_no = input("请输入转账卡号：").strip()
    if is_in_db(ipt_accept_card_no):
        accept_card = bankcard.CreditCard(ipt_accept_card_no, query_card_info(ipt_accept_card_no))
        ipt_transfer_money = int(input("请输入转账金额：").strip())
        if ipt_transfer_money <= card_obj.card_total:
            card_obj.transfer(accept_card, ipt_transfer_money)
            card_obj.record_log("转账", ipt_transfer_money, accept_card.card_no)
            print(massage_info.format("转账成功！"))
        else:
            print(massage_info.format("您的余额不足，请重新确认转账金额！"))
    else:
        print(massage_info.format("卡号不存在，请重新输入！"))


def my_deposit(card_obj):
    """存款功能，前端逻辑"""
    ipt_deposit_money = int(input("请放入金额：").strip())
    print(massage_info.format("验钞中，请等待。。。"))
    time.sleep(3)
    card_obj.deposit(ipt_deposit_money)
    card_obj.record_log("存款", ipt_deposit_money, "ATM机")
    print(massage_info.format("存款成功！"))
