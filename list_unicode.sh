#!/bin/bash

# Usage: ./list_unicode.sh
#
# this script gets all the (non-BMP) unicode points being used in
# the source document (it assumes utf-8 for the input).  It can also
# generate a range of unicode points  The output is
# suitable for the iswa_graphite script


while getopts "s:f:l:" opt; do
  case $opt in
    s) DOCUMENT=$OPTARG
       ;;
		f) FIRST=$OPTARG
			 ;;
		l) LAST=$OPTARG
			 ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# sanity check

if [[ -n $FIRST ]] && [[ -n $LAST ]]
then
	if (($LAST > $FIRST))
	then
		LAST=$(printf "%d" $LAST)
		FIRST=$(printf "%d" $FIRST)
		for i in $(eval echo {$FIRST..$LAST})
		do
			printf "%X\n" $i
		done
	else
		echo "Wrong range: $FIRST - $LAST" >&2
	fi
else
	iconv -f utf8 -t utf32be $DOCUMENT | hexdump -v -e '4/1 "%02X" "\n"' | grep -v ^000000 | sort | uniq
fi
