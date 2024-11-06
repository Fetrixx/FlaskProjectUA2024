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


document.addEventListener("DOMContentLoaded", function() {
    // Cargar publicaciones al cargar la página
    loadPosts();

    // Función para cargar publicaciones
    function loadPosts() {
        fetch('/load_posts')
            .then(response => response.json())
            .then(posts => {
                const postsContainer = document.getElementById('posts-container');
                postsContainer.innerHTML = '';  // Limpiar publicaciones previas
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'post';
                    postElement.innerHTML = `
                        <h3>${post.data}</h3>
                        ${post.image_url ? `<img src="${post.image_url}" alt="Image">` : ''}
                        ${post.video_url ? `<iframe src="${post.video_url}"></iframe>` : ''}
                        <p>Publicado por el usuario ${post.user_id} en ${post.date}</p>
                    `;
                    postsContainer.appendChild(postElement);
                });
            })
            .catch(error => console.error('Error al cargar publicaciones:', error));
    }

    // Función para agregar una nueva publicación
    document.getElementById('post-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevenir recarga
        const formData = new FormData(this);
        
        fetch('/add_post', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                loadPosts();  // Volver a cargar las publicaciones
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error al agregar publicación:', error));
    });
});