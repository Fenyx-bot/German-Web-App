# German Web App

After cloning this repo make sure to run this right after<br>
```bash
git clone https://github.com/Fenyx-bot/German-Web-App && cd German-Web-App 
```

Create a new venv and activate it
For Linux
```bash
python -m venv venv && source venv/bin/activate
```

For Windows (PowerShell)
```bash
python -m venv venv && source venv/bin/Activate.ps1
```

For more info <a href="https://docs.python.org/3/library/venv.html#how-venvs-work">Python virutal env docs</a>

```bash
pip install -r requirements.txt
```

Now you are good to go ;)

For the first run, this will scrape the data and saved into a file called "words.json" and fill the database
```bash
python main.py -s 
```
