// script.js
(function () {
    'use strict';

    /* ---------- STATE ---------- */
    let currentStep = 1;
    const TOTAL_STEPS = 4;

    /* ---------- DOM REFS ---------- */
    const form = document.getElementById('registerForm');
    const steps = Array.from(document.querySelectorAll('.step'));
    const stepLabels = Array.from(document.querySelectorAll('.step-label'));
    const progressFill = document.getElementById('progressFill');
    const stepCurrentEl = document.getElementById('stepCurrent');

    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    const countrySelect = document.getElementById('country');

    const accountCards = Array.from(document.querySelectorAll('.account-card'));
    const showMoreBtn = document.getElementById('showMoreTypes');

    const pinInput = document.getElementById('pin');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const matchMsg = document.getElementById('matchMsg');
    const strengthText = document.getElementById('strengthText');
    const strengthSegments = Array.from(document.querySelectorAll('.strength-segment'));
    const strengthRules = Array.from(document.querySelectorAll('.strength-rules li'));

    const successModal = document.getElementById('successModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');

    /* ---------- INIT: populate countries ---------- */
    function populateCountries() {
        COUNTRIES.forEach((name) => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            countrySelect.appendChild(opt);
        });
    }
    populateCountries();

    /* ---------- STEP NAVIGATION ---------- */
    function renderStep() {
        steps.forEach((sec) => {
            sec.classList.toggle('active', Number(sec.dataset.step) === currentStep);
        });

        stepLabels.forEach((label) => {
            const n = Number(label.dataset.step);
            label.classList.remove('active', 'done');
            if (n === currentStep) label.classList.add('active');
            else if (n < currentStep) label.classList.add('done');
        });

        progressFill.style.width = (currentStep / TOTAL_STEPS) * 100 + '%';
        stepCurrentEl.textContent = currentStep;

        prevBtn.disabled = currentStep === 1;

        if (currentStep === TOTAL_STEPS) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
        }

        // Scroll form into view on step change (useful on mobile)
        document.querySelector('.form-wrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function goNext() {
        if (!validateStep(currentStep)) return;
        if (currentStep < TOTAL_STEPS) {
            currentStep++;
            renderStep();
        }
    }

    function goPrev() {
        if (currentStep > 1) {
            currentStep--;
            renderStep();
        }
    }

    prevBtn.addEventListener('click', goPrev);
    nextBtn.addEventListener('click', goNext);

    /* ---------- VALIDATION HELPERS ---------- */
    function setError(fieldName, message) {
        const errEl = document.querySelector(`[data-error-for="${fieldName}"]`);
        const inputEl = document.getElementById(fieldName);
        if (errEl) errEl.textContent = message || '';
        if (inputEl) inputEl.classList.toggle('invalid', Boolean(message));
    }

    function isEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    function isPhone(value) {
        return /^[+\d][\d\s().-]{6,}$/.test(value);
    }

    /* ---------- STEP VALIDATORS ---------- */
    function validateStep(step) {
        let valid = true;

        if (step === 1) {
            const firstName = document.getElementById('firstName').value.trim();
            const lastName = document.getElementById('lastName').value.trim();
            const username = document.getElementById('username').value.trim();

            if (!firstName) { setError('firstName', 'Legal first name is required'); valid = false; }
            else setError('firstName', '');

            if (!lastName) { setError('lastName', 'Legal last name is required'); valid = false; }
            else setError('lastName', '');

            if (!username) { setError('username', 'Username is required'); valid = false; }
            else if (username.length < 3) { setError('username', 'Username must be at least 3 characters'); valid = false; }
            else setError('username', '');
        }

        if (step === 2) {
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const country = countrySelect.value;

            if (!email) { setError('email', 'Email address is required'); valid = false; }
            else if (!isEmail(email)) { setError('email', 'Enter a valid email address'); valid = false; }
            else setError('email', '');

            if (!phone) { setError('phone', 'Phone number is required'); valid = false; }
            else if (!isPhone(phone)) { setError('phone', 'Enter a valid phone number'); valid = false; }
            else setError('phone', '');

            if (!country) { setError('country', 'Please select your country'); valid = false; }
            else setError('country', '');
        }

        if (step === 3) {
            const pin = pinInput.value.trim();
            if (!/^\d{4}$/.test(pin)) {
                setError('pin', 'PIN must be exactly 4 digits');
                valid = false;
            } else {
                setError('pin', '');
            }
        }

        if (step === 4) {
            const password = passwordInput.value;
            const confirm = confirmPasswordInput.value;
            const agree = document.getElementById('agreeTerms').checked;

            const strongEnough = passwordRules(password).every(Boolean);
            if (!strongEnough) valid = false;

            if (password !== confirm || !confirm) {
                valid = false;
            }

            if (!agree) {
                setError('agreeTerms', 'You must accept the Terms of Service and Privacy Policy');
                valid = false;
            } else {
                setError('agreeTerms', '');
            }
        }

        return valid;
    }

    /* ---------- ACCOUNT TYPE CARDS ---------- */
    accountCards.forEach((card) => {
        card.addEventListener('click', () => {
            accountCards.forEach((c) => c.classList.remove('selected'));
            card.classList.add('selected');
            const input = card.querySelector('input[type="radio"]');
            input.checked = true;
        });
    });

    showMoreBtn.addEventListener('click', () => {
        document.querySelectorAll('.account-card.hidden-type').forEach((c) => c.classList.add('show'));
        showMoreBtn.classList.add('hidden');
    });

    /* ---------- PIN: digits only ---------- */
    pinInput.addEventListener('input', () => {
        pinInput.value = pinInput.value.replace(/\D/g, '').slice(0, 4);
    });

    /* ---------- PASSWORD STRENGTH ---------- */
    function passwordRules(pw) {
        return [
            pw.length >= 8,            // length
            /[A-Z]/.test(pw),          // upper
            /\d/.test(pw),             // number
            /[^A-Za-z0-9]/.test(pw),   // special
        ];
    }

    function updateStrength() {
        const pw = passwordInput.value;
        const rules = passwordRules(pw);
        const ruleKeys = ['length', 'upper', 'number', 'special'];

        ruleKeys.forEach((key, i) => {
            const li = strengthRules.find((el) => el.dataset.rule === key);
            li.classList.toggle('met', rules[i]);
        });

        const score = rules.filter(Boolean).length;

        strengthSegments.forEach((seg, i) => {
            seg.style.background = i < score ? strengthColor(score) : 'var(--line)';
        });

        const labels = ['Too weak', 'Weak', 'Fair', 'Good', 'Strong'];
        strengthText.textContent = labels[score];
        strengthText.style.color = score >= 3 ? 'var(--success)' : (score >= 1 ? 'var(--gold)' : 'var(--error)');

        checkPasswordMatch();
    }

    function strengthColor(score) {
        if (score <= 1) return '#b3261e';
        if (score === 2) return '#c08a3e';
        if (score === 3) return '#7a9a3c';
        return '#1f4d3e';
    }

    function checkPasswordMatch() {
        const pw = passwordInput.value;
        const confirm = confirmPasswordInput.value;

        if (!confirm) {
            matchMsg.textContent = '';
            matchMsg.className = 'match-msg';
            return;
        }

        if (pw === confirm) {
            matchMsg.textContent = 'Passwords match';
            matchMsg.className = 'match-msg match';
        } else {
            matchMsg.textContent = 'Passwords do not match';
            matchMsg.className = 'match-msg no-match';
        }
    }

    passwordInput.addEventListener('input', updateStrength);
    confirmPasswordInput.addEventListener('input', checkPasswordMatch);

    /* ---------- LIVE FIELD CLEAR-ON-TYPE ---------- */
    ['firstName', 'lastName', 'username', 'email', 'phone', 'country', 'pin'].forEach((id) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('input', () => setError(id, ''));
        el.addEventListener('change', () => setError(id, ''));
    });

    document.getElementById('agreeTerms').addEventListener('change', () => setError('agreeTerms', ''));

    /* ---------- FORM SUBMIT ---------- */
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!validateStep(4)) return;

        // Collect all form data
        const formData = {
            firstName: document.getElementById('firstName').value.trim(),
            middleName: document.getElementById('middleName').value.trim(),
            lastName: document.getElementById('lastName').value.trim(),
            username: document.getElementById('username').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            country: countrySelect.value,
            accountType: document.querySelector('input[name="accountType"]:checked').value,
            currency: document.getElementById('currency').value,
            pin: pinInput.value,
            password: passwordInput.value,
        };

        console.log('Registration payload (demo only — never log real passwords/PINs in production):', formData);

        // In a real app: send formData to your backend here, e.g.
        // fetch('/api/register', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(formData) })

        successModal.classList.add('show');
    });

    modalCloseBtn.addEventListener('click', () => {
        successModal.classList.remove('show');
        // Redirect to login in a real app:
        // window.location.href = '/login';
    });

    /* ---------- INITIAL RENDER ---------- */
    renderStep();
})();