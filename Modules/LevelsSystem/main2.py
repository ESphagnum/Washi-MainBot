import discord
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement, RoleAward
from PIL import Image, ImageDraw, ImageFont
import io
import os
from typing import Optional

class LevelingSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.leveling = DiscordLevelingSystem(
            rate=1,
            per=60,
            database_file_path="Saves/LevelsSystem/DiscordLevelingSystem.db",
            awards= { 1310050065683058829 : [
                    RoleAward(level_requirement=5, role_id=1373199249139040286),  # Замените на реальные ID ролей
                    RoleAward(level_requirement=10, role_id=1373199294567546880),
                    RoleAward(level_requirement=15, role_id=1373199337265430661)
                ]}
            
        )
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Начисляем опыт
        await self.leveling.award_xp(message)
        
        # Проверяем повышение уровня
        user_data = await self.leveling.get_user_data(message.author)
        if user_data.has_level_up:
            channel = message.channel
            await channel.send(
                f'🎉 Поздравляю, {message.author.mention}! Ты достиг {user_data.level} уровня!'
            )
    
    @commands.command(name='rank', aliases=['level', 'профиль', 'уровень'])
    async def rank(self, ctx, member: Optional[discord.Member] = None):
        """Показывает карточку профиля с уровнем"""
        member = member or ctx.author
        user_data = await self.leveling.get_user_data(member)
        
        image = await self._generate_profile_card(member, user_data)
        
        with io.BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, f'{member.name}_profile.png'))
    
    async def _generate_profile_card(self, member, user_data):
        """Генерирует изображение профиля"""
        # Создаем изображение
        img = Image.new('RGB', (800, 300), color=(54, 57, 63))
        draw = ImageDraw.Draw(img)
        
        # Загружаем аватар
        avatar_asset = member.avatar.with_size(256)
        avatar_data = await avatar_asset.read()
        avatar = Image.open(io.BytesIO(avatar_data)).resize((200, 200))
        
        # Круглая маска для аватара
        mask = Image.new('L', (200, 200), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 200, 200), fill=255)
        img.paste(avatar, (50, 50), mask)
        
        # Шрифты
        try:
            title_font = ImageFont.truetype("arial.ttf", 40)
            normal_font = ImageFont.truetype("arial.ttf", 30)
        except:
            title_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
        
        # Текст
        draw.text((270, 50), str(member), font=title_font, fill=(255, 255, 255))
        draw.text((270, 120), f"Уровень: {user_data.level}", font=normal_font, fill=(255, 255, 255))
        draw.text((270, 160), f"Опыт: {user_data.xp}/{user_data.next_level_xp}", font=normal_font, fill=(255, 255, 255))
        draw.text((270, 200), f"Место в топе: #{await self._get_user_rank(member)}", font=normal_font, fill=(255, 255, 255))
        
        # Прогресс бар
        progress = user_data.xp / user_data.next_level_xp
        bar_width = 400 * progress
        draw.rectangle([270, 250, 270 + bar_width, 270], fill=(114, 137, 218))
        draw.rectangle([270, 250, 670, 270], outline=(255, 255, 255), width=2)
        
        return img
    
    async def _get_user_rank(self, member):
        """Возвращает место пользователя в топе"""
        leaderboard = await self.leveling.get_leaderboard(member.guild)
        user_ids = [user.user_id for user in leaderboard]
        return user_ids.index(member.id) + 1 if member.id in user_ids else len(user_ids) + 1
    
    @commands.command(name='leaderboard', aliases=['топ', 'top'])
    async def leaderboard(self, ctx):
        """Показывает таблицу лидеров"""
        top_users = await self.leveling.get_leaderboard(ctx.guild)
        
        embed = discord.Embed(
            title="🏆 Топ участников сервера",
            color=discord.Color.gold()
        )
        
        for index, user_data in enumerate(top_users[:10], start=1):
            member = ctx.guild.get_member(user_data.user_id)
            if member:
                embed.add_field(
                    name=f"{index}. {member.display_name}",
                    value=f"Уровень: {user_data.level} | Опыт: {user_data.total_xp}",
                    inline=False
                )
        
        embed.set_footer(text=f"Используйте {ctx.prefix}rank чтобы увидеть свой уровень")
        await ctx.send(embed=embed)
    
    @commands.command(name='set-level', aliases=['установить-уровень'])
    @commands.has_permissions(administrator=True)
    async def set_level(self, ctx, member: discord.Member, level: int):
        """Устанавливает уровень пользователю (только для админов)"""
        if level < 1:
            return await ctx.send("Уровень должен быть положительным числом!")
        
        await self.leveling.set_level(member, level)
        await ctx.send(f"Уровень пользователя {member.mention} установлен на {level}")

def setup(bot):
    bot.add_cog(LevelingSystemCog(bot))
