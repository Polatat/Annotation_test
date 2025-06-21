
# Description
 21/06/2025

This repository is for  gene annotation  from
file PGS (PGS cataloog) [title](https://www.google.com/url?sa=j&url=https%3A%2F%2Fwww.pgscatalog.org%2Fscore%2FPGS000337%2F&uct=1747741898&usg=ibLCbAeDlazjwOuSa7hsUA-wVw8.&opi=73833047&source=chat.) regarding to Polygenic riisk score in Coronary artery disease from Koyama S et al. Nat Genet (2020).

Annotated with Infinium Asian Screening Array file:
[title](https://support.illumina.com/downloads/infinium-asian-screening-array-v1-0-support-files.html)

## Installation

You need to create the environment and install the packages before run the scripts. 

``` bash

python -m venv .venv

source .venv/bin/activate

pip install -r requirement.txt

``` 

## File structure

The folder structure is following this :

``` bash
├── data/
│   ├── PGS_test/
│   │   ├── pgs_varaints_test01.csv
│   │   ├── pgs_varaints_test01.txt
│   │   ├── ASA_hg19_annotated_test_file.txt
│   │   ├── ASA-24v1-0_A1.hg19.annotated.txt
│   │   └── PGS000337.txt
├── log/
│   └── log_file_01.txt
├── notebook/
│   └── annotation_notebook.ipynb
├── result/
│   ├── annovar_result_test/
│   │   └── annoovar_PGS_annotation_test.csv
│   ├── PGS000337_annotated_001_unmatching.csv
│   ├── PGS000337_annotated_002_matching.csv
│   ├── PGS000337_annotated_test.csv
│   └── unique_gene_list.txt
├── script/
│   ├── annotation.py
│   ├── annovar_file_prepare.py
│   └── exactgene.py
├── .gitignore
├── README.md
└── requirement.txt

```


## Variant Annotation and Analysis Workflow

The genetic variants associated with the Polygenic Score (PGS) PGS000337 were subjected to two distinct annotation pipelines to characterize their genomic context and potential functional significance.

**1. Custom Annotation against the ASA Reference File**

The PGS variant list was initially annotated against a custom annotation file derived from the Infinium Asian Screening Array (ASA). This procedure was executed using the annotation.py script and resulted in two distinct output files:

**PGS000337_annotated_001_unmatching.csv:** This file contains the complete list of all original PGS variants. A **left-join** methodology was used to ensure that variants were retained even if they did not have a corresponding entry in the ASA annotation file.

**PGS000337_annotated_002_matching.csv**: This file represents a filtered subset containing only the PGS variants that were successfully matched to an entry in the ASA annotation file, generated using an **inner-join** methodology.

**2. Functional Annotation using ANNOVAR**

An independent and more comprehensive functional annotation was performed using the ANNOVAR software (v. 2025-03-02 22:37:01 -0500 (Sun,  2 Mar 2025, written in Perl). This workflow did not involve the custom ASA file.

Input File Preparation: The initial PGS variant list was converted into the required 5-column ANNOVAR format (.avinput) using the annovar_file_prepare.py script.

Annotation Command: The prepared input file, PGS00337.avinput, was processed with the table_annovar.pl command. Annotation was performed against standard bioinformatics databases, including RefSeq for gene information, gnomAD for population frequencies, and ClinVar for clinical significance.
Output: This pipeline generated the richly annotated file annoovar_PGS_annotation_test.csv, where each variant is described by multiple functional metrics.


**3. Gene List Extraction**

A script, exacgene.py, was created to extract a non-redundant list of gene names from the annotated results. However, this method was determined to obscure the direct variant-to-gene relationship, which is preserved in the complete annotated CSV files.




## ANNOVAR  Command 

``` bash

 perl table_annovar.pl data/pgs_variants.avinput \                         
  humandb/ \
  -buildver hg19 \
  -out my_first_anno_test \
  -protocol refGene,gnomad211_exome,clinvar_20240917 \
  -operation g,f,f \
  -nastring . -csvout
  ```

  **Note:**  Please note that I still do not understand completely with each command in the program but these are detail that I know from now. Moreover, I think there are more columns that involve in cancer like benign and malignant in annoovar_PGS_annotation_test.csv because I use clinvar_20240917 database.



| Command | Description|             
| --------- | ----------|
| perl table_annovar.pl | Executes the main ANNOVAR script that combines multiple annotations into a single output table.|
| data/pgs_variants.avinput | The path to your input file, which contains the list of variants to be annotated. |
|humandb/| The path to the directory where ANNOVAR's downloaded database files are stored.|
|-buildver hg19| Specifies the genome build version. This tells ANNOVAR your input coordinates are based on Human Genome Reference Build 19.|
|-out my_first_anno_test| Sets the prefix for your output file. The final result will be named my_first_anno_test.hg19_multianno.csv.|
|-protocol refGene,...| Defines the specific annotations to perform. In this case: refGene (gene information), gnomad211_exome (population frequency), and clinvar_20240917 (clinical significance).|
|-operation g,f,f| Specifies the type of operation for each protocol in the list (g = gene-based, f = filter-based). The order must match the -protocol list.|
|-nastring .| Sets the string to use for missing values. If an annotation isn't found for a variant, it will be marked with a period (.).|


| -csvout|  A helpful flag that consolidates all results into a single, easy-to-use Comma-Separated Values (.csv) file.| 

**More detailed:** [title](https://annovar.openbioinformatics.org/en/latest/)