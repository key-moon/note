gcc -O3 crack.c -o crack

for i in {0..7}
do
  rm -r res_128_$i.txt
  ./crack 128 $i &
done

sleep infinity
