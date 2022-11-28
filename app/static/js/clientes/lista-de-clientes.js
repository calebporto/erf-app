function visualizarAttrData(id, doctype, person, personData) {
    const nome = document.querySelector('#person-name'+ id +'')
    const cnpjCpf = document.querySelector('#person-cnpj-cpf'+ id +'')
    const razaoSocial = document.querySelector('#person-r-social'+ id +'')
    const ie = document.querySelector('#person-ie'+ id +'')
    const email = document.querySelector('#person-email'+ id +'')
    const tel = document.querySelector('#person-tel'+ id +'')
    const cep = document.querySelector('#person-cep'+ id +'')
    const logradouro = document.querySelector('#person-logradouro'+ id +'')
    const numero = document.querySelector('#person-num'+ id +'')
    const bairro = document.querySelector('#person-bairro'+ id +'')
    const complemento = document.querySelector('#person-complemento'+ id +'')
    const cidade = document.querySelector('#person-cidade'+ id +'')
    const uf = document.querySelector('#person-uf'+ id +'')

    nome.innerHTML = person.name
    email.innerHTML = person.email
    tel.innerHTML = personData.tel
    cep.innerHTML = personData.cep
    logradouro.innerHTML = personData.public_place
    numero.innerHTML = personData.place_number
    bairro.innerHTML = personData.district
    complemento.innerHTML = personData.complement
    cidade.innerHTML = personData.city
    uf.innerHTML = personData.uf
    if (doctype == 1) {
        cnpjCpf.innerHTML = personData.cpf
        razaoSocial.innerHTML = ''
        ie.innerHTML = ''
    } else if (doctype == 2) {
        cnpjCpf.innerHTML = personData.cnpj
        razaoSocial.innerHTML = personData.cp_name
        ie.innerHTML = personData.ie
    }
}

function editarAttrData(id, doctype, person, personData) {
    const nome = document.querySelector('#edit-nome'+ id +'')
    const nascimento = document.querySelector('#edit-nasc'+ id +'')
    const cpf = document.querySelector('#edit-cpf'+ id +'')
    const masculino = document.querySelector('#edit-sexo-m'+ id +'')
    const feminino = document.querySelector('#edit-sexo-f'+ id +'')
    const nomeFantasia = document.querySelector('#edit-nome-fantasia'+ id +'')
    const razaoSocial = document.querySelector('#edit-razao-social'+ id +'')
    const cnpj = document.querySelector('#edit-cnpj'+ id +'')
    const ie = document.querySelector('#edit-ie'+ id +'')
    const email = document.querySelector('#edit-email'+ id +'')
    const tel = document.querySelector('#edit-telefone'+ id +'')
    const cep = document.querySelector('#edit-cep'+ id +'')
    const logradouro = document.querySelector('#edit-logradouro'+ id +'')
    const numero = document.querySelector('#edit-numero'+ id +'')
    const complemento = document.querySelector('#edit-complemento'+ id +'')
    const bairro = document.querySelector('#edit-bairro'+ id +'')
    const cidade = document.querySelector('#edit-cidade'+ id +'')
    const uf = document.querySelector('#edit-uf'+ id +'')

    email.value = person.email
    tel.value = personData.tel
    cep.value = personData.cep
    logradouro.value = personData.public_place
    numero.value = personData.place_number
    bairro.value = personData.district
    complemento.value = personData.complement
    cidade.value = personData.city
    uf.value = personData.uf
    if (doctype == 1) {
        nome.value = person.name
        cpf.value = personData.cpf
        nascimento.value = personData.birth
        if (personData.gender == 'masculino' || personData.gender == 'm') {
            masculino.checked = true;
        } else {
            feminino.checked = true;
        }
    } else if (doctype == 2) {
        if (personData.ie == 'null') {
            ie.value = ''
        } else {
            ie.value = personData.ie
        }
        nomeFantasia.value = person.name
        cnpj.value = personData.cnpj
        razaoSocial.value = personData.cp_name
    }
}


function visualizarDataLoad(value) {
    var doctype = parseInt((document.querySelector('#doctype'+ value +'')).value)
    var id = parseInt(value)
    
    if (doctype == 1) {
        fetch('/painel-administrativo/clientes/get-person?filter=pf&arg='+ id +'')
            .then(function(response) {
                return response.json()
            })
            .then(function(data) {
                visualizarAttrData(id, doctype, data.new_person, data.new_person_data)
            })
    } else {
        fetch('/painel-administrativo/clientes/get-person?filter=pj&arg='+ id +'')
            .then(function(response) {
                return response.json()
            })
            .then(function(data) {
                visualizarAttrData(id, doctype, data.new_person, data.new_person_data)
            })
    }
}

function editarDataLoad(value) {
    var doctype = parseInt((document.querySelector('#doctype'+ value +'')).value)
    var id = parseInt(value)
    
    if (doctype == 1) {
        fetch('/painel-administrativo/clientes/get-person?filter=pf&arg='+ id +'')
            .then(function(response) {
                return response.json()
            })
            .then(function(data) {
                editarAttrData(id, doctype, data.new_person, data.new_person_data)
            })
    } else {
        fetch('/painel-administrativo/clientes/get-person?filter=pj&arg='+ id +'')
            .then(function(response) {
                return response.json()
            })
            .then(function(data) {
                editarAttrData(id, doctype, data.new_person, data.new_person_data)
            })
    }
}

$('#find-btn').on('click', function() {
    $('.table-list tr').remove()
    $('.table-list').append('<tr class="td-row-waiting"></tr>')
    $('.td-row-waiting').append('<div class="spinner-border text-warning" role="status"></div>')
    $('.spinner-border').append('<span class="visually-hidden">Loading...</span>')

    let arg = $('#find').val()

    window.location.href = "/painel-administrativo/clientes/lista-de-clientes?filter=nome&arg="+ arg +"";
})

$('#limpar-filtro').on('click', function() {
    window.location.href = "/painel-administrativo/clientes/lista-de-clientes";
})
