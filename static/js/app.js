document.addEventListener("DOMContentLoaded", () => {
    // Automatically hide success/info messages after a few seconds.
    document.querySelectorAll(".message").forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";
            message.style.transition = "opacity .4s";
            setTimeout(() => message.remove(), 400);
        }, 3500);
    });

    // Prevent accidental double-submit on checkout/order forms.
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const button = form.querySelector('button[type="submit"]');
            if (button && button.dataset.lockSubmit === "true") return;
            if (button && (button.textContent.includes("Place order"))) {
                button.dataset.lockSubmit = "true";
                button.disabled = true;
                button.textContent = "Processing...";
            }
        });
    });
});
