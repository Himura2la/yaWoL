#!python3
# -*- encoding: utf-8 -*-

import subprocess
import time
import sys
import pywakeonlan.wakeonlan as wol


def wake(target, ping_requests):
    wol.send_magic_packet(target['mac'], ip_address=target['broadcast'])
    print("Magic packet for %s sent to %s." % (target['mac'], target['broadcast']))

    ping_proc = subprocess.Popen(['ping', '-n', str(ping_requests), target['host']],
                                 stdout=subprocess.PIPE)
    i, success = 0, False
    while ping_proc.poll() is None:
        try:
            line = ping_proc.stdout.readline().decode().replace('\r', '').replace('\n', '')
            if 'timed out' in line:
                i += 1
                print('%s [%d]' % (line, i), end='\r', flush=True)
            elif 'Reply' in line:
                print("\n%s\nIt's alive !!!" % line)
                success = True
                break
            else:
                print(line)
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\nOK, terminating ping...")
            ping_proc.terminate()
    print()
    ping_proc.terminate()
    if success:
        return True
    print("Target does not answer... T_T")
    return False

if __name__ == "__main__":
    hosts = [l.split(',') for l in open('hosts.csv').read().split('\n')]
    hosts = {r[0]: {'host': r[1],
                    'broadcast': r[2],
                    'mac': r[3]} for r in hosts if len(r) == 4}

    wake(hosts[sys.argv[1]], 20)
