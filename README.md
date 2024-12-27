# templates

Create SSH access key on a linux machine
```
ssh-keygen -t ed25519 -C "essans@me.com"
```

and save as (for eg) ```github_template``` then:

```
pbcopy < github_template.pub
```

to copy public key to clipboard from where it can be pasted into github as a new ssh key
