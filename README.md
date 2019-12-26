# Skiing Vacation Planner

An IOT assistant that will help with planning your next ski trip!  

![](./imgs/1.jpeg "")

#### Background

My girlfriends' parents enjoy skiing, and have several favorite ski resorts throughout the US.  I wanted to make something
that would show them the current conditions at glance of their favorite resorts, as well as what traveling there would 
look like.  I wanted it to be present in their home with minimal configuration.

### Guide to this Guide

I created this to work with a Raspberry Pi 3B+ with the official 7" touchscreen.  In order to get this up and running
for yourself, dear reader, I've split this repository up into two separate branches for two purposes.  First, the branch
for development and testing on a desktop (`master`), and the branch to get your own IOT device up and running on the Pi (`pi_branch`).
I would suggest starting with checking out the master branch, getting all the kinks worked out on your desktop machine 
before setting up your pi.  This guide is a work in progress, as is this repo, so let me know via a PR/Issue what doesn't
work for you.

### Description

Some basic configuration is required. Once that is complete, spinning up an instance of the planner _should_ be easy.
Ski resort information is defined in a configuration file.  Information about the users' home location is then put into a secrets
so that travel information can be calculated.  When all setup is complete, the planner runs on a Raspberry Pi and will
automatically update with recent info about the ski resorts defined in the configuration file. Two APIs are used, and
the ncessary API keys are documented in the desktop setup section.

# Desktop / Common Setup

#### Amadeus Setup

[Amadeus](https://developers.amadeus.com/) is a service for grabbing flight and hotel data based on user input.  I had to use production keys to get flights
to the smaller airports.  Costs thus far for me are zero, but I be sure to check out their [pricing](https://developers.amadeus.com/pricing)
page to make sure you aren't going to incur any unexpected costs.  [Instructions for obtaining keys here.](https://developers.amadeus.com/get-started/category?id=79&durl=334&parentId=NaN)

#### Google Maps Setup

Google Maps allows for obtaining traffic and driving information for driving data.  [Instructions for obtaining API keys are here.](https://developers.google.com/maps/gmp-get-started)

#### Secrets

Copy `secrets.yaml.example` into a new file in the root directory called `secrets.yaml` and add your api keys. In addition,
add your origin airport by IATA code as well as the coordinates that a driver would start their journey from.  In this
way, you'll be able to use the google maps API to get driving times / distances from your origin to the ski resort, as well
as flights.  

#### Resorts Config

Within the `config.yaml` there are a few hardcoded ski resorts along with their information.  They have been marked with
the "driving" flag if they are within driving distance of Newark, NJ (EWR), but you may want to change this for yourself.
This will determine whether or not the planner shows a driving estimation or a flying estimation for travel time.

### Initialization

Once the configuration and secrets parameters are to your liking, set up on a [python virtual environment](https://docs.python.org/3/library/venv.html).  This has only
been tested with Python3.  You shouldn't be using Python2 for anything anymore, so I'm not going to bother trying to 
support it.  Once you've set up a virtual environment, install the required packages (`$ pip install -r requirments.txt`).
Try out spinning up the planner for yourself:

`$ python main.py`

From here, feel free to play around with the source code.  There are various `TODO`s scattered throughout the repo that 
could probably use addressing.  In addition, the resilency of this thing is... not great yet, so you might want to beef it up.

# Raspberry Pi Setup

This walkthrough will demonstrate how I created my implementation of the project.  The software will run on Windows/MacOSX/Linux
and can be run with simply cloning this repository, installing the required packages, and running the main program.  However, 
in order to create the IOT device, continue reading below.

#### Necessary Materials

1. [Raspberry Pi 3B+](https://www.adafruit.com/product/3775)
2. [Raspberry Pi Touchscreen](https://www.adafruit.com/product/2718)
3. (optionally) [Raspberry Pi Touchscreen Case](https://smarticase.com/products/smartipi-touch)
4. [Raspberry Pi Power Supply](https://www.adafruit.com/product/1995)
5. [MicroSD card >8gb](https://smile.amazon.com/gp/product/B07K83HSLF)

#### Raspberry Pi Setup

1. [Set up the raspberry pi and give it the latest version of Raspbian.](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. (if no case) [attach the touchscreen](https://cdn-shop.adafruit.com/product-files/2718/2718build.jpg)
3. (if you have a case) [install it into the case](https://www.youtube.com/watch?v=XKVd5638T_8)
4. Add a keyboard and make sure that the raspberry pi desktop is running

## Initialization on the Pi

After completing the raspberry pi setup and setting up Raspbian on your Pi install the necessary packages.

