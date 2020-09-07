#!/usr/bin/env bash

LANG=ko_KR.utf8
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/11.2/client64/lib

###########################
PRO_NM="manager.py"
PYTHON_PATH="/usr/local/bin/python3.6"
###########################
pid_chk=`ps -ef |grep "${PRO_NM}" |grep -v grep |wc -l`

if [[ ${pid_chk} -ne  0 ]]; then
    echo "이미 프로세스가 실행중 입니다."
    exit
else
    cd ..
    nohup ${PYTHON_PATH} ./manager.py >> ./log/scanning.out 2>> ./log/scanning.err &
fi

if [[ 0 -eq $? ]]; then
sleep 3
cnt=`ps -ef |grep "${PRO_NM}" |grep -v grep |awk '{print $2}' |wc -l`
    if [[ ${cnt} -ge 3 ]];then
        echo "프로세스 정상 실행 되었습니다!! (CNT: ${cnt})"
    else
        echo "프로세스 실행 실패!!"
    fi
else
    echo "프로세스 실행 실패!!"
fi
