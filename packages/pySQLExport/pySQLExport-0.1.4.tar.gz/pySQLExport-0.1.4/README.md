# pySQLExport

A command line tool to interact with multiple databases and export to various formats.

## Installation

You can install the package using pip:

```sh
pip install pySQLExport
```
## Configuration

Before using `pySQLExport`, ensure you have a configuration file or environment variables set up for your database connection.

## Usage
You can run pySQLExport in either interactive mode, which allows you to run multiple queries and export to multiple formats. You can also pass command line arguments for single-run exports or queries.


### Interactive Mode

If you run `pySQLExport` without arguments, it will start in interactive mode:

```sh
pySQLExport
```

### Command Line Interface

#### Running a Query

To run a query and display the results in the terminal:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml
```

#### Exporting Results

To export query results to a CSV file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=csv --outfile results.csv
```

To export query results to a JSON file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.json
```
To export query results to a XML file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.xml
```
To export query results to a html file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.html
```

In interactive mode, you can enter the database information, run queries, and choose how to export the results.

### Example

Here’s a complete example of how to use `pySQLExport`:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output csv --outfile results.csv
```

1. **Run the command above.**
2. **The results will be exported to a file named `results.csv`.**

### Summary of Commands

- **Run a query and display results**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config-file config.yaml
  ```

- **Export results to CSV**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config-file config.yaml --output csv --outfile results.csv
  ```

- **Export results to JSON**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config_file config.yaml --output json --outfile results.json
  ```
- **Export results to html**:
```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.xml
```
- **Export results to xml**:
```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.html
```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.
