$('#tipo-cliente').on('change', function(){
    $('#form-cadastro').each(function(){
        this.reset();
    });
    $('#formulario-button').css('display', 'flex')
    if ($(this).val() == 1) {
        // Minlenght default
        $('#sexo').attr({'required': true});
        $('#cpf').attr({'required': true, 'minlength': 14});
        $('#nome').attr({'required': true, 'minlength': 8});
        $('#nascimento').attr({'required': true, 'minlength': 10});
        $('#telefone').attr({'required': true, 'minlength': 14});
        $('#email').attr({'required': true, 'minlength': 10});
        $('#cep').attr({'required': true, 'minlength': 10});
        $('#logradouro').attr({'required': true, 'minlength': 2});
        $('#numero').attr({'required': true, 'minlength': 1});
        $('#bairro').attr({'required': true, 'minlength': 1});
        $('#cidade').attr({'required': true, 'minlength': 2});
        $('#uf').attr({'required': true, 'minlength': 2});
        // Escondendo form cnpj e exibindo form cpf
        $('#formulario-cnpj').css('display', 'none');
        $('#formulario-cpf').css('display', 'block');
        // minlength cnpj zerado
        $('#cnpj').attr({'required': false, 'minlength': 0});
        $('#nome-fantasia').attr({'required': false, 'minlength': 0});
        $('#razao-social').attr({'required': false, 'minlength': 0});
        $('#ie').attr({'required': false, 'minlength': 0});
        $('#telefone2').attr({'required': false, 'minlength': 0});
        $('#email2').attr({'required': false, 'minlength': 0});
        $('#cep2').attr({'required': false, 'minlength': 0});
        $('#logradouro2').attr({'required': false, 'minlength': 0});
        $('#numero2').attr({'required': false, 'minlength': 0});
        $('#bairro2').attr({'required': false, 'minlength': 0});
        $('#cidade2').attr({'required': false, 'minlength': 0});
        $('#uf2').attr({'required': false, 'minlength': 0});
    }
    else {
        // minlength cnpj default
        $('#cnpj').attr({'required': true, 'minlength': 18});
        $('#nome-fantasia').attr({'required': true, 'minlength': 6});
        $('#razao-social').attr({'required': true, 'minlength': 6});
        $('#ie').attr({'required': true, 'minlength': 9});
        $('#telefone2').attr({'required': true, 'minlength': 14});
        $('#email2').attr({'required': true, 'minlength': 12});
        $('#cep2').attr({'required': true, 'minlength': 10});
        $('#logradouro2').attr({'required': true, 'minlength': 4});
        $('#numero2').attr({'required': true, 'minlength': 1});
        $('#bairro2').attr({'required': true, 'minlength': 3});
        $('#cidade2').attr({'required': true, 'minlength': 1});
        $('#uf2').attr({'required': true, 'minlength': 2});
        // escondendo form cpf e exibindo form cnpj
        $('#formulario-cpf').css('display', 'none');
        $('#formulario-cnpj').css('display', 'block');
        // minlength cpf zerado
        $('#sexo1').attr({'required': false});
        $('#sexo2').attr({'required': false});
        $('#cpf').attr({'required': false, 'minlength': 0});
        $('#nome').attr({'required': false, 'minlength': 0});
        $('#nascimento').attr({'required': false, 'minlength': 0});
        $('#telefone').attr({'required': false, 'minlength': 0});
        $('#email').attr({'required': false, 'minlength': 0});
        $('#cep').attr({'required': false, 'minlength': 0});
        $('#logradouro').attr({'required': false, 'minlength': 0});
        $('#numero').attr({'required': false, 'minlength': 0});
        $('#bairro').attr({'required': false, 'minlength': 0});
        $('#cidade').attr({'required': false, 'minlength': 0});
        $('#uf').attr({'required': false, 'minlength': 0});
    }
})