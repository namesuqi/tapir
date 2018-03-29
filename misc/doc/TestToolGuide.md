**测试工具使用手册**
---------------------------------------
#注意事项
    工具目录：misc/tools
    执行方法：python misc/tools/tool_name/main.py
    发现问题，及时反馈

#工具使用
###本地多SDK播放工具
    本地启动指定个数的节点（可以用做播放节点，也可以用做雷锋节点）
    测试工具：misc/tools/local_sdk_play
    环境准备：sdk文件ys_service_static放在该工具目录下
    测试数据：misc/tools/local_sdk_play/main.py [start|stop]
    数据调整：SDK_NUM：启动多少个SDK, URL：播放频道的url, START_PLAYER：是否启动fake player

###远程多SDK启动工具（仅支持一台远程机器）
    远程1台机器上启动指定个数的节点（用做雷锋节点）
    测试工具：misc/tools/remote_sdk_start
    环境准备：sdk文件ys_service_static放在/misc/sdk/linux目录下
    测试数据：misc/tools/remote_sdk_start/main.py [start|stop]
    数据调整：SDK_NUM：启动多少个SDK, SDK_IP:远程SDK机器IP地址
    
###获取多SDK Peer ID的工具（仅支持一台远程机器）
    获得1台机器上指定个数的节点的Peer ID
    测试工具：misc/tools/remote_peer_id
    环境准备：远程SDK是使用remote_sdk_start工具启动的
    测试数据：misc/tools/remote_peer_id/main.py
    数据调整：BY_HTTP:是否使用http接口来获得数据，SDK_NUM：启动多少个SDK, SDK_IP:远程SDK机器IP地址




#后续计划

