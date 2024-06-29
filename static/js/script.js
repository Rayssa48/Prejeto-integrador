 // Selecione o elemento do checkbox
 var checkbox = document.getElementById('destaque');

 // Adicione um ouvinte de evento para capturar o envio do formulário
 document.querySelector('form').addEventListener('submit', function() {
     // Verifique se o checkbox está marcado
     if (!checkbox.checked) {
         // Se não estiver marcado, defina o valor do campo 'destaque' como 'false'
         var hiddenInput = document.createElement('input');
         hiddenInput.type = 'hidden';
         hiddenInput.name = 'destaque';
         hiddenInput.value = 'false';
         this.appendChild(hiddenInput); // Adicione o input hidden ao formulário
     }
 });

 function previewImage(event) {
  var reader = new FileReader();
  reader.onload = function () {
      var preview = document.getElementById('preview');
      preview.src = reader.result;
      preview.classList.remove('d-none');
  };
  reader.readAsDataURL(event.target.files[0]);
};