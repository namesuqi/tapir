**客户端自动测试执行手册**
---------------------------------------
#注意事项
    执行前确保测试代码是最新的。
    执行前确保SDK机器的域名解析正确。
    执行前确保SDK版本号和Push服务器版本号正确。
    执行过程中出现的错误不要轻易放过，不要因为重跑一遍后通过了，就轻易放过之前发现的潜在问题。
    在tapir目录执行用例：python testsuite/protocol/puff/testcase.py
    正式执行机器ip地址：192.168.4.234， 192.168.4.235

#用例执行
###puff协议测试
    模拟雷锋和LivePush交互，验证puff协议
    测试用例：testsuite/protocol/puff
    测试数据: lib/protocol/puff/puff_data.py
    数据调整：FILE_URL_DEFAULT, FILE_URL_TEST3, FILE_URL_NOT_EXIST,LIVE_PUSH_HOST

###nat穿透自动化
    通过nat_simulator模拟各种nat环境，验证:
        1.sdk探测的nat类型是否与预期类型相符。
        2.各nat类型的sdk间能否成功穿透。
    测试用例: tapir/testsuite/linux/penetrate/penetrate.py
    测试数据: tapir/lib/sdk/penetrate/pene_constant.py
    数据调整: CHANNEL为能播放的频道
    本地SDK路径：tapir/misc/sdk/daily_routine/ys_service_static
    (备注: 执行穿透自动测试时需要保证测试环境控制面部署可用，stun与sdk版本)

###linux init用例执行
    检验SDK peer_id、port、yunshang file
    测试用例：tapir/testsuite/linux/int
    测试数据：tapir/lib/sdk/sdk_constant.py
    数据调整：REMOTE_SDK_IP, EXPECT_SDK_VERSION,
    SDK目录：tapir/misc/sdk/daily_routine/ys_service_static

###linux login用例执行
    检验SDK login
    测试用例：tapir/testsuite/linux/login/login.py
    测试数据：tapir/lib/sdk/sdk_constant.py
    数据调整：REMOTE_SDK_IP
    SDK目录：tapir/misc/sdk/daily_routine/ys_service_static

#后续计划