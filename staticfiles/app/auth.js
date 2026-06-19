document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const toggle = document.getElementById('togglePassword');
    const errors = document.getElementById('formErrors');

    // 🔒 Password visibility toggle
    toggle.addEventListener('click', () => {
        const type = password.type === 'password' ? 'text' : 'password';
        password.type = type;
        toggle.textContent = type === 'password' ? '👁️' : '🙈';
        toggle.setAttribute('aria-label', type === 'password' ? 'Show password' : 'Hide password');
    });

    // 📝 Helper to show errors
    function showErrors(msgs) {
        errors.innerHTML = msgs.map(m => `<div>${m}</div>`).join('');
        errors.hidden = false;
        errors.classList.add('shake'); // animation
        setTimeout(() => errors.classList.remove('shake'), 500);
        errors.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // ✅ Form validation before submit
    form.addEventListener('submit', e => {
        errors.hidden = true;
        errors.textContent = '';
        const msgs = [];

        if (!username.value.trim()) msgs.push('Username is required.');
        if (!password.value.trim()) msgs.push('Password is required.');
        if (password.value && password.value.length < 6) msgs.push('Password must be at least 6 characters.');

        if (msgs.length) {
            e.preventDefault();
            showErrors(msgs);
            return;
        }

        // Allow normal Django POST if valid
        errors.hidden = true;
    });

    // 🎯 Accessibility: focus first input on load
    if (username) username.focus();

    // ⌨️ Keyboard shortcut: Enter toggles password visibility if focused on toggle
    toggle.addEventListener('keyup', e => {
        if (e.key === 'Enter' || e.key === ' ') toggle.click();
    });
});
