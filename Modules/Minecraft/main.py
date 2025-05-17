import discord
from discord.ext import commands, tasks
from discord import app_commands
from mcstatus import JavaServer
from Config.Minecraft.config import *
import json
import os

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_info = {}
        self.data_file = save_path
        self.load_data()
        self.update_embed.start()

    def cog_unload(self):
        self.update_embed.cancel()
        self.save_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                # Преобразуем ключи из строк в int (ID каналов)
                self.server_info = {int(k): v for k, v in data.items()}
        else:
            self.server_info = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.server_info, f, indent=4)

    @app_commands.command(name="command", description="Пример команды для Minecraft")
    async def example_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Minecraft Command",
            description="Это пример команды для Minecraft модуля.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="set_channel", description="Установить канал для обновления информации о сервере")
    @app_commands.describe(server_address="Адрес сервера (например, example.com:25565)")
    async def set_channel(self, interaction: discord.Interaction, server_address: str, player_list: bool):
        # Проверка прав
        if not any(role.id in allowed_role_ids for role in interaction.user.roles):
            embed = discord.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для выполнения этой команды.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        channel = interaction.channel
        
        if channel.id in self.server_info:
            embed = discord.Embed(
                title="Ошибка",
                description="Этот канал уже используется для отслеживания сервера.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.server_info[channel.id] = {
            "address": server_address,
            "message": None,
            "last_status": None,
            "players": player_list
        }
        self.save_data()

        embed = discord.Embed(
            title=loc["embed"]["set_channel"]["title"],
            description=loc["embed"]["set_channel"]["description"].format(server_address),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        await self.update_server_embed(channel)

    @app_commands.command(name="server_list", description="Показать список всех отслеживаемых серверов")
    async def server_list(self, interaction: discord.Interaction):
        # Проверка прав
        if not any(role.id in allowed_role_ids for role in interaction.user.roles):
            embed = discord.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для выполнения этой команды.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not self.server_info:
            embed = discord.Embed(
                title="Список серверов",
                description="Нет отслеживаемых серверов.",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="Список отслеживаемых серверов",
            color=discord.Color.blue()
        )

        for channel_id, server_data in self.server_info.items():
            channel = self.bot.get_channel(channel_id)
            channel_name = f"Удалённый канал ({channel_id})" if channel is None else channel.mention
            embed.add_field(
                name=f"Сервер: {server_data['address']}",
                value=f"Канал: {channel_name}\nСтатус: {server_data.get('last_status', 'неизвестно')}\nОтображение игроков: {'Да' if server_data['players'] else 'Нет'}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="delete_server", description="Удалить сервер из отслеживания")
    @app_commands.describe(channel_id="ID канала, который отслеживает сервер")
    async def delete_server(self, interaction: discord.Interaction, channel_id: str):
        # Проверка прав
        if not any(role.id in allowed_role_ids for role in interaction.user.roles):
            embed = discord.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для выполнения этой команды.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            channel_id_int = int(channel_id)
        except ValueError:
            embed = discord.Embed(
                title="Ошибка",
                description="Неверный формат ID канала.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if channel_id_int not in self.server_info:
            embed = discord.Embed(
                title="Ошибка",
                description="Указанный канал не отслеживает ни один сервер.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Удаляем сообщение бота, если оно существует
        server_data = self.server_info[channel_id_int]
        channel = self.bot.get_channel(channel_id_int)
        
        if channel is not None and server_data["message"] is not None:
            try:
                message = await channel.fetch_message(server_data["message"])
                await message.delete()
            except:
                pass

        # Удаляем сервер из списка
        del self.server_info[channel_id_int]
        self.save_data()

        embed = discord.Embed(
            title="Успех",
            description="Сервер удалён из отслеживания.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_server_embed(self, channel):
        if channel.id not in self.server_info:
            return

        server_data = self.server_info[channel.id]
        address = server_data["address"]
        player_list = server_data["players"]
        last_status = server_data["last_status"]

        try:
            server = JavaServer.lookup(address)
            status = server.status()
            players_online = status.players.online
            players_max = status.players.max
            players = []

            if hasattr(status.players, 'sample') and status.players.sample is not None:
                players = [player.name for player in status.players.sample]

            embed = discord.Embed(
                title=loc["embed"]["update"]["online"]["title"].format(address),
                description=loc["embed"]["update"]["online"]["description"].format(players_online, players_max),
                color=discord.Color.green()
            )
            if player_list:
                if players:
                    embed.add_field(name=loc["embed"]["update"]["online"]["players_list_field"]["name"], value="\n".join(players), inline=False)
                else:
                    embed.add_field(name=loc["embed"]["update"]["online"]["players_list_field"]["name"], value=loc["embed"]["update"]["online"]["players_list_field"]["no_info"], inline=False)

            try:
                await channel.edit(name=f"mc-{address.replace(':', '-')}-online")
            except:
                pass

            server_data["last_status"] = "online"

        except Exception as e:
            embed = discord.Embed(
                title=loc["embed"]["update"]["offline"]["title"].format(address),
                description=loc["embed"]["update"]["offline"]["description"],
                color=discord.Color.red()
            )
            server_data["last_status"] = "offline"

            try:
                await channel.edit(name=f"mc-{address.replace(':', '-')}-offline")
            except:
                pass

        try:
            if server_data["message"] is None:
                message = await channel.send(embed=embed)
                server_data["message"] = message.id
                self.save_data()
            else:
                try:
                    message = await channel.fetch_message(server_data["message"])
                    await message.edit(embed=embed)
                except discord.NotFound:
                    message = await channel.send(embed=embed)
                    server_data["message"] = message.id
                    self.save_data()
                except discord.Forbidden:
                    pass
        except Exception as e:
            print(loc["error"]["update_error"].format(e))

    @tasks.loop(minutes=1)
    async def update_embed(self):
        # Удаляем серверы с удалёнными каналами
        channels_to_remove = []
        
        for channel_id in list(self.server_info.keys()):
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                channels_to_remove.append(channel_id)
                continue
            
            # Проверяем, существует ли сообщение бота
            server_data = self.server_info[channel_id]
            if server_data["message"] is not None:
                try:
                    await channel.fetch_message(server_data["message"])
                except discord.NotFound:
                    # Сообщение удалено - удаляем сервер
                    channels_to_remove.append(channel_id)
                    continue
                except discord.Forbidden:
                    pass
            
            await self.update_server_embed(channel)
        
        # Удаляем несуществующие серверы
        for channel_id in channels_to_remove:
            del self.server_info[channel_id]
        
        if channels_to_remove:
            self.save_data()

    @update_embed.before_loop
    async def before_update_embed(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Minecraft(bot))