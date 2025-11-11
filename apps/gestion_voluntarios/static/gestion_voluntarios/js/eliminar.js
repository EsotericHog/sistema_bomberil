document.addEventListener('DOMContentLoaded', function() {
    
    // --- Referencias a los elementos del DOM ---
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modal = document.getElementById('deleteModal');
    const backdrop = document.getElementById('deleteModalBackdrop');
    const volunteerNameSpan = document.getElementById('volunteerName');
    const deleteForm = document.getElementById('deleteForm');
    
    // Botones para cerrar el modal
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');

    // --- Función para abrir el modal ---
    function openModal(event) {
        // Prevenir que el link navegue (MUY IMPORTANTE)
        event.preventDefault(); 
        
        const button = event.currentTarget;
        
        // 1. Obtener los datos del botón
        const url = button.href; // La URL de eliminación
        const name = button.dataset.name; // El nombre del voluntario (desde data-name)

        // 2. Poblar el modal
        volunteerNameSpan.textContent = name;
        deleteForm.action = url; // Asignar la URL al 'action' del formulario

        // 3. Mostrar el modal
        modal.classList.add('show');
        backdrop.classList.add('show');
    }

    // --- Función para cerrar el modal ---
    function closeModal() {
        modal.classList.remove('show');
        backdrop.classList.remove('show');
    }

    // --- Asignar Eventos ---
    
    // Asignar evento de click a todos los botones de eliminar
    deleteButtons.forEach(button => {
        button.addEventListener('click', openModal);
    });

    // Asignar eventos para cerrar el modal
    closeModalBtn.addEventListener('click', closeModal);
    cancelModalBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);
});