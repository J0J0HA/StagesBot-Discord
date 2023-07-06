# StagesBot

> INFO: There is also an english version of this document: [README.en.md](README.en.md)

Eine Alternative zu dem Discord-Stages-Kanal, wenn man "Communtiy" nicht aktivieren möchte.

## Installation

1. PIP-Pakete installieren

   ```bash
   pip install -r requirements.txt
   ```

2. `setup.py` starten und Anweisungen befolgen. (Alternativ siehe [Manuelles Einrichten der config.yml](#manuelles-einrichten-der-configyml))
3. Zum Starten `main.py` starten.

### Manuelles Einrichten der config.yml

Hier ist eine Beispiel-`config.yml`:

```yaml
bot-token: ABC # Dein Bot-Token
guild-id: 123 # Deine Guild-ID
```

## Befehle

- `/stages create name:<NAME> [ask_to_speak:<ATS> ask_to_join:<ATJ>]` - Erstellt einen Stages-Sprachkanal mit dem Namen `<NAME>`. Wenn `<ATS>` ``True`` ist, müssen andere erst die Erlaubnis bekommen, Sprechen zu dürfen. Wenn `<ATJ>` ``True`` ist, müssen andere erst die Erlaubnis bekommen, zuzuhören.
- `/stages delete name:<NAME>` - Löscht einen Stages-Sprachkanal mit dem Namen `<NAME>`
- `/stages allow_speak name:<NAME> mamber:<MEMBER>` - Erlaubt dem Nutzer `<MEMBER>`, im Stages-Sprachkanal mit dem Namen `<NAME>` zu sprechen.
- `/stages disallow_speak name:<NAME> mamber:<MEMBER>` - Hebt die Erlaubnis auf.
- `/stages allow_listen name:<NAME> mamber:<MEMBER>` - Erlaubt dem Nutzer `<MEMBER>`, im Stages-Sprachkanal mit dem Namen `<NAME>` zuzuhören.
- `/stages disallow_listen name:<NAME> mamber:<MEMBER>` - Hebt die Erlaubnis auf.
- `/stages ban name:<NAME> mamber:<MEMBER>` - Verbirgt den Stages-Sprachkanal mit dem Namen `<NAME>` für den Nutzer Nutzer `<MEMBER>` und verhindert sein Beitreten.
- `/stages unban name:<NAME> mamber:<MEMBER>` - Hebt den Ban auf.
