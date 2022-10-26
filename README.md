<h1>
    Simples API com FastAPI-Python</h1>
<p>
    Api criada com o framework python FastAPI, com principio de consolidar meus conhecimentos.
</p>
<hr>
<h5>
    Crie e ative sua Venv no python e rode o comando pip install -r requirements.txt para instalar as dependências da aplicação, com a venv ativada rode o comando uvicorn app:app para rodar api.
</h5>
<hr>
<p>A API contém <b>Usuários - Produtos - Pedidos</b>
</p>


<h3>
Autenticação
</h3>

<ul>
    <li> /auth/token/ POST - Autentica o Usuário, Caso autenticado retorna seu Token de acesso (JWT)
    <li> /auth/me/ GET - Retorna os dados do Usuário logado
</ul>

<h3>
    Cargos
</h3>
<p>
    <b>Admin - Vendedor - Comprador</b>
</p>
<p> Só adiciona e retira cargo a outros usuários somente quem tem a permissão de <b> Admin</b>.
<p>
o <b>Admin</b> não consegue retirar o seu próprio cargo de <b>Admin</b>.
</p>
<ul>
    <li> /usuarios/cargos/{id}/{cargo} GET - Adiciona cargo ao ID indicado
    <li> /usuarios/cargos/{id}/{cargo} DELETE -
    Retira o cargo do usuário com ID indicado

</ul>


<h3>
    Usuários
</h3>

<ul>
    <li> /usuarios/ GET - Retorna dados de todos os Usuários
    <li> /usuarios/ POST - Cria um Usuário (Email e Username são unicos)
    <li> /usuarios/{id}/ GET - Retorna dados do Usuário referente ao Id
    <li> /usuarios/{id}/ PATCH - Atualiza parcialmente os dados do usuário. Necessita da autenticação do usuário logado ou de um <b>Admin</b> do Sistema
    <li> /usuarios/{id}/ DELETE - Apaga os dados do Usuário referente ao Id . Somente <b> Admin</b> apaga dados de outros usuários. <br>
    <b>Obs</b>: o <b>Admin</b> logado não consegue apagar o seu usuário , somente outro <b>Admin</b>.
</ul>

<h3>
Produtos
</h3>
<p>
    Os produtos poderão ser comprados , se tornando assim um <b> Pedido.</b> Necessita o <b>Usuário </b>estar autenticado para requisição de seus respectivos endpoints.
</p>
<ul>
    <li> /usuarios/produtos GET - Retorna dados de todos os Produtos
    <li> /usuarios/produtos POST - Cria um novo produto.
</ul>