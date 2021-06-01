# savnac :books:
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

A command line tool to view assignments and announcements for [Canvas](https://github.com/instructure/canvas-lms) courses.

## :pushpin: Installation
```
git clone https://github.com/MC-Software-Solutions/savnac.git
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
|----------|--------|
|:heavy_check_mark:|Initial commit|
|:heavy_check_mark:|Show submitted/unsubmitted status of assignments|
|:heavy_check_mark:|Creata a savnac web application|
||Creata a savnac Android application|
||Creata a savnac IOS application|
