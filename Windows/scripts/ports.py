import socket
import time
import threading
import json
import psutil
import pythoncom
import wmi
import os
import sys
from queue import Queue


def port_scan(port_list, services, processes, tcp_conns, udp_conns, arr, thread_lock):
    t_IP = '127.0.0.1'
    s = None
    if port_list[1] == "TCP":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.01)
    try:
        s.connect((t_IP, port_list[0]))
        with thread_lock:

            process = None
            try:
                process = processes[tcp_conns[port_list[0]]] if port_list[1] == "TCP" else processes[udp_conns[port_list[0]]]
            except KeyError:
                pass

            service = None
            try:
                service = services[tcp_conns[port_list[0]]] if port_list[1] == "TCP" else services[udp_conns[port_list[0]]]
            except KeyError:
                pass

            if (service == None and process == None):
                return

            arr.append({
                'portNumber': port_list[0],
                'state': 'open',
                'service': service,
                'product': process,
                'protocol': port_list[1]
            })
    except (socket.error, OSError, KeyError):
        pass



def threader(q, services, processes, tcp_conns, udp_conns, arr, thread_lock):
    while True:
        worker = q.get()
        port_scan(worker, services, processes, tcp_conns, udp_conns, arr, thread_lock)
        q.task_done()
        
        if q.empty():
            break


def get_data(filter):

    services = {}
    processes = {}
    tcp_conns = {}
    udp_conns = {}
    arr = []
    q = Queue()

    for sev in psutil.win_service_iter():
        if sev.status() == psutil.STATUS_RUNNING:
            processes[sev.pid()] = sev.name()

    for proc in psutil.process_iter(['pid', 'name']):
        services[proc.info['pid']] = proc.info['name']

    for net in psutil.net_connections(kind='tcp'):
        tcp_conns[net.laddr.port] = net.pid

    for net in psutil.net_connections(kind='udp'):
        udp_conns[net.laddr.port] = net.pid

    thread_lock = threading.Lock()

    for x in range(100):
        t = threading.Thread(target=threader, args=(q, services, processes, tcp_conns, udp_conns, arr, thread_lock))
        t.daemon = True
        t.start()

    ports = list(range(1, 65536))
    if filter == None:
        for port in ports:
            q.put([port, "TCP"])
        for port in ports:
            q.put([port, "UDP"])

    elif filter == 'tcp':
         for port in ports:
            q.put([port, "TCP"])

    elif filter == 'udp':
         for port in ports:
            q.put([port, "UDP"])

    q.join()
    pythoncom.CoInitialize()
    computer = wmi.WMI()
    return {"ports": arr }