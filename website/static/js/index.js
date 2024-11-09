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


function toggleUrlFields() {
    const contentType = document.getElementById('content_type').value;
    const imageField = document.getElementById('image_url_field');
    const videoField = document.getElementById('video_url_field');

    if (contentType === 'image') {
        imageField.style.display = 'block';
        videoField.style.display = 'none';
    } else if (contentType === 'video') {
        videoField.style.display = 'block';
        imageField.style.display = 'none';
    } else {
        imageField.style.display = 'none';
        videoField.style.display = 'none';
    }
}



function toggleLikeComment(commentId) {
    fetch(`/like-comment/${commentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // Incluye el token CSRF si es necesario
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Actualiza el contador de likes en el HTML
        const likeCountElement = document.querySelector(`#like-count-${commentId}`);
        likeCountElement.textContent = data.likes_count;

        // Cambia el estado del botón (opcional)
        const likeButton = document.querySelector(`#like-button-${commentId}`);
        likeButton.textContent = data.liked ? 'Quitar Me gusta' : 'Me gusta';
    })
    .catch(error => console.error('Error:', error));
}

function goToUserProfile(userId) {
    // Navega al perfil del usuario con el ID correspondiente
    window.location.href = '/profile/' + userId; // Asegúrate de que la ruta en Flask sea '/profile/<user_id>'
}

function goToUsersFollowed() {
    window.location.href = '/my-following';
}


function logoutUser(userId) {
    // Navega al perfil del usuario con el ID correspondiente
    window.location.href = '/logout'; // Asegúrate de que la ruta en Flask sea '/profile/<user_id>'
}

function gotoSignUp(userId) {
    // Navega al perfil del usuario con el ID correspondiente
    window.location.href = '/sign-up'; // Asegúrate de que la ruta en Flask sea '/profile/<user_id>'
}
  

function toggleComments(postId) {
    var commentsSection = document.getElementById('comments-' + postId);
    var toggleArrow = document.getElementById('toggleArrow-' + postId);
    var toggleText = document.getElementById('toggleText-' + postId);

    // Toggle visibilidad
    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
        commentsSection.style.display = 'block';
        toggleArrow.classList.remove('fa-arrow-down');
        toggleArrow.classList.add('fa-arrow-up');
        toggleText.textContent = 'Ocultar Hilo';  // Cambia el texto a 'Ocultar Hilo'
    } else {
        commentsSection.style.display = 'none';
        toggleArrow.classList.remove('fa-arrow-up');
        toggleArrow.classList.add('fa-arrow-down');
        toggleText.textContent = 'Ver Hilo';  // Cambia el texto a 'Ver Hilo'
    }
}



function toggleEditUrlFields(postId) {
    var contentType = document.getElementById("editContentType-" + postId).value;
    document.getElementById("editImageUrlField-" + postId).style.display = (contentType === 'image') ? 'block' : 'none';
    document.getElementById("editVideoUrlField-" + postId).style.display = (contentType === 'video') ? 'block' : 'none';
  }

  /*

  function openEditPostModal(postId, content, imageUrl, videoUrl, contentType) {
    document.getElementById("editPostModal").style.display = "block";
    document.getElementById("editPostContent").value = JSON.parse(content);
    document.getElementById("editImageUrl").value = imageUrl || "";
    document.getElementById("editVideoUrl").value = videoUrl || "";
    document.getElementById("editContentType").value = contentType;
    toggleEditUrlFields();
  }
  */

  function openEditPostModal(postId, data, imageUrl = '', videoUrl = '', contentType = 'text') {
    // Encuentra y muestra el contenedor del formulario de edición específico
    var editContainer = document.getElementById("editPostContainer-" + postId);
    editContainer.style.display = "block";
    
    // Rellena los campos del formulario con los datos actuales de la publicación
    document.getElementById("editPostContent-" + postId).value = data;
    document.getElementById("editContentType-" + postId).value = contentType;
  
    // Muestra y oculta los campos de URL según el tipo de contenido
    toggleEditUrlFields(postId);
  
    if (contentType === 'image') {
      document.getElementById("editImageUrl-" + postId).value = imageUrl;
    } else if (contentType === 'video') {
      document.getElementById("editVideoUrl-" + postId).value = videoUrl;
    }
  }




function openEditCommentModal(commentId, commentData) {
    var modal = document.getElementById("editCommentModal-" + commentId);
    var textarea = document.getElementById("editCommentContent-" + commentId);
    textarea.value = commentData;
    modal.style.display = "block";
  }
  

  function closeEditPostModal(postId) {
    var editContainer = document.getElementById("editPostContainer-" + postId);
    editContainer.style.display = "none";
  }
  
  function closeEditCommentModal(commentId) {
    var modal = document.getElementById("editCommentModal-" + commentId);
    modal.style.display = "none";
  }


  /*
  function playCuakSound() {
    // Obtener el elemento de audio
    var cuakSound = document.getElementById('cuakSound');
    
    // Reproducir el sonido
    cuakSound.play();
  }
*/
/*
//  function playCuakThenSubmit() {
function playCuakSound() {
    var cuakSound = document.getElementById('cuakSound');

    // Reproducir el sonido
    cuakSound.play();

    // Esperar un momento antes de enviar el formulario
    setTimeout(function() {
      // Aquí puedes hacer el envío del formulario o redirigir a otra página
      document.forms[0].submit(); // Enviar el primer formulario en la página
    }, 500); // 500 ms de retraso para permitir que el sonido se reproduzca primero
  }*/

  function playCuakSound(event) {
    event.preventDefault(); // Evita el envío inmediato del formulario

    // Obtener el formulario
    var form = document.forms[0];

    // Verificar si el formulario es válido
    if (form.checkValidity()) {
      // Reproducir el sonido
      var cuakSound = document.getElementById('cuakSound');
      cuakSound.play();

      // Esperar un poco para que el sonido se reproduzca antes de enviar
      setTimeout(function() {
        form.submit(); // Enviar el formulario
      }, 500); // 500 ms de retraso para permitir que el sonido se reproduzca primero
    } else {
      // Si el formulario no es válido, puedes mostrar un mensaje o manejar el error
      alert('Por favor, completa todos los campos correctamente.');
    }
  }

  function forcePlayCuakSound() {
    // Obtener el elemento de audio
    var cuakSound = document.getElementById('cuakSound');
    // Reproducir el sonido
    cuakSound.play();

  }