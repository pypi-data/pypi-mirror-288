This is a Python implementation of [BayesPrism](https://github.com/Danko-Lab/BayesPrism).


Usage
```python
from pybayesprism import process_input, prism

sc_dat_filtered = process_input.cleanup_genes(sc_dat, "count.matrix", "hs", \
                  ["Rb", "Mrp", "other_Rb", "chrM", "MALAT1", "chrX", "chrY"], 5)
                  
sc_dat_filtered_pc = process_input.select_gene_type(sc_dat_filtered, ["protein_coding"])

my_prism = prism.Prism.new(reference = sc_dat_filtered_pc, 
                          mixture = bk_dat, input_type = "count.matrix", 
                          cell_type_labels = cell_type_labels, 
                          cell_state_labels = cell_state_labels, 
                          key = "tumor", 
                          outlier_cut = 0.01, 
                          outlier_fraction = 0.1)

bp_res = my_prism.run(n_cores = 36, update_gibbs = True)      
```
