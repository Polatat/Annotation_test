
import pandas as pd
import sys

# --- Configuration ---
# File paths for your input files
PGS_FILE_PATH = '../data/PGS000337.txt'
ANNOTATION_FILE_PATH = '../data/GASA-24v1-0_A1.hg19.annotated.txt'
OUTPUT_FILE_PATH = '../result/PGS000337_annotated_002_matching.csv' # The final, merged file

def annotate_variants():
    """
    Reads a PGS scoring file and an annotation file, merges them based on
    chromosome and position, and saves only the matched variants to a CSV file.
    """
    try:
        # --- 1. Load the PGS Scoring File ---
        # We skip the header lines that start with '#'
        pgs_variants = pd.read_csv(
            PGS_FILE_PATH,
            sep='\t',
            comment='#',
            dtype={'chr_name': str} # Read chromosome as string to avoid issues
        )
        print(f"Successfully loaded {len(pgs_variants)} variants from {PGS_FILE_PATH}")

        # --- 2. Load the Annotation File ---
        annotations = pd.read_csv(
            ANNOTATION_FILE_PATH,
            sep='\t',
            dtype={'Chr': str} # Read chromosome as string
        )
        print(f"Successfully loaded {len(annotations)} annotations from {ANNOTATION_FILE_PATH}")

        # --- 3. Create the Common Matching Key in Both DataFrames ---
        # This key will be in the format 'chromosome:position'
        pgs_variants['chr_pos_key'] = pgs_variants['chr_name'] + ':' + pgs_variants['chr_position'].astype(str)
        annotations['chr_pos_key'] = annotations['Chr'] + ':' + annotations['MapInfo'].astype(str)
        print("Created 'chr_pos_key' for matching in both files.")

        # --- 4. Merge the two DataFrames using an 'inner' join ---
        # An 'inner' join keeps ONLY the rows where the key exists in BOTH files.
        # This effectively removes any variants that don't have an annotation.
        annotated_df = pd.merge(
            pgs_variants,
            annotations,
            on='chr_pos_key',
            how='inner'
        )
        print("Successfully merged the two files, keeping only matched variants.")

        # --- 5. Analyze and Clean up the final DataFrame ---
        # The number of rows in the new dataframe is the number of matches.
        matches_found = len(annotated_df)
        print(f"Found and kept {matches_found} matching annotations for the {len(pgs_variants)} variants.")

        # You can drop the extra key columns if you want a cleaner output
        # Also, we can rename columns for clarity
        annotated_df.drop(columns=['chr_pos_key', 'Chr', 'MapInfo'], inplace=True, errors='ignore')
        annotated_df.rename(columns={'Name': 'Annotation_Name', 'Alleles': 'Annotation_Alleles'}, inplace=True)


        # --- 6. Save the Result ---
        annotated_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print(f"\nSuccess! Matched annotations file has been saved to: {OUTPUT_FILE_PATH}")
        print(f"The final file contains {len(annotated_df)} variants.")

    except FileNotFoundError as e:
        print(f"Error: Could not find a file. Please make sure the file paths are correct.")
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# --- Run the Annotation Process ---
if __name__ == "__main__":
    annotate_variants()