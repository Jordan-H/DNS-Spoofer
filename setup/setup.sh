cd ~/Documents/
wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-6.0.0-linux_x86_64-portable.tar.bz2
chmod 755 pypy-6.0.0-linux_x86_64-portable.tar.bz2
tar xvjf pypy-6.0.0-linux_x86_64-portable.tar.bz2
wget https://netfilter.org/projects/libmnl/files/libmnl-1.0.4.tar.bz2
chmod 755 libmnl-1.0.4.tar.bz2
tar xvjf libmnl-1.0.4.tar.bz2
wget https://netfilter.org/projects/libnfnetlink/files/libnfnetlink-1.0.1.tar.bz2
chmod 755 libnfnetlink-1.0.1.tar.bz2
tar xvjf libnfnetlink-1.0.1.tar.bz2
wget https://netfilter.org/projects/libnetfilter_queue/files/libnetfilter_queue-1.0.3.tar.bz2
chmod 755 libnetfilter_queue-1.0.3.tar.bz2
tar xvjf libnetfilter_queue-1.0.3.tar.bz2
cd pypy-6.0.0-linux_x86_64-portable/bin/
./pypy -m ensurepip
./pip install scapy
ln -s -T ~/Documents/pypy-6.0.0-linux_x86_64-portable/bin/pypy  ~/Documents/py
dnf install redhat-rpm-config -y
yum install python-devel -y
cd ~/Documents/
cd libmnl-1.0.4
./configure
make
sudo make install
cd ..
cd libnfnetlink-1.0.1
./configure
make
sudo make install
cd ..
echo "/usr/local/lib" >> /etc/ld.so.conf
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
cd libnetfilter_queue-1.0.3
./configure
make
sudo make install
cd ..
cd pypy-6.0.0-linux_x86_64-portable/bin/
./pip install NetfilterQueue
sudo ldconfig
#alias pypy="~/Documents/pypy-6.0.0-linux_x86_64-portable/bin/pypy"
