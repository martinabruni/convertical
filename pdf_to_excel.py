import pdfplumber
import pandas as pd


# Function to extract and process data from the PDF
def generate_excel(pdf_path, output_excel_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract the first page (assuming the calendar is on the first page)
        page = pdf.pages[0]

        # Extract the table from the page
        table = page.extract_table()

        # Create a DataFrame from the extracted table data, skipping the first column
        df = pd.DataFrame(table[1:])  # Skip the first row with headers
        df = df.iloc[:, 1:]  # Skip the first column
        # Rename the first "Orario" column to "Orario inizio" and the second to "Orario fine"
        df.columns = df.iloc[0]  # Set the first row as the header
        df = df.drop(index=0)  # Remove the first row after setting it as the header
        df.rename(
            columns={df.columns[1]: "Orario inizio", df.columns[2]: "Orario fine"},
            inplace=True,
        )

        # Rename the last empty column to 'Professore'
        df.rename(columns={df.columns[-1]: "Professore"}, inplace=True)

        # Filter rows where 'Unità formativa' is not empty
        df_filtered = df[df["Unità formativa"].notna() & (df["Unità formativa"] != "")]

        # Save the processed data to an Excel file
        df_filtered.to_excel(output_excel_path, index=False)


if __name__ == "__main__":
    generate_excel("./calendario.pdf", "./output_calendario.xlsx")
