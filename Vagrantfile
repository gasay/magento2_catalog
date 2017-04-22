
Vagrant.configure("2") do |config|

    config.vm.box = "ubuntu/trusty64"
    config.vm.network "private_network", ip: "10.0.0.30"
    config.vm.synced_folder ".", "/vagrant", type: "nfs"
    ENV['LC_ALL']="en_US.UTF-8"

    config.vm.provider "virtualbox" do |vb|

        vb.name = “catalog_ubuntu_lemp_php7"
        vb.memory = 8192
        vb.cpus = 1
    end


	config.vm.hostname = "www.catalog.dev"

  	config.hostsupdater.aliases = [
  	        "www.catalog.dev",
		“catalog.dev"
	]



    config.vm.provision "shell", inline: <<-SHELL
        
        cd /vagrant
        
        /vagrant/tools/go-lemp.bash

    SHELL
end
