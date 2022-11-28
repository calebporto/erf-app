function visualizarAttrData(id, item, itemData, itemTaxData) {
    const nome = document.querySelector('#item-nome'+ id +'')
    const preco = document.querySelector('#item-preco'+ id +'')
    const peso = document.querySelector('#item-peso'+ id +'')
    const ean = document.querySelector('#item-ean'+ id +'')
    const estoque = document.querySelector('#item-estoque'+ id +'')
    const custo = document.querySelector('#item-custo'+ id +'')
    const marca = document.querySelector('#item-marca'+ id +'')
    const categoria = document.querySelector('#item-categoria'+ id +'')
    const medida = document.querySelector('#item-medida'+ id +'')
    const ncm = document.querySelector('#item-ncm'+ id +'')
    const origem = document.querySelector('#item-origem'+ id +'')
    const desconto = document.querySelector('#item-desconto'+ id +'')
    const cest = document.querySelector('#item-cest'+ id +'')
    const divImagem = document.querySelector('#divVisualizarImagem'+ id)
    const imagem = document.querySelector('#visualizarImagem'+ id)


    nome.innerHTML = item.name != null ? (item.name).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase()) : null
    preco.innerHTML = item.price != null ? (item.price).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) : null
    peso.innerHTML = item.weight != null ? ((item.weight).toFixed(3)).replace('.', ',') + ' Kg' : null
    ean.innerHTML = item.ean
    estoque.innerHTML = item.inventory
    custo.innerHTML = itemData.cost != null ? (itemData.cost).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) : null
    marca.innerHTML = itemData.brand != null ? (itemData.brand).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase()) : null
    categoria.innerHTML = itemData.category != null ? (itemData.category).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase()) : null
    medida.innerHTML = itemTaxData.measure
    ncm.innerHTML = itemTaxData.ncm
    origem.innerHTML = itemTaxData.origin == 0 ? 'Nacional' : 'Importado'
    desconto.innerHTML = itemTaxData.discount != null ? itemTaxData.discount + '%' : null
    cest.innerHTML = itemTaxData.cest

    if (itemData.image_id != null) {
        imagem.src = '/static/media/produtos/'+ itemData.image_id
    } else {
        var notImage = document.createElement('p')
        var notImageText = document.createTextNode('O produto não tem imagem cadastrada.')
        notImage.appendChild(notImageText)
        divImagem.innerHTML = ''
        divImagem.appendChild(notImage)
    }
}
function visualizarDataLoad(value) {
    var id = parseInt(value)

    fetch('/painel-administrativo/produtos/get-item?id='+ id +'')
        .then(function(response) {
            return response.json()
        })
        .then(function(data) {
            visualizarAttrData(id, data.item, data.item_simple_data, data.item_tax_data)
        })
}

function editarAttrData(id, item,itemData, itemTaxData) {
    const nome = document.querySelector('#edit-nome'+ id)
    const preco = document.querySelector('#edit-preco'+ id)
    const peso = document.querySelector('#edit-peso'+ id)
    const ean = document.querySelector('#edit-ean'+ id)
    const estoque = document.querySelector('#edit-estoque'+ id)
    const custo = document.querySelector('#edit-custo'+ id)
    const marca = document.querySelector('#edit-marca'+ id)
    const categoria = document.querySelector('#edit-categoria'+ id)
    const ncm = document.querySelector('#edit-ncm'+ id)
    const desconto = document.querySelector('#edit-desconto'+ id)
    const cest = document.querySelector('#edit-cest'+ id)
    const imagemNome = document.querySelector('#imagem-nome'+ id)
    const imagem = document.querySelector('#imagem'+ id)
    const imagemDiv = document.querySelector('#imagemDiv'+ id)

    
    nome.value = item.name
    preco.value = ((item.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })).replace('R$', '')).replace(/\s/g, '')
    peso.value = ((item.weight).toFixed(3)).replace('.',',')
    ean.value = item.ean
    estoque.value = item.inventory
    custo.value = itemData.cost != null ? ((itemData.cost.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })).replace('R$', '')).replace(/\s/g, '') : null
    marca.value = itemData.brand
    categoria.value = itemData.category
    ncm.value = itemTaxData.ncm
    desconto.value = itemTaxData.discount
    cest.value = itemTaxData.cest
    imagemNome.value = itemData.image_id
    
    const editMedida = document.querySelector('#edit-medida-'+ id)
    const editOrigem = document.querySelector('#edit-origem-'+ id)

    // Pegando o elemento correspondente à medida para alterar o selected
    const optionMedida = document.querySelector('#option-medida-'+ itemTaxData.measure + id)
    const newOptionMedida = optionMedida
    // Alterando selected para true
    newOptionMedida.selected = true
    // Substituindo a opção normal pela opção com selected true
    editMedida.replaceChild(newOptionMedida, optionMedida)

    // Pegando o elemento correspondente a origem para alterar o selected
    const optionOrigem = document.querySelector('#option-origem-'+ itemTaxData.origin + id)
    const newOptionOrigem = optionOrigem
    // Alterando o selected para true
    newOptionOrigem.selected = true
    // Substituindo a opção normal pela opção com selected=true
    editOrigem.replaceChild(newOptionOrigem, optionOrigem)

    //Renderizando imagem do produto
    if (itemData.image_id != null) {
        imagemNome.value = itemData.image_id
        imagem.src = '/static/media/produtos/'+ itemData.image_id
    } else {
        var notImage = document.createElement('p')
        var notImageText = document.createTextNode('O produto não tem imagem cadastrada.')
        notImage.appendChild(notImageText)
        imagemDiv.replaceChild(notImage, imagem)
    }
}
function editarDataLoad(value) {
    var id = parseInt(value)

    fetch('/painel-administrativo/produtos/get-item?id='+ id +'')
        .then(function(response) {
            return response.json()
        })
        .then(function(data) {
            editarAttrData(id, data.item, data.item_simple_data, data.item_tax_data)
        })
}

$('#find-btn').on('click', function() {
    $('.table-list tr').remove()
    $('.table-list').append('<tr class="td-row-waiting"></tr>')
    $('.td-row-waiting').append('<div class="spinner-border text-warning" role="status"></div>')
    $('.spinner-border').append('<span class="visually-hidden">Loading...</span>')

    let arg = $('#find').val()

    window.location.href = "/painel-administrativo/produtos/lista-de-produtos?filter="+ arg;
})

$('#limpar-filtro').on('click', function() {
    window.location.href = "/painel-administrativo/produtos/lista-de-produtos";
})