# Electrical Cabinet Repository README

This README provides an overview of the Electrical Cabinet repository, including its purpose, setup instructions, unit testing guidelines, reference links, and a usage example.

### What is this repository for? ###

- This repository is a part of the Opsys automation infrastructure.
- It serves as the control interface for an electrical cabinet, facilitating various operations such as managing interlocks, controlling lights, lasers, power states, and other features.

### How do I get set up? ###

To set up the electrical cabinet control interface, follow these steps:

1. Install the `opsys-electrical-cabinet` package using pip:
    ```
    pip install opsys-electrical-cabinet
    ```

### Unit Testing ###

To run unit tests for the electrical cabinet control interface, execute the following command:
python -m unittest -v
.

### Usage Example ###

Here's an example demonstrating the usage of the electrical cabinet control interface:

```python
from opsys_electrical_cabinet.electrical_cabinet import ElectricalCabinet

# Initialize the ElectricalCabinet instance with the IP address of the PLC
cabinet = ElectricalCabinet()
cabinet.init_tcp_conn(ip_address='192.168.0.2')

# Read the state of the gimbal interlock
interlock_state = cabinet.get_gimbal_interlock_state()

# Set the state of the laser
cabinet.set_laser_state(1)

# Read the state of the TRX cover
trx_cover_state = cabinet.get_trx_cover_state()