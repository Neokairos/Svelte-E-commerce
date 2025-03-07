import { toast } from '@zerodevx/svelte-toast';

export function showNotification(message, duration) {
    toast.push(message, { duration: duration});
}
export function showNotificationError(message, duration) {
    toast.push(message, { duration: duration ,theme: {
        '--toastBackground': 'darkred',
        '--toastColor': 'bisque',
        '--toastBarBackground': 'tomato'
      }});
}

export function showNotificationSuccess(message, duration) {
    toast.push(message, { duration: duration,theme: {
        '--toastBackground': 'seagreen',
        '--toastColor': 'bisque',
        '--toastBarBackground': 'olive'
      }});
}
