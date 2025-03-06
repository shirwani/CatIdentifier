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
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/DeepCatIdentifier/datasets'
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/DeepCatIdentifier/ops'
    # ssh root@<TRAINING_SERVER> 'mkdir -p /root/DeepCatIdentifier/models'
    # scp ./training.py                     root@<TRAINING_SERVER>:/root/DeepCatIdentifier/.
    # scp ./testing.py                      root@<TRAINING_SERVER>:/root/DeepCatIdentifier/.
    # scp ./utils.py                        root@<TRAINING_SERVER>:/root/DeepCatIdentifier/.
    # scp ./requirements.txt                root@<TRAINING_SERVER>:/root/DeepCatIdentifier/.
    # scp ./datasets/cv.h5                  root@<TRAINING_SERVER>:/root/DeepCatIdentifier/datasets/.
    # scp ./datasets/test.h5                root@<TRAINING_SERVER>:/root/DeepCatIdentifier/datasets/.
    # scp ./datasets/test_catvnoncat.h5     root@<TRAINING_SERVER>:/root/DeepCatIdentifier/datasets/.
    # scp ./datasets/train.h5               root@<TRAINING_SERVER>:/root/DeepCatIdentifier/datasets/.
    # scp ./datasets/train_catvnoncat.h5    root@<TRAINING_SERVER>:/root/DeepCatIdentifier/datasets/.
    # scp ./config.json                     root@<TRAINING_SERVER>:/root/DeepCatIdentifier/.

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
cd ~/DeepCatIdentifier
source venv/bin/activate
pip install -r requirements.txt
python training.py

############################################################################
# DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
############################################################################
cd ~/DeepCatIdentifier
./ops/copy-models-to-app-server
    # scp ./models/* root<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/models/.


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
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/models'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/templates'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/js'
    # ssh root@<APPLICATION_SERVER> 'mkdir -p /var/www/flask-apps/DeepCatIdentifier/static/images'
    # scp ./application.py              root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/.
    # scp ./utils.py                    root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/.
    # scp ./static/js/script.js         root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/static/js/.
    # scp ./templates/getUserInput.html root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./templates/showResult.html   root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./templates/imageError.html   root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/templates/.
    # scp ./static/images/*             root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/static/images/
    # scp ./requirements.txt            root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/.
    # scp ./config.json                 root@<APPLICATION_SERVER>:/var/www/flask-apps/DeepCatIdentifier/.


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

