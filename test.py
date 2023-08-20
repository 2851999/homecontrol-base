from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.midea import MideaConfig


config = MideaConfig()
# config.account.username = "new_test"
# config.save()

print(config.account)

device = ACDevice.discover("Test", "192.168.1.85", config.account)
print(device)
