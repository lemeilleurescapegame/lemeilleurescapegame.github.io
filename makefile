git :
	git add .
	git commit -m '$m'
	git push 

git_tag :
	git add .
	git commit -m "$(m)"
	git tag $(tag)
	git push origin $(tag)
