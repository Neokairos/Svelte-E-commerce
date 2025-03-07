<script>

    import { notificationData,notificationErrorData, notificationSuccessData } from "$lib/store/notificationStore";
	import { get } from "svelte/store";
    function Not() {
        notificationSuccessData.update(() => 'NIgaa...');
    }
    function ErrorNot() {
        notificationErrorData.update(() => 'NIgaa...');
    }
    


</script>


<button class='btn btn-light rounded hover:rounded-full transition-all ease-in-out duration-300' on:click={Not}>Click me!</button>

<button class='btn btn-light' on:click={ErrorNot}>!</button>