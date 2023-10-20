#!/bin/sh

INSPECT_DIR=/var/spool/filter
SENDMAIL="/usr/sbin/sendmail -G -i"
 
EX_TEMPFAIL=75
EX_UNAVAILABLE=69

trap "rm -f in.$$" 0 1 2 3 15

cd $INSPECT_DIR || {
    echo $INSPECT_DIR does not exist; exit $EX_TEMPFAIL; }

cat >in.$$ || { 
    echo Cannot save mail to file; exit $EX_TEMPFAIL; }

# in.$$ contain the message content

# Filtering example, reject all sender that is @example.com
if [ -n "$(echo "$2" | grep '@example.com')" ]; then
    echo Message is not accepted; exit $EX_UNAVAILABLE;
fi

$SENDMAIL "$@" <in.$$

exit $?