// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';


export default defineConfig({
	plugins: [sveltekit()],

	server: {
			https: {
		  	key: fs.readFileSync('./certificates/private.key'),
		  	cert: fs.readFileSync('./certificates/server.crt'),
		},}

	
});

   