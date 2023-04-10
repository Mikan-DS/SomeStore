// Добавление анимации для кнопок при наведении
const buttons = document.querySelectorAll('.button');
console.log(buttons)
buttons.forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.transform = 'scale(1.03)';
    });

    button.addEventListener('mouseout', () => {
        button.style.transform = 'scale(1)';
    });
});
