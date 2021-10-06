# MkRadar
*Markdowns monitoring system and static site generator*

Usually, when people changing their source code they keep forgetting to update related documents on the wiki side, 
also, having a well-structured wiki which we can track it easily and 
changing it smoothly is hard, therefore, here we are trying to find a solution for these problems.

We believe holding the whole documentation alongside the codes as the markdown files will empower us to solve the mentioned issues. 
The idea is building a tool that monitors markdown files and download and compiles them if they changed, 
it should cover these goals:

* YAML based config system to let everybody add or change the wiki pages as the code
* Generates a pretty static site from markdown files
* Battle-tested
* Easy to use in a custom documentation process/system/methodology
 
## Configuration 

To centralize all the configuration there is a file named `radar_config.yaml` 
that let us add a new entity for each MarkDown URL and all other related metadata that is needed.
The structure of the file looks like this, remember  `title`, `category` and `url` are mandatory, and 
we are using them to generate static site menu items,
but you are able to add more fields to add more meaning for each entity like `tags`.

```
--- 
wikiPages: 
  - 
    title: aws-nuke
    category: OPS
    type: public
    url: "https://github.com/rebuy-de/aws-nuke/blob/master/README.md"
  - 
    category: OPS
    title: site24*7
    notification: false
    tags: "terraform, go, shell"
    url: "https://github.com/Bonial-International-GmbH/terraform-provider-site24x7/blob/master/README.md"
```

After adding the desired MarkDowns you can easily run the program 
 with the help of `docker-compose up` command.
 then you can find the generated static website files in `website/html/` folder.
*Attention:* If you are going to use this in the production it is better to set `LOG_LEVEL` environment variable to the `ERROR` level, you can find it in the `docker-compose.yaml` file.

## AWS S3

We are Supporting uploading the static file directory to the S3.
With the help of that, you can make the outcome of this program persistent
 for example in the case that you are using this program in a k8s job.
You need only define the right environment variable which you can find in the `docker-compose.yaml` file.

## Private Repositories 

Here is the list of supported private git services and how we should create authentication for them:

### Github:
- Go to the https://gitlab.com/-/profile/personal_access_tokens
- Give a name, grant `read_repository` permission and create your token
- Enter that to the `docker-compose.yaml` file's environment section
- For each entity in `radar_config.yaml` which should authenticate you should add `type: private`

### Bitbucket:
- Go to the https://bitbucket.org/account/settings/app-passwords/
- Give a label and grant read permission to the repositories
- Then you should find your username which you can find at https://bitbucket.org/account/settings/
- Then enter them to the `docker-compose.yaml` file's environment section
- For each entity in `radar_config.yaml` which should authenticate you should add `type: private`

## Special thanks and kudos

We are using [MkDocs](https://www.mkdocs.org) to generate the static website from markdown files, 
 and it is an elegant tool thanks to its contributors.   
  
## Future plans and Development environment

- Support Private repository of Gitlab
- It should use [ThreadPoolExecutor](https://tutorialedge.net/python/concurrency/python-threadpoolexecutor-tutorial/) instead of Thread
- Categories relation should be decoupled from the rest of the entities in the `radar_config.yaml`
- It should support AWS DBs like Aurora
- It should download embedded images from private and public repositories
- It should support downloading nested meltdown files from the initial markdown

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 
```

To see the cli options:

```
python main.py --help
```

for running tests:

```
 python -m unittest tests/*.py 
 ```
