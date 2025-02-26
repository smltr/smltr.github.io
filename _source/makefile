format:
	python3 format.py unformatted_resume.txt ../resume.txt --width 80 --padding 3 -m 1
	python3 format.py unformatted_resume.txt ../mobile_resume.txt --width 53 --padding 1 -m 1
	cp ../resume.txt ~/Desktop/sam_trouy_resume.txt

push:
	git add ../.
	git commit -m "Publish"
	git push
