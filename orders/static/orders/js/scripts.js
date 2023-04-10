// Добавление анимации для кнопок при наведении
const expand_buttons = document.querySelectorAll('.expand_button');
expand_buttons.forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.transform = 'scale(1.03)';
    });

    button.addEventListener('mouseout', () => {
        button.style.transform = 'scale(1)';
    });
});
