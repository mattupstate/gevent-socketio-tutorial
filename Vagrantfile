# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :vm do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.network :hostonly, "192.168.0.10"

    config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "cookbooks"
      chef.add_recipe "redisio::install"
      chef.add_recipe "redisio::enable"

      chef.json.merge!({
        'redisio' => {
          'servers' => [
            {'port' => '6379'}
          ]
        }
      })
    end
  end
end