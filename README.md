# n4m3s

Retrieves the common name and alternate names of a certificate published on a server

## Requirements

n4m3s currently supports Python 3.

The recommended version for Python 3 is 3.4.x

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-d            | --domain      | Domain name to enumerate it's CN and Subjects Alt Name
-f            | --file        | File contains a list with domains name to enumerate it's CN and Subjects Alt Name 
-v            | --verbose     | Enable the verbose mode and display results in realtime
-o            | --output      | Save the results to text file
-h            | --help        | show the help message and exit

### Examples

* To list all the basic options and switches use -h switch:

```python n4m3s.py -h```

* To retrieve common name of specific domain:

``python n4m3s.py -d example.com``

## License

[MIT](LICENSE) © [gallorrojo](https://github.com/gallorrojo).
