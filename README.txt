Portfolio Analysis

Submission by Maya Gusak
Deadline 11.06.2024


The following files are submitted for assessment:

stats.py
Notebook.ipynb
app.py
index.html
Dockerfile


stats.py contains the majority of the computation involving the two files px_etf.csv and tx_etf.csv. 
Running this application as main will output these computations. 
The file output.txt contains this output, precomputed.
[run: python stats.py]

Notebook.ipynb is a Jupyter Notebook version of these computations, with some explanations of the 
financial pricing theory. I have also included some graphs for data visualization.
[run: jupyter notebook Notebook.ipynb]

app.py uses flask to run a simple web application displaying these results. I added some interactive
functionality like sliders that modify computed values, and Notebook.ipyb should also be accessible from 
a link at the top of the web application. The html is written in templates\index.html.
[run: python app.py]

The docker container running stats.py is available at https://hub.docker.com/repository/docker/maya4maya4/portfolio_analysis/.

Dockerfile allows docker to build a container image to run app.py. Unfortunately, I had issues
with building; installing libraries like pandas, flask, etc. was impossible due to
an SSL connection error, and after a few hours digging around, I found that the official python images 
have these bugs when the Docker Desktop version is outdated. I updated Docker Desktop to the newest version,
tried manually installing SSL libraries, but the fix that ended up working for me was to use ubuntu
as a base image. See further discussion: https://stackoverflow.com/questions/60674509/certificate-verify-failed-on-pip-install-on-docker
I also struggled running app.py and Notebook.ipynb from inside the container because of connection issues.  
[run stats.py: docker run --rm qc_container]
[run interactive: docker run -it -p 8888:8888 -p 5000:5000 --rm qc_container]


Thanks again to Quantica for this assignment! I learned a lot and am excited to share
my solution. 

Please feel free to contact me at +41 78 261 05 79 or mgusak@ethz.ca if there are any issues and I would be happy to discuss further.
