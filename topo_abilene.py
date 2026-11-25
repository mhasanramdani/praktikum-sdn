#!/usr/bin/env python3
import argparse
import json
import sys

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def load_model(path):
    with open(path) as f:
        model = json.load(f)
    switches = model.get("switches", [])
    hosts = model.get("hosts", [])
    links = model.get("links", [])
    if len(switches) != 11 or len(hosts) != 3 or len(links) != 14:
        sys.exit("Model tidak lengkap: perlu 11 switch, 3 host, 14 link.")
    names = {s["name"] for s in switches}
    for h in hosts:
        if h["switch"] not in names:
            sys.exit("Model tidak lengkap: switch host tidak dikenal.")
    for lk in links:
        if lk["a"] not in names or lk["b"] not in names:
            sys.exit("Model tidak lengkap: link menyebut switch tak dikenal.")
    return model


def build(model, controller_ip, controller_port, datapath):
    net = Mininet(controller=RemoteController, switch=OVSSwitch)
    net.addController("c0", ip=controller_ip, port=controller_port)
    sw = {}
    for s in model["switches"]:
        sw[s["name"]] = net.addSwitch(
            s["name"], dpid=s["dpid"], datapath=datapath,
            protocols="OpenFlow13", failMode="secure")
    hs = {}
    for h in model["hosts"]:
        hs[h["name"]] = net.addHost(h["name"], ip=h["ip"], mac=h["mac"])
    for h in model["hosts"]:
        net.addLink(hs[h["name"]], sw[h["switch"]], port2=h["port"])
    for lk in model["links"]:
        net.addLink(sw[lk["a"]], sw[lk["b"]],
                    port1=lk["port_a"], port2=lk["port_b"])
    return net


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--controller", required=True)
    parser.add_argument("--port", type=int, default=6653)
    parser.add_argument("--datapath", choices=["user", "kernel"],
                        default="user")
    args = parser.parse_args()

    setLogLevel("info")
    model = load_model(args.config)
    net = build(model, args.controller, args.port, args.datapath)
    net.start()
    net.staticArp()
    info("*** Topology Abilene berjalan: 11 switch, 14 link, 3 host\n")
    CLI(net)
    net.stop()


if __name__ == "__main__":
    main()