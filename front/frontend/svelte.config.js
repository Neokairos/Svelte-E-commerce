import adapter from '@sveltejs/adapter-auto';
import { sveltePreprocess } from 'svelte-preprocess';
import path from 'path';
/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: sveltePreprocess(),

	kit: {
		adapter: adapter(),
		alias: {
			'$app': path.resolve('node_modules/@sveltejs/kit/src/runtime/app'),
			'$lib': path.resolve('src/lib'),
		},


}};

export default config;
