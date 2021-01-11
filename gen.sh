#!/bin/bash

echo "############## DESTINATION ##############"

for i in {1..72}
do
#echo $i
ii=`expr $i - 1`
#echo $ii
#printf "%x\n" $ii
echo "<input form=\"take\" id=\"out"$i"\" type=\"radio\" name=\"destination\" value=\"`printf "%x\n" $ii`""\"><label for=\"out"$i"\" class=\"out"$i"-label four col\">OUTPUT $i</label>"
done

echo "############## SOURCE ##############"

for i in {1..72}
do
#echo $i
ii=`expr $i - 1`
#echo $ii
#printf "%x\n" $ii
echo "<input form=\"take\" id=\"in"$i"\" type=\"radio\" name=\"source\" value=\"`printf "%x\n" $ii`""\"><label for=\"in"$i"\" class=\"in"$i"-label four col\">INPUT $i</label>"
done
