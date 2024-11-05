function deleteNote(noteId) {
  console.log(noteId)
  fetch("/delete-note", {
    method: "POST",
    // body: JSON.stringify({ noteId: noteId }),
    headers: {
      "Content-Type": "application/json", // incluir el encabezado
    },
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/"; // redirigirse a la página principal después de eliminar
  }).catch((error) => {
    console.error("Error al eliminar la nota:", error); // Manejo de errores
  });;
}
