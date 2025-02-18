document.addEventListener('DOMContentLoaded', function() {

    function validatePassword(passwordField) {
        const password = passwordField.value;
        const hasNumber = /\d/.test(password);

        if (password.length < 8 || !hasNumber) {
            setError(passwordField, 'Password must be at least 8 characters long and contain at least one number.');
            return false;
        }
        clearError(passwordField);
        return true;
    }

    function validateConfirmPassword(passwordField, confirmPasswordField) {
        if (passwordField.value !== confirmPasswordField.value) {
            setError(confirmPasswordField, 'Passwords do not match.');
            return false;
        }
        clearError(confirmPasswordField);
        return true;
    }

    function setError(field, message) {
        field.classList.add('error');
        let tooltip = field.parentElement.querySelector('.tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            field.parentElement.appendChild(tooltip);
        }
        tooltip.textContent = message;
        tooltip.classList.add('active');
    }

    function clearError(field) {
        field.classList.remove('error');
        const tooltip = field.parentElement.querySelector('.tooltip');
        if (tooltip) {
            tooltip.classList.remove('active');
        }
    }

    const registerForm = document.getElementById('registerForm');
    const resetPasswordForm = document.getElementById('resetPasswordForm');

    if (registerForm) {
        const passwordField = registerForm.querySelector('input[name="password1"]');

        registerForm.addEventListener('submit', function(event) {
            const isPasswordValid = validatePassword(passwordField);
            if (!isPasswordValid) {
                event.preventDefault();
            }
        });

        passwordField.addEventListener('input', function() {
            validatePassword(passwordField);
        });
    }

    if (resetPasswordForm) {
        const newPasswordField = resetPasswordForm.querySelector('input[name="new_password"]');
        const confirmPasswordField = resetPasswordForm.querySelector('input[name="confirm_password"]');

        resetPasswordForm.addEventListener('submit', function(event) {
            const isNewPasswordValid = validatePassword(newPasswordField);
            const isConfirmPasswordValid = validateConfirmPassword(newPasswordField, confirmPasswordField);

            if (!isNewPasswordValid || !isConfirmPasswordValid) {
                event.preventDefault();
            }
        });

        newPasswordField.addEventListener('input', function() {
            validatePassword(newPasswordField);
        });

        confirmPasswordField.addEventListener('input', function() {
            validateConfirmPassword(newPasswordField, confirmPasswordField);
        });
    }
});
