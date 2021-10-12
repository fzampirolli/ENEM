/*
=====================================================================
Copyright (C) 2021 UFABC, developed by Francisco de Assis Zampirolli
from Federal University of ABC and individual contributors.
All rights reserved.

This file is part of "ENEM Interativo".

Languages: Python 3.8.5, Javascript, HTML and many libraries
described at github.com/fzampirolli/ENEM

You should cite some references included in vision.ufabc.edu.br
in any publication about it.

ENEM Interativo is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License
(gnu.org/licenses/agpl-3.0.txt) as published by the Free Software
Foundation, either version 3 of the License, or (at your option)
any later version.

ENEM Interativo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
=====================================================================
 */

// run localhost with python3 -m http.server --cgi 8080

var questionElement, letras, ANO, COR, AREAS, TIPOS, AnswersStudent, questionsStr, TAM, question, questions = [],
  relatorios = "", CODIGOS,
  choice, flagCookie = 1,
  choices;

// número de zeros a esquerda
Number.prototype.pad = function (size) {
  let s = String(this);
  while (s.length < (size || 2)) {
    s = "0" + s;
  }
  return s;
}

var dadosJSON = ""

function deleteAllCookies() {
  var c = document.cookie.split("; ");
  for (i in c)
    document.cookie = /^[^=]+/.exec(c[i])[0] + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
}

function loadJSON(prova) {
  TIPOS = prova.split("_")
  COR = TIPOS[7];
  AREAS = TIPOS.slice(8, 10);
  CODIGOS = TIPOS.slice(10, 12);
  ANO = TIPOS[1];

  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "../DADOS/ITENS_PROVA_" + ANO + ".json", false);
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      dadosJSON = String(this.responseText);
    }
  };
  xhttp.send();

  if (document.cookie.length != 0) {
    mystr = document.cookie;
    //alert(mystr)
    myarray = mystr.split(',');
    if (TIPOS.join() == myarray.slice(0, TIPOS.length).join()) {
      AnswersStudent = myarray.slice(TIPOS.length, myarray.indexOf('='));
      flagCookie = 0;
      //alert(AnswersStudent.length)
    } else {
      flagCookie = 1;
      deleteAllCookies();
    }
  }
}

function initializationVariables(prova) {
  TIPOS = prova.split("_")
  COR = TIPOS[7];
  AREAS = TIPOS.slice(8, 10);
  CODIGOS = TIPOS.slice(10, 12);

  [questions, relatorios] = parseGAB()

  TAM = questions.length;

  questionsStr = new Array(TAM);
  if (AREAS.includes('LC')) {
    for (let i = 0; i < 5; i++) { // for LC
      questionsStr[i] = "question" + String(i + 1)  // question1, question2, ..., question5
    }
    for (let i = 5; i < TAM; i++) {
      questionsStr[i] = "question" + (i - 4).pad(2, 1) // question01, question02, ...
    }
  } else {
    for (let i = 90; i < 90 + TAM; i++) {
      questionsStr[i] = "question" + String(i + 1) // question91, question92, ...
    }
  }

  letras = ['A', 'B', 'C', 'D', 'E']
  if (flagCookie) {
    AnswersStudent = new Array(TAM);
  }
}

function get(x) {
  return document.getElementById(x);
}

function renderQuestion(pos0, flag_LC) {
  let data = ""
  questionElement = get(questionsStr[pos0]);
  let pos2 = pos0;
  let idSTR = ""
  if (flag_LC) {
    if (pos0 < 5) {
      idSTR += String(pos0 + 1)
    } else {
      idSTR += (pos0 + 1).pad(2, 1)
    }
  } else {
    idSTR += String(pos0 + 1)
    pos2 = pos0 - 90
  }
  question = questions[pos2].question

  data = "<form id=" + idSTR + " style='color:black; position: absolute; top: -10px; left: 0px; font-size: 30px; background-color: lightgreen; width: 1000px; height: 68px;'>" +
    "<table style='position: absolute; top: 12px; left: 10px;'>" +
    "<thead>" +
    "<tr>" +
    "<th> Questão " + question + "   </th>"
  for (let i = 0; i < letras.length; i++) {
    if (AnswersStudent[pos2] == letras[i]) {
      data +=
        "<th><INPUT style='transform: scale(2);' TYPE='RADIO' NAME='choices" + idSTR + "' VALUE=" + letras[i] + " checked> " + letras[i] + " </th>"
    } else {
      data +=
        "<th><INPUT style='transform: scale(2);' TYPE='RADIO' NAME='choices" + idSTR + "' VALUE=" + letras[i] + "> " + letras[i] + " </th>"
    }
  }
  data += "<th>   <input id=" + idSTR + " type='submit' value='Salvar Sempre' onclick='checkAnswer(this.id)' style='font-size : 25px; width: 200px; height: 42px; background-color: lightblue;'/></th>"
  //data += "<th>   <input id=" + idSTR + " type='submit' value='Estatísticas' onclick='checkStatistcs(this.id)' style='font-size : 25px; width: 160px; height: 42px; background-color: lightblue;'/></th>";

  if (flag_LC) {
    data += "<th>     " + (pos2 + 1) + "/" + (questions.length - 5) + "</th></tr></thead></table></form>";
  } else {
    data += "<th>     " + (pos2 + 1) + "/" + questions.length + "</th></tr></thead></table></form>";
  }

  questionElement.innerHTML = data;
}

function renderQuestions() {
  let elmnt = document.getElementsByTagName("body")[0];
  let prova = elmnt.getAttributeNode('id').value;

  initializationVariables(prova)

  for (let i = 0; i < TAM; i++) {
    if (AREAS.includes('LC')) {
      renderQuestion(i, AREAS.includes('LC'));
    } else {
      renderQuestion(i + 90, AREAS.includes('LC'));
    }
  }
}

function checkAnswer(pos0) {
  choices = document.getElementsByName("choices" + pos0);
  choice = ''
  for (let i = 0; i < choices.length; i++) {
    if (choices[i].checked) {
      choice = choices[i].value;
      break;
    }
  }
  if (AREAS.includes('LC')) {
    AnswersStudent[parseInt(pos0) - 1] = choice
  } else {
    AnswersStudent[parseInt(pos0) - 90 - 1] = choice
  }

  document.cookie = TIPOS.join() + ',' + AnswersStudent.join() + ',';

  renderQuestion(parseInt(pos0) - 1, AREAS.includes('LC'));
}

function GetSortOrder(prop) {   // sort array by prop
  return function (a, b) {
    if (a[prop] > b[prop]) {
      return 1;
    } else if (a[prop] < b[prop]) {
      return -1;
    }
    return 0;
  }
}

function parseGAB() {
  let out = "q; correto; marcado; acertos; irt; gráficos; vídeos; subárea<br>";
  out += "acertos e irt são estatísticas das respostas realizadas no ENEM<br>";
  P = TIPOS[2]
  CAD = TIPOS[4]
  DIA = TIPOS[6]
  out += "<p>prova" + P + "; CAD" + CAD + "; DIA " + DIA + ";" + COR + ";" + AREAS + "</p>"

  //const range = (min, max) => Array.from({length: max - min + 1}, (_, i) => min + i);
  //tiposProvas = range(503, 518);

  CODIGOS = TIPOS.slice(10, 12);

  let obj;
  //console.log(dadosJSON)
  obj = JSON.parse(dadosJSON)

  questions = [];
  let questions0 = [];
  let typeC = typeof obj
  if (typeC = "object") {
    //for (let t in obj) {
    //out += "<br>COR: " + COR
    for (CODIGO in CODIGOS) {
      out += '\n\n' + CODIGOS[CODIGO] + '\n'
      let cod = obj[CODIGOS[CODIGO]];
      let typeC = typeof cod;
      if (typeC = "object") {
        out += '\n\n' + cod['COR'] + '; ' + cod['AREA'] + '\n';
        let a = AREAS.indexOf(cod['AREA'])
        let questoes = cod['QUESTIONS'];
        let typeQ = typeof questoes
        if (typeQ = "object") {
          for (let q in questoes) {
            if (cod['AREA'] == 'LC') { // trata numero da questao
              if (q.length == 1) {
                out += q + ','
                questions0.push({
                  question: "" + q,
                  answer: questoes[q]["answer"],
                  ability: questoes[q]["ability"],
                  images: questoes[q]["images"]
                })
              } else {
                questions.push({
                  question: "" + q,
                  answer: questoes[q]["answer"],
                  ability: questoes[q]["ability"],
                  images: questoes[q]["images"]
                })
              }
            } else if (cod['AREA'] == 'CH') {
              let qSTR = String(45 + parseInt(q))
              questions.push({
                question: "" + qSTR,
                answer: questoes[q]["answer"],
                ability: questoes[q]["ability"],
                images: questoes[q]["images"]
              })
            } else if (!('LC' in AREAS)) {
              let qSTR = String(90 + a * 45 + parseInt(q))
              questions.push({
                question: "" + qSTR,
                answer: questoes[q]["answer"],
                ability: questoes[q]["ability"],
                images: questoes[q]["images"]
              })
            }
          }
        }
      }
    }
  }
  if (AREAS.includes('LC')) {
    questions = questions.sort(GetSortOrder("question"));
    if (questions0.length) {
      questions = questions0.concat(questions);
    }
  } else {
    questions = questions.sort(GetSortOrder("question"));
    questions = questions.slice(81, 90).concat(questions.slice(0, 81));
  }

  return [questions, out];
}

function checkStatistcs(pos0) {
  let w = window.open('', '', 'width=450,height=800,resizeable,scrollbars');
  let report = ""

  let myFlag = false
  if ((parseInt(CODIGOS[0]) >= 503 && parseInt(CODIGOS[0]) <= 518) || (parseInt(CODIGOS[1]) >= 503 && parseInt(CODIGOS[1]) <= 518)) {
    myFlag = true
  }

  report += ' <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>\n' +
    '    <script type="text/javascript">\n' +
    '        $("#btnPrint").live("click", function () {\n' +
    '            var divContents = $("#dvContainer").html();\n' +
    '            var printWindow = window.open(\'\', \'\', \'height=400,width=800\');\n' +
    '            printWindow.document.write(\'<html><head><title>DIV Contents</title>\');\n' +
    '            printWindow.document.write(\'</head><body >\');\n' +
    '            printWindow.document.write(divContents);\n' +
    '            printWindow.document.write(\'</body></html>\');\n' +
    '            printWindow.document.close();\n' +
    '            printWindow.print();\n' +
    '        });\n' +
    '    </script>'

  report += '<title>ENEM Interativo</title>'

  report += '<form id="form1">\n'
  // botão para impressão
  report += '<input type="button" value="Imprimir" id="btnPrint" style="text-align: right;"/>\n'
  report += '<div id="dvContainer">\n<h1>'
  report += '<a href="../../">ENEM Interativo</a>\n'
  report += '<p style="font-size: 15px;">\n'
  report += 'Copyright 2021 - '
  report += '<a href="http://ufabc.edu.br" target="_blank">UFABC</a> - versão beta</p></h1>'
  report += '<hr>'

  // incluir data/hora
  report += '<script type="text/javascript">\n' +
    'let d = new Date();\n' +
    'document.write(d.toLocaleString());\n' +
    '</script>'

  let elmnt = document.getElementsByTagName("body")[0];
  let prova = elmnt.getAttributeNode("id").value
  report += "<h3>Cor " + COR + " - Exames: " + AREAS + "</h3>"
  if (AREAS.includes('LC')) {
    report += "<h5>Questões de Inglês: 1, 2, 3, 4, 5<br>"
    report += "Questões de Espanhol: 01, 02, 03, 04, 05<br>"
    report += "Os gráficos são dos alunos que escolheram inglês</h5>"
  }
  report += '<style type="text/css">\n' +
    '.tg  {border-collapse:collapse;border-spacing:0;}\n' +
    '.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:10px;\n' +
    '  overflow:hidden;padding:6px 3px;word-break:normal;}\n' +
    '.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:10px;\n' +
    '  font-weight:normal;overflow:hidden;padding:6px 3px;word-break:normal;}\n' +
    '.tg .tg-baqh{text-align:center;vertical-align:top}\n' +
    '.tg .tg-amwm{font-weight:bold;text-align:center;vertical-align:top}\n' +
    '</style>'
  report += '<table class="tg">\n' +
    '<thead>\n' +
    '  <tr>\n' +
    '    <th class="tg-amwm">N.</th>\n' +
    '    <th class="tg-amwm">Correta</th>\n' +
    '    <th class="tg-amwm">Marcada</th>\n' +
    '    <th class="tg-amwm">Habilidade</th>\n' +
    '    <th class="tg-amwm"><a href="../../statistics.html" target="_blank">Estatísticas (TRI)</a></th>\n' +
    '    <th class="tg-amwm"><a href="../../statistics.html" target="_blank">Estatísticas (boxplot)</a></th>\n' +
    '  </tr>\n' +
    '</thead>\n' +
    '<tbody>\n'

  let correct = 0
  for (let i = 0; i < AnswersStudent.length; i++) {
    report += '<tr>\n'
    report += '<td class="tg-baqh">' + questions[i].question + "</td>";
    report += '<td class="tg-baqh">' + questions[i].answer + "</td>";
    if (AnswersStudent[i]) {
      report += '<td class="tg-baqh">' + AnswersStudent[i] + "</td>";
    } else {
      report += '<td class="tg-baqh">' + "" + "</td>";
    }
    report += '<td class="tg-baqh">' + questions[i].ability + "</td>";
    if (AREAS.includes('LC')) {
      if ((i < 5 || i >= 10) && myFlag) {
        report += '<td class="tg-baqh"><a href="../FIGS/' + questions[i].images[0] + '" target="_blank">' + 'TRI' + '</a></td>'
        report += '<td class="tg-baqh"><a href="../FIGS/' + questions[i].images[1] + '" target="_blank">' + 'BOX' + '</a></td>'
      } else {
        report += '<td class="tg-baqh">' + '' + '</td>';
        report += '<td class="tg-baqh">' + '' + '</td>';
      }
    } else if (myFlag) {
      report += '<td class="tg-baqh"><a href="../FIGS/' + questions[i].images[0] + '" target="_blank">' + 'TRI' + '</a></td>'
      report += '<td class="tg-baqh"><a href="../FIGS/' + questions[i].images[1] + '" target="_blank">' + 'BOX' + '</a></td>'
    } else {
      report += '<td class="tg-baqh">' + '' + '</td>';
      report += '<td class="tg-baqh">' + '' + '</td>';
    }
    if (questions[i].answer == AnswersStudent[i]) {
      correct++;
    }
    report += '</tr>\n'

  }
  report += '</tbody>\n' +
    '</table>'


  if (AREAS.includes('LC')) {
    report += "<h4>Total de respostas corretas: " + correct + " de " + String(parseInt(TAM) - 5) + "</h4>"

  } else {
    report += "<h4>Total de respostas corretas: " + correct + " de " + TAM + "</h4>"
  }
  report += '</div>\n</form>' // final da página para impressão

  //report += relatorios;

  w.document.write(report);
  w.document.close(); // needed for chrome and safari
  renderQuestion(parseInt(pos0) - 1, AREAS.includes('LC'));
}

window.addEventListener("load", renderQuestions);


///////////////////////////////////////////////////////////////// time
// Código retirado de
// https://legacy.sawtoothsoftware.com/forum/16442/insert-a-chronometer

var centesimas = 0;
var segundos = 0;
var minutos = 0;
var horas = 0;

function inicio() {
  control = setInterval(cronometro, 10);
  document.getElementById("inicio").disabled = true;
  document.getElementById("parar").disabled = false;
  document.getElementById("continuar").disabled = true;
  document.getElementById("reinicio").disabled = false;
}

function parar() {
  clearInterval(control);
  document.getElementById("parar").disabled = true;
  document.getElementById("continuar").disabled = false;
}

function reinicio() {
  clearInterval(control);
  centesimas = 0;
  segundos = 0;
  minutos = 0;
  horas = 0;
  Centesimas.innerHTML = ":00";
  Segundos.innerHTML = ":00";
  Minutos.innerHTML = ":00";
  Horas.innerHTML = "00";
  document.getElementById("inicio").disabled = false;
  document.getElementById("parar").disabled = true;
  document.getElementById("continuar").disabled = true;
  document.getElementById("reinicio").disabled = true;
}

function cronometro() {
  if (centesimas < 99) {
    centesimas++;
    if (centesimas < 10) {
      centesimas = "0" + centesimas
    }
    Centesimas.innerHTML = ":" + centesimas;
  }
  if (centesimas == 99) {
    centesimas = -1;
  }
  if (centesimas == 0) {
    segundos++;
    if (segundos < 10) {
      segundos = "0" + segundos
    }
    Segundos.innerHTML = ":" + segundos;
  }
  if (segundos == 59) {
    segundos = -1;
  }
  if ((centesimas == 0) && (segundos == 0)) {
    minutos++;
    if (minutos < 10) {
      minutos = "0" + minutos
    }
    Minutos.innerHTML = ":" + minutos;
  }
  if (minutos == 59) {
    minutos = -1;
  }
  if ((centesimas == 0) && (segundos == 0) && (minutos == 0)) {
    horas++;
    if (horas < 10) {
      horas = "0" + horas
    }
    Horas.innerHTML = horas;
  }
}
