<script>
	// import { page } from '$app/state';
	import { userData } from '$lib/store/userStore';
	import alien from './weed_alien.svg';
	import { logOutUser } from '$lib/utils/requestUtils';
	// import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	
</script>

<header>

	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
		
		<div class="container-fluid">
			<!-- Image integrated into the navbar -->
			<img src={alien} alt="WEED" class="navbar-image" style="height: 80px;" />
			<ul class="navbar-nav ">
				<!-- Home link moved to the left -->
				<li class="nav-item me-auto">
					<a class="nav-link" href="/shop">
						<span>
							<i class="icon icon-home" ></i>
						</span>
						<span >Home</span>
						
					</a>

				</li>
				
				{#if !userData.username}
					<li class="nav-item me-3 hover-animation">
						<a class="nav-link" href="/accounts/login">Account</a>
						<div class="down-sub">
							<a
								class="btn btn-secondary butn"
								href="/accounts/login"
								on:click|preventDefault={() => goto('/accounts/login')}
							>
								Log in
							</a>
							<div class="ou">or</div>
							<a class="underlined-text" href="/accounts/register"> New Here? Create Account </a>
						</div>
					</li>
				{:else}
					<li class="nav-item me-3 hover-animation">
						<a class="nav-link" href="{`/accounts/user/${userData.id}/${userData.username}`}">Account</a>
						<div class="down-sub">
							<!--displaying user name or log out-->
							<a
								class="btn btn-secondary butn"
								href={`/accounts/user/${userData.id}/${userData.username}`}
								on:click|preventDefault={() =>
									goto(`/accounts/user/${userData.id}/${userData.username}`)}
							>
								{userData.username}
							</a>
							<div class="ou">or</div>
							<a href={null} on:click={logOutUser} style="font-size:medium;" class="underlined-text">Logout</a>
						</div>
					</li>
				{/if}
			</ul>
		</div>
	</nav>
</header>
