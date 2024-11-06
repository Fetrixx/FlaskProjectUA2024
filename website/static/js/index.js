// toggleCommentForm.js
function toggleCommentForm(postId) {
  var form = document.getElementById("commentForm-" + postId);
  if (form.style.display === "none" || form.style.display === "") {
      form.style.display = "block"; // Mostrar el formulario
  } else {
      form.style.display = "none"; // Ocultar el formulario
  }
}

function toggleReplyForm(commentId) {
  var form = document.getElementById("replyForm-" + commentId);
  if (form.style.display === "none" || form.style.display === "") {
      form.style.display = "block"; // Mostrar el formulario de respuesta
  } else {
      form.style.display = "none"; // Ocultar el formulario de respuesta
  }
}


// Función para confirmar la eliminación de un comentario
function confirmDelete(event) {
  if (!confirm("¿Estás seguro de que deseas eliminar este comentario?")) {
      event.preventDefault(); // Evitar que se envíe el formulario si el usuario cancela
  }
}

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
  // Manejar el botón "Comentar"
  document.querySelectorAll('.comment-btn').forEach(button => {
      button.addEventListener('click', function() {
          const postId = this.dataset.postId; // Obtener el ID del post desde un atributo data
          toggleCommentForm(postId); // Llamar a la función para alternar el formulario
      });
  });

  // Manejar el botón "Responder"
  document.querySelectorAll('.reply-btn').forEach(button => {
      button.addEventListener('click', function() {
          const commentId = this.dataset.commentId; // Obtener el ID del comentario desde un atributo data
          toggleReplyForm(commentId); // Llamar a la función para alternar el formulario de respuesta
      });
  });

  /*
  // Manejar los formularios de eliminación con confirmación
  document.querySelectorAll('.delete-comment-btn').forEach(button => {
      button.addEventListener('click', function(event) {
          confirmDelete(event); // Llamar a la función de confirmación antes de eliminar
      });
  });

  */
});
