const items = document.getElementsByClassName('rating-section');

for (let item of items) {
    const [inc, counter, dec] = item.children;
    inc.addEventListener('click', () => {
	alert('Hello!');
    })
}
