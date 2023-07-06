# StagesBot

An alternative to the Discord Stages channel if you don't want to activate "Communtiy".

## Installation

1. Install PIP packages

    ```bash
    pip install -r requirements.txt
    ```

2. Start `setup.py` and follow the instructions. (Alternatively see [Manual setup of config.yml](#manual-setup-of-configyml))
3. Start `main.py` to start.

### Manual setup of config.yml

Here is an example `config.yml`:

```yaml
bot-token: ABC # Your bot token
guild-id: 123 # Your guild id
```

## Commands

- `/stages create name:<NAME> [ask_to_speak:<ATS> ask_to_join:<ATJ>]` - Creates a Stages voice channel with the name `<NAME>`. If `<ATS>` is ``True``, others must first be given permission to speak. If `<ATJ>` is ``True``, others must first be given permission to listen.
- `/stages delete name:<NAME>` - Deletes a Stages voice channel with the name `<NAME>`
- `/stages allow_speak name:<NAME> mamber:<MEMBER>` - Allows user `<MEMBER>` to speak with name `<NAME>` in Stages voice channel.
- `/stages disallow_speak name:<NAME> mamber:<MEMBER>` - Revokes the permission.
- `/stages allow_listen name:<NAME> mamber:<MEMBER>` - Allows user `<MEMBER>` to listen in Stages voice channel with name `<NAME>`.
- `/stages disallow_listen name:<NAME> mamber:<MEMBER>` - Disallows the permission.
- `/stages ban name:<NAME> mamber:<MEMBER>` - Hides Stages voice channel with name `<NAME>` from user `<MEMBER>` and prevents him from joining.
- `/stages unban name:<NAME> mamber:<MEMBER>` - Unban.
