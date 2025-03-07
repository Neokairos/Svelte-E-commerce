<script>
	// @ts-nocheck

	import axios from 'axios';
	import { productStore } from '../../../store';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	// @ts-ignore
	export let data;
	// @ts-ignore
	let product;
	let loading = true;

	onMount(async function () {
		try {
			if ($productStore.all.some((product) => product.id == data.id)) {
				product = $productStore.all.find((product) => product.id == data.id);
				loading = false;
			} else {
				const endpoint = `http://127.0.0.1:8000/api/products/${data.id}`;
				let res = await axios.get(endpoint);
				product = res.data;
				productStore.update((n) => ({ ...n, all: [...n.all, product], current: product }));
				loading = false;
			}
		} catch (err) {
			console.log('error at Details: ', err);
			product = null;
			loading = false;
		}
	});
</script>

<section
	class="container mt-5"
	in:fly={{ y: 100, duration: 500, delay: 650 }}
	out:fly={{ duration: 500 }}
>
	{#if loading}
		<div class="center">
			<div class="loader" role="status"></div>
		</div>
	{:else if !loading}
		<div class="row mt-4">
			<div class="col-12 col-md-4">
				<img src={product.image} alt="product" class="w-100 mb-1" />
				<b >Seller: {product.seller}</b>
				<br/>
				<a href="/shop" class="btn btn-danger">Back</a>
			</div>

			<div class="col-12 col-md-7">

				<div >
					<h1 class="mb-4 product-name-id">{product.title}</h1>
					<span class="product-price mb-4 "><abbr id="currency" title="US Dollar">$</abbr>{product.price}</span>
		
				</div>
				<a href="/shop/{product.id}/buy" class="buy-button">Buy</a>
				<p class="mt-3">Description:<br/>- {product.description}</p>
			
			</div>
		</div>
	{:else}
		<p>No product was found with ID {data.id}</p>
		<a href="/shop" class="btn btn-danger p-8 mb-5 mt-2 pr-5">Back</a>
	{/if}
</section>

