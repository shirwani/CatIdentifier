######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
    ssh root@172-104-24-151.ip.linodeusercontent.com 'mkdir -p /root/DeepCatIdentifier/datasets'
    ssh root@172-104-24-151.ip.linodeusercontent.com 'mkdir -p /root/DeepCatIdentifier/models'
    scp ./training.py                     root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/.
    scp ./testing.py                      root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/.
    scp ./utils.py                        root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/.
    scp ./requirements.txt                root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/.
    scp ./datasets/train.h5               root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/datasets/.
    scp ./datasets/cv.h5                  root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/datasets/.
    scp ./datasets/test.h5                root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/datasets/.
    scp ./config.json                     root@172-104-24-151.ip.linodeusercontent.com:/root/DeepCatIdentifier/.

#######################################################################
# RUNNING TRAINING ON THE TRAINING SERVER
#
# Prereqs:
#   Install python 3.12 if it's not already installed on the server
#   Make sure python3 is aliased to python 3.12
#######################################################################
    mkdir -p ~/DeepCatIdentifier
    cd ~/DeepCatIdentifier
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python training.py

############################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
############################################################################
    cd ~/DeepCatIdentifier
    scp ./models/* root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/models/.


##########################
# APPLICATION SERVER SETUP
##########################
    # Update /etc/nginx/sites-available/sites on the application server
    sudo ln -s /etc/nginx/sites-available/sites /etc/nginx/sites-enabled
    sudo service nginx restart

###############################
# APPLICATION ENVIRONMENT SETUP
###############################
    cd /var/www/flask-apps/DeepCatIdentifier
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install gunicorn
    pip install -r requirements.txt

################################################
# COPYING FILES FROM LOCAL -> APPLICATION SERVER
################################################
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/models'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/templates'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/js'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/images'
    scp ./application.py              root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/.
    scp ./utils.py                    root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/.
    scp ./static/js/script.js         root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/static/js/.
    scp ./templates/getUserInput.html root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/templates/.
    scp ./templates/showResult.html   root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/templates/.
    scp ./templates/imageError.html   root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/templates/.
    scp ./static/images/*             root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/static/images/
    scp ./requirements.txt            root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/.
    scp ./config.json                 root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepCatIdentifier/.


###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
cd /var/www/flask-apps/DeepCatIdentifier
python3 -m venv venv
source venv/bin/activate
pkill -f DeepCatIdentifier
# python application.py

# Get model name from config.json
# nohup gunicorn -b 127.0.0.1:5004 application:app > /dev/null 2>&1 &
# Get model name from environment variable
# MODEL="m_20250306125531.pkl" nohup gunicorn -b 127.0.0.1:5004 application:app > /dev/null 2>&1 &

