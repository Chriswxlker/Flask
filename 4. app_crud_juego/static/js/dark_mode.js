document.addEventListener("DOMContentLoaded", () => {
    const themeSwitchCheckbox = document.querySelector(".theme-switch__checkbox");
    const body = document.body;

    // Leer la preferencia guardada en localStorage
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        // Aplicar el tema guardado
        body.classList.add(savedTheme);
        themeSwitchCheckbox.checked = savedTheme === "dark-mode";
    } else {
        // Si no hay tema guardado, respetar la preferencia del sistema
        const isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
        body.classList.add(isDarkMode ? "dark-mode" : "light-mode");
        themeSwitchCheckbox.checked = isDarkMode;
    }

    // Cambiar el tema cuando se interactúe con el checkbox
    themeSwitchCheckbox.addEventListener("change", () => {
        if (themeSwitchCheckbox.checked) {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark-mode"); // Guardar preferencia en localStorage
        } else {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            localStorage.setItem("theme", "light-mode"); // Guardar preferencia en localStorage
        }
    });
});
