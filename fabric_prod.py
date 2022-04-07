#!/usr/bin/python
#! -*- encoding:utf-8 -*-
from  fabric.api import local, run, cd, env, prefix, put, get, lcd, execute, env, hosts
from fabric.api import sudo, task
import os
from fabric.operations import local as lrun, run
from fabric.state import env

#from ilogue.fexpect import expect, expecting, run
from fabric.contrib.console import confirm, prompt
from fabric.contrib import django


django.settings_module('jannonces.settings')
from django.conf import settings


# serveur OVH 51.254.101.190:8000
env.hosts = [ '92.222.76.243']
env.user = 'admin'

env.local = ['127.0.0.1']
env.prod = ['admin@92.222.76.243']
env.password = 'Grutil002'
app = 'demo'

# repertoire admin
REMOTE_HOME_ADMIN = '/home/admin/'
# repertoire admin
REMOTE_VIRTUAL_DIR = '/home/admin/.virtualenvs/'
#
REMOTE_SOURCE_DIR = '/home/admin/.virtualenvs/envWejob/src/'
#/path/to/project en prod
REMOTE_WORKING_DIR = os.path.join(REMOTE_VIRTUAL_DIR, 'envWejob', 'src')

#/path/to/project en prod
LOCAL_VIRTUAL_DIR = '/home/abdel/.virtualenvs/envWejob/'
LOCAL_WORKING_DIR = os.path.join(LOCAL_VIRTUAL_DIR, 'jannonces')

def install_fabric():
    # installation deployeur
    rep = confirm("vous voulez installer outils de deployement fabric ?")
    if rep :
        run("aptitude update && aptitude upgrade && aptitude autoclean")
        run("aptitude install fabric")

def install_module_image():
    # install traitement Image Pillo
    rep = confirm("vous voulez installer des modules python Image Pillow ?")
    
    if rep :
        run("aptitude install python-imaging libmagickwand-dev")
        code_dir = "~"
        with cd(code_dir):
            run("pip install libjpeg-dev")
            run("pip install Pillow")

def apache_reload():
     if rep :
        run("vous voulez redemarrer votre apache2")
        run("sudo service apache2 restart")

def test():
    # compresser les fichier jannonce
    # copie de l'archive sur le serveur distant
    # !! erreur lors de linstall mysql-python erreur :: EnvironmentError: mysql_config not found
    # pour resoudre faire ==> sudo apt-get install libmysqlclient-dev

    code_dir = os.path.join(LOCAL_WORKING_DIR, "hub.git")
    run("df -h && free -h")
    run("lsb_release -a")
    run("git version ")

def commit():
    with cd( HOME_WORKING_DIR):
        local("git --version && git branch")
        local("git add -p && git commit")

def derniere_git():
    dest_dir = os.path.join(REMOTE_WORKING_DIR, "hub.git")
    with cd(dest_dir):
        run("ls -lt")
        run("df -h && free -h")
        run("lsb_release -a")
        """
        run("git --version && git branch")
        run("git log")
        """
        
def push(site):
    """
    envoie des modifs vers le depot de prod
    """
    
    rep = confirm("vous voulez envoie des source vers %s ?" % site)
    git_dir = os.path.join(REMOTE_WORKING_DIR , "hub.git")
    with cd(git_dir):
        if rep :
                # 2-envoie des source vers prod_1
                local("git push %s master" % site)
        

def creer_database():
    """
    creer database
    """
    
    rep = confirm("vous voulez creer la base jannonce ?")
    if rep :
        with cd( REMOTE_WORKING_DIR):
            run("mysqladmin -u root -p create jannoncedb")


        
def dump_production_database():
    """
    sauvegarde database
    """
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "grutil"
    DATABASE_NAME = "jannoncedb"
    
    
    rep = confirm("vous voulez sauvegarder la base jannonce ?")
    if rep :
        local('mysqldump -u %s -p %s > data/jannonce-db.sql' % (
            DATABASE_USER,
            DATABASE_NAME
        ))
        
    # cp la sauvegarde sur le serveur
    rep = confirm("vous voulez copier la sauvegarde sur le serveur ?")
    if rep :
        put("data/Wejob-db.sql", REMOTE_WORKING_DIR)

def deploy_via_git():
    code_dir = REMOTE_WORKING_DIR
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")

def creer_depot_distant(nom_depot):
    """
    cree un hub git des source
    deporter
    utilisation :
    fab -f fabric_prod.py creer_depot_distant:wejob_prod
    """
    rep = confirm("vous voulez creer un depot distant ?")
    if rep :
        with cd(REMOTE_SOURCE_DIR):
            run("mkdir hub.git")
            run("cd hub.git && git init --bare") # --bare cad sans rep de trw
        
        # ajouter un depot distant
    rep = confirm("vous voulez ajoute un depot distant %s ?" % nom_depot)
    if rep :
        #2 compresser les fichier jannonce
        with lcd(LOCAL_WORKING_DIR):
            # 1- ajouter un depot distant 51.254.101.190
            local("git remote add %s ssh://admin@92.222.76.243"  % nom_depot + REMOTE_SOURCE_DIR + "hub.git/")
            
    rep = confirm("vous voulez envoie des source vers %s ?" % nom_depot)
    if rep :
            # 2-envoie des source vers prod_3
            local("git push %s master"  % nom_depot)
    
    
    rep = confirm("vous voulez cloner la version en prod distant ?")
    if rep :
        # 3- cloner la version en prod distant
        with cd(REMOTE_SOURCE_DIR):
            # copy sur le repertoire prod
            run("git clone hub.git prod")

        
        
def creer_post_update():
    """
    creer un le fichier post-update pour reporter automatiquement
    les maj des sources de hub.git
    """
    repertoire = os.path.join(REMOTE_WORKING_DIR , 'hub.git', 'hooks')
    rep = confirm("vous voulez creer le fichier maj post-update ?")
    
    if rep :
        with lcd( LOCAL_WORKING_DIR):
            # cree le fichier post-update
            with open("post-update", "w") as fd:
                ligne = "#!/bin/bash/" + "\n"
                ligne += "cd " + REMOTE_WORKING_DIR + "/hub.git/" + "\n"
                ligne += "unset GIT_DIR" + "\n"
                ligne += "git pull prod_1 master" + "\n"
                # ecriture
                fd.write(ligne)
        # rcp le fichier post-update
        put( "post-update", repertoire , use_sudo=False)

        # ajout de droit execution
        with cd(repertoire):
            run("chmod +x post-update")
               
def preparer():
    code_dir = "/tmp"
    with cd(code_dir):
        # 
        run("apt-get update && apt-get upgrade")
        run("apt-get install aptitude gcc")
        # installer openssh
        install_openssh()
        # installer paquets antivirus
        install_antivirus()
        # install gestionnaire version GIT
        install_git_version()
        # installer serveur Apache / PHP
        install_apache_php()
        # Fabric
        install_fabric()
        #FTP
        install_ftp()
        # installer modules python image Pillow
        install_module_image()
    

def copy():
    """
    transfert de fchiers 
    """
    rep_dest = os.path.join(REMOTE_WORKING_DIR)
    
    with cd(rep_dest):
        put( LOCAL_WORKING_DIR + "/requires.txt", REMOTE_WORKING_DIR , use_sudo=True)
        put( LOCAL_WORKING_DIR + "/fixtures.json", REMOTE_WORKING_DIR , use_sudo=True)

def install_requires():
    """
    installer les modules requis"
    """
    with cd(REMOTE_SOURCE_DIR):
        rep = confirm("vous voulez installer des modules pythonrequire ?")
    
        if rep :
            run( "workon envWejob && cdvirtualenv ")
            # installer les modules requires
            run("sudo pip install -r  requires.txt")
            
        
        rep = confirm("vous voulez installer la base de donnée mysql ?")
    
        if rep :
            # install de la base Mysql
            run("mysqladmin create jannoncesdb -u root -p")
        
        rep = confirm("vous voulez Creer le schèma de base de données ?")
    
        if rep :
            # install de la base Mysql
            with cd(REMOTE_SOURCE_DIR + "/prod/" ):
                run("pwd")
                run("python manage.py makemigrations")
                run("python manage.py migrate")
                run("python manage.py  createsuperuser")
                
            
        
def install_virtualenv():
    # install pip et virtualenv
        
    rep = confirm("vous voulez installer Virtualenv  ?")
    if rep :
        #run("aptitude update && aptitagude upgrade && aptitude autoclean")
        run("aptitude install python-dev python-pip")
        run("aptitude install virtualenv virtualenvwrapper")
  
def make_virtualenv(nom):
    """
    Creer l'environnement de trw
    """
    data_profile  =  """
# virtual environments:
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
export PIP_VIRTUALENV_BASE=$WORKON_HOME
export PIP_RESPECT_VIRTUALENV=true
if [[ -r /usr/local/bin/virtualenvwrapper.sh ]]; then
    source /usr/local/bin/virtualenvwrapper.sh
else
    echo "WARNING: Can't find virtualenvwrapper.sh"
fi

alias ll='ls -ltr'
alias df='df -hT'
"""
    rep = confirm("vous voulez creer un environnement pour %s  ?" % nom)
    if rep :
        with cd(REMOTE_HOME_ADMIN):
            # 1/ creer l'environnement de trw
            run("mkdir -p ~/.virtualenvs && cd  ~/.virtualenvs")
            run("source ~/.profile")
            run("mkvirtualenv %s" % nom)
            run("workon %s && cdvirtualenv" % nom)
"""
@task
def localhost():
    env.run = local
    env.hosts = ['localhost']
    env.sudo_user = 'abdel'
"""

def dump_fixtures():
    """
    exporter des donnees fixtures
    env.user = 'abdel'
    env.sudo_user = 'abdel'
    env.local_user = 'abdel'
    #
    django.utils.timezone.now`
    """
    
    cmd = "./manage.py dumpdata --indent 2  wejob.categorie wejob.typecontrat > fixtures.json"
    with lcd( LOCAL_WORKING_DIR):
        rep = confirm("vous voulez exporter des data fixtures ?")
        if rep :
            local("pwd")
            local( cmd )
