from json import loads
from secrets import token_hex
from flask import Blueprint, flash, render_template, redirect, request
import os
from app.models.basemodels import Complete_Item_, Item_, Item_Simple_Data_, Item_Tax_Data_
from ....providers.functions import get_request, post_request, delete_request

ITEM_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/media/produtos')

produtos_bp = Blueprint(
    'produtos',
    __name__,
    url_prefix='/produtos',
    template_folder='templates',
    static_folder='/app/static'
)

@produtos_bp.route('/')
def produtos():
    return redirect('/painel-administrativo/produtos/lista-de-produtos')

@produtos_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_produtos():
    if request.method == 'POST':
        preco = float(((request.form.get('preco')).replace('.','')).replace(',', '.'))
        if (request.form.get('peso')).count(',') > 1:
            flash('Peso incorreto. Verifique os dados e tente novamente.')
            return redirect('/painel-administrativo/produtos/cadastrar')
        peso = float((request.form.get('peso')).replace(',', '.'))
        estoque = int(request.form.get('estoque'))
        custo = float(((request.form.get('custo')).replace('.','')).replace(',', '.')) if request.form.get('custo') else None
        desconto = int(request.form.get('desconto')) if request.form.get('desconto') else None
        brand = (request.form.get('marca')).lower() if request.form.get('marca') else None
        category = (request.form.get('categoria')).lower() if request.form.get('categoria') else None
        imagem = request.files.get('imagem')
        nome_imagem = None
        if imagem:
            nome_imagem = f'{token_hex(20)}.png'  # Criando o nome da imagem em um token hexadecimal
            file_path = os.path.join(ITEM_UPLOAD_FOLDER, nome_imagem)
            imagem.save(file_path)
        
        send = Complete_Item_(
            item=Item_(
                name=(request.form.get('nome')).lower(),
                price=preco,
                ean=request.form.get('ean'),
                weight=peso,
                inventory=estoque,
                is_active=True
            ),
            item_simple_data=Item_Simple_Data_(
                cost=custo,
                brand=brand,
                category=category,
                image_id=nome_imagem
            ),
            item_tax_data=Item_Tax_Data_(
                ncm=request.form.get('ncm'),
                measure=request.form.get('medida'),
                origin=request.form.get('origem'),
                discount=desconto,
                cest=request.form.get('cest'),
            )
        )
        response = post_request('/items-service/add-item', send.json())
        if response.status_code == 200:
            flash('Produto adicionado')
        elif response.status_code == 400:
            flash('Erro na requisição. Verifique os dados.')
        else:
            flash('Erro no servidor. Estamos trabalhando para corrigir.')
        return redirect('/painel-administrativo/produtos/cadastrar')
    else:
        return render_template('/cadastrar-produtos.html')

@produtos_bp.route('/lista-de-produtos', methods=['GET', 'POST'])
def lista_de_produtos():
    if request.method == 'POST':
        if request.form.get('type') == 'alterar':
            id = int(request.form.get('id'))
            nome = (request.form.get('nome')).lower() if request.form.get('nome') else None
            preco = request.form.get('preco') if request.form.get('preco') else None
            peso = request.form.get('peso') if request.form.get('peso') else None
            ean = request.form.get('ean') if request.form.get('ean') else None
            estoque = int(request.form.get('estoque')) if request.form.get('estoque') else None
            custo = request.form.get('custo') if request.form.get('custo') else None
            marca = (request.form.get('marca')).lower() if request.form.get('marca') else None
            categoria = (request.form.get('categoria')).lower() if request.form.get('categoria') else None
            ncm = request.form.get('ncm') if request.form.get('ncm') else None
            medida = request.form.get('medida') if request.form.get('medida') else None
            origem = int(request.form.get('origem')) if request.form.get('origem') else None
            desconto = float(request.form.get('desconto')) if request.form.get('desconto') else None
            cest = request.form.get('cest') if request.form.get('cest') else None

            preco = float((preco.replace('.','')).replace(',', '.')) if preco else None
            peso = float(peso.replace(',', '.')) if peso else None
            custo = float((custo.replace('.','')).replace(',', '.')) if custo else None

            imagem_nome = request.form.get('imagem_nome')
            imagem_file = request.files.get('imagem')
            if imagem_file:
                if imagem_nome:
                    os.remove(f'app/static/media/produtos/{imagem_nome}')
                    file_path = os.path.join(ITEM_UPLOAD_FOLDER, imagem_nome)
                    imagem_file.save(file_path)
                else:
                    imagem_nome = f'{token_hex(20)}.png'  # Criando o nome da imagem em um token hexadecimal
                    file_path = os.path.join(ITEM_UPLOAD_FOLDER, imagem_nome)
                    imagem_file.save(file_path)
            else:
                imagem_nome = None

            send = Complete_Item_(
                item=Item_(
                    id=id,
                    name=nome,
                    price=preco,
                    ean=ean,
                    weight=peso,
                    inventory=estoque
                ),
                item_simple_data=Item_Simple_Data_(
                    cost=custo,
                    brand=marca,
                    category=categoria,
                    image_id=imagem_nome
                ),
                item_tax_data=Item_Tax_Data_(
                    ncm=ncm,
                    measure=medida,
                    origin=origem,
                    discount=desconto,
                    cest=cest
                )
            )
            response = post_request('/items-service/update-item', send.json())
            if response.status_code == 200:
                flash('Dados alterados com sucesso.')
            
        elif request.form.get('type') == 'bloquear':
            id = int(request.form.get('id'))
            send = Complete_Item_(
                item=Item_(
                    id=id,
                    is_active=False
                ),
                item_simple_data=Item_Simple_Data_(),
                item_tax_data=Item_Tax_Data_()
            )
            response = post_request('/items-service/update-item', send.json())
            if response.status_code == 200:
                flash('Item bloqueado para venda.')

        elif request.form.get('type') == 'desbloquear':
            id = int(request.form.get('id'))
            send = Complete_Item_(
                item=Item_(
                    id=id,
                    is_active=True
                ),
                item_simple_data=Item_Simple_Data_(),
                item_tax_data=Item_Tax_Data_()
            )
            response = post_request('/items-service/update-item', send.json())
            if response.status_code == 200:
                flash('Item desbloqueado.')

        elif request.form.get('type') == 'excluir':
            id = int(request.form.get('id'))
            response = delete_request(f'/items-service/delete-item?id={id}')
            if response.status_code == 200:
                flash('Item excluído.')
        else:
            flash('Erro no servidor. Estamos trabalhando para corrigir')
        
        if response.status_code == 400:
            flash('Erro na requisição. Verifique os dados')
        elif response.status_code == 500:
            flash('Erro no servidor. Estamos trabalhando para corrigir')
        return redirect('/painel-administrativo/produtos/lista-de-produtos')

    else:
        if request.args.get('filter'):
            filter = request.args.get('filter')
            print(filter)
            response = get_request(f'/items-service/get-simple-item?type_data=name&name=%{filter}%')
            if response.status_code == 200:
                produtos = loads(response.text)
                for i, produto in enumerate(produtos):
                    data = Item_(**produto)
                    produtos[i] = data
                produtos_ordenados = sorted(produtos, key=lambda row:(row.name).lower())
                flash(f'Exibindo resultado para produtos que contenham "{filter}" no nome.')
                return render_template('/lista-de-produtos.html', produtos=produtos_ordenados)
            elif response.status_code == 400:
                flash('Erro na requisição. Verifique os dados')
            else:
                flash('Erro no servidor. Estamos trabalhando para corrigir.')


        response = get_request('/items-service/get-simple-item?type_data=all')
        if response.status_code == 200:
            produtos = loads(response.text)
            for i, produto in enumerate(produtos):
                data = Item_(**produto)
                produtos[i] = data
            produtos_ordenados = sorted(produtos, key=lambda row:(row.name).lower())
            flash('Exibindo resultado para todos os produtos.')
        elif response.status_code == 400:
            produtos_ordenados = []
            flash('Erro no servidor. Estamos trabalhando para corrigir.')
        else:
            produtos_ordenados = []
            flash('Erro no servidor. Estamos trabalhando para corrigir.')
        return render_template('/lista-de-produtos.html', produtos=produtos_ordenados)

# Endpoint para ajax
@produtos_bp.route('/get-item')
def get_item():
    id = int(request.args.get('id'))
    if id:
        response = get_request(f'/items-service/get-item?type_data=id&id={id}')
        if response.status_code == 200:
            item_response = loads(response.text)[0]
            item = Complete_Item_(
                item=Item_(**item_response['item']),
                item_simple_data=Item_Simple_Data_(**item_response['item_simple_data']),
                item_tax_data=Item_Tax_Data_(**item_response['item_tax_data'])
            )
            return item.json()
        else:
            pass
    else:
        pass