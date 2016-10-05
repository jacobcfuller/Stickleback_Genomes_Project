Depth of coverage files are named as in `musDNA_NAMING.md`


Depth of coverage was calculated using `bedtools genomecov` and
only used the third column of output, as such:

```bash
bedtools genomecov -ibam $BAM_FILE -g $REF_FASTA | \
    awk '{print $3}' >> OUT_FILE.txt
```

I then stitched these files together, creating a tab-delimited
table where each column is a sample's depth at a given position.
Positions are inferred from the row number.

Below is an example illustrating how I combined files:

```bash
cast_names=(cast_H12 cast_H15 cast_H28 cast_H34)
dom_names=(dom_DF dom_D8 dom_D9 dom_D22)

# Add headers
echo ${cast_names[@]/#cast_/} | tr ' ' '\t' | gzip > cast_19b9.txt.gz
echo ${dom_names[@]/#dom_/} | tr ' ' '\t' | gzip > dom_19b9.txt.gz

# Add data
paste ${cast_names[@]/%/.txt} | gzip >> cast_19b9.txt.gz
paste ${dom_names[@]/%/.txt} | gzip >> dom_19b9.txt.gz
