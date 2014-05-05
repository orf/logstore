# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.provision "docker" do |d|
    d.pull_images "networld/rabbitmq"
    d.pull_images "dockerfile/elasticsearch"
    d.pull_images "paintedfox/postgresql"

    d.run "networld/rabbitmq"
    d.run "dockerfile/elasticsearch"
    d.run "paintedfox/postgresql"
  end
end
