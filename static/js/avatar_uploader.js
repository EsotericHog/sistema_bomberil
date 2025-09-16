/**
 * Función genérica para manejar la subida de avatares vía AJAX.
 * @param {string} containerId - El ID del contenedor principal del avatar.
 */
function inicializarCargadorAvatar(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Contenedor de avatar con ID "${containerId}" no encontrado.`);
        return;
    }

    const botonSubir = container.querySelector('.js-avatar-upload-button');
    const inputSubir = container.querySelector('.js-avatar-upload-input');
    const imagenAvatar = container.querySelector('.js-avatar-image');
    const apiUrl = container.dataset.apiUrl; // La URL de la API se lee desde el HTML
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!botonSubir || !inputSubir || !imagenAvatar || !apiUrl) {
        console.error("Faltan elementos esenciales (botón, input, imagen o data-api-url) dentro del contenedor.");
        return;
    }

    // 1. Clic en el botón activa el input de archivo
    botonSubir.addEventListener('click', () => {
        inputSubir.click();
    });

    // 2. Cuando se selecciona un archivo
    inputSubir.addEventListener('change', () => {
        const file = inputSubir.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('nuevo_avatar', file);

        // Muestra un indicador de carga (opcional pero recomendado)
        container.classList.add('uploading');

        // 3. Envío del archivo con Fetch
        fetch(apiUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                // Si la respuesta no es 2xx, la convertimos en un error
                return response.json().then(err => { throw new Error(err.error || 'Error del servidor') });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // 4. Éxito: actualiza la imagen
                imagenAvatar.src = data.new_avatar_url + '?' + new Date().getTime();
            } else {
                // Muestra el error que viene del servidor
                alert('Error al subir la imagen: ' + (data.error || 'Error desconocido'));
            }
        })
        .catch(error => {
            alert('Ha ocurrido un error de conexión: ' + error.message);
            console.error('Error en fetch:', error);
        })
        .finally(() => {
            // Quita el indicador de carga
            container.classList.remove('uploading');
            // Resetea el input para poder subir el mismo archivo de nuevo si se desea
            inputSubir.value = '';
        });
    });
}