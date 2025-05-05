#!/bin/zsh

# Preprocessing scripts
print -P '%F{green}Preprocessing thesis...%f '

python scripts/OrderCodeVersionTable.py
python scripts/ReallocateBibTokens.py
python scripts/Trineify.py -ow y
python scripts/Transclusions.py

latexmk -shell-escape -pdf main.tex

print -P '%F{green}Compiled thesis using latexmk%f '

# do dangerous stuff
date --iso-8601='seconds' | tr '\n' ',' >> wc.txt
pdftotext main.pdf - | tr -d '.' | wc -w >> wc.txt
print -P "%F{green}Generated word count files%f "

print -P "%F{green}Preprocessing Stage I (parsing todos)...%f "
python scripts/ParseTodos.py
rm main.todos

cp wc.txt ../live_website/PhD/wc.txt
cp quotes.html ../live_website/PhD/quotes.html

# pandoc -s --toc main.tex -o TOC.html -t html --template=pandoctemplate.md

#########################
# Output Postprocessing #
#########################

print -P "%F{green}Postprocessing thesis into chapters...%f "
mkdir -p rendered_chapters
mv main.pdf PhD_Thesis.pdf
python scripts/SplitPDF.py
mv main.log log

print -P "%F{green}Running latexmk cleanup.%f "
latexmk -f -c main.tex
# latexmk -f -c main-autopp.tex
rm -f main-pics.pdf
rm -f main-autopp.todos

notify-send --hint int:transient:1 "Thesis Compiler" "Main compilation finished. Postprocessing is about to begin -- input required."

read -q "REPLY?Commit work to GitHub? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	print -P "%F{green}Committing to GitHub...%f "
	cd ../live_website
	git add PhD/wc.txt PhD/quotes.html PhD/index.html
	git commit -m "update thesis progress" -S
	git push origin master
	cd ../PhD\ Thesis
	sleep 1
	git add .
	git commit -m "update thesis progress" -S
	git push origin main
	sleep 1
fi