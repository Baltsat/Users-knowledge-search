<script lang="ts">
  import MaterialSymbolsLightMatchCase from '~icons/material-symbols-light/match-case';
  export let card;

  let [title] = card.fields.fileName
  let [description] = card.fields.description
  let [slide] = card.fields.slide
  let score = Number(card._score).toLocaleString()
</script>

<div class="bg-base-200 rounded-xl w-full p-3 flex gap-4 items-center shadow-md">
	<div class="image"></div>
	<div class="shrink w-full">
    <div class="flex w-full justify-between items-center">
		  <h2 class="text-xl font-bold truncate" {title} >Файл: {title}</h2>
      <div class="flex gap-1 items-center text-neutral/70">
        <span>{score}</span>
      </div>
    </div>
		<span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-primary">Слайд: {slide}</span>
		<!-- <span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-info">Данные</span> -->
		<!-- <span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-primary">+3</span> -->
		<p class="line-clamp-3 text-xs mt-1 text-neutral/80">
			{description}
		</p>
	</div>
</div>

<style>
	.image {
		background-image: url('/img/sample.png');
		width: 150px;
		height: 100px;
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;
		border-radius: 20px;
	}
</style>
