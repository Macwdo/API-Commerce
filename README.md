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
    <li> /usuarios/cargos/{id}/{cargo} <b>GET</b>  - Adiciona cargo ao ID indicado
    <li> /usuarios/cargos/{id}/{cargo} <b>DELETE</b> -
    Retira o cargo do usuário com ID indicado

</ul>


<h3>
    Usuários
</h3>

<ul>
    <li> /usuarios/admin <b>GET</b> - Retorna dados de todos os <b>Usuário</b> e suas informações de <b>Pedidos</b> e <b>Produtos</b> . <br>
    <li> /usuarios/admin/{id} <b>GET</b> - Retorna dados do <b>Usuário</b> referente ao id e suas informações de <b>Pedidos</b>  e <b>Produtos</b> . <br>
    <b>Obs:</b> Endpoint feito apenas para <b>Admins</b>
    <hr>
    <li> /usuarios/ <b>GET</b> - Retorna dados de todos os <b>Usuário</b>. Exceto suas informações de pedidos e vendas .
    <li> /usuarios/{id}/ <b>GET</b> - Retorna dados do <b>Usuário</b> referente ao Id
    <li> /usuarios/ <b>POST</b> - Cria um <b>Usuário</b> (Email e Username são unicos)
    <li> /usuarios/{id}/ <b>PATCH</b> - Atualiza parcialmente os dados do <b>Usuário</b>. Necessita da autenticação do  <b>Usuário</b> logado ou de um <b>Admin</b> do Sistema
    <li> /usuarios/{id}/ <b>DELETE</b> - Apaga os dados do <b>Usuário</b> referente ao Id . Somente <b> Admin</b> apaga dados de outros  <b>Usuários</b>. <br>
    <b>Obs</b>: o <b>Admin</b> logado não consegue apagar o seu <b>Usuário</b> , somente outro <b>Admin</b>.
</ul>

<h3>
Produtos
</h3>
<p>
    Os <b>Produtos</b> poderão ser comprados , se tornando assim um <b> Pedido.</b> Necessita o <b>Usuário </b>estar autenticado para requisição de seus respectivos endpoints. Para criar um produto necessita do cargo <b>Vendedor</b>.
</p>
</p>
<ul>
    <li> /usuarios/produtos <b>GET</b>  - Retorna dados de todos os <b>Produtos</b> 
    <li> /usuarios/produtos/{id} <b>GET</b>  - Retorna dados do <b>Produtos</b>  referente ao id
    <li> /usuarios/produtos <b>POST</b>  - Cria um novo <b>Produto</b> . Necessita o <b>Usuário</b> estar autenticado e que tenha o cargo de vendedor
    <li> /usuarios/patch/{id} <b>PATCH</b> - Atualiza parcialmente os dados do <b>Produto</b>. Necessita da autenticação do  <b>Usuário</b> que criou o <b>Produto</b> ou de um <b>Admin</b> do Sistema
    <li> /usuarios/produtos/{id}/ <b>Delete</b> - Apaga os dados do <b>Produto</b> referente ao Id
    <b>Obs</b>: Somente o Criador do <b> Produto </b> ou <b>Admin</b> consegue apagar.
</ul>

<h3>
Pedidos
</h3>
<p>
    Os <b>Pedidos</b> são solicitações feitas pelo <b>Usuário</b> com o cargo de <b>Comprador</b> a um determinado <b>Produto</b>. O criador precisa fazer a confirmação da entrega desse <b> Pedido</b>. Necessita estar autenticado para requisição de seus respectivos endpoints e com o cargo <b>Comprador</b> para fazer a solicitação de um  <b>Pedido</b>.
</p>

<ul>
    <li> /usuarios/pedidos <b>GET</b>  - Retorna dados de todos os <b>Pedidos</b> referente ao <b>Usuário</b> autenticado.
    <li> /usuarios/pedidos/{id} <b>GET</b>  -Retorna dados do <b>Pedidos</b> referente ao id indicado , caso pertença ao <b>Usuário</b> autenticado.
    <li> /usuarios/pedidos <b>POST</b>  - Cria um novo <b>Pedido</b> . Necessita o <b>Usuário</b> estar autenticado e que tenha o cargo de <b>Comprador</b>
    <li> /usuarios/pedidos/{id} <b>PATCH</b> - Atualiza parcialmente os dados do <b>Pedido</b>. caso ele não tenha sido entregue. Necessita da autenticação do  <b>Usuário</b> que criou o <b>Pedido</b> ou de um <b>Admin</b> do Sistema
    <li>usuarios/pedidos/atualizar/{id} <b>GET</b> - Faz a confirmação da entrega do <b> Pedido </b>. Necessita estar autenticado como o <b>Vendedor</b> e criador do <b>Pedido</b> ou <b>Admin</b> do sistema.
    <li> /usuarios/produtos/{id}/ <b>Delete</b> - Apaga os dados do <b>Pedido</b> referente ao Id caso o <b> Pedido </b> tenha sido entregue.
    <br><b>Obs</b>: Somente o <b>Usuario</b> que fez a solicitação do <b> Pedido </b> ou <b>Admin</b> consegue apagar.


</ul>