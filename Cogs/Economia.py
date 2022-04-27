import json
import random
import discord
from discord.ext import commands

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def _help(self, ctx):

        Economia = discord.Embed(title = 'Meus comandos',
        color = ctx.author.color)
        Economia.add_field(
            name= 'Comandos Economia', 
            value=
            '''
            Beg - Voce pode ganhar de 0 a 2000 edinhos
            Edinhos - Mostra quantos edinhos você tem ou do membro mencionado
            Edinhostop - Mostra o rank de pessoas mais ricas
            Loteria - Você pode apostar na sorte e quadruplicar seus edinhos
            Transferir - Você pode transferir edinhos para outras pessoas
            ccap - Jogue cara ou coroa valendo seus edinhos
            ''',
            inline = False)
        Economia.set_thumbnail(url = self.bot.user.avatar_url)

        await ctx.send(embed = Economia)

    @commands.command(aliases = ['SetE', 'GiveEdinho', 'giveE', 'Se'])
    async def SetEdinho(self, ctx, id:int, *, dindin = 0):
        
        if ctx.message.author.id == 'Id DO Dono':

            if dindin == 0:
                await ctx.send(f'Nenhum edinho foi setado para <@{id}>')
            else:

                await open_account(ctx.author)

                users = await get_bank_data()

                SetM = int(dindin)
                
                await ctx.send(f'Foram dados {SetM} edinhos para <@{id}>')

                users[str(id)]['Edinhos'] += SetM

                with open('mainbank.json', 'w') as f:
                    json.dump(users,f)

                user = self.bot.get_user(int(id))

                try:
                    await user.send(f'Seus {dindin} edinhos foram setados <@{id}>')
                except:
                    return

        else:
            await ctx.send(f'Você não tem permissão para usar esse comando {ctx.author.mention}')

    @commands.command(aliases = ['RemoveE', 'RmvE'])
    async def RemoveEdinhos(self, ctx, id:int, *, dindin = 0):

        if ctx.message.author.id == 'ID DO DONO':

            if dindin == 0:
                await ctx.send(f'Nenhum edinho foi Removido para <@{id}>')
            else:

                await open_account(ctx.author)

                users = await get_bank_data()

                SetM = int(dindin)
                
                await ctx.send(f'Foram Removidos {SetM} edinhos para <@{id}>')

                users[str(id)]['Edinhos'] -= SetM

                with open('mainbank.json', 'w') as f:
                    json.dump(users,f)

                user = self.bot.get_user(int(id))

        else:
            await ctx.send(f'Você não tem permissão para usar esse comando {ctx.author}')

    @commands.command()
    async def _Carteira(self, ctx, membro: discord.Member = None):

            if membro == None:
                membro = ctx.author
            else:
                membro = membro

            await open_account(membro)
            users = await get_bank_data()

            wallet_amt = users[str(membro.id)]['Edinhos']

            if membro == None:
                em = discord.Embed(title = f"{ctx.author.name} Edinhos", color = discord.Color.red())
                em.add_field(name ='Edinhos', value = wallet_amt)

                await ctx.send(embed = em)
            else:
                em = discord.Embed(title = f"{membro.name} Edinhos", color = discord.Color.red())
                em.add_field(name ='Edinhos', value = wallet_amt)

                await ctx.send(embed = em)

    @commands.command()
    async def _beg(self, ctx):
            await open_account(ctx.author)

            user = ctx.author

            users = await get_bank_data()

            edinhos = random.randint(0,int(2000))
            
            await ctx.send(f'Você ganhou {edinhos} edinhos!!')

            users[str(user.id)]['Edinhos'] += edinhos

            with open('mainbank.json', 'w') as f:
                json.dump(users,f)

    @commands.command()
    async def _Transferir(self, ctx, membro: discord.Member, edinhos = None):
            await open_account(ctx.author)
            await open_account(membro)

            if edinhos == None:
                await ctx.reply(f'Você precisa selecionar uma quantidade de edinho para sacar')

            bal = await update_bank(ctx.author)

            dindin = int(edinhos)

            if dindin > bal[1]:
                await ctx.reply(f'Você não tem dinheiro suficiente')
                return
            if dindin < 0:
                await ctx.reply(f'A quantia deve ser positiva')
                return

            await update_bank(ctx.author,-1*dindin)
            await update_bank(membro,dindin)
            await ctx.reply(f'Voce transferiu {dindin} edinhos')

    @commands.command()
    async def _loteria(self, ctx, edinhos = None):
            await open_account(ctx.author)

            if edinhos == None:
                await ctx.reply(f'Você precisa selecionar uma quantidade de edinho para Jogar')

            bal = await update_bank(ctx.author)

            dindin = int(edinhos)

            if dindin > bal[0]:
                await ctx.reply(f'Você não tem dinheiro suficiente')
                return
            if dindin < 0:
                await ctx.reply(f'A quantia deve ser positiva')
                return

            final = []
            for i in range(3):
                a = random.choice(['::pineapple:',':grapes:',':kiwi:',])

                final.append(a)

            await ctx.reply(str(final))


            if final[0] == final[1] == final[2]:

                await update_bank(ctx.author,4*dindin)
                await ctx.reply(f'Você ganhou {4*dindin} edinhos!!')
            else:
                await update_bank(ctx.author,-1*dindin)
                await ctx.reply(f'Você perdeu {dindin} edinhos')

    @commands.command()
    async def _Caraoucoroaap(self, ctx, edinhos = int, escolha = None):
            await open_account(ctx.author)

            user = ctx.author

            users = await get_bank_data()

            bal = await update_bank(ctx.author)

            dindin = int(edinhos)

            if dindin > bal[0]:
                await ctx.reply(f'Você não tem dinheiro suficiente para apostar')
                return

            if dindin < 0:
                await ctx.reply(f'A quantia deve ser positiva')
                return

            random1 = random.choice(['cara', 'coroa'])

            edinho = edinhos

            if random1 == escolha:
                await ctx.reply(f'Caiu {escolha}\nParabens, você ganhou {edinhos*2} edinhos')
                users[str(user.id)]['Edinhos'] += edinhos*2
            elif random1 != escolha:
                await ctx.reply(f'Caiu {random1}\nSad, você perdeu {edinhos} edinhos')
                users[str(user.id)]['Edinhos'] -= edinhos

            with open('mainbank.json', 'w') as f:
                json.dump(users,f)

    @commands.command()
    async def _edinhostop(self, ctx):

        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["Edinhos"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"Top 5 mais ricos")
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = await self.bot.fetch_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == 5:
                break
            else:
                index += 1
        await ctx.send(embed=em)

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['Edinhos'] = 0

    with open('mainbank.json', 'w') as f:
        json.dump(users,f, indent=4)
    return True

async def get_bank_data():
    with open('mainbank.json', 'r') as f:
        users = json.load(f)

        return users

async def update_bank(user, change = 0 ,mode = 'Edinhos'):

    users  = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json', 'w') as f:
        json.dump(users,f, indent=4)

    bal = [users[str(user.id)]['Edinhos'],users[str(user.id)]['Edinhos']]
    return bal

def setup(bot):
    bot.add_cog(Economia(bot))