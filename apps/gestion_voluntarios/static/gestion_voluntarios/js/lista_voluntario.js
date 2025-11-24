document.addEventListener('DOMContentLoaded', function() {
    // 1. ELIMINADA la referencia a 'estacion-filter'
    const rangoSelect = document.getElementById('rango-filter');
    const searchInput = document.getElementById('search-input');

    function aplicarFiltros() {
        // 2. Ya no leemos el valor de estación
        const rango = rangoSelect.value;
        const busqueda = searchInput.value;

        const url = new URL(window.location.href);
        
        // 3. ELIMINADA la línea: url.searchParams.set('estacion', estacion);
        // Ya no enviamos el parámetro estación por URL, el backend usa la sesión.

        // Lógica para Rango
        if (rango && rango !== 'global') {
            url.searchParams.set('rango', rango);
        } else {
            url.searchParams.delete('rango'); // Limpiamos la URL si selecciona "Todos"
        }
        
        // Lógica para Búsqueda
        if (busqueda) {
            url.searchParams.set('q', busqueda);
        } else {
            url.searchParams.delete('q');
        }

        window.location.href = url.toString();
    }

    // 4. Event Listener solo para Rango (Estación eliminado)
    if (rangoSelect) {
        rangoSelect.addEventListener('change', aplicarFiltros);
    }

    // 5. Mantenemos tu lógica de búsqueda exacta (Enter o delay de 800ms)
    if (searchInput) {
        let timeout = null;
        searchInput.addEventListener('keyup', function(e) {
            clearTimeout(timeout);
            if (e.key === 'Enter') {
                aplicarFiltros();
            } else {
                // Pequeño retardo para buscar automáticamente al dejar de escribir
                timeout = setTimeout(aplicarFiltros, 800);
            }
        });
    }
});