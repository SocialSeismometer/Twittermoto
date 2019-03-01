# Twittermoto
Python code for collecting and analysing tweets, and detecting earthquakes


# Installation
Clone this repository and install the package using pip:
```
git clone https://github.com/twittermoto/Twittermoto.git
cd twittermoto
pip install -e .
```

# Usage
First you must enter your Twitter Developer keys and tokens in [twittermoto/config.py](https://github.com/twittermoto/Twittermoto/blob/master/twittermoto/config.py) before you can use the data collection scripts.

Twittermoto can be imported into any python script in your environment. An example Python script could be:

```
import twittermoto as tm

tm.run()
```
