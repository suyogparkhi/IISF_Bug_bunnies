# IISF_Bug_bunnies
This is the repository of Bug Bunnies , Group-3 IISF Space Hackathon 2023
<br><br>
Problem Statement :
<br>
Group 3, Topic 1: Optimized Geospatial Data Management for Bhuvan Platform.
<br><br>
Our Approach :
<br>
Implemented Modified MinHash algorithm on the given unstructured geospatial data . This Algorithm converts binary and text convertable files to text files and applies shingling which generates a pickle file . This is the output of the preprocessing step . We run the MinHash algorithm on the generated pickle file . The Minhash algorithm gives a set of n nearest redundant files (for eg. if file1 , file2 and file3 are similar the ouptput will be the set of 3 ie. {file1 , file2 , file3}) . Integrating this output with the fronted to display redundant files and addition/deletion of files . Now , our data is ready for geospatial processing and storage . We store and process the geospatial data efficiently using postgreSQL and duckDB . Implementing an efficient cataloging system for this data using filtering techniques . 
<br><br>
Tech Stacks :
<br>
Python , Flask , duckDB 
<br><br>
updates (timestamp : 17th jan 10 pm) :
<br>
1) Completed with data preprocessing and MinHash Algorithm 
2) 50% frontend completed
3) Yet to integrate MinHash with frontend
4) Sample Cataloging completed
5) Yet to write generic code to implement Cataloging and its frontend integration
<br>
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
<br>
Working Model :
<br>
Frontend :
<img width="1470" alt="Screenshot 2024-01-17 at 11 23 23 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/f3bd5f27-4801-48cc-9658-ff1ca44f67b9">
<br>
MinHash :
Preprocessing (conversion to txt) :
![WhatsApp Image 2024-01-17 at 23 29 57](https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/a075c172-e138-4239-a29d-afc132f92cdb)
list of redundant files :
![WhatsApp Image 2024-01-17 at 23 30 21](https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/54e0d93d-2bdf-4fe8-b70f-a747cb5a4e51)
jaccard simmilarity :
![WhatsApp Image 2024-01-17 at 23 30 34](https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/0d459433-8a21-4b30-b84c-fad74de394a1)
redundancy set :
![WhatsApp Image 2024-01-17 at 23 30 49](https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/01f40868-efc8-49a3-9dd0-54d7f694e27f)
Gespatial configuration using duckDB :
<br>
<img width="1225" alt="Screenshot 2024-01-17 at 11 25 11 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/18eb8cea-3de7-439f-b4a2-95d1e9860b7c">
<img width="1358" alt="Screenshot 2024-01-17 at 11 25 17 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/4efe337f-9197-4163-ba1e-939d973ba879">
<img width="1470" alt="Screenshot 2024-01-17 at 11 25 39 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/5de4bff3-79ce-44ac-886b-56f585a0e9c9">
<br>
Sample Cataloging :
<img width="1213" alt="Screenshot 2024-01-17 at 11 23 59 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/2c24e0c2-419b-400c-ab38-9b7db11a2bb2">
<img width="1270" alt="Screenshot 2024-01-17 at 11 24 06 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/4b1e1141-3834-471b-ad26-efb15fa04168">
<img width="1193" alt="Screenshot 2024-01-17 at 11 24 19 PM" src="https://github.com/suyogparkhi/IISF_Bug_bunnies/assets/120791980/fc730d1f-b53d-43c3-a235-5e473b39837c">
<br>



