#!/bin/bash
LANG=ko_KR.utf8

PRO_NM="manager"
pid_chk=`ps -ef |grep "${PRO_NM}" |grep -v grep |wc -l`

if [[ ${pid_chk} -eq  0 ]]; then
echo "실행중인 프로세스가 없습니다."
exit
fi

echo "프로세스 종료 중"
for (( i=0; i <= 10; i++ )); do
kill `ps -ef | grep "${PRO_NM}" |grep -v grep |awk '{print $2}'`
echo "."
sleep 1s 

pid_chk=`ps -ef |grep "${PRO_NM}" |grep -v grep |wc -l`
if [[ ${pid_chk} -eq 0 ]]; then
echo -e "프로세스 종료 성공 하였습니다."
exit
fi

if [[ ${i} -eq 9 ]];then
kill -9 `ps -ef | grep "${PRO_NM}" |grep -v grep |awk '{print $2}'`
echo -e "프로세스 강제 종료 하였습니다."
sleep 2s
ps -ef |grep "${PRO_NM}" |grep -v grep
exit
fi
done
