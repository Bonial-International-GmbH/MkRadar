# MkRadar
*Markdown Wiki Generator*

## Attention

This repo in not ready for production use and still acting as a POC

## problem
We are facing two problems:

Usually, when people changing their code they keep forgetting to update related documents on the wiki side
Having a complete and well-structured wiki which we can track its changes and change its structure smoothly is hard
 
## solution
Holding Documentation inside git as the markdown files will empower us to track the changes and have rollback possibility. The idea is building a tool which can empower us to compile markdown files that are right beside their codes, it should cover the below areas:  

* Generates a pretty static site from markdown files
* YAML based config system to let everybody add or change the wiki pages and cover configuration as code 
* Battle-tested
* Easy to use in a custom documentation process/system/methodology
 

By using a Yaml file that will empower everybody to enter the MarkDown URL and add tags, groups, …. we can centralize all the configuration.

Then in a regular period, we can check all the URLs and turn them to base64 hash and check with the old existing ones.

```
--- 
wikiPages: 
  - 
    category: OPS
    notification: true
    tags: "aws, go"
    title: aws-nuke
    url: "https://github.com/rebuy-de/aws-nuke/blob/master/README.md"
  - 
    category: OPS
    notification: false
    tags: "terraform, go, shell, provider"
    title: site24*7
    url: "https://github.com/Bonial-International-GmbH/terraform-provider-site24x7/blob/master/Makefile"
```
Static site generators from markdown files which we should check:

* mkdocs.org
* sphinx-doc.org
* gitbook.com
* gohugo.io
* https://github.com/getpelican/pelican

We should also research the location of storage and the possibility of tracking outdated documents.

## Providers 

We are supporting different web services like github, bitbucket, ....
Some of them also providing private repositories, therefore, we should so some kind of authuntication \
here is the list of supported private services and how we should login to them:

### Bitbucket:
- first you should create a https://bitbucket.org/account/settings/app-passwords/
- then you should find your username which you can find in https://bitbucket.org/account/settings/
- Then enter ir to _bitbucket method in the `helpers/providers.py` file. (TODO: We will change this)

  
## Development environment:

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```