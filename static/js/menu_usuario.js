document.addEventListener('DOMContentLoaded', function() {
    const btnTema = document.getElementById('btn-alternar-tema');
    const txtTema = document.getElementById('texto-tema-actual');
    
    // Función helper para obtener cookies (CSRF Token)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Lógica para alternar tema
    if (btnTema) {
        btnTema.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.dataset.url;
            const csrftoken = getCookie('csrftoken');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Error en la petición');
            })
            .then(data => {
                if (data.status === 'ok') {
                    // Actualizar UI inmediatamente
                    if (data.dark_mode) {
                        document.body.classList.add('dark-mode');
                        if (txtTema) txtTema.textContent = 'Oscuro';
                    } else {
                        document.body.classList.remove('dark-mode');
                        if (txtTema) txtTema.textContent = 'Claro';
                    }
                }
            })
            .catch(error => {
                console.error('Error al cambiar el tema:', error);
            });
        });
    }
});