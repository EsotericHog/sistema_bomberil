    // --- Lógica de Pestañas y Filtros (Tu script anterior) ---
    function openTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.style.display = 'none';
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        
        const selectedTab = document.getElementById(tabId);
        if (selectedTab) {
            selectedTab.style.display = 'block';
            selectedTab.classList.add('active');
        }
        const activeBtn = document.querySelector(`button[onclick="openTab('${tabId}')"]`);
        if (activeBtn) activeBtn.classList.add('active');
    }

    document.addEventListener('DOMContentLoaded', function() {
        const searchProfesion = document.getElementById('search-profesion');
        const searchCargo = document.getElementById('search-cargo');
        const filterTipoCargo = document.getElementById('filter-tipo-cargo');

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('q_cargo') || urlParams.has('tipo_cargo')) {
            openTab('rangos');
        } else {
            openTab('profesiones');
        }

        function updateFilters(contexto) {
            const url = new URL(window.location.href);
            
            if (contexto === 'profesiones') {
                if (searchProfesion.value) url.searchParams.set('q_profesion', searchProfesion.value);
                else url.searchParams.delete('q_profesion');
                url.searchParams.delete('q_cargo');
                url.searchParams.delete('tipo_cargo');
            } 
            else if (contexto === 'rangos') {
                if (searchCargo.value) url.searchParams.set('q_cargo', searchCargo.value);
                else url.searchParams.delete('q_cargo');
                if (filterTipoCargo.value && filterTipoCargo.value !== 'global') url.searchParams.set('tipo_cargo', filterTipoCargo.value);
                else url.searchParams.delete('tipo_cargo');
                url.searchParams.delete('q_profesion');
            }
            window.location.href = url.toString();
        }

        if(searchProfesion) searchProfesion.addEventListener('keyup', function(e) { if (e.key === 'Enter') updateFilters('profesiones'); });
        if(searchCargo) searchCargo.addEventListener('keyup', function(e) { if (e.key === 'Enter') updateFilters('rangos'); });
        if(filterTipoCargo) filterTipoCargo.addEventListener('change', function() { updateFilters('rangos'); });
    });