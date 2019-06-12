import random
import time
import uuid


# 产生16位的UUID字符串
def generate_shop_uuid():
    tmp = str(uuid.uuid4())
    return ''.join(tmp.split('-')[0:3])


# 订单编号
def showcreate_order(uid):
    return "{time_str}{uid}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                             uid=uid,
                                             ran_str=random.randint(10, 99),
                                             )
