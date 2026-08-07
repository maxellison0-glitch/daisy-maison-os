# Making signauto its own repository (one-time)

This folder is the complete signauto system, seeded here because the GitHub
integration could not create repositories. To stand it up as its own repo:

1. On github.com create an empty **private** repository `maxellison0-glitch/signauto`
   (no README, no .gitignore).
2. From this folder:

```powershell
git init -b main
git add -A
git commit -m "signauto initial"
git remote add origin https://github.com/maxellison0-glitch/signauto
git push -u origin main
```

3. Delete this file from the new repo, and delete this whole folder from
   daisy-maison-os. `git clone` the new repo somewhere clean and work there.

(Or: create the empty repo, then tell the Claude session "repo created" and it
pushes this exact tree for you.)
