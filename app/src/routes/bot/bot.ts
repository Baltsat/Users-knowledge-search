import { env } from '$env/dynamic/private';
import { Markup, Scenes, Telegraf } from 'telegraf';
import { message } from 'telegraf/filters';

export const bot = new Telegraf(env.BOT_TOKEN);

bot.start(async (ctx) => {
	await ctx.reply(
		'Доброе пожаловать в хранилище. Чтобы запустить приложение нажмите на кнопку',
		// Markup.keyboard([Markup.button.webApp('Приложение', `${env.ORIGIN}/bot`)])
	);
});

bot.on(message('text'), async (ctx) => {
	await ctx.reply(ctx.message.text);
});

bot.on(message('document'), async (ctx) => {
	console.log(ctx.message.document.mime_type);
});
