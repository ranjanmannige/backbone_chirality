import os

current_filename = "ramachandran_chirality.tex"
target_filename_base = "ramachandran_chirality"
target_dir = "for_peerj"

if not os.path.isdir(target_dir):
	os.makedirs(target_dir)


os.system("cp wlpeerj.cls "+target_dir+"/"+"wlpeerj.cls")
os.system("cp wlpeerj.bst "+target_dir+"/"+"wlpeerj.bst")

f = open(current_filename,"r")
block = f.read()
f.close()

get_filenames = re.compile('[\]includegraphics[^{]*\{([^}]+)\}',re.M)
print get_filenames.findall(block)
exit()


old_to_new_fig_names = {
#"PLOS-submission.eps":"PLOS-submission.eps",
"figures/fig1.eps":  "Fig1.eps",
"figures/fig2.eps":  "Fig2.eps",
"figures/pathogenicity3.eps":  "Fig3.eps",
"figures/fig_ss_line2.eps":  "Fig4.eps",
"figures/collage2.eps":  "Fig5.eps",
"figures/fig_classes4.eps":  "Fig6.eps",
"figures/binary_birth_b.eps":  "Fig7.eps",
"figures/fig_coords2.eps":  "Fig8.eps",
"figures/sigma_vs_rmsa_and_rmsd_b.eps":  "Fig9.eps"
}


for oldfn,newfn in old_to_new_fig_names.items():
	command = "cp "+oldfn+" "+target_dir+"/"+newfn
	print command
	os.system(command)
	
	"""
	if oldfn[-len(".pdf"):] == ".pdf":
		oldfn = oldfn[:-len(".pdf")]
	
	if newfn[-len(".pdf"):] == ".pdf":
		newfn = newfn[:-len(".pdf")]
	"""
	
	#if not oldfn[-len(".eps"):] == ".eps":
	block = block.replace(oldfn,newfn)
exit()
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
