import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import path from 'path'
import UnoCSS from 'unocss/vite';

export default defineConfig({
	plugins: [sveltekit(), UnoCSS()],

	server: {
		cors: {
			origin: '*',
			methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
			preflightContinue: false,
			optionsSuccessStatus: 204,
		}
	},

	
	build: {
		transpile: ['@sveltejs/vite-plugin-svelte'],
		rollupOptions: {
			preserveEntrySignatures: 'strict',
		},
		sourcemap: true
	},
	
	test: {
		include: ['src/**/*.{test,spec,vitest}.{js,ts}']
	},
	
	kit: {
		alias: {
			'$trinkets': path.resolve ('./src/trinkets')
		}
	}
});
