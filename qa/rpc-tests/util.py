# Copyright (c) 2014 The Cryptotarget100M Core developers
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Helpful routines for regression testing
#

# Add python-cryptotarget100Mrpc to module search path:
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-cryptotarget100Mrpc"))

from decimal import Decimal
import json
import shutil
import subprocess
import time

from cryptotarget100Mrpc.authproxy import AuthServiceProxy, JSONRPCException
from util import *

START_P2P_PORT=11000
START_RPC_PORT=11100

def check_json_precision():
    """Make sure json library being used does not lose precision converting CRT100M values"""
    n = Decimal("20000000.00000003")
    satoshis = int(json.loads(json.dumps(float(n)))*1.0e8)
    if satoshis != 2000000000000003:
        raise RuntimeError("JSON encode/decode loses precision")

def sync_blocks(rpc_connections):
    """
    Wait until everybody has the same block count
    """
    while True:
        counts = [ x.getblockcount() for x in rpc_connections ]
        if counts == [ counts[0] ]*len(counts):
            break
        time.sleep(1)

def sync_mempools(rpc_connections):
    """
    Wait until everybody has the same transactions in their memory
    pools
    """
    while True:
        pool = set(rpc_connections[0].getrawmempool())
        num_match = 1
        for i in range(1, len(rpc_connections)):
            if set(rpc_connections[i].getrawmempool()) == pool:
                num_match = num_match+1
        if num_match == len(rpc_connections):
            break
        time.sleep(1)
        

cryptotarget100Md_processes = []

def initialize_chain(test_dir):
    """
    Create (or copy from cache) a 200-block-long chain and
    4 wallets.
    cryptotarget100Md and cryptotarget100M-cli must be in search path.
    """

    if not os.path.isdir(os.path.join("cache", "node0")):
        devnull = open("/dev/null", "w+")
        # Create cache directories, run cryptotarget100Mds:
        for i in range(4):
            datadir = os.path.join("cache", "node"+str(i))
            os.makedirs(datadir)
            with open(os.path.join(datadir, "cryptotarget100M.conf"), 'w') as f:
                f.write("regtest=1\n");
                f.write("rpcuser=rt\n");
                f.write("rpcpassword=rt\n");
                f.write("port="+str(START_P2P_PORT+i)+"\n");
                f.write("rpcport="+str(START_RPC_PORT+i)+"\n");
            args = [ "cryptotarget100Md", "-keypool=1", "-datadir="+datadir ]
            if i > 0:
                args.append("-connect=127.0.0.1:"+str(START_P2P_PORT))
            cryptotarget100Md_processes.append(subprocess.Popen(args))
            subprocess.check_call([ "cryptotarget100M-cli", "-datadir="+datadir,
                                    "-rpcwait", "getblockcount"], stdout=devnull)
        devnull.close()
        rpcs = []
        for i in range(4):
            try:
                url = "http://rt:rt@127.0.0.1:%d"%(START_RPC_PORT+i,)
                rpcs.append(AuthServiceProxy(url))
            except:
                sys.stderr.write("Error connecting to "+url+"\n")
                sys.exit(1)

        # Create a 200-block-long chain; each of the 4 nodes
        # gets 25 mature blocks and 25 immature.
        for i in range(4):
            rpcs[i].setgenerate(True, 25)
            sync_blocks(rpcs)
        for i in range(4):
            rpcs[i].setgenerate(True, 25)
            sync_blocks(rpcs)

        # Shut them down, and remove debug.logs:
        stop_nodes(rpcs)
        wait_cryptotarget100Mds()
        for i in range(4):
            os.remove(debug_log("cache", i))

    for i in range(4):
        from_dir = os.path.join("cache", "node"+str(i))
        to_dir = os.path.join(test_dir,  "node"+str(i))
        shutil.copytree(from_dir, to_dir)

def start_nodes(num_nodes, dir):
    # Start cryptotarget100Mds, and wait for RPC interface to be up and running:
    devnull = open("/dev/null", "w+")
    for i in range(num_nodes):
        datadir = os.path.join(dir, "node"+str(i))
        args = [ "cryptotarget100Md", "-datadir="+datadir ]
        cryptotarget100Md_processes.append(subprocess.Popen(args))
        subprocess.check_call([ "cryptotarget100M-cli", "-datadir="+datadir,
                                  "-rpcwait", "getblockcount"], stdout=devnull)
    devnull.close()
    # Create&return JSON-RPC connections
    rpc_connections = []
    for i in range(num_nodes):
        url = "http://rt:rt@127.0.0.1:%d"%(START_RPC_PORT+i,)
        rpc_connections.append(AuthServiceProxy(url))
    return rpc_connections

def debug_log(dir, n_node):
    return os.path.join(dir, "node"+str(n_node), "regtest", "debug.log")

def stop_nodes(nodes):
    for i in range(len(nodes)):
        nodes[i].stop()
    del nodes[:] # Emptying array closes connections as a side effect

def wait_cryptotarget100Mds():
    # Wait for all cryptotarget100Mds to cleanly exit
    for cryptotarget100Md in cryptotarget100Md_processes:
        cryptotarget100Md.wait()
    del cryptotarget100Md_processes[:]

def connect_nodes(from_connection, node_num):
    ip_port = "127.0.0.1:"+str(START_P2P_PORT+node_num)
    from_connection.addnode(ip_port, "onetry")

def assert_equal(thing1, thing2):
    if thing1 != thing2:
        raise AssertionError("%s != %s"%(str(thing1),str(thing2)))
