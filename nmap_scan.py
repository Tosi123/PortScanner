# -*- coding: utf-8 -*-

import time
import nmap
import json
import logging
from logging import handlers

# -sP Ping Check
# -T(1~5) 속도 5가 제일 빠름
# -sS Syn/Ack 응답이 오면 그포트는 열려있는 상태 스텔스 스캔
# -sV 서버나 데몬 버전 출력
# -A 운영체제 탐지, 버전 탐지, script scanning, traceroute 기능
# -v 좀더 많은 정보
# -O 운영체제 탐지 기능을 활성화


class ScanManager:

    def __init__(self):
        self.address = ['127.0.0.1']
        self.port = ''
        self.scanner = nmap.PortScanner()
        self.json_base = None

    def ping_check(self):
        ''' Health Check 함수
            Args:
                address (list)  Scan IP 리스트
            Return:
                [{'ip': '(str)', 'hostname': '(str)', 'mac': '(str)', 'status': '(str)', 'time': '(str)'}]
        '''
        result = []

        try:
            if str(type(self.address)) == "<class 'list'>":
                logging.info(
                    "Nmap Ping Check List: {list}".format(list=self.address))
                for ip in self.address:
                    # Nmap Start
                    self.scanner.scan(ip, arguments='-sP -v')
                    logging.debug("Nmap Command: {cmd}".format(
                        cmd=self.scanner.command_line()))
                    # Host 1개씩 dict로 만든 후 List 입력
                    for host in self.scanner.all_hosts():
                        check_data = {}
                        # Mac Addresses 존재 여부 확인
                        if "mac" in self.scanner[host]['addresses']:
                            check_data = {'ip': host, 'hostname': self.scanner[host].hostname(
                            ), 'mac': self.scanner[host]['addresses']['mac'], 'status': self.scanner[host].state(), 'time': time.strftime('%Y%m%d%H%M%S')}
                            logging.info("{ip} Host Name: {val}".format(
                                ip=host, val=self.scanner[host].hostname()))
                            logging.info("{ip} Status: {val}".format(
                                ip=host, val=self.scanner[host].state()))
                            logging.info("{ip} MAC Addresses: {val}".format(
                                ip=host, val=self.scanner[host]['addresses']['mac']))
                            logging.debug("{ip} Check Data: {val}".format(
                                ip=host, val=check_data))
                        # Mac Addresses 없을시 Null 처리
                        else:
                            check_data = {'ip': host, 'hostname': self.scanner[host].hostname(
                            ), 'mac': '', 'status': self.scanner[host].state(), 'time': time.strftime('%Y%m%d%H%M%S')}
                            logging.info("{ip} Host Name: {val}".format(
                                ip=host, val=self.scanner[host].hostname()))
                            logging.info("{ip} Status: {val}".format(
                                ip=host, val=self.scanner[host].state()))
                            logging.info(
                                "{ip} MAC Addresses Not Found".format(ip=host))
                            logging.debug("{ip} Check Data: {val}".format(
                                ip=host, val=check_data))
                        # 결과 데이터에 추가
                        result.append(check_data)
                        logging.info(
                            "Result Append Success: {ip}".format(ip=host))
                logging.info(
                    "Ping Check Success: Area={area}".format(area=self.address))
                logging.debug("Return Result Data: {val}".format(val=result))
                return result
            else:
                logging.error("IP Address: {area}".format(ip=self.address))
                logging.error("IP Address Is Not List Type")
                return False
        except Exception as e:
            logging.error(
                "Ping Cehck Fail: IP={ip}, Error={detail}".format(ip=self.address, detail=e))
            return False

    def port_scan(self):
        ''' Port Scan 함수
            Args:
                address (list)  Scan IP 리스트
            Return:
                json[{'ip': '(str)', 'hostname': '(str)', 'mac': '(str)', 'status': '(str)', 'time': '(str)'}]
        '''
        result = []

        try:
            if str(type(self.address)) == "<class 'list'>":
                logging.info(
                    "Nmap Port Scan List: {list}".format(list=self.address))
                for ip in self.address:
                    self.scanner.scan(ip, arguments='-sS -O -A')
                    logging.debug("Nmap Command: {cmd}".format(
                        cmd=self.scanner.command_line()))

                    # Host 1개씩 dict로 만든 후 List 입력
                    for host in self.scanner.all_hosts():
                        check_data = {}
                        port_data = self.json_base

                        # 디버깅용 데이터 출력
                        logging.debug("Scanner Full Data: IP={ip}, DATA={data}".format(
                            ip=host, data=self.scanner[host]))
                        # Port Scan Data 입력
                        try:
                            # TCP 데이터 입력
                            tcp_port = self.scanner[host]['tcp'].keys()
                            sorted(tcp_port)

                            for port in tcp_port:
                                data = {"port": port, "status": self.scanner[host]['tcp'][port]['state'], "name": self.scanner[host]['tcp'][port]
                                        ['name'], "product": self.scanner[host]['tcp'][port]['product'], "version": self.scanner[host]['tcp'][port]['version']}
                                port_data['protocol'][0]['tcp'].append(data)
                            json_port = json.dumps(port_data)
                            logging.info(
                                "TCP Json Dumps Success: {ip}".format(ip=host))
                        except Exception as e:
                            logging.error(
                                "TCP Error: IP={ip}, Error={e}".format(ip=host, e=e))

                        # OS 데이터가 있는지 확인
                        os_data = self._os_check(host)

                        # Mac Addresses 존재 여부 확인
                        if "mac" in self.scanner[host]['addresses']:
                            check_data = {'ip': host, 'hostname': self.scanner[host].hostname(
                            ), 'mac': self.scanner[host]['addresses']['mac'], 'os': os_data['os'], 'model': os_data['model'], 'port_data': json_port, 'status': self.scanner[host].state(), 'time': time.strftime('%Y%m%d%H%M%S')}
                            logging.info("{ip} Host Name: {val}".format(
                                ip=host, val=self.scanner[host].hostname()))
                            logging.info("{ip} Status: {val}".format(
                                ip=host, val=self.scanner[host].state()))
                            logging.info("{ip} MAC Addresses: {val}".format(
                                ip=host, val=self.scanner[host]['addresses']['mac']))
                            logging.debug("{ip} Check Data: {val}".format(
                                ip=host, val=check_data))
                        # Mac Addresses 없을시 Null 처리
                        else:
                            check_data = {'ip': host, 'hostname': self.scanner[host].hostname(
                            ), 'mac': '', 'os': os_data['os'], 'model': os_data['model'], 'port_data': json_port, 'status': self.scanner[host].state(), 'time': time.strftime('%Y%m%d%H%M%S')}
                            logging.info("{ip} Host Name: {val}".format(
                                ip=host, val=self.scanner[host].hostname()))
                            logging.info("{ip} Status: {val}".format(
                                ip=host, val=self.scanner[host].state()))
                            logging.info(
                                "{ip} MAC Addresses Not Found".format(ip=host))
                            logging.debug("{ip} Check Data: {val}".format(
                                ip=host, val=check_data))
                        # 결과 데이터에 추가
                        result.append(check_data)
                        logging.info(
                            "Result Append Success: {ip}".format(ip=host))
                logging.info(
                    "Port Scan Success: Area={area}".format(area=self.address))
                logging.debug("Return Result Data: {val}".format(val=result))
                return result
            else:
                logging.error("IP Address: {area}".format(area=self.address))
                logging.error("IP Address Is Not List Type")
                return False
        except Exception as e:
            logging.error(
                "Port Scan Fail: IP={ip}, Error={detail}".format(ip=host, detail=e))
            return False

    def _os_check(self, host):
        result = {'os': '', 'model': ''}
        try:
            logging.info("OS Data Check: {os}".format(
                os=self.scanner[host]['osmatch']))
            result['os'] = str(self.scanner[host]['osmatch'][0]['osclass'][0]['vendor']) + \
                "|" + str(self.scanner[host]['osmatch']
                          [0]['osclass'][0]['osgen'])
            result['model'] = self.scanner[host]['vendor'].get(
                self.scanner[host]['addresses']['mac'])
            return result
        except Exception as e:
            logging.warn("OS Data Error: {detail}".format(detail=e))
            return result

    def json_load(self):
        try:
            # Json File Load
            with open('./format.json', 'r') as file:
                self.json_base = json.load(file)
            logging.info("Json Load Success")
            return True
        except Exception as e:
            logging.error("Json Load Fail")
            return False
