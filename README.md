# SDN Modul 4 — Jobsheet 1: Mininet dan Topologi Dasar

Praktikum Cloud dan Virtualisasi Jaringan: menyiapkan Mininet di
dalam container Docker, memverifikasi topologi dasar, serta melakukan
pengujian traffic sebagai persiapan sebelum menggunakan SDN controller.

## Lingkungan

- Windows dengan Docker Desktop
- Image: iwaseyusuke/mininet:ubuntu-22.04 (container mn-lab4, network sdn-lab4)
- Mininet 2.3.0 dan Open vSwitch 2.17.5
- Datapath userspace (netdev), failMode standalone, tanpa controller

## Topologi yang Diuji

- single,2 dan single,3
- tree, depth=2, fanout=2
- linear,3

## Hasil Utama pada linear,3 (h1 ke h3)

| Kondisi | RTT rata-rata | Throughput |
| --- | --- | --- |
| Baseline | 1,158 ms | 670 Mbits/sec |
| TCLink (bw 10 Mbit/s, delay 5 ms) | 52,019 ms | 9,50 Mbits/sec |

Pengujian layanan HTTP dari h2 ke server Python di h1 berhasil dengan
respons HTTP/1.0 200 OK. Pada uji perubahan status link, link s1-s2 yang
dimatikan membuat h1 terputus dari h3 (packet loss 100%), sedangkan h2 ke
h3 tetap terhubung, dan konektivitas pulih setelah link dihidupkan kembali.

## Catatan Gangguan dan Perbaikan

Pengukuran iperf pada awalnya gagal (macet dan timeout) walaupun ping
berhasil. Penyebabnya adalah checksum offload pada antarmuka veth yang
tidak dilengkapi oleh datapath userspace, sehingga paket TCP dibuang oleh
penerima. Perbaikannya adalah menonaktifkan offload dengan ethtool pada
antarmuka host, setelah itu iperf berjalan normal.
