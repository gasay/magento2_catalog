
sudo chmod -R 0777 /usr/local/bin
sudo mkdir -p /var/lib/gems && sudo chmod -R 0777 /var/lib/gems

sudo LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/php
printf "y\n" | sudo apt-add-repository ppa:brightbox/ruby-ng
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update

sudo apt-get install -y software-properties-common python-software-properties
sudo apt-get install -y fish git zip unzip snmp

sudo apt-get install -y nodejs
sudo apt-get install -y npm

sudo apt-get install -y ruby2.4 ruby2.4-dev
gem install compass

sudo apt-get install -y redis-server redis-tools
sudo apt-get install -y mongodb-org

sudo apt-get install -y \
    php7.0 \
    php7.0-dev \
    php7.0-fpm \
    php7.0-cli \
    php7.0-common \
    php7.0-json \
    php7.0-opcache \
    php7.0-mysql \
    php7.0-phpdbg \
    php7.0-mbstring \
    php7.0-gd \
    php7.0-imap \
    php7.0-ldap \
    php7.0-pgsql \
    php7.0-pspell \
    php7.0-recode \
    php7.0-snmp \
    php7.0-tidy \
    php7.0-dev \
    php7.0-intl \
    php7.0-gd \
    php7.0-curl \
    php7.0-zip \
    php7.0-xml \
    php7.0-mcrypt \
    php-xdebug

sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password \"''\""
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password \"''\""
sudo apt-get install -y mysql-common-5.6 mysql-server-5.6 mysql-client-5.6

sudo apt-get install -y nginx
sudo service nginx restart
