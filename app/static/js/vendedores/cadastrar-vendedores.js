function enviarIdVendedor(id, personTypeList) {
    window.location.href = '/painel-administrativo/vendedores/cadastrar?setPersonToSeller='+ id+'&persontype='+personTypeList
}

var enviarFormulario = document.querySelector('#form-submit-btn');

enviarFormulario.addEventListener('click', function(event) {
    var cpf = document.querySelector('#cpf');
    var form = document.querySelector('#cadastrar-form');
    if (cpf.value.length != 14){
        alert('Preencha o CPF corretamente.')
    } else {
        fetch('/painel-administrativo/vendedores/cpf-exists?cpf='+ cpf.value)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.length > 0) {
                event.preventDefault()
                
                var divForm = document.querySelector('#formulario-cpf')
                
                form.removeChild(divForm);
    
                var name = ((data[0]).person.name).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase());
    
                // Div incluir vendedor de cpf existente
                var newDivForm = document.createElement('div');
                newDivForm.className = 'formulario';
                newDivForm.id = 'formulario-confirmar';
    
                // Criando título
                var newDivTitle = document.createElement('p');
                newDivTitle.className = 'new-form-title';
                newDivTitle.textContent = 'Já existe cadastro com esse CPF. Deseja incluir '+ name +' como vendedor?';
                
                // Criando botões
                var divButtons = document.createElement('div');
                divButtons.className = 'formulario-button';
    
                var simBtn = document.createElement('button');
                simBtn.className = 'confirm-btn form-button';
                simBtn.textContent = 'Sim';
                simBtn.id = 'sim-btn';
                simBtn.type = 'button'
                simBtn.value = (data[0]).person.id;
                simBtn.addEventListener('click', function() {
                    enviarIdVendedor((data[0]).person.id, (data[0]).person.persontype);
                });
                
                var naoBtn = document.createElement('button');
                naoBtn.className = 'dismiss-btn form-button';
                naoBtn.textContent = 'Não';
                naoBtn.id = 'nao-btn';
                naoBtn.type = 'button'
                naoBtn.addEventListener('click', function() {
                    window.location.href = '/painel-administrativo/vendedores/cadastrar'
                })
    
                divButtons.appendChild(naoBtn);
                divButtons.appendChild(simBtn);
    
                newDivForm.appendChild(newDivTitle);
                newDivForm.appendChild(divButtons);
                form.appendChild(newDivForm);
    
            } else {
                var sexo = document.getElementsByName('sexo')
                if (sexo[0].checked == false && sexo[1].checked == false ) {
                    alert('Selecione o sexo.')
                    return
                }
                var nome = document.querySelector('#nome').value
                if (nome.length < 8 || nome.length > 50){
                    alert('O nome deve ter entre 8 e 50 caracteres')
                    return
                }
                var nascimento = document.querySelector('#nascimento').value
                var dateNow = new Date()
                var ano = dateNow.getFullYear()
                if (nascimento.length != 10){
                    alert('Preencha a data de nascimento corretamente.')
                    return
                } else if (parseInt(nascimento.slice(0,2)) > 31) {
                    alert('Dia de nascimento inválido.')
                    return
                } else if (parseInt(nascimento.slice(3,5)) > 12) {
                    alert('Mês de nascimento inválido.')
                    return
                } else if (parseInt(nascimento.slice(6,10)) < 1900 || parseInt(nascimento.slice(6,10)) > ano) {
                    alert('Ano de nascimento inválido.')
                    return
                } else if (parseInt(nascimento.slice(3,5)) == 2 && parseInt(nascimento.slice(0,2)) > 29) {
                    alert('Dia de nascimento inválido.')
                    return
                }
                var telefone = document.querySelector('#telefone').value
                if (telefone.length < 14 || telefone.length > 15){
                    alert('Preencha o telefone corretamente.')
                    return
                }
                var email = document.querySelector('#email').value
                if (email.length < 10 || email.length > 50 || email.indexOf('@') == -1){
                    alert('Preencha o e-mail corretamente')
                    return
                }
                var cep = document.querySelector('#cep').value
                if (cep.length != 10){
                    alert('Preencha o CEP corretamente')
                    return
                }
                var logradouro = document.querySelector('#logradouro').value
                if (logradouro.length < 2 || logradouro.length > 50){
                    alert('O logradouro deve ter entre 2 e 50 caracteres')
                    return
                }
                var numero = document.querySelector('#numero').value
                if (numero.length < 1 || numero.length > 5){
                    alert('O número deve ter entre 1 e 5 caracteres. Caso não tenha número, use o número 0.')
                    return
                }
                var bairro = document.querySelector('#bairro').value
                if (bairro.length < 2 || bairro.length > 50){
                    alert('O bairro deve ter entre 2 e 50 caracteres')
                    return
                }
                var complemento = document.querySelector('#complemento').value
                if (complemento.length > 50){
                    alert('O complemento deve ter entre no máximo 50 caracteres')
                    return
                }
                var cidade = document.querySelector('#cidade').value
                if (cidade.length < 2 || cidade.length > 50){
                    alert('A cidade deve ter entre 2 e 50 caracteres')
                    return
                }
                var uf = document.querySelector('#uf').value
                if (uf.length != 2){
                    alert('Preencha o UF corretamente.')
                    return
                }
                form.submit()
            }
        })
    }
});