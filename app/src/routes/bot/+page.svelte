<script lang="ts">
	import { WebApp } from '$lib/stores';
	import PhMagnifyingGlassBold from '~icons/ph/magnifying-glass-bold';

  import Card from './Card.svelte';

	let search = '';

	async function handleEnter(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			submit();
		}
	}

	async function submit() {
		$WebApp.showAlert(`Submit ${search}`);
	}
</script>

<div class="w-full flex gap-2">
	<input
		class="input input-bordered w-full"
		placeholder="Ваш поисковый запрос..."
		bind:value={search}
		on:keydown={handleEnter}
	/>
	<button 
    class="btn btn-square btn-primary"
    disabled={!search}
  ><PhMagnifyingGlassBold width={22} height={22} /></button>
</div>

<div class="w-full flex flex-col gap-2 mt-2">
  <div class="bg-base-200 rounded-md px-2 py-3 mb-4">
    <p class="text-center">✅ Вот что удалось найти!</p>
  </div>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
</div>