<script lang="ts">
  import MaterialSymbolsUpload from '~icons/material-symbols/upload';
</script>

<div class="bg-base-200 rounded-xl w-full p-3 flex gap-4 items-center shadow-md">
	<div class="image"></div>
	<div class="shrink w-full">
    <div class="flex w-full justify-between items-center">
		  <h2 class="text-xl font-bold">Martech - Pharma</h2>
      <div class="flex gap-1 items-center text-neutral/70">
        <span> 09.11.2024</span>
        <MaterialSymbolsUpload/>
      </div>
    </div>
		<span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-secondary">ИИ</span>
		<span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-info">Данные</span>
		<span class="text-xs rounded-full mx-0.5 px-2 py-0.5 border border-primary">+3</span>
		<p class="line-clamp-3 text-xs mt-1 text-neutral/80">
			Задача организации, в особенности же дальнейшее развитие различных форм деятельности в
			значительной степени обуславливает создание форм развития. Равным образом постоянное информационно-пропагандистское
			обеспечение нашей деятельности в значительной степени обуславливает создание направлений
			прогрессивного развития. Товарищи!
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
