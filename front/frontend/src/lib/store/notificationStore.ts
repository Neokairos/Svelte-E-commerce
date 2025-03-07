import { writable } from 'svelte/store';


export const notificationData = writable<string>('');
export const notificationErrorData = writable<string>('');
export const notificationSuccessData = writable<string>('');