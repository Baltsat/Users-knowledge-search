<script lang="ts">
	import { WebApp } from '$lib/stores';
	import PhMagnifyingGlassBold from '~icons/ph/magnifying-glass-bold';
	import { Firework } from 'svelte-loading-spinners';
	import { rpc } from '$root/routes/controller';

	import Card from './Card.svelte';

	let search = '';
	let loading = false;
	let data = [];

	async function handleEnter(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			submit();
		}
	}

	async function submit() {
		loading = true;
		data = await rpc.FastApi.search(search);
		loading = false;
	}
</script>

<div class="w-full flex gap-2">
	<input
		class="input input-bordered w-full"
		placeholder="Ваш поисковый запрос..."
		bind:value={search}
		on:keydown={handleEnter}
	/>
	<button on:click={submit} class="btn btn-square btn-primary" disabled={!search || loading}
		><PhMagnifyingGlassBold width={22} height={22} /></button
	>
</div>

<div class="w-full flex flex-col gap-2 mt-2">
	{#if loading}
		<div class="w-full flex items-center justify-center">
			<Firework color="#3030FF" />
		</div>
	{:else if data.length}
		<div class="bg-base-200 rounded-md px-2 py-3 mb-4">
			<p class="text-center">✅ Вот что удалось найти!</p>
		</div>
		{#each data as card}
			<Card {card} />
		{/each}
	{:else}
		<p class="text-center mt-5 text-xl text-neutral-500">Просто начните искать 👀</p>
	{/if}
</div>
