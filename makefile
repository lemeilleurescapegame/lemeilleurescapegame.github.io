git :
	git add .
	git commit -m '$m'
	git push 


git_send_public:
	cd _site
	git init
	git config user.name "github-actions"
	git config user.email "github-actions@github.com"
	git remote set-url origin git@github.com:lemeilleurescapegame/lemeilleurescapegame.github.io.git
	git checkout main
	git add .
	git commit -m "Update"
	git push -f origin main
