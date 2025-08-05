//MaNIPULACIÓN DINÁMICA DE ELEMENTOS DEL NAV

// Barra lateral de navegación
const nav = document.getElementById('barra_lateral');
// Secciones de la barra lateral
const SeccionesBarraLateral = document.querySelectorAll('.barra_lateral__seccion');
// Flechas de despliegue de cada sección
const FlechasSeccionesBarraLateral = document.querySelectorAll('.barra_lateral__flecha_modulo');

// Botón Menú hamburguesa para activar/desactivar sidebar
const BotonToggleNav = document.getElementById('BotonToggleNav');
// Botón para cerrar sidebar
const BotonCerrarNav = document.getElementById('BotonCerrarNav');
// Resolución para activar el menú hamburguesa
const mediaQuery = window.matchMedia('(min-width: 1000px)');




// Si se hace click en la flecha de cada módulo, se despliegan sus opciones
if(nav) {
    nav.addEventListener('click', (e) => {
        if(e.target.classList.contains('barra_lateral__flecha_modulo')) {
            e.target.parentElement.parentElement.classList.toggle('scale_nav_options');
            e.target.classList.toggle('rotate180');
        }
        });
}



// Mostrar/ocultar la barra lateral de navegación en resolución móvil
if (BotonToggleNav && nav) {
    BotonToggleNav.addEventListener('click', (e) => {
        nav.classList.toggle('barra_lateral-activada');
        BotonCerrarNav.classList.toggle('barra_lateral__boton_cerrar-activado');

        SeccionesBarraLateral.forEach(seccion => {
            seccion.classList.remove('scale_nav_options');
        });
        FlechasSeccionesBarraLateral.forEach(flecha => {
            flecha.classList.remove('rotate180');
        })
        
    })
}



// Ocultar barra lateral de navegación en resolución móvil
if (BotonCerrarNav && nav && SeccionesBarraLateral && FlechasSeccionesBarraLateral) {
    BotonCerrarNav.addEventListener('click', (e) => {
        nav.classList.toggle('barra_lateral-activada');
        BotonCerrarNav.classList.remove('barra_lateral__boton_cerrar-activado');

        SeccionesBarraLateral.forEach(seccion => {
            seccion.classList.remove('scale_nav_options');
        });
        FlechasSeccionesBarraLateral.forEach(flecha => {
            flecha.classList.remove('rotate180');
        })


    })
}



// Reestablecer elementos cuando las dimensiones de la pantalla aumentan
function handleResolutionChange(e) {
  if (e.matches) {
    // Pantalla ancha - quitar clase
    nav.classList.remove('barra_lateral-activada');
    BotonCerrarNav.classList.remove('barra_lateral__boton_cerrar-activado');
  }
}
mediaQuery.addEventListener('change', handleResolutionChange);
// Ejecutar inmediatamente para el estado inicial
handleResolutionChange(mediaQuery);