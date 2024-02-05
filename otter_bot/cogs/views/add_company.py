import discord


class ButtonAddCompany(discord.ui.View):
    accepted: bool = None

    @discord.ui.button(label="Accept",
                       style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Company added succesfully!  ✅")
        available = True
        self.stop() 

    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Company declined succesfully! ❌")
        available = False
        self.stop()

    async def disable_items(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("This request has expired! ⌛")
        await self.disable_items()
    