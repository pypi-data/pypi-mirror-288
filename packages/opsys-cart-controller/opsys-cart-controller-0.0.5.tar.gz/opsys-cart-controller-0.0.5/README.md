# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is cart controller implementation for cart moving on rail

### How do I get set up? ###

* pip install opsys-cart-controller

### Unit Testing

* python -m unittest -v

### Reference Links

* R:\Lidar\Dima\Software\Motor Control.zip -
  The zip file contains all required drivers for installation
  and the server side code with usage instructions

### Usage Example
```
from opsys_cart_controller.cart_controller import CartController

cart = CartController(laser_com=4, ps_com=8)

cart.setup_cart_motor()
distance = cart.get_distance()
print(f'Current Distance: {cart.get_distance()}')
cart.move_cart_motor(dest=10)
```