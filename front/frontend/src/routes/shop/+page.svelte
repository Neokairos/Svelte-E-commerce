<script>
	// @ts-nocheck

	import axios from 'axios';
	import { onMount } from 'svelte';
	import { productStore } from '../../store';
	import { variables } from '$lib/utils/constants';
	import { fly } from 'svelte/transition';
	let loading = true;
	onMount(async function () {
		try {
			if (!$productStore.all.length) {
				const endpoint = `${variables.BASE_API_URI}/products`;
				const response = await axios.get(endpoint);
				productStore.update((n) => ({ ...n, all: response.data }));
				loading = false;
			} else {
				loading = false;
			}
		} catch (err) {
			loading = false;
			console.log(err);
		}
	});
</script>

<div>
	<h2 class="my-4">Products</h2>

	<section in:fly={{ y: 100, duration: 500, delay: 650 }} out:fly={{ duration: 500 }}>
		
		{#if loading}
			<div class="center ">
				<div class="loader" role="status"></div>
			</div>
		{:else}
			<div class="row">
				{#each $productStore.all as item}
					<div class="col-12 col-sm-6 col-md-4">
						<div class="card w-100 h-100">
							<div class="box-image">
								<a href="/shop/{item.id}">
									<img class="product-img" src={item.image} alt="item" />
								</a>

								<div class="overlay">
									<a href="/shop/{item.id}" class="image-button">
										<span>View</span>
										<span>
											<i class="icon icon-search"></i>
										</span>

									</a>
									<a href="/shop/cart" class="image-button">
										<span>Add to Cart</span>
										<span>
											<i class="icon icon-cart"></i>
										</span>						
									</a>

								</div>
							</div>
							<div class="card-body d-flex flex-column justify-content-between gap-4">
								<div>
									<a href="/shop/{item.id}" class="product-title">{item.title}</a>
									<span class="product-price">${item.price}</span>

									<i class="card-text" style="font-size: small; display:block"
										>Seller: <a href="/shop/user/profile" id="seller">{item.seller}</a></i
									>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</section>
</div>
