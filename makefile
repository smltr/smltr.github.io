format:
	python3 format.py unformatted_resume.txt site/resume.txt --width 80 --padding 3 -m 1

push:
	git add .
	git commit -m "Publish"
	git push
