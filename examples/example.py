from ephyr_control import *

config = MixClientSettings.parse_file("mix.client.example.json")
esc = EphyrStreamControl.build(config["love"])

# connect to all available languages
esc.connect()

# change audio volume of original and translation
esc["fr"].org.volume(100)
esc["fr"].trn.volume(15)
