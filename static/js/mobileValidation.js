document.getElementById('contactForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const phone = document.getElementById('phone');
    const error = document.getElementById('phoneError');
    const phoneValue = phone.value.trim();

    if (phoneValue.length !== 10) {
        error.textContent = 'Phone number must be exactly 10 digits.';
        error.style.display = 'block';
        return;
    }

    error.style.display = 'none';

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const res = await fetch(this.action, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (result.status === 'success') {
            console.log(result.message); 
        } else {
            error.textContent = result.message;
            error.style.display = 'block';
        }
    } catch (err) {
        console.error('Submission error:', err);
    }
});
