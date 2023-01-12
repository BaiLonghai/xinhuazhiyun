# -*- coding: utf-8 -*-
import threading
import time

import requests
import yaml
import os
from collections import namedtuple
import platform    # For getting the operating system name
import re

# 定义网络状态
NetworkState = namedtuple("NetworkState", ["status", "latency"])


def check_server_network(server_name, server_ip, timeout):
    """
    检查服务器网络状态
    :param server_name: 服务器名称
    :param server_ip: 服务器IP
    :param timeout: 检查超时时间
    :return: NetworkState
    """
    # 定义网络不通状态
    network_down = NetworkState("down", 0)

    # 检查服务器IP是否可以访问
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = os.popen('ping {} 1 {}'.format(param, server_ip)).read()
        print(result)
        if 'ttl' in result or 'TTL' in result:
            time = float(re.findall('time=(.*)ms', result)[0])
        else:
            return network_down
    except:
        return network_down

    # 返回网络状态
    return NetworkState("up", time/1000)


def monitor_server(server_name, server_ip, check_interval, timeout, silent_time, dingtalk_api):
    """
    监控服务器网络
    :param server_name: 服务器名称
    :param server_ip: 服务器IP
    :param check_interval: 检查间隔
    :param timeout: 超时时间
    :param silent_time: 沉默时间
    :param dingtalk_api: 钉钉API
    """
    # 设置报警次数
    alarm_count = 0

    # 设置网络状态
    network_state = NetworkState("up", 0)

    while True:
        # 获取当前时间
        current_time = time.localtime()

        # 检查当前时间是否在沉默时间内
        if silent_time[0] <= current_time.tm_hour <= silent_time[1]:
            # 清空报警次数
            alarm_count = 0
            # 等待下一个检查周期
            time.sleep(check_interval)
            continue

        # 检查网络状态
        new_state = check_server_network(server_name, server_ip, timeout)

        # 判断网络是否联通
        if new_state.status == 'down':
            # 网络不通，发送报警
            send_dingtalk_alarm(f"{server_name}网络不通", dingtalk_api)
            network_state = NetworkState("down", 0)
            alarm_count += 1
            if alarm_count == 3:
                # 连续报警，发送报警
                send_dingtalk_alarm(f"{server_name}连续报警{alarm_count}次", dingtalk_api)
                # 清空报警次数
                alarm_count = 0
            # 等待下一个检查周期
            time.sleep(check_interval)
            continue

        # 判断网络是否恢复
        if new_state.status == "up" and network_state.status == "down":
            # 网络恢复，发送恢复报警
            send_dingtalk_alarm(f"{server_name}网络恢复", dingtalk_api)
            # 清空报警次数
            alarm_count = 0
            network_state = NetworkState("up", 0)

        # 判断网络延迟是否超时
        if new_state.latency > timeout:
            # 网络延迟超时，发送报警
            send_dingtalk_alarm(f"{server_name}网络延迟为{new_state.latency*1000:.2f}ms", dingtalk_api)
        # 等待下一个检查周期
        time.sleep(check_interval)


def send_dingtalk_alarm(message, dingtalk_api):

    # 构建请求数据
    data = {
        'msgtype': 'text',
        'text': {
            'content': message
        }
    }

    # 发送报警信息
    response = requests.post(dingtalk_api, json=data)
    if response.status_code == 200:
        print('报警信息发送成功')
    else:
        print('报警信息发送失败')


def main():
    # 读取配置文件
    with open("config.yaml", encoding='utf8') as f:
        config = yaml.safe_load(f)
        f.close()

    # 解析配置参数
    check_interval = config["checkInterval"]
    if check_interval[-1] == 'h':  # 小时
        check_interval = int(check_interval[:-1]) * 3600
    elif check_interval[-1] == 'm':  # 分钟
        check_interval = int(check_interval[:-1]) * 60
    elif check_interval[-2:] == 'ms':  # 毫秒
        check_interval = int(check_interval[:-2])/1000
    elif check_interval[-1] == 's':  # 秒
        check_interval = int(check_interval[:-1])
    else:
        check_interval = int(check_interval)

    timeout = config["timeout"]
    if timeout[-1] == 'h':  # 小时
        timeout = int(timeout[:-1]) * 3600
    elif timeout[-1] == 'm':  # 分
        timeout = int(timeout[:-1]) * 60
    elif timeout[-2:] == 'ms':  # 毫秒
        timeout = int(timeout[:-2]) / 1000
    elif timeout[-1] == 's':  # 秒
        timeout = int(timeout[:-1])
    else:
        timeout = int(timeout)

    silent_time = config["silentTime"]

    # 解析服务器列表
    servers = []
    for project in config["project"]:
        for site in project["site"]:
            servers.append(
                (
                    f"{project['name']}-{site['name']}",
                    site["ip"],
                    check_interval,
                    timeout,
                    [int(i) for i in silent_time.split('-')],
                    project["dingtalk"]
                )
            )

    # 启动服务器监控线程
    for server in servers:
        threading.Thread(
            target=monitor_server,
            args=server,
            #daemon=True
        ).start()


# 主线程循环
if __name__ == '__main__':
    main()
