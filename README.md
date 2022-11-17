# NetCloud-Gateway-Reporter

## Summary
Generates an Excel sheet of routers and their IPv4 addresses in a 
configured NetCloud instance.

_Note: If you have any questions or comments you can always use GitHub
discussions, or email me at farinaanthony96@gmail.com._

#### Why
Providing a fresh list of IPv4 addresses of gateways in NetCloud enables
engineers to have reliable knowledge to connect or ping gateways.

## Requirements
- Python >= 3.9
- configparser
- pandas
- requests

## Usage
- Edit the config file with relevant NetCloud API information and 
  the name of the output Excel file.

- Simply run the script using Python:
  `python NetCloud-Gateway-Reporter.py`

## Compatibility
Should be able to run on any machine with a Python interpreter. This
script was only tested on a Windows machine running Python 3.9.

## Disclaimer
The code provided in this project is an open source example and should
not be treated as an officially supported product. Use at your own
risk. If you encounter any problems, please log an
[issue](https://github.com/CC-Digital-Innovation/NetCloud-Gateway-Reporter/issues).

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History
-  version 1.0.1 - 2022/11/17
    - Update pandas library
    - Update README.md
    - Add requirements.txt file


-  version 1.0.0 - 2022/08/23
    - Initial release

## Credits
Anthony Farina <<farinaanthony96@gmail.com>>
