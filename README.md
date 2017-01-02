# Supplementary Information for the paper: On the other hand: chirality and the peptide

The subdirectory 'manuscript/' contains the lates manuscript: ramachandran_chirality.pdf<br>
The subdirectory 'manuscript/figures/' contains the latest figure files in vector (PDF) format.
'>cd manuscript; python compileme.py'compiles the latex file 'ramachandran_chirality.tex' and produces 'ramachandran_chirality.pdf' ('>' indicates the command line prompt). For the this command to work out-of-the-box, you will need pdflatex (try '>pdflatex') and bibtex (try '>bibtex'). To use another latex executable, modify 'manuscript/compileme.py'.<br><br>

The main file that produces all other the main data within the paepr is './study_handedness.py' (tested in Python 2.7; requirements: Numpy, Scipy, Biopython, Matplotlib, Seaborn). The location of each figure's panel is stored in 'output.txt'.<br><br>

<b><i>To setup:</b></i> <br>
<b>*</b> Uncompress 'imports_and_data.tgz' ('>tar xvzf something.tar.gz'). This creates the main home for results -- './graphs/' (another directory './pdbs/' will also be created by the python script) -- and './local_imports' (which is used by the python script; also, useful VMD scripts are available there).<br><br>
<b>*</b> To re-render peptide configurations, you will need VMD (try '>vmd'; it is available here: <a href='http://www.ks.uiuc.edu/Research/vmd/'>www.ks.uiuc.edu/Research/vmd/</a>).<br>

