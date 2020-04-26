# IRTM_SARS-COV2


Branches:
_________

******************
Master
******************

[...]

******************
Extract_abstracts
******************

	----------------------
	Extraction_CSV-Txt.py 
	----------------------
	--> Run w/o arguments
	eg: Python Extraction_CVS-Txt.py

		Reads			"metadata.csv"
		Creates dir		"Extractes_abstracts"
		Stors  1.txt/abs	"abs_<index>.txt
		
	----------------------
	tfidf.py
	----------------------
	--> Run w/ <corpus> <interest>		
	eg: Python tfidf.py Extracted_abstract_sample 20

		Outputs <interest> number of words for each abstracts in <corpus>
		
	
