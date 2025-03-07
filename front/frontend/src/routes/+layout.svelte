<script lang="ts">
	import { userData } from '$lib/store/userStore';
	import { navigating } from '$app/stores';
	import { loading } from '$lib/store/loadingStore';
	import { notificationData, notificationErrorData, notificationSuccessData } from '$lib/store/notificationStore';
	import { fly } from 'svelte/transition';
	import { afterUpdate, onMount } from 'svelte';
	import Loader from '$lib/components/Loader/Loader.svelte';
	import Header from '$lib/components/Header/Header.svelte';

	import { showNotification, showNotificationError, showNotificationSuccess } from '$lib/utils/notificationUtils';
	import { SvelteToast } from '@zerodevx/svelte-toast';
	import { getCurrentUser, browserGet } from '$lib/utils/requestUtils';
	import { variables } from '$lib/utils/constants';
	import Page from './+page.svelte';
	
	$: loading.setNavigate(!!$navigating);
	$: loading.setLoading(!!$navigating, 'Loading...');
	$: $notificationData, $notificationErrorData, notificationSuccessData


	/*onMount(async () => {
		if (browserGet('refreshToken')) {
			console.log('TRUE refresh token was found on onMount')
			const [response, errs] = await getCurrentUser(
				`${variables.BASE_API_URI}/token/refresh`,
				`${variables.BASE_API_URI}/user`
			);
			if (errs.length <= 0) {
				userData.set(response);
				console.log('userdata set',userData, response)
			}
		}
	}); */

	afterUpdate(async () => {
		//Notification Handling
		if ($notificationData !== '' ) {

			showNotification($notificationData,3000)
			notificationData.set('');
		} 
		 if ($notificationErrorData !== '' ) {

			showNotificationError($notificationErrorData,3000)
			notificationErrorData.set('');

		}
		 if ($notificationSuccessData !== '' ) {
				showNotificationSuccess($notificationSuccessData,3000)
				notificationSuccessData.set('');
			} 

		if (browserGet('refreshToken')) {
			console.log('TRUE refresh token was found on afterUpdate')
			const [response, error] = await getCurrentUser(
				`${variables.BASE_API_URI}/token/refresh`,
				`${variables.BASE_API_URI}/user`
			);
			userData.update(() => response);

			if (error.length > 0) {
    		console.error('layout error: ', error);
		} else if (Object.keys(response).length > 0)
			console.log('layout response: ', response)
}

		
	});
</script>

<svelte:head><Header /></svelte:head>

<div class="top-center">
	<SvelteToast />
</div>

<main>
	<Loader />
	<slot />
</main>
