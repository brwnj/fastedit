# Simple Fasta Editing
Quickly alter the headers of fasta entries using a CSV.

# Installation
```
git clone git@github.com:brwnj/fastedit.git
cd fastedit
python setup.py install
```

# Usage
Our test fasta:
```
>entry_1
ACGTACTGACGTACTG
>entry_2
ACGTACTGACGTAC
>entry_3
TGACGTACGTA
```

Retrieve the headers from the fasta:
```
fastedit get --verbose -o headers.csv my.fasta
3 headers exported.
```

Edit your CSV file to rename or exclude from resultant fasta:
```
entry_1,new_name_for_entry_1
entry_2,
```

Create new fasta using your CSV:
```
fastedit put --verbose my.fasta headers.csv
>new_name_for_entry_1
ACGTACTGACGTACTG
>entry_2
ACGTACTGACGTAC
Input fasta contained 3 records
You renamed 1 and kept a total of 2
```
