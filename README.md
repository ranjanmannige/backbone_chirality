# Supplementary Information for the paper: An exhaustive survey of regular peptide conformations using a new metric for backbone handedness (h)

The subdirectory 'manuscript/' contains the latest manuscript: ramachandran_handedness.pdf<br>
The subdirectory 'manuscript/figures/' contains the latest figure files in vector (PDF) format.
'>cd manuscript; python compileme.py'compiles the latex file 'ramachandran_handedness.tex' and produces 'ramachandran_handedness.pdf' ('>' indicates the command line prompt). For the this command to work out-of-the-box, you will need pdflatex (try '>pdflatex') and bibtex (try '>bibtex'). To use another latex executable, modify 'manuscript/compileme.py'.<br><br>

The main Python script that produces most of the main data within the paper is './study_handedness.py' (tested in Python 2.7; requirements: a local installation of VMD, and the following Python modules: Numpy, Scipy, Biopython, Matplotlib; optional: Seaborn). The location of each figure's panel is stored in 'output.txt'. Another Python script ('./study_ss.py') downloads (from SCOP), analyzes and graphs various backbone structural distributions (e.g., distribution of secondary structural elements in Ramachandran plots).<br><br>


<b><i>To setup:</b></i> <br>
<b>*</b> Uncompress 'imports_and_data.tgz' ('>tar xvzf imports_and_data.tgz'). This creates the main home for results -- './graphs/' (another directory './pdbs/' will also be created by the python script) -- and './local_imports' (which is used by the python script; also, useful VMD scripts are available there).<br><br>
<b>*</b> To re-render peptide configurations, you will need VMD (try '>vmd'; it is available here: <a href='http://www.ks.uiuc.edu/Research/vmd/'>www.ks.uiuc.edu/Research/vmd/</a>).<br>

