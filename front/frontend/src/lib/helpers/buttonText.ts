export const changeText = (e: Event, text: string) => {
	const button = e.target as HTMLButtonElement;
	const originalText = button.textContent;
	const originalClass = button.className; // Store the original class
  
	// Change the button text and class
	button.textContent = text;
	button.className = 'btn btn-success-darker w-100 mt-3'; // Change color class
  
	// Revert the button text and class back to the original state after   2 seconds
	setTimeout(() => {
	  button.textContent = originalText;
	  button.className = originalClass; // Revert the class
	},   2000); //   2000 milliseconds =   2 seconds
  };
  