# ExternalSorting
The Experiments of SEU course Data Structure and Algorithm (Seminar)

This experiment focuses on optimizing external merge sort for large-scale data processing to improve sorting efficiency and reduce disk I/O overhead. In the first experiment, a baseline external merge sort process was implemented, generating initial runs and completing sorting via two-way merging, serving as a basis for subsequent optimizations. In the second experiment, a strategy involving buffers and a minimum loser tree was introduced to enable dynamic run generation, extending run length and effectively reducing the number of I/O operations. The third experiment employed a multi-way merge strategy to further reduce the number of merge passes and I/O operations. Experimental results show that optimizing run generation and applying a multi-way merge strategy significantly enhance overall sorting performance.
