<script>
	import { onMount } from 'svelte';
	import { scale, fly } from 'svelte/transition';
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { signIn, signOut } from '@auth/sveltekit/client';

	import IcRoundStorage from '~icons/ic/round-storage';
	import Moon from '~icons/ph/moon';
	import Sun from '~icons/ph/sun';

	import { SignIn } from '@auth/sveltekit/components';
	import { theme, user } from '$lib/stores';

	import '../app.css';
</script>

<header class="max-w-2xl w-full mx-auto">
	<div class="navbar bg-base-100">
		<div class="flex-1">
			<a class="text-xl flex items-center" href="/">
				<IcRoundStorage />
				<span class="ml-1">Хранилище</span>
			</a>
		</div>

		<div class="flex items-center gap-1">
			<span class="truncate sm:w-[120px]">
				{#if $user}
					{$user.first_name} {$user.last_name}
				{:else}
					Анонимный пользователь
				{/if}
			</span>
			<button
				class="btn btn-square btn-sm flex items-center gap-4 transition hover:text-primary"
				on:click={() => ($theme = $theme === 'light' ? 'dark' : 'light')}
			>
				{#if $theme === 'light'}
					<span in:scale={{ duration: 300 }}>
						<Sun width="24" />
					</span>
				{:else}
					<span in:scale={{ duration: 300 }}>
						<Moon width="24" />
					</span>
				{/if}
			</button>
		</div>
	</div>
</header>
{#key $page}
	<main in:fade class="grow h-full w-full @container/main flex flex-col px-2 max-w-2xl mx-auto ">
		<slot />
	</main>
{/key}

<style>
  
</style>