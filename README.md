# backbone_chirality

The main file that produces all other graphs and renderings is 'study_handedness.py'.<br>
'>cd manuscript; python compileme.py' compiles the latex file 'ramachandran_chirality.tex' and produces 'ramachandran_chirality.pdf'.<br><br>

<b><i>To setup:</b></i> <br>
<b>1)</b> Uncompress 'local_imports.tar.gz' and 'raw_data.tgz' by right-clicking on the file and choosing the appropriate un-compression option or ">tar xvzf something.tar.gz' ('>' indicates the command line prompt)<br>
<b>2)</b> make sure that you have access to Python <v3.0 (try '>which python'), and, the following python modules: Numpy, Biopython, Matplotlib.<br>
<b>3)</b> In case you want to re-compile the Latex file (within manuscript/), run '>python compileme.py'. For it to work out-of-the-box, you will need pdflatex (try '>pdflatex') and bibtex (try '>bibtex'). To use another latex executable, modify 'manuscript/compileme.py'.<br>
<b>4)</b> To re-render peptide configurations, you will need VMD (try '>vmd'; it is available here: <a href='http://www.ks.uiuc.edu/Research/vmd/'>www.ks.uiuc.edu/Research/vmd/</a>).<br>

