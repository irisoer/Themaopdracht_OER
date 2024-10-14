# Project Installatie Handleiding

Deze handleiding helpt je bij het opzetten van een Python virtual environment, het installeren van de benodigde dependencies, en het configureren van je VSCode-werkruimte voor een efficiënte ontwikkelervaring.

## 1. Een Virtual Environment aanmaken

Om een virtual environment te maken, volg je de volgende stappen:

1. Open een terminal of command prompt.
2. Navigeer naar je projectmap.
3. Voer het volgende commando uit om een virtual environment aan te maken:
   ```bash
   python -m venv venv
4. Activeer de virtual environment:
    ### Op Windows:
    ```bash
    venv\Scripts\activate
    ```
    ### Op MacOS/Linux
    ```bash
    source venv/bin/activate
    ```
    Je ziet nu dat je virtual environment geactiveerd is (meestal door een (venv) voor je prompt).

## 2. Dependencies installeren
Zodra je virtual environment is geactiveerd, kun je de afhankelijkheden van het project installeren. Zorg ervoor dat je een requirements.txt-bestand hebt in de hoofdmap van je project.

Voer het volgende commando uit om de dependencies te installeren:
```bash
pip install -r requirements.txt
```

## 3. VSCode configureren
Maak een .vscode-map in de hoofdmap van je project als deze nog niet bestaat.

Voeg een bestand genaamd settings.json toe met de volgende inhoud om de omgeving en editor correct in te stellen:
```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.envFile": "${workspaceFolder}/.env",
    "editor.formatOnPaste": false,
    "editor.formatOnSave": true,
    "editor.formatOnType": true,
    "files.trimTrailingWhitespace": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        },
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.python"
    },
    "python.languageServer": "Pylance",
    "python.testing.pytestEnabled": true,
    "[sql]": {
        "editor.formatOnSave": false,
        "editor.formatOnType": false,
        "editor.formatOnPaste": false
    }
}
```
Dit zorgt ervoor dat je Python-omgeving correct is ingesteld, en dat je code netjes wordt opgemaakt bij het opslaan.