import pandas as pd
import sys
from pathlib import Path

# --- Configuration ---
# The annotated file you created in the previous step
ANNOTATED_FILE_PATH = Path ('result/PGS000337_annotated_002_matching.csv')
# The new file where the unique gene list will be saved
OUTPUT_GENE_LIST_FILE = Path('result/unique_gene_list_test.txt')
# The name of the column that contains the gene names
GENE_COLUMN_NAME = 'Gene(s)'


def extract_unique_genes():
    """
    Reads an annotated variant file, extracts the unique gene names,
    and saves them to a new text file.
    """
    try:
        # --- 1. Load the Annotated CSV File ---
        annotated_df = pd.read_csv(ANNOTATED_FILE_PATH)
        print(f"Successfully loaded {len(annotated_df)} variants from {ANNOTATED_FILE_PATH}")

        # --- 2. Check if the Gene Column Exists ---
        if GENE_COLUMN_NAME not in annotated_df.columns:
            print(f"Error: Column '{GENE_COLUMN_NAME}' not found in the file.")
            print("Please make sure the column name is correct.")
            sys.exit(1)

        # --- 3. Extract Unique Gene Names ---
        # First, drop any rows where the gene name is missing (NaN)
        # Then, get the unique values from the column
        unique_genes = annotated_df[GENE_COLUMN_NAME].dropna().unique()

        # Sort the list alphabetically
        unique_genes.sort()

        print(f"\nFound {len(unique_genes)} unique gene(s).")
        print("--------------------")
        # Print the list to the console
        for gene in unique_genes:
            print(gene)
        print("--------------------")


        # --- 4. Save the Unique List to a File ---
        with open(OUTPUT_GENE_LIST_FILE, 'w') as f:
            for gene in unique_genes:
                f.write(f"{gene}\n")

        print(f"\nSuccess! Unique gene list has been saved to: {OUTPUT_GENE_LIST_FILE}")


    except FileNotFoundError:
        print(f"Error: The file '{ANNOTATED_FILE_PATH}' was not found.")
        print("Please make sure this file exists in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


# --- Run the Extraction Process ---
if __name__ == "__main__":
    extract_unique_genes()
