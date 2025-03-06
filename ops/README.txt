#######################
# TRAINING SERVER SETUP
#######################
mkdir -p ~/DeepCatIdentifier
cd ~/DeepCatIdentifier
sudo apt update
apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
./ops/copy-files-to-training-server
    # mkdir -p /root/DeepCatIdentifier/datasets
    # mkdir -p /root/DeepCatIdentifier/ops
    # mkdir -p /root/DeepCatIdentifier/models
    # scp ./DeepCatIdentifier/training.py                   -> /root/DeepCatIdentifier/.
    # scp ./DeepCatIdentifier/testing.py                    -> /root/DeepCatIdentifier/.
    # scp ./DeepCatIdentifier/utils.py                      -> /root/DeepCatIdentifier/.
    # scp ./DeepCatIdentifier/requirements.txt              -> /root/DeepCatIdentifier/.
    # scp ./DeepCatIdentifier/datasets/cv.h5                -> /root/DeepCatIdentifier/datasets/.
    # scp ./DeepCatIdentifier/datasets/test.h5              -> /root/DeepCatIdentifier/datasets/.
    # scp ./DeepCatIdentifier/datasets/test_catvnoncat.h5   -> /root/DeepCatIdentifier/datasets/.
    # scp ./DeepCatIdentifier/datasets/train.h5             -> /root/DeepCatIdentifier/datasets/.
    # scp ./DeepCatIdentifier/datasets/train_catvnoncat.h5  -> /root/DeepCatIdentifier/datasets/.
    # scp ./DeepCatIdentifier/config.json                   -> /root/DeepCatIdentifier/.
    # scp ./DeepCatIdentifier/ops/deploy-model              -> /root/DeepCatIdentifier/ops/.

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
source venv/bin/activate
pip install -r requirements.txt
python training.py

############################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
############################################################################
cd ~/DeepCatIdentifier
./ops/copy-models-to-app-server
    # scp ./models/* -> /var/www/flask-apps/DeepCatIdentifier/models/.


##########################
# APPLICATION SERVER SETUP
##########################
# Update /etc/nginx/sites-available/sites on the application server
sudo ln -s /etc/nginx/sites-available/sites /etc/nginx/sites-enabled
sudo service nginx restart

###############################
# APPLICATION ENVIRONMENT SETUP
###############################
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

################################################
# COPYING FILES FROM LOCAL -> APPLICATION SERVER
################################################
./ops/copy-files-to-app-server
    # mkdir -p /var/www/flask-apps/DeepCatIdentifier/models
    # mkdir -p /var/www/flask-apps/DeepCatIdentifier/templates
    # mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/js
    # mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/images
    # scp ./application.py                -> /var/www/flask-apps/DeepCatIdentifier/.
    # scp ./utils.py                      -> /var/www/flask-apps/DeepCatIdentifier/.
    # scp ./static/js/script.js           -> /var/www/flask-apps/DeepCatIdentifier/static/js/.
    # scp ./templates/getUserInput.html   -> /var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./templates/showResult.html     -> /var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./templates/imageError.html     -> /var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./static/images/*               -> /var/www/flask-apps/DeepCatIdentifier/static/images/
    # scp ./requirements.txt              -> /var/www/flask-apps/DeepCatIdentifier/.
    # scp ./config.json                   -> /var/www/flask-apps/DeepCatIdentifier/.

###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
cd /var/www/flask-apps/DeepCatIdentifier
python3 -m venv venv
source venv/bin/activate
pkill -f DeepCatIdentifier
# python application.py

# Get model name from config.json
# nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &
# Get model name from environment variable
# MODEL="m_20250304205801.keras" nohup gunicorn -b 127.0.0.1:5002 application:app > /dev/null 2>&1 &




