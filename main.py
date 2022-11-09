# importar a classe flask e o objeto request:
from flask import Flask, request, jsonify
from math import sqrt

# criar o objeto flask app:
app = Flask(__name__)

@app.route('/')
def cumprimentar():
    return 'ola, mundo'

@app.route('/testes/1')
def teste_GET_implicito():
    return jsonify({"resp": "Teste 1: método GET implicito."})

@app.route('/testes/2', methods=['GET'])
def teste_GET_explicito():
    return jsonify({"resp": "Teste 2: método GET explicito."})

@app.route('/testes/3', methods=['POST'])
def teste_POST():
    return jsonify({"resp": "Teste 3: método POST."})

@app.route('/testes/4', methods=['GET', 'POST'])
def teste_GET_POST():
    return jsonify({"resp": "Teste 4: método GET ou POST."})

# http://127.0.0.1:5000/testes/1?linguagem=Python
@app.route("/testes/5")
def teste_query_string_1_argumento_get():
    lang = request.args.get('linguagem')
    return '''<h1>Linguagem informada: {}</h1>'''.format(lang)

# http://127.0.0.1:5000/testes/2?linguagem=Python&framework=Flask
@app.route("/testes/6")
def teste_query_string_2_argumentos_get():
    lang = request.args.get('linguagem')
    framework = request.args.get('framework')
    return '''<h1>Linguagem informada: {}</h1>
              <h1>Framework informado: {}</h1>'''.format(lang, framework)

# http://127.0.0.1:5000/testes/3?linguagem=Python&framework=Flask
@app.route("/testes/6")
def teste_query_string_2_argumentos_vetor():
    lang = request.args['linguagem']
    framework = request.args['framework']
    return '''<h1>Linguagem informada: {}</h1>
              <h1>Framework informado: {}</h1>'''.format(lang, framework)

# http://127.0.0.1:5000/calcula/temperatura?celsius=27
@app.route('/calcula/temperatura')
def calcula_temp_celsius_fahrenheit():
    celsius = float(request.args['celsius'])
    fahrenheit = (celsius * 1.8) + 32
    return '''<h1> A temperatura informada em celsius de {}°
     equivale a {} fahrenheit'''.format(celsius, fahrenheit)

# http://127.0.0.1:5000/calcula/media?nota1=8&nota2=3&nota3=10
@app.route('/calcula/media')
def calcula_media_das_notas():
    nota1 = float(request.args['nota1'])
    nota2 = float(request.args['nota2'])
    nota3 = float(request.args['nota3'])
    media = (nota1 + nota2 + nota3) / 3
    if media >= 0 and  media <= 3: msg = 'REPROVADO'
    if media >= 3 and media < 7: msg = 'EXAME'
    if media >= 7 and media <= 10: msg = 'APROVADO'
    return '''<h1> As notas {}, {} e {}, tem média de {}</h1>
    <h2> O resultado do aluno ficou como {}.</h2>'''.format(nota1, nota2, nota3, media, msg)


# Aceita requisições com os métodos GET e POST.
# GET: gera um formulário em HTML para o usuário enviar dados para o servidor.
# POST: lê os dados enviados pelo usuário através do furmulário HTML.

# http://127.0.0.1:5000/forms/1
@app.route('/forms/1', methods=['GET', 'POST'])
def teste_dados_form_html():
    # trata a requisição com método POST:
    if request.method == 'POST':
        lang = request.form.get('lang')
        frame = request.form.get('frame')
        # ou:
        # lang = request.form['lang']
        # frame = request.form['frame']
        return '''
        <h1>Linguagem informada: {}</h1>
        <h1>Framework informado: {}</h1>'''.format(lang, frame)
    
    # caso contrario, trata a requisição como método GET:
    return '''
        <form method="POST">
            <div>
                <label>Linguagem: <input type="text" name="lang"></label>
            </div>
            <div>
                <label>Framework: <input type="text" name="frame"></label>
            </div>
            <input type="submit" value="enviar"
        </form>
        '''

# ----------- ERR0 ---------------------------------------------
# http://127.0.0.1:5000/forms/2
@app.route('/forms/2', methods=['GET', 'POST'])
def testes_dados_form_html_numeros():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        num3 = float(request.form['num3'])
        minimo = min([num1, num2, num3])
        maximo = max([num1, num2, num3])
        media = (num1 + num2 + num3)/3
        return '''
            <h1>Os numeros {}, {}, e {} tem média {}</h1>
            <h1>O menor foi {} e o maior foi {}</h1>'''.format(num1, num2, num3, media, minimo, maximo)
    return '''
    <form method="POST">
        <div>
            <label>Numero 1: <input type="number" name="num1"></label>
        </div>
        <div>
            <label>Numero 2: <input type="number" name="num2"></label>
        </div>
        <div>
            <label>Numero 3: <input type="number" name="num3"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''

# http://127.0.0.1:5000/forms/3
@app.route('/forms/3', methods=['GET', 'POST'])
def teste_dados_formulario_html_imc():
    if request.method == 'POST':    
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = peso / (altura ** 2)
        if imc <= 18.5: msg = 'Abaixo do peso'
        if imc >= 18.6 and imc <= 24.9: msg = 'Peso ideal (parabéns)'
        if imc >= 25.0 and imc <= 29.9: msg = 'Levemente acima do peso'
        if imc >= 30.0 and imc <= 34.9: msg = 'Obesidade grau I'
        if imc >= 35.0 and imc <= 39.9: msg = 'Obesidade grau II (severa)'
        if imc >= 40.0: msg = 'Obesidade grau III (mórbida)'
        return '''
            <h1> O indivisuo possui {}Kg e mede {}m</h1>
            <h1>O seu IMC foi de {} {}</h1>'''.format(peso, altura, imc, msg)
    return '''
    <form method="POST">
        <div>
            <label>Peso em Kg: <input type="text" name="peso"></label>
        </div>
        <div>
            <label>Altura em m: <input type="text" name="altura"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''



if __name__ == "__main__":
# executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)
