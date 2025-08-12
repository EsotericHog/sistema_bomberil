/*
const ModalDesactivarUsuario = document.getElementById('ModalDesactivarUsuario')
const confirmarDesactivarUsuario = document.getElementById('confirmarDesactivarUsuario')

ModalDesactivarUsuario.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})
*/

document.addEventListener('DOMContentLoaded', function () {
  // 1. Seleccionar el elemento HTML del modal
  const ModalDesactivarUsuario = document.getElementById('ModalDesactivarUsuario');
  
  // Si el elemento del modal no existe, no hacemos nada más.
  if (!ModalDesactivarUsuario) {
    console.error("No se encontró el elemento del modal #ModalDesactivarUsuario.");
    return;
  }

  // 2. Crear una instancia del Modal de Bootstrap a partir del elemento HTML
  const modalBootstrap = new bootstrap.Modal(ModalDesactivarUsuario);
  
  // Seleccionar el formulario que está dentro del modal
  const formDesactivarUsuario = document.getElementById('formDesactivarUsuario');

  // 3. Añadir el listener a todos los botones que deben abrir el modal
  document.querySelectorAll('.boton-desactivar-usuario').forEach(boton => {
    boton.addEventListener('click', function () {
      
      // Esta lógica para obtener la URL y actualizar el formulario sigue igual
      const urlAccion = this.dataset.formAction;

      if (formDesactivarUsuario && urlAccion) {
        formDesactivarUsuario.action = urlAccion;
      } else {
        console.error("No se encontró el formulario o la URL en el data-attribute.");
      }

      // 4. Mostrar el modal usando el método de Bootstrap
      modalBootstrap.show();
    });
  });
  
  // ¡Ya no necesitas el código para cerrar el modal!
  // Bootstrap lo hace automáticamente con 'data-bs-dismiss="modal"'.
});