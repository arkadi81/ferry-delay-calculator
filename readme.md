# FERRY DEPARTURE DELAY CALCULATOR
This a py program which recieves predefined csv files as command line arguments.
The files contain departure and arrival info for BC ferries.
The program queries user for the desired month and departure port, and based on the information
in the files calculates average delay time.

The code is inspired by UVIC Seng 265 course assignment 3
By arkadi, 20171218

## Usage
* ferry_delays.py <input-file-names> <more-input-files> ...

or use the provided ./go.sh

## Programming skills utilized:
- Working with simple py variable formats (int, str, dict)
- understanding mutable, immutable vars and scope (LEGB)
- File I/O
- Base use of functions
- Base flow control and debugging
- Exception handling
- Input and error checking
- Simple time calculations

## TODO
- refactoring some of the functionality could allow for more reusable code
- the time calculation capacity could be expended into a custom time object, which would be able to calculate deltas etc