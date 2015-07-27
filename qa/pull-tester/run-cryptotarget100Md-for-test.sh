#!/bin/bash
# Copyright (c) 2013 The Cryptotarget100M Core developers
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
DATADIR="/home/sb/crt100m/cryptotarget100M/.cryptotarget100M"
rm -rf "$DATADIR"
mkdir -p "$DATADIR"/regtest
touch "$DATADIR/regtest/debug.log"
tail -q -n 1 -F "$DATADIR/regtest/debug.log" | grep -m 1 -q "Done loading" &
WAITER=$!
PORT=`expr $BASHPID + 10000`
"/home/sb/crt100m/cryptotarget100M/src/cryptotarget100Md" -connect=0.0.0.0 -datadir="$DATADIR" -rpcuser=user -rpcpassword=pass -listen -keypool=3 -debug -debug=net -logtimestamps -port=$PORT -regtest -rpcport=`expr $PORT + 1` &
CRYPTOTARGET100MD=$!

#Install a watchdog.
(sleep 10 && kill -0 $WAITER 2>/dev/null && kill -9 $CRYPTOTARGET100MD $$)&
wait $WAITER

if [ -n "$TIMEOUT" ]; then
  timeout "$TIMEOUT"s "$@" $PORT
  RETURN=$?
else
  "$@" $PORT
  RETURN=$?
fi

(sleep 15 && kill -0 $CRYPTOTARGET100MD 2>/dev/null && kill -9 $CRYPTOTARGET100MD $$)&
kill $CRYPTOTARGET100MD && wait $CRYPTOTARGET100MD

# timeout returns 124 on timeout, otherwise the return value of the child
exit $RETURN
