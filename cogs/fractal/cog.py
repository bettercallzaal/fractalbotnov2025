import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime
from ..base import BaseCog
from .views import MemberConfirmationView
from .group import FractalGroup

class FractalCog(BaseCog):
    """Cog for handling ZAO Fractal voting commands and logic"""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.logger = logging.getLogger('bot')
        self.active_groups = {}  # Dict mapping thread_id to FractalGroup
        self.daily_counters = {}  # Dict mapping guild_id -> {date: counter}
    
    def _get_next_group_name(self, guild_id: int) -> str:
        """Generate auto-incremented group name for the day"""
        today = datetime.now().strftime("%b %d, %Y")
        
        if guild_id not in self.daily_counters:
            self.daily_counters[guild_id] = {}
        
        if today not in self.daily_counters[guild_id]:
            self.daily_counters[guild_id][today] = 0
        
        self.daily_counters[guild_id][today] += 1
        counter = self.daily_counters[guild_id][today]
        
        return f"Fractal Group {counter} - {today}"
    
    @app_commands.command(
        name="zaofractal",
        description="Create a new ZAO fractal voting group from your current voice channel"
    )
    async def zaofractal(self, interaction: discord.Interaction):
        """Create a new ZAO fractal voting group from voice channel members"""
        # Check if interaction has already been responded to
        if interaction.response.is_done():
            return
        
        try:
            await interaction.response.defer(ephemeral=True)
        except discord.NotFound:
            # Interaction expired or invalid, try to send a regular message
            return
        except discord.InteractionResponded:
            # Already responded, continue with followup
            pass
        
        # Check user's voice state
        voice_check = await self.check_voice_state(interaction.user)
        if not voice_check['success']:
            try:
                await interaction.followup.send(voice_check['message'], ephemeral=True)
            except:
                # If followup fails, try regular channel message
                await interaction.channel.send(f"{interaction.user.mention} {voice_check['message']}")
            return
        
        members = voice_check['members']
        member_mentions = ", ".join([member.mention for member in members])
        
        # Send member confirmation
        view = MemberConfirmationView(self, members, interaction.user)
        try:
            await interaction.followup.send(
                f"**Start fractal with:** {member_mentions}?",
                view=view,
                ephemeral=True
            )
        except:
            # If followup fails, send to channel
            await interaction.channel.send(
                f"{interaction.user.mention} **Start fractal with:** {member_mentions}?",
                view=view
            )
    
    @app_commands.command(
        name="endgroup",
        description="End an active fractal group (facilitator only)"
    )
    async def end_group(self, interaction: discord.Interaction):
        """End an active fractal group"""
        await interaction.response.defer(ephemeral=True)
        
        # Check if in a fractal thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command can only be used in a fractal group thread.", ephemeral=True)
            return
        
        # Check if this is an active fractal group
        group = self.active_groups.get(interaction.channel.id)
        if not group:
            await interaction.followup.send("❌ This thread is not an active fractal group.", ephemeral=True)
            return
        
        # Check if user is facilitator
        if interaction.user.id != group.facilitator.id:
            await interaction.followup.send("❌ Only the group facilitator can end the fractal group.", ephemeral=True)
            return
        
        # End the fractal group
        await group.end_fractal()
        del self.active_groups[interaction.channel.id]
        
        await interaction.followup.send("✅ Fractal group ended successfully.", ephemeral=True)
    
    @app_commands.command(
        name="status",
        description="Show the current status of an active fractal group"
    )
    async def status(self, interaction: discord.Interaction):
        """Show the status of an active fractal group"""
        await interaction.response.defer(ephemeral=True)
        
        # Check if in a fractal thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command can only be used in a fractal group thread.", ephemeral=True)
            return
        
        # Check if this is an active fractal group
        group = self.active_groups.get(interaction.channel.id)
        if not group:
            await interaction.followup.send("❌ This thread is not an active fractal group.", ephemeral=True)
            return
        
        # Build status message
        status = f"# ZAO Fractal Status\n\n"
        status += f"**Group:** {interaction.channel.name}\n"
        status += f"**Facilitator:** {group.facilitator.mention}\n"
        status += f"**Current Level:** {group.current_level}\n"
        status += f"**Members:** {len(group.members)}\n"
        status += f"**Active Candidates:** {len(group.active_candidates)}\n"
        status += f"**Votes Cast:** {len(group.votes)}/{len(group.members)}\n\n"
        
        # Winners so far
        if group.winners:
            status += "**Winners:**\n"
            for level, winner in sorted(group.winners.items(), reverse=True):
                status += f"Level {level}: {winner.mention}\n"
        
        await interaction.followup.send(status, ephemeral=True)
    
    # Admin Commands
    @app_commands.command(
        name="admin_end_fractal",
        description="[ADMIN] Force end any active fractal group"
    )
    @app_commands.describe(thread_id="ID of the thread to end (optional)")
    async def admin_end_fractal(self, interaction: discord.Interaction, thread_id: str = None):
        """Admin command to force end fractals"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if thread_id:
            # End specific fractal
            try:
                thread_id_int = int(thread_id)
                if thread_id_int in self.active_groups:
                    group = self.active_groups[thread_id_int]
                    await group.end_fractal()
                    await interaction.followup.send(f"✅ Ended fractal in {group.thread.mention}", ephemeral=True)
                else:
                    await interaction.followup.send("❌ No active fractal found with that thread ID.", ephemeral=True)
            except ValueError:
                await interaction.followup.send("❌ Invalid thread ID format.", ephemeral=True)
        else:
            # Show list of active fractals to choose from
            if not self.active_groups:
                await interaction.followup.send("❌ No active fractals to end.", ephemeral=True)
                return
            
            status = "**Active Fractals:**\n"
            for thread_id, group in self.active_groups.items():
                status += f"• {group.thread.mention} (ID: {thread_id}) - Level {group.current_level}\n"
            status += "\nUse `/admin_end_fractal thread_id:<ID>` to end a specific one."
            
            await interaction.followup.send(status, ephemeral=True)
    
    @app_commands.command(
        name="admin_list_fractals",
        description="[ADMIN] List all active fractal groups"
    )
    async def admin_list_fractals(self, interaction: discord.Interaction):
        """Admin command to list all active fractals"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if not self.active_groups:
            await interaction.followup.send("✅ No active fractal groups.", ephemeral=True)
            return
        
        status = f"**Active Fractal Groups ({len(self.active_groups)}):**\n\n"
        for thread_id, group in self.active_groups.items():
            status += f"**{group.thread.name}**\n"
            status += f"• Thread: {group.thread.mention}\n"
            status += f"• Facilitator: {group.facilitator.mention}\n"
            status += f"• Current Level: {group.current_level}\n"
            status += f"• Members: {len(group.members)}\n"
            status += f"• Active Candidates: {len(group.active_candidates)}\n"
            status += f"• Votes Cast: {len(group.votes)}\n\n"
        
        await interaction.followup.send(status, ephemeral=True)
    
    @app_commands.command(
        name="admin_cleanup",
        description="[ADMIN] Clean up old/stuck fractal groups"
    )
    async def admin_cleanup(self, interaction: discord.Interaction):
        """Admin command to cleanup stuck fractals"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        cleaned_count = 0
        to_remove = []
        
        for thread_id, group in self.active_groups.items():
            try:
                # Check if thread still exists and is accessible
                thread = self.bot.get_channel(thread_id)
                if not thread or thread.archived:
                    to_remove.append(thread_id)
                    cleaned_count += 1
            except:
                to_remove.append(thread_id)
                cleaned_count += 1
        
        # Remove invalid groups
        for thread_id in to_remove:
            del self.active_groups[thread_id]
        
        await interaction.followup.send(
            f"✅ Cleanup complete. Removed {cleaned_count} inactive fractal groups.",
            ephemeral=True
        )
