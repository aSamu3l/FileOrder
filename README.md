<a id="top"></a>

# FileOrder

<details>
  <summary>Index</summary>
  <ol>
    <li><a href="#description">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul><li><a href="#requirements">Requirements</a></li></ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li>
      <a href="#language">Language</a>
      <ul><li><a href="#supported-languages">Supported Languages</a></li></ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

## Description
FileOrder is a Python application that allows you to organize files in a specified folder. The application enables searching, moving, and copying files from a source folder to a destination folder, with the ability to filter files by name and extension.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features
- Selection of source and destination folders.
- Filtering files by name and/or extension.
- Option for case-sensitive search.
- Moving and copying selected files.
- Customizable user interface with support for light and dark modes.
- Multilingual support (English and Italian).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/aSamu3l/FileOrder.git
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Requirements
- Python 3.10 or higher

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
1. Run the `main.py` file:
    ```sh
    python main.py
    ```
2. Use the interface to select the source and destination folders.
3. Filter files by name and/or extension.
4. Search for files and select those to move or copy.
5. Press the "Move" or "Copy" buttons to perform the desired operation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Configuration
### Language
The application language can be configured by modifying the `settings/setting.json` file or by using the application settings.
If you want to change the language manually, you can edit the `lang` field in the `settings/setting.json` file:
```json
{
    "lang": "EN"
}
```
Languages can be updated by anyone with a pull request to `settings/lang.json`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Supported Languages
- [x] English (EN)
- [x] Italian (IT)

## License
This project is licensed under the `Apache-2.0 License`. See the `LICENSE` file for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributors

<a href="https://github.com/aSamu3l/FileOrder/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aSamu3l/FileOrder" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>