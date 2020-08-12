# Airdropz Candy

Airdropz is an automated candy dispenser which uses cryptocurrency for payments via Coinbase Commerce.

The system is composed of a coninuously polling Flask server on the
Raspberry Pi which queries Coinbase Commerce for new payment events to
determine when to dispense candy. It also uses a simple "Point of Sale"
website hosted on [www.airdropz.xyz](www.airdropz.xyz) which is used to
intiate checkout. 

When the flask app receives a new payment event it triggers a servo expected to be mounted to the candy machine to dispense candy.

## Demo

[![alt
text](./media/youtube-img.jpg)](https://www.youtube.com/watch?v=UmbGezcIINY)

## Repos
[RPi Flask Server](./flask-app): Flask server on Raspberry Pi
that polls CBCommerce API and dispenses candy.

[Point of Sale Portal](./point-of-sale): HTML page that links
to Coinbase Commerce checkout screen. 

## Author
@RobertSimoes



