<svelte:head>
  <script src="https://telegram.org/js/telegram-web-app.js" on:load={() => tgInit()}></script>
</svelte:head>

<script lang="ts">
	import { theme } from '$root/lib/stores';
  import { onMount } from 'svelte'
	import { user, WebApp } from '$lib/stores';
  
  function tgInit() {
    // @ts-ignore
    $WebApp = window.Telegram.WebApp;
  }

  onMount(() => {tgInit()})

</script>

<slot/>
