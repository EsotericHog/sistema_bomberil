        // Lógica de las pestañas
        function openTab(tabName) {
            var i;
            var x = document.getElementsByClassName("tab-content");
            var buttons = document.getElementsByClassName("tab-button");
            
            for (i = 0; i < x.length; i++) {
                x[i].style.display = "none";
            }
            for (i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove("active");
            }
            document.getElementById(tabName).style.display = "block";
            
            // Encuentra el botón correcto y añade la clase 'active'
            for (i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.toLowerCase().includes(tabName)) {
                    buttons[i].classList.add("active");
                }
            }
        }
        
        // Muestra la pestaña de profesiones al cargar (por defecto)
        document.addEventListener('DOMContentLoaded', (event) => {
            document.getElementById('profesiones').style.display = 'block';

            // Lógica para el Modal de Edición
            const modal = document.getElementById('editModal');
            const closeBtn = document.querySelector('.close-button');

            document.querySelectorAll('.btn-edit').forEach(button => {
                button.addEventListener('click', (e) => {
                    const row = e.target.closest('tr');
                    const id = e.target.dataset.id;
                    const type = e.target.dataset.type;
                    
                    const name = row.children[1].textContent;

                    document.getElementById('edit-id').value = id;
                    document.getElementById('edit-type').value = type;
                    document.getElementById('edit-name').value = name;
                    document.getElementById('modal-title-type').textContent = (type === 'profesion' ? 'Profesión' : 'Rango');
                    
                    modal.style.display = 'block';
                });
            });

            closeBtn.onclick = () => { modal.style.display = 'none'; };
            window.onclick = (event) => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            };
        });