# Slack Music Bot

A bot for slack that connects to an MPD server (In this instance: Mopidy) and allows users to provide Youtube links as well as search Youtube for songs to play.

## Getting Started

To get started, you will probably need a debian based system: This was written for a Raspberry PI. 

TODO: Add instructions to configure PI (Should be coming within a week)

### Prerequisites

You will probably want these things installed:
```
Mopidy
Python 3
```

### Installing

Quite easy once the instructions for what originally do on the PI are finished. For now:

Install all the requirements
```
pip install -r requirements.txt
```

Setup the values in config.yml for your situtation

Run the bot!
```
python run.py config.yml
```

You can test it's running by typing @musicbot ping; it should reply with "Pong!"


## Contributing

Be reasonable, and make a pull request! Should be relatively simple to add your own commands... Check out commands.py! 

## Authors

* **Aidan Handa** - *Initial work* 

## Acknowledgments

* Hat tip to anyone who's code was used
* Mr. Schmit for running the Music Server in his class
* Adam for entertainment and new ideas
