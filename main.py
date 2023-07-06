import nextcord
from nextcord.ext import commands
from settings import Config, Stage


config = Config("config.yml")
config.save()

bot = commands.Bot()


async def update_permissions(member: nextcord.Member):
    if member.voice is None or member.voice.channel is None:
        return
    temp_channel = await member.guild.create_voice_channel(
        "Updating Permissions...",
        overwrites={
            member.guild.get_member(bot.user.id): nextcord.PermissionOverwrite(
                view_channel=True
            ),
            member: nextcord.PermissionOverwrite(view_channel=True),
            member.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
        },
    )
    try:
        channel = member.voice.channel
        await member.move_to(temp_channel)
        await member.move_to(channel)
    finally:
        await temp_channel.delete()


@bot.event
async def on_ready():
    print("Online.")


@bot.slash_command(guild_ids=[config.GUILD_ID])
async def stages(interaction: nextcord.Interaction):
    await interaction.send("That is impossible.", ephemeral=True)


@stages.subcommand()
async def help(interaction: nextcord.Interaction):
    await interaction.send(
        """**Commands**:
- `/stages create name:<NAME> [ask_to_speak:<ATS> ask_to_join:<ATJ>]` - Creates a Stages voice channel with the name <NAME>. If <ATS> is True, others must first be given permission to speak. If <ATJ> is true, others must first be given permission to listen.
- `/stages delete name:<NAME>` - Deletes a Stages voice channel named <NAME>
- `/stages allow_speak name:<NAME> mamber:<MEMBER>` - Allows user <MEMBER> to speak with name <NAME> in Stages voice channel.
- `/stages disallow_speak name:<NAME> mamber:<MEMBER>` - Revokes the permission.
- `/stages allow_listen name:<NAME> mamber:<MEMBER>` - Allows user <MEMBER> to listen in Stages voice channel with name <NAME>.
- `/stages disallow_listen name:<NAME> mamber:<MEMBER>` - Revokes the permission.
- `/stages ban name:<NAME> mamber:<MEMBER>` - Hides Stages voice channel with name <NAME> for user <MEMBER> and prevents him from joining.
- `/stages unban name:<NAME> mamber:<MEMBER>` - Unban.""",
        ephemeral=True,
    )


@stages.subcommand()
async def create(
    interaction: nextcord.Interaction,
    name: str,
    ask_to_speak: bool = True,
    ask_to_join: bool = False,
):
    if name in config.STAGES_BY_NAME:
        await interaction.send(
            f"There is already a stage named '{name}'.", ephemeral=True
        )
        return

    channel = await interaction.guild.create_voice_channel(
        f"Stage: {name}",
        overwrites={
            interaction.guild.get_member(bot.user.id): nextcord.PermissionOverwrite(
                view_channel=True, connect=True
            )
        },
    )

    role_ids = {
        "admin": interaction.user.id,
        "speaker": None,
        "listener": None,
        "banned": None,
    }

    if ask_to_speak:
        role_speaker = await interaction.guild.create_role(
            name=f"Stage '{name}' Speaker", mentionable=True
        )
        role_ids["speaker"] = role_speaker.id
        await channel.set_permissions(role_speaker, speak=True, connect=True)
        await channel.set_permissions(interaction.guild.default_role, speak=False)
    if ask_to_join:
        role_listener = await interaction.guild.create_role(
            name=f"Stage '{name}' Listener", mentionable=False
        )
        role_ids["listener"] = role_listener.id

        await channel.set_permissions(role_listener, connect=True, speak=False)
        await channel.set_permissions(interaction.guild.default_role, connect=False)

    role_banned = await interaction.guild.create_role(
        name=f"Stage '{name}' Banned", mentionable=False
    )
    role_ids["banned"] = role_banned.id
    await channel.set_permissions(role_banned, view_channel=False)

    config.STAGES.append(
        Stage(
            {
                "name": name,
                "channel-id": channel.id,
                "ask-to-speak": ask_to_speak,
                "ask-to-listen": ask_to_join,
                "role-ids": role_ids,
            }
        )
    )
    config.save()
    config.update_stages_by_name()
    await interaction.send(f"Stage was created: {channel.jump_url}", ephemeral=True)


@stages.subcommand()
async def allow_speak(
    interaction: nextcord.Interaction, name: str, member: nextcord.Member
):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    if not stage.ASK_TO_SPEAK:
        await interaction.send(
            "ask-to-speak is not enabled, and therefore this command is deactivated.",
            ephemeral=True,
        )
        return
    role_speaker = interaction.guild.get_role(stage.ROLE_ID_SPEAKER)
    await member.add_roles(role_speaker)
    await update_permissions(member)
    await interaction.send(
        f"User {member.mention} can now speak in the Stage '{name}'", ephemeral=True
    )


@stages.subcommand()
async def disallow_speak(
    interaction: nextcord.Interaction, name: str, member: nextcord.Member
):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    if not stage.ASK_TO_SPEAK:
        await interaction.send(
            "ask-to-speak is not enabled, and therefore this command is deactivated.",
            ephemeral=True,
        )
        return
    role_speaker = interaction.guild.get_role(stage.ROLE_ID_SPEAKER)
    await member.remove_roles(role_speaker)
    await update_permissions(member)
    await interaction.send(
        f"User {member.mention} can no longer speak in the Stage '{name}'",
        ephemeral=True,
    )


@stages.subcommand()
async def allow_listen(
    interaction: nextcord.Interaction, name: str, member: nextcord.Member
):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    if not stage.ASK_TO_LISTEN:
        await interaction.send(
            "ask-to-listen is not enabled, and therefore this command is deactivated.",
            ephemeral=True,
        )
        return
    role_listener = interaction.guild.get_role(stage.ROLE_ID_LISTENER)
    await member.add_roles(role_listener)
    await interaction.send(
        f"User {member.mention} can now listen in the Stage '{name}'", ephemeral=True
    )


@stages.subcommand()
async def disallow_listen(
    interaction: nextcord.Interaction, name: str, member: nextcord.Member
):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    if not stage.ASK_TO_LISTEN:
        await interaction.send(
            "ask-to-listen is not enabled, and therefore this command is deactivated.",
            ephemeral=True,
        )
        return
    role_listener = interaction.guild.get_role(stage.ROLE_ID_LISTENER)
    await member.remove_roles(role_listener)
    await member.move_to(None)
    await interaction.send(
        f"User {member.mention} can no longer listen in the Stage '{name}'",
        ephemeral=True,
    )


@stages.subcommand()
async def ban(interaction: nextcord.Interaction, name: str, member: nextcord.Member):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    role_banned = interaction.guild.get_role(stage.ROLE_ID_BANNED)
    await member.add_roles(role_banned)
    await member.move_to(None)
    await interaction.send(
        f"User {member.mention} is now banned from the Stage '{name}'", ephemeral=True
    )


@stages.subcommand()
async def unban(interaction: nextcord.Interaction, name: str, member: nextcord.Member):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    role_banned = interaction.guild.get_role(stage.ROLE_ID_BANNED)
    await member.remove_roles(role_banned)
    await interaction.send(
        f"User {member.mention} is no longer banned from the Stage '{name}'",
        ephemeral=True,
    )


@stages.subcommand()
async def delete(interaction: nextcord.Interaction, name: str):
    if not name in config.STAGES_BY_NAME:
        await interaction.send(f"No stage named '{name}' found.", ephemeral=True)
        return

    stage = config.STAGES_BY_NAME[name]
    await interaction.guild.get_channel(stage.CHANNEL_ID).delete()
    if stage.ASK_TO_SPEAK:
        await interaction.guild.get_role(stage.ROLE_ID_SPEAKER).delete()
    if stage.ASK_TO_LISTEN:
        await interaction.guild.get_role(stage.ROLE_ID_LISTENER).delete()
    await interaction.guild.get_role(stage.ROLE_ID_BANNED).delete()
    await interaction.send(
        f"Stage '{name}' was deleted.",
        ephemeral=True,
    )
    del config.STAGES_BY_NAME[name]
    config.update_stages()
    config.save()


@allow_speak.on_autocomplete("name")
@disallow_speak.on_autocomplete("name")
@allow_listen.on_autocomplete("name")
@disallow_listen.on_autocomplete("name")
@ban.on_autocomplete("name")
@unban.on_autocomplete("name")
@delete.on_autocomplete("name")
async def autocomplete_name(
    interaction: nextcord.Interaction, name: str, member: nextcord.Member
):
    await interaction.response.send_autocomplete(
        [stage.NAME for stage in config.STAGES if stage.NAME.startswith(name)]
    )


bot.run(config.BOT_TOKEN)
