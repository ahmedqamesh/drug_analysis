# Drug Interaction Analysis Tool 
This script helps in understanding drug interactions by reading data from an Excel file and processing it to find interactions between specified drugs. It supports searching by drug name or drug ID and provides detailed information about the active ingredients and any potential interactions.

## General Features
- Reads multiple sheets from an Excel file and processes drug data.
- Retrieves drug information, including active ingredient details.
- Detects and displays possible interactions between drugs.
- Prints detailed drug interaction information with corresponding risks.
  
### Getting Started
1. **Clone the Repository:**
   Clone the repository to download the source code:
   ```bash
   git clone https://github.com/yourusername/drug-interaction-tool.git
   cd drug-interaction-tool
2. **Install Required Packages:**
Install the required Python packages using pip:
```
pip install pandas numpy colorama termcolor openpyxl xlrd
```
3. **Prepare the Excel File: **
Ensure your Excel file (data-entry.xlsx) is in the same directory as the script or provide the full path to the file.
4.**Run the Script:**
Run the script to process drug interaction data:
```
python main_assignment_test.py
```
### Using the Tool

1. **Search by Drug Name or Drug ID:**
   - Enter `1` for searching by drug name.
   - Enter `2` for searching by drug ID.

2. **Enter the Drugs Under Test:**
   - Provide the drug names or IDs separated by commas.

### Example Usage

```bash
Please enter the search criteria [1. for Drug Name or 2. for Drug ID]: 1
Please enter the drugs under test [Separated by commas]: Chlorothiazide, Abilify

## Contributing and Contact Information:
We welcome contributions from the community please contact : `ahmed.qamesh@gmail.com`.
