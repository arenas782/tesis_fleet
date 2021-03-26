const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 5000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  function confirmation(ev) {
    ev.preventDefault();
    var urlToRedirect = ev.currentTarget.getAttribute('href'); //use currentTarget because the click may be on the nested i tag and not a tag causing the href to be empty
    console.log(urlToRedirect); // verify if this is the right URL
    Swal.fire({
      title: "Eliminar registro",
      text: "Esta acción no se puede deshacer",
      icon: "warning",
      
      showCancelButton: true,
      cancelButtonText: "Cancelar",
      confirmButtonText: "Eliminar",
      allowOutsideClick: false
    })
    .then((result) => {
      // redirect with javascript here as per your logic after showing the alert using the urlToRedirect value
      if (result.isConfirmed) {          
        window.location.href = urlToRedirect;
      }
    });
  }
