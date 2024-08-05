# UK Postcodes Library

The UK Postcodes Library is a comprehensive Python library designed to handle UK postcode validation and parsing. It provides multiple handlers for parsing postcodes using various methods, including regular expressions, API calls, and CSV files. The library is suitable for both online and offline use cases, offering flexibility and ease of use for developers working with UK postcode data.

## Requirements

- Python 3.10 (tested, should work with other versions too)
- Additional dependencies are listed in the `requirements.txt` file.

## How to Install

### Using PIP

The easiest way to install the UK Postcodes Library is by using PIP:

```bash
pip install postcode_parser_uk
```

### Using the Wheel File from Releases

1. Download the `.whl` file from the releases page.
2. Install the `.whl` file using PIP:

```bash
pip install path_to_whl_file.whl
```

### Cloning the Repository and Building with Makefile

1. Clone the repository:

```bash
git clone URL_TO_REPOSITORY
cd REPOSITORY_NAME
```

2. Install the dependencies:

```bash
make install
```

3. Build the project:

```bash
make build
```

4. Install the built package:

```bash
pip install dist/package_name.whl
```


## How to Use

### Quickstart

Using the UkPostcodeParser Class with the Default Handler:
```python

from postcode_parser_uk import UkPostcodeParser

# Create an instance of the UkPostcodeParser class
parser = UkPostcodeParser()

# Parse a single postcode using the default handler (RegexParsingHandler)
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = parser.parse("SW1W 0NY")

# Validate the result
if result.is_valid:
    print(result.value)

# Handle failure
if result.is_failure:
    print(result.error)

# Get the parsed postcode
parsed_postcode = result.value
```

### Overview of Parsing Handlers

The UK Postcodes Library provides several handlers for parsing UK postcodes:

- `RegexParsingHandler`: Uses regular expressions to parse standard and special UK postcodes.
- `OSDataHubNamesAPIParsingHandler`: Uses the OS Data Hub Names API to parse UK postcodes.
- `PostcodesIOAPIParsingHandler`: Uses the Postcodes.io API to parse UK postcodes.
- `ONSPDCsvFileParsingHandler`: Uses the ONSPD CSV file to parse UK postcodes.

### RegexParsingHandler

#### Description

The `RegexParsingHandler` uses regular expressions to parse UK postcodes that follow the standard format as well as special UK postcodes that do not follow the standard format. This handler is useful for parsing postcodes offline without the need for an internet connection.

#### Postcode Regular Expression

The postcode validation is based on BS7666 and is not case-sensitive. The validation is implemented by evaluating the postcode string against the following regular expressions:

- `^[A-Z]{1,2}[0-9R][0-9A-Z]? ?[0-9][ABDEFGHJLNPQRSTUWXYZ]{2}$`
- `^BFPO ?[0-9]{1,4}$`
- `^([AC-FHKNPRTV-Y]\d{2}|D6W)? ?[0-9AC-FHKNPRTV-Y]{4}$`

The postcode must satisfy at least one of these regular expressions. For more details, you can refer to the [Web Services Interface Specification (PDF)](https://assets.publishing.service.gov.uk/media/632b07338fa8f53cb77ef6b8/WS02_LRS_Web_Services_Interface_Specification_v6.4.pdf), specifically on page 77.

#### Example

```python

from postcode_parser_uk import RegexParsingHandler

regex_handler = RegexParsingHandler()

# Parse a single postcode using the regex handler
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = regex_handler.parse("SW1W 0NY")

# Validate the result
if result.is_valid:
    print(result.value)  # Output the parsed postcode

# Handle failure
if result.is_failure:
    print(result.error)  # Output the error

# Get the parsed postcode
parsed_postcode = result.value  # UKPostCode or SpecialUKPostCode object
```

### OSDataHubNamesAPIParsingHandler

#### Description

The `OSDataHubNamesAPIParsingHandler` uses the OS Data Hub Names API to parse UK postcodes. The API requires an API key to access the service. You can sign up for an API key here: [OS Data Hub](https://osdatahub.os.uk/).

Optionally, you can set the `OSDATAHUB_API_KEY` in the environment. This can be done using a `.env` file placed in the root directory.

#### Example

```python
from postcode_parser_uk import OSDataHubNamesAPIParsingHandler

osdatahub_api_handler = OSDataHubNamesAPIParsingHandler(api_key="your_api_key_here")

# Parse a single postcode using the OS Data Hub API handler
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = osdatahub_api_handler.parse("SW1W 0NY")

# Validate the result
if result.is_valid:
    print(result.value)

# Handle failure
if result.is_failure:
    print(result.error)

# Get the parsed postcode
parsed_postcode = result.value
```


### PostcodesIOAPIParsingHandler

#### Description

The `PostcodesIOAPIParsingHandler` uses the Postcodes.io API to parse UK postcodes. The API does not require an API key to access the service. You can find more information about the API here: [Postcodes.io](https://postcodes.io/).

#### Example

```python
from postcode_parser_uk import PostcodesIOAPIParsingHandler

postcodesio_api_handler = PostcodesIOAPIParsingHandler()

# Parse a single postcode using the Postcodes.io API handler
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = postcodesio_api_handler.parse("SW1W 0NY")

# Validate the result
if result.is_valid:
    print(result.value)

# Handle failure
if result.is_failure:
    print(result.error)

# Get the parsed postcode
parsed_postcode = result.value
```

### ONSPDCsvFileParsingHandler

#### Description

The `ONSPDCsvFileParsingHandler` uses a ONSPD CSV file to parse UK postcodes. The handler requires the path to the zipped ONSPD CSV file. These files can be downloaded from the website: [ONS Geoportal](https://geoportal.statistics.gov.uk/search?collection=Datasets). For example, [ONS Postcode Directory (May 2024)](https://geoportal.statistics.gov.uk/datasets/a8a2d8d31db84ceea45b261bb7756771/about). When using the file, keep the file zipped and provide the path to the zipped file. This handler is useful for parsing postcodes offline without the need for an internet connection.

#### Example

```python
from postcode_parser_uk import ONSPDCsvFileParsingHandler

onspd_excel_file_handler = ONSPDCsvFileParsingHandler(path="path_to_zipped_onspd_csv_file_here")

# Parse a single postcode using the ONSPD CSV file handler
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = onspd_excel_file_handler.parse("SW1W 0NY")

# Validate the result
if result.is_valid:
    print(result.value)

# Handle failure
if result.is_failure:
    print(result.error)

# Get the parsed postcode
parsed_postcode = result.value
```

### Using the UkPostcodeParser Class

#### Description

The `UkPostcodeParser` class provides a high-level interface for parsing UK postcodes using different handlers.

#### Example

```python
from postcode_parser_uk import UkPostcodeParser

# Create an instance of the UkPostcodeParser class
parser = UkPostcodeParser(
    osdatahub_api_key="your_api_key_here",
    onspd_zip_file_path="path_to_zipped_onspd_csv_file_here",
)

# Parse a single postcode using the default handler (RegexParsingHandler)
# Postcodes are normalized before parsing (whitespace stripped, converted to uppercase)
result = parser.parse("SW1W 0NY")

# To use other handlers, specify the handler type when calling the parse method
# Handler types: 'regex', 'osdatahub_api', 'postcodesio_api', 'onspd_excel_file'
# If not specified the handler type will default to "regex"
result = parser.parse("SW1W 0NY", handler_type='osdatahub_api')

# Validate the result
if result.is_valid:
    print(result.value)

# Handle failure
if result.is_failure:
    print(result.error)

# Get the parsed postcode
parsed_postcode = result.value


# Parsing a batch
results = parser.parse_batch(["SW1W 0NY", "PO16 7GZ", "GU16 7HF", "L1 8JQ"])
```

## How to Test

### Using Makefile

In the root folder, execute:

```bash
make test
```

### Manually Running Tests

In the root folder, execute:

```bash
python -m unittest discover -s tests
```



## Additional Information

### Uk postcodes

For more information on UK postcodes, including special cases and formatting rules, you can refer to the Wikipedia page on [Postcodes in the United Kingdom](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting).


### Makefile

The Makefile provides a set of commands to streamline development workflow.

#### Makefile Commands

- **Install Dependencies**: Create a virtual environment and install all dependencies.

  ```bash
  make install
  ```

- **Run Tests**: Execute all tests using `unittest`.

  ```bash
  make test
  ```

- **Lint Code**: Check the code for linting errors using `flake8`.

  ```bash
  make lint
  ```

- **Format Code**: Format the code using `black`.

  ```bash
  make format
  ```

- **Prepare**: Run tests, lint, and format the code.

  ```bash
  make prepare
  ```

- **Build**: Build the project into a wheel file.

  ```bash
  make build
  ```

- **All**: Install dependencies, run all checks, and build the project.

  ```bash
  make all
  ```