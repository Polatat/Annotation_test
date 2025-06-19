import pandas as pd
import sys
from pathlib import Path
# --- Configuration ---
# The name of your PGS scoring file downloaded from the PGS Catalog
PGS_FILE_PATH = Path('data/PGS000337.txt')
# The name of the output file that will be used as input for ANNOVAR
ANNOVAR_INPUT_FILE = 'pgs_variants.avinput'

def convert_pgs_to_annovar_input():
    """
    Reads a PGS Catalog scoring file and converts it into the 5-column format
    required by ANNOVAR.
    """
    try:
        # --- 1. Load the PGS Scoring File ---
        # We skip the header lines that start with '#'
        pgs_variants = pd.read_csv(
            PGS_FILE_PATH,
            sep='\t',
            comment='#',
            dtype={'chr_name': str, 'chr_position': int}
        )
        print(f"Successfully loaded {len(pgs_variants)} variants from {PGS_FILE_PATH}")

        # --- 2. Create the ANNOVAR-formatted DataFrame ---
        # Create an empty DataFrame with the required column names
        annovar_df = pd.DataFrame()

        # Fill the columns based on the PGS data
        annovar_df['Chr'] = pgs_variants['chr_name']
        annovar_df['Start'] = pgs_variants['chr_position']
        annovar_df['End'] = pgs_variants['chr_position'] # For SNPs, Start and End are the same
        
        # --- 3. Extract Reference Allele ---
        # The reference allele is the 3rd part of the 'variant_description' string (e.g., 'G' in '1:959231:G:A')
        # We split the string by the ':' character and take the 3rd element (index 2)
        try:
            annovar_df['Ref'] = pgs_variants['variant_description'].str.split(':').str[2]
        except IndexError:
            print("Error: Could not extract reference allele from 'variant_description'.")
            print("Please ensure the column is in the format 'Chr:Pos:Ref:Alt'.")
            sys.exit(1)

        annovar_df['Alt'] = pgs_variants['effect_allele'] # The effect allele is our alternative allele

        # --- 4. Add other columns from the original file (optional but useful) ---
        # This helps you merge the ANNOVAR results back to your original data later
        annovar_df['Original_Effect_Weight'] = pgs_variants['effect_weight']
        annovar_df['Original_Variant_Description'] = pgs_variants['variant_description']


        # --- 5. Save the Result to a File ---
        # ANNOVAR input should NOT have a header row and should be tab-separated.
        annovar_df.to_csv(ANNOVAR_INPUT_FILE, sep='\t', index=False, header=False)

        print(f"\nSuccess! ANNOVAR input file created: {ANNOVAR_INPUT_FILE}")
        print(f"It contains {len(annovar_df)} variants ready for annotation.")
        print("\n--- File Preview (first 5 lines) ---")
        print(annovar_df.head().to_string(index=False, header=False))
        print("------------------------------------")


    except FileNotFoundError:
        print(f"Error: The file '{PGS_FILE_PATH}' was not found.")
        print("Please make sure this file exists in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


# --- Run the Conversion Process ---
if __name__ == "__main__":
    convert_pgs_to_annovar_input()
