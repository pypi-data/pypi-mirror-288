# Unit/Dimensioned Quantities Module

## Overview

The **unitvalue** Module is a Python library designed to handle various unit conversions. It allows for the creation of `UnitValue` objects, which can represent values with different units and convert between them.

## Features

- Create `UnitValue` objects with specified units and values.
- Convert between different units within the same dimension (e.g., meters to kilometers).
- Support for different measurement systems (e.g., metric and imperial).
- Arithmetic operations with unit handling (addition, subtraction, multiplication, division).
- Error handling for unsupported units and invalid operations.

## Installation

```Powershell
pip install dimensioned-values
```

## Usage

### Creating a UnitValue

To create a `UnitValue` object, use the `create_dimensioned_quantity` function:

```python
from unitvalue import create_dimensioned_quantity

# Create a UnitValue object with a specified unit and value
distance = create_dimensioned_quantity('meter', 100)
# Or initialize instance yourself
distance = UnitValue("METRIC", "DISTANCE", "m", 100)
```

### Converting Units

You can convert the unit of a `UnitValue` object using the `to` method:

```python
# Convert the distance to kilometers
distance.to(unit='kilometer')
print(distance)  # Output: 0.1 kilometer

# Convert to base metric unit (Useful for Scinetifc calculations)
distance.convert_base_metric()
print(distance)
```

### Arithmetic Operations

`UnitValue` objects support arithmetic operations, maintaining unit consistency (The units do not even need to be in the same system or magnitude for you to perform arithmetic on them as the module will handle this). It is important to knwo all arithmetic operations return a value in the base metric units:

```python
from unitvalue import create_dimensioned_quantity

length1 = create_dimensioned_quantity('meter', 50)
length2 = create_dimensioned_quantity('meter', 30)

# Addition
total_length = length1 + length2
print(total_length)  # Output: 80 m

# Subtraction
remaining_length = length1 - length2
print(remaining_length)  # Output: 20 m

# Multiplication by a scalar
double_length = length1 * 2
print(double_length)  # Output: 100 m

# Division by a scalar
half_length = length1 / 2
print(half_length)  # Output: 25 m

# Multiplication between UnitValue Objects
area = lenght1 * length2
print(area) # Output: 150 m^2

# Divivsion between UnitValue Objects
l = area / length2
print(l) # Output: 50 m

# UnitValue object to the power
volume = lenght1**3
print(volume)  # Output: 125000 m^3
```

### Accessing Unit Information

You can access the unit, measurement type, and system of a `UnitValue` object using properties:

```python
print(distance.get_unit)  # Output: 'kilometer'
print(distance.get_measurement_type)  # Output: 'LENGTH'
print(distance.get_system)  # Output: 'METRIC'
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License.
