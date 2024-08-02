# bioseq_analysis

A package for biosequence analysis.

## Installation

pip install git+https://github.com/jcevall1/alig_seq_dist.git


## Usage

```python
from bioseq_analysis.analysis import get_dist_date_files

input_pattern = "data/*.csv"
aligned_sequence_fasta_file = "sequences.fasta"

get_dist_date_files(input_pattern, aligned_sequence_fasta_file)
```
