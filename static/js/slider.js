document.addEventListener('DOMContentLoaded', () => {
    // Seleccionamos TODOS los sliders que haya en la página
    const sliders = document.querySelectorAll('.slider-container');

    // Iteramos sobre cada slider para que funcionen de forma independiente
    sliders.forEach(sliderContainer => {
        const slider = sliderContainer.querySelector('.slider');
        const items = sliderContainer.querySelectorAll('.slider-item'); // <-- CAMBIO CLAVE AQUÍ
        const prevBtn = sliderContainer.querySelector('.prev-btn');
        const nextBtn = sliderContainer.querySelector('.next-btn');

        if (!slider || !prevBtn || !nextBtn || items.length === 0) {
            return;
        }

        let currentIndex = 0;
        const totalItems = items.length;
        let itemsPerView;

        function updateSlider() {
            itemsPerView = parseInt(getComputedStyle(slider).getPropertyValue('--cards-per-view'));
            const maxIndex = totalItems - itemsPerView;

            if (currentIndex > maxIndex) currentIndex = maxIndex;
            if (currentIndex < 0) currentIndex = 0;

            const itemWidth = items[0].offsetWidth + parseInt(getComputedStyle(slider).gap);
            slider.style.transform = `translateX(-${currentIndex * itemWidth}px)`;

            prevBtn.style.display = currentIndex === 0 ? 'none' : 'flex';
            nextBtn.style.display = currentIndex >= maxIndex ? 'none' : 'flex';
        }

        nextBtn.addEventListener('click', () => {
            const maxIndex = totalItems - itemsPerView;
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateSlider();
            }
        });

        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateSlider();
            }
        });

        window.addEventListener('resize', updateSlider);
        updateSlider();
    });
});