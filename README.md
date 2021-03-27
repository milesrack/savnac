# savnac
A command line tool to view assignments and announcements for Canvas courses.

## :pushpin: Prerequisites
### :computer: Windows
[Python 3](https://www.python.org/downloads/)
### :computer: MacOS
```
brew install python3
```
### :computer: Linux
#### Debian / Ubuntu / Linux Mint
```
sudo apt-get install python3
sudo apt-get install python3-pip
```
#### Fedora
```
sudo dnf install python3
sudo dnf install python3-pip
```
#### Redhat / RHEL / CentOS
```
sudo yum install python3
sudo yum install python3-pip
```
#### Arch Linux
```
sudo pacman -S python
sudo pacman -S python-pip
```

## :pushpin: Installation
```
git clone https://github.com/milesrack/savnac.git
cd savnac
pip3 install -r requirements.txt
```

## :pushpin: Usage
```
python3 savnac.py
```
The first time you run the program you will be prompted for your API token. To get this you will have to log into Canvas and navigate to `Account` -> `Settings` -> `New Access Token` -> `Generate Token`. Make sure to store a copy of this elsewhere on the file system for safekeeping. 

The domain should be **only** the domain name. Do not include `https://` or any slashes. For example, `browardschools.instructure.com` would be correct for the domain but `https://browardschools.instructure.com/` would not work.

If you ever need to change the information entered during setup or your `config.yml` file gets deleted, you can create a new one or edit the existing one using this format:
```yml
api_token: API_TOKEN
domain: ORGANIZATION_DOMAIN
```

## :pushpin: Todo
|Status|Task|
|------|----|
|:white_check_mark:|Initial commit|
|:black_square_button:|Show submitted/unsubmitted status of assignments|
|:black_square_button:|Creata a savnac web application|
