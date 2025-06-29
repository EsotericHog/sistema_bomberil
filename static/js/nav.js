//Manipulación dinámica de elementos del nav
const nav = document.getElementById('barra_lateral');

if(nav) {
    nav.addEventListener('click', (e)=>{
        /*if(e.target.classList.contains('barra_lateral__modulo')) {
                e.target.parentElement.classList.toggle('scale_nav_options');
                e.target.children[1].classList.toggle('rotate180');
            }
            else if(e.target.classList.contains('barra_lateral__modulo_nombre')) {
                e.target.parentElement.parentElement.classList.toggle('scale_nav_options');
                e.target.nextElementSibling.classList.toggle('rotate180');
            }
            else if(e.target.classList.contains('barra_lateral__flecha_modulo')) {
                e.target.parentElement.parentElement.classList.toggle('scale_nav_options');
                e.target.classList.toggle('rotate180');
            }
        */
       // Si se hace click en la flecha de cada módulo, se despliegan sus opciones
        if(e.target.classList.contains('barra_lateral__flecha_modulo')) {
            e.target.parentElement.parentElement.classList.toggle('scale_nav_options');
            e.target.classList.toggle('rotate180');
        }
        });
}