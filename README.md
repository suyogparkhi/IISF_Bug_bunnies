# IISF_Bug_bunnies
This is the repository of Bug Bunnies , Group-3 IISF Space Hackathon 2023
<br>
Problem Statement :
<br>
Group 3 : Topic 1: Optimized Geospatial Data Management for Bhuvan Platform.
<br>
Our Approach :
Implemented Modified MinHash algorithm on the given unstructured geospatial data . This Algorithm converts binary and text convertable files to text files and applies shingling which generates a pickle file . This is the output of the preprocessing step . We run the MinHash algorithm on the generated pickle file . The Minhash algorithm gives a set of n nearest redundant files (for eg. if file1 , file2 and file3 are similar the ouptput will be the set of 3 ie. {file1 , file2 , file3}) . Integrating this output with the fronted to display redundant files and addition/deletion of files . Now , our data is ready for geospatial processing and storage . We store and process the geospatial data efficiently using postgreSQL and duckDB . Implementing an efficient cataloging system for this data using filtering techniques . 
<br>
Tech Stacks :
<br>
Python , Flask , duckDB .
<br>
updates (timestamp : 17th jan 10 pm) :
<br>
1) Completed with data preprocessing and MinHash Algorithm 
2) 50% frontend completed
3) Yet to integrate MinHash with frontend
4) Sample Cataloging completed
5) Yet to write generic code to implement Cataloging and its frontend integration
   
Installations:
<br>
<code>
pip install flask
pip install duckdb leafmap
conda create -n geo python=3.11
conda activate geo
conda install -c conda-forge mamba
mamba install -c conda-forge python-duckdb duckdb-engine jupysql leafmap
</code>
