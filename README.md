# XKCD COMICS TO VK

Script publishes random [XKCD](https://xkcd.com/) comics in [VK](https://vk.com/).

## How to install?

Python3 should be already installed. 

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project
## Launch.
#### Added to `.env` file:
- `CLIENT_ID` - vk app id
- `GROUP_ID` - [vk group id](https://regvk.com/id/)
- `VK_ACCESS_TOKEN` - [vk access token](https://vk.com/dev/implicit_flow_user)
- `IMG_PATH` - path to images folder

After you have set the environment variables, run the script:
```shell
python3 main.py
```
The comics will be published in your public in VK

=========================================================

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).
 