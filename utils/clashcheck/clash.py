import os
import yaml
import flag
import socket
import maxminddb
import platform
import psutil
import requests
from tqdm import tqdm
from pathlib import Path


def push(list, outfile):
    country_count = {}
    count = 1
    clash = {'proxies': [], 'proxy-groups': [
            {'name': 'automatic', 'type': 'url-test', 'proxies': [], 'url': 'https://www.google.com/favicon.ico',
             'interval': 300}, {'name': '🌐 Proxy', 'type': 'select', 'proxies': ['automatic']}],
             'rules': ['MATCH,🌐 Proxy']}
    with maxminddb.open_database('Country.mmdb') as countrify:
        for i in tqdm(range(int(len(list))), desc="Parse"):
            x = list[i]
            try:
                float(x['password'])
            except:
                try:
                    float(x['uuid'])
                except:
                    try:
                        ip = str(socket.gethostbyname(x["server"]))
                    except:
                        ip = str(x["server"])
                    try:
                        country = str(countrify.get(ip)['country']['iso_code'])
                    except:
                        country = 'UN'
                    flagcountry = country
                    try:
                        country_count[country] = country_count[country] + 1
                        x['name'] = str(flag.flag(flagcountry)) + " " + country + " " + str(count)
                    except:
                        country_count[country] = 1
                        x['name'] = str(flag.flag(flagcountry)) + " " + country + " " + str(count)
                    clash['proxies'].append(x)
                    clash['proxy-groups'][0]['proxies'].append(x['name'])
                    clash['proxy-groups'][1]['proxies'].append(x['name'])
                    count = count + 1

    with open(outfile, 'w') as writer:
        yaml.dump(clash, writer, sort_keys=False)


def checkenv():
    operating_system = str(platform.system() + '/' +  platform.machine() + ' with ' + platform.node())
    print('Try to run Clash on '+ operating_system)
    if operating_system.startswith('Darwin'):
        if 'arm64' in operating_system:
            clashname='./clash-darwin-arm64'
        elif 'x86_64' in operating_system:
            clashname='./clash-darwin-amd64'
        else:
            print('System is supported(Darwin) but Architecture is not supported.')
            exit(1)
    elif operating_system.startswith('Linux'):
        if 'x86_64' in operating_system:
            clashname='./clash-linux-amd64'
        elif 'aarch64' in operating_system:
            clashname='./clash-linux-arm64'
        else:
            print('System is supported(Linux) but Architecture is not supported.')
            exit(1)
    elif operating_system.startswith('Windows'):
        if 'AMD64' in operating_system:
            clashname='clash-windows-amd64.exe'
        else:
            print('System is supported(Windows) but Architecture is not supported.')
            exit(1)
    else:
        print('System is not supported.')
        exit(1)

    return clashname, operating_system


def checkuse(clashname, operating_system):
    pids = psutil.process_iter()
    for pid in pids:
        if(pid.name() == clashname):
            if operating_system.startswith('Darwin'):
                os.kill(pid.pid,9)
            elif operating_system.startswith('Linux'):
                os.kill(pid.pid,9)
            elif operating_system.startswith('Windows'):
                os.popen('taskkill.exe /pid:'+str(pid.pid))
            else:
                print(clashname, str(pid.pid) + " ← kill to continue")
                exit(1)


def filter(config):
    list = config["proxies"]
    ss_supported_ciphers = ['aes-128-gcm', 'aes-192-gcm', 'aes-256-gcm', 'aes-128-cfb', 'aes-192-cfb', 'aes-256-cfb', 'aes-128-ctr', 'aes-192-ctr', 'aes-256-ctr', 'rc4-md5', 'chacha20', 'chacha20-ietf', 'xchacha20', 'chacha20-ietf-poly1305', 'xchacha20-ietf-poly1305']
    ssr_supported_obfs = ['plain', 'http_simple', 'http_post', 'random_head', 'tls1.2_ticket_fastauth', 'tls1.2_ticket_auth']
    ssr_supported_protocol = ['origin', 'auth_sha1_v4', 'auth_aes128_md5', 'auth_aes128_sha1', 'auth_chain_a', 'auth_chain_b']
    vmess_supported_ciphers = ['auto', 'aes-128-gcm', 'chacha20-poly1305', 'none']
    iplist = {}
    passlist = []
    count = 1
    clash = {'proxies': [], 'proxy-groups': [
            {'name': 'automatic', 'type': 'url-test', 'proxies': [], 'url': 'https://www.google.com/favicon.ico',
             'interval': 300}, {'name': '🌐 Proxy', 'type': 'select', 'proxies': ['automatic']}],
             'rules': ['MATCH,🌐 Proxy']}
    with maxminddb.open_database('Country.mmdb') as countrify:
        for i in tqdm(range(int(len(list))), desc="Parse"):
            try:
                x = list[i]
                authentication = ''
                x['port'] = int(x['port'])
                if x['password'].isdigit():
                    x['password'] = int(x['password'])
                try:
                    ip = str(socket.gethostbyname(x["server"]))
                except:
                    ip = x['server']
                try:
                    country = str(countrify.get(ip)['country']['iso_code'])
                except:
                    country = 'UN'
                if x['type'] == 'ss':
                    try:
                        if x['cipher'] not in ss_supported_ciphers:
                            ss_omit_cipher_unsupported = ss_omit_cipher_unsupported + 1
                            continue
                        if ip in iplist:
                            ss_omit_ip_dupe = ss_omit_ip_dupe + 1
                            continue
                        else:
                            iplist[ip] = []
                            iplist[ip].append(x['port'])
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SSS'
                        authentication = 'password'
                    except:
                        continue
                elif x['type'] == 'ssr':
                    try:
                        if x['cipher'] not in ss_supported_ciphers:
                            continue
                        if x['obfs'] not in ssr_supported_obfs:
                            continue
                        if x['protocol'] not in ssr_supported_protocol:
                            continue
                        if ip in iplist:
                            continue
                        else:
                            iplist.append(ip)
                            iplist[ip].append(x['port'])
                        authentication = 'password'
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SSR'
                    except:
                        continue
                elif x['type'] == 'vmess':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        if x['cipher'] not in vmess_supported_ciphers:
                            continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'VMS'
                        authentication = 'uuid'
                    except:
                        continue
                elif x['type'] == 'trojan':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'TJN'
                        authentication = 'password'
                    except:
                        continue
                elif x['type'] == 'snell':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SNL'
                        authentication = 'psk'
                    except:
                        continue
                elif x['type'] == 'http':
                    try:
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'HTT'
                        # authentication = 'userpass'
                    except:
                        continue
                elif x['type'] == 'socks5':
                    try:
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SK5'
                        # authentication = 'userpass'
                    except:
                        continue
                else:
                    continue

                if ip in iplist and x['port'] in iplist[ip]:
                    if x[authentication] in passlist:
                        continue
                    else:
                        passlist.append(x[authentication])
                else:
                    try:
                        iplist[ip].append(x['port'])
                    except:
                        iplist[ip] = []
                        iplist[ip].append(x['port'])

                clash['proxies'].append(x)
                clash['proxy-groups'][0]['proxies'].append(x['name'])
                clash['proxy-groups'][1]['proxies'].append(x['name'])
                count = count + 1

            except:
                #print('shitwentwrong' + str(x))
                continue

    return clash
