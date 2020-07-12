TEXT="abcdefg往"
LC_CTYPE=C
case $TEXT in
  *[![:cntrl:][:print:]]*) echo "Contain Non-ASCII";;
esac
