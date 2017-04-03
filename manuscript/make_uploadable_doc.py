import os,re

current_filename = "ramachandran_handedness.tex"
target_filename_base = "ramachandran_handedness"
target_dir = "./for_peerj"

if not os.path.isdir(target_dir):
	os.makedirs(target_dir)


latex_files_needed = ['wlpeerj.cls','wlpeerj.bst'] #'all.bib'
for latexfn in latex_files_needed:
	command = "cp  "+latexfn+" "+target_dir+"/"+latexfn 
	print command
	os.system(command)

f = open(current_filename,"r")
block = f.read()
f.close()

get_filenames = re.compile('includegraphics[^{]*\{([^}]+)\}',re.M)
filenames =  get_filenames.findall(block)
old_to_new_fig_names = []
for fni in range(len(filenames)):
	oldfn = filenames[fni]
	newfn = "Fig"+str(fni+1)+"."+oldfn.split(".")[-1]
	
	command = "cp "+oldfn+" "+target_dir+"/"+newfn
	print command
	os.system(command)
	block = block.replace(oldfn,newfn)

fn = target_dir+"/"+target_filename_base.rstrip("_")+".tex"
f=open(fn,"w")
f.write(block)
f.close()

FILENAME = target_filename_base.rstrip("_")

runmetemplate = """import os
fn = "FILENAME"
os.system("pdflatex "+fn)
os.system("bibtex "+fn)
os.system("pdflatex "+fn)
os.system("pdflatex "+fn)
os.system("evince "+fn+".pdf")
"""

fn = target_dir+"/runme.py"
f = open(fn,"w")
f.write(runmetemplate.replace("FILENAME",FILENAME))
f.close()
print fn
