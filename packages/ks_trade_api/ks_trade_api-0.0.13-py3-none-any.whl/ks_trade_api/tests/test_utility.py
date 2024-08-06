from ks_trade_api.utility import get_rth_flag
from datetime import time
from ks_trade_api.constant import RthFlag

pre_rth_time = time(9,29,59,999)
rth_time = time(15,59,59,999)
post_rth_time = time(19,59,59,999)
night_rth_time1 = time(23,59,59,999)
night_rth_time2 = time(3,59,59,999)

assert(get_rth_flag(pre_rth_time) == RthFlag.PRE_RTH)
assert(get_rth_flag(rth_time) == RthFlag.RTH)
assert(get_rth_flag(post_rth_time) == RthFlag.POST_RTH)
assert(get_rth_flag(night_rth_time1) == RthFlag.NIGHT)
assert(get_rth_flag(night_rth_time2) == RthFlag.NIGHT)