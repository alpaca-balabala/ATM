from ATM.db .dbhelper import *
from ATM.log.loghelper import *
import datetime


class BankCard:
    """
    属性：
        卡号:card_no
        用户名:card_user
        密码：card_pwd
        权限：card_status
    方法：
        重置密码：reset_pwd()
        更改权限：reset_status()
    """
    def __init__(self, card_no, card_info_dict):
        """银行卡类构造函数"""
        self.card_no = card_no
        self.card_user = card_info_dict["card_user"]
        self.card_pwd = card_info_dict["card_pwd"]
        self.card_status = card_info_dict["card_status"]
        self.card_total = card_info_dict["credit_card_line"]
        self.bill_total = 0

    def reset_pwd(self, value):
        """重置密码方法"""
        update_card_info(self.card_no, "card_pwd", value)

    def reset_status(self, value):
        """更改权限方法"""
        self.card_status = value

    def withdrawals(self, money):
        """取现方法"""
        self.card_total -= money
        update_card_info(self.card_no, "credit_card_line", self.card_total)

    def transfer(self, accept_obj, money):
        """转账功能"""
        self.card_total -= money
        update_card_info(self.card_no, "credit_card_line", self.card_total)
        accept_obj.card_total += money
        update_card_info(accept_obj.card_no, "credit_card_line", accept_obj.card_total)

    def deposit(self, money):
        """存款方法"""
        self.card_total += money
        update_card_info(self.card_no, "credit_card_line", self.card_total)

    def record_log(self, record_handle, record_money, record_to_obj):
        """记录写入日志"""
        now_time = str(datetime.datetime.now())
        record_list = [now_time, record_handle, record_money, record_to_obj]
        record(self.card_no, record_list)

    def show_log(self):
        """显示历史账单"""
        log_data = show_card_history(self.card_no)
        log_data1 = filter(lambda x: x[1] != "存款", show_card_history(self.card_no))    # 过滤存款记录
        self.bill_total = sum(i[2] for i in log_data)  # 计算账单金额
        return log_data1


class CreditCard(BankCard):

    def __init__(self, card_no, card_info_dict):
        """信用卡类构造方法"""
        super().__init__(card_no, card_info_dict)
        self.credit_line = card_info_dict["credit_card_line"]

    def set_cardit_line(self, value):
        """设置信用额度方法"""
        self.credit_line = value
