import pandas as pd
import sys
from pathlib import Path

# --- Configuration ---
# The annotated file you created in the previous step
ANNOTATED_FILE_PATH = Path ('result/annovar_result_test/annoovar_PGS_annotation_test.csv')
# The new file where the unique gene list will be saved
OUTPUT_GENE_LIST_FILE = Path('result/annovar_gene_extraction.txt')
# A list of possible column names that might contain the gene names.
POSSIBLE_GENE_COLUMNS = ['Gene.refGene', 'Gene(s)', 'Gene']


def extract_unique_genes():
    """
    Reads an annotated variant file, extracts the unique gene names,
    and saves them to a new text file.
    """
    try:
        # --- 1. Load the Annotated CSV File ---
        annotated_df = pd.read_csv(ANNOTATED_FILE_PATH)
        print(f"Successfully loaded {len(annotated_df)} variants from {ANNOTATED_FILE_PATH}")

        # --- 2. Find which gene column exists in the file ---
        gene_column_name = None
        for col in POSSIBLE_GENE_COLUMNS:
            if col in annotated_df.columns:
                gene_column_name = col
                break

        if gene_column_name is None:
            print(f"Error: Could not find a gene column. Searched for {POSSIBLE_GENE_COLUMNS}.")
            print("Please check the CSV file and update POSSIBLE_GENE_COLUMNS in the script if needed.")
            sys.exit(1)
        print(f"\nFound gene information in column: '{gene_column_name}'")

        # --- 3. Extract Unique Gene Names ---
        # First, drop any rows where the gene name is missing (NaN)
        # Then, get the unique values from the column
        unique_genes = annotated_df[gene_column_name].dropna().unique()

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
